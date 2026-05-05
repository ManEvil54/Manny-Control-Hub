from firebase_functions import https_fn, scheduler_fn
from firebase_admin import initialize_app, firestore
import os
import requests
from datetime import datetime
from trader_bridge import place_sniper_order, load_config
from advanced_wick_defense import evaluate_rejection_risk

initialize_app()
db = firestore.client()

# Tradovate API Config (Should use Secret Manager in production)
BASE_URL = "https://live.tradovateapi.com/v1"

def get_tradovate_token():
    # Tradovate uses OAuth2
    # These would ideally be in environment variables or Secret Manager
    auth_data = {
        "name": os.environ.get("TRADOVATE_NAME", "YOUR_NAME"),
        "password": os.environ.get("TRADOVATE_PASS", "YOUR_PASSWORD"),
        "appId": "MCH_Sniper",
        "appVersion": "1.0",
        "cid": os.environ.get("TRADOVATE_CID", "YOUR_CID"),
        "sec": os.environ.get("TRADOVATE_SEC", "YOUR_SECRET")
    }
    response = requests.post(f"{BASE_URL}/auth/accesstokenrequest", data=auth_data)
    return response.json().get('accessToken')

def get_trade_tier(daily_count):
    """Returns position sizing and wick defense parameters based on trade sequence."""
    if daily_count == 0:
        return {"qty": 1, "wick_max": 0.25, "label": "SCOUT", "conviction": "LOW"}
    elif daily_count == 1:
        return {"qty": 2, "wick_max": 0.15, "label": "SCALING", "conviction": "MEDIUM"}
    else:
        return {"qty": 3, "wick_max": 0.10, "label": "MAX_CONVICTION", "conviction": "HIGH"}

@https_fn.on_request()
def tradovate_webhook(req: https_fn.Request) -> https_fn.Response:
    # 1. Security Check
    data = req.get_json()
    if data.get("secret") != "MANNY_SNIPER_2026":
        return https_fn.Response("Unauthorized", status=401)

    # 2. Registry Check: System Kill Switch (Spoke Verification)
    # Ping the useSystemStore source of truth
    system_ref = db.collection("system_status").document("prize_ev_bot")
    system_data = system_ref.get().to_dict()
    if system_data and system_data.get("kill_switch"):
        print("KILL SWITCH DETECTED: Aborting execution across all spokes.")
        return https_fn.Response("Vetoed: Global Kill Switch is ACTIVE", status=403)

    # 3. Wick Defense Data: Hub Metadata (Spoke Data Feed)
    # Pull Nasdaq proximity directly from useHubStore source
    hub_ref = db.collection("hub_current_state").document("live")
    hub_doc = hub_ref.get()
    hub_data = hub_doc.to_dict() if hub_doc.exists else {}
    market_metadata = hub_data.get("market_data", {})
    nasdaq_proximity = market_metadata.get("nasdaq_proximity", 0)
    rejection_mode = nasdaq_proximity > 95 # ATH Proximity threshold

    # 4. Extract Signal
    symbol = data.get("symbol")
    action = data.get("action").capitalize()
    wick_percentage = data.get("wick_pct", 0)

    # NEW: Advanced Wick Defense (Environment Switch)
    current_price = data.get("price", 0)
    candle = {
        'high': data.get("high", current_price),
        'low': data.get("low", current_price),
        'open': data.get("open", current_price),
        'close': current_price
    }
    
    # Tighten tolerance if in Rejection Mode (ATH Proximity)
    if rejection_mode:
        print(f"REJECTION MODE: Tightening wick defense. Nasdaq @ {nasdaq_proximity}%")
        wick_percentage *= 1.5 # Artificial inflation of risk

    rejection_status = evaluate_rejection_risk(candle)
    if "HARD_VETO" in rejection_status:
        return https_fn.Response(rejection_status)

    # 5. Get Current Bot State from Firestore
    agent_ref = db.collection("agents").document("market_command")
    agent_doc = agent_ref.get()
    agent_data = agent_doc.to_dict() if agent_doc.exists else {"daily_trades": 0}
    daily_count = agent_data.get("daily_trades", 0)

    # 6. Apply Tiered Logic
    tier = get_trade_tier(daily_count)
    
    # Veto logic
    if wick_percentage > tier['wick_max']:
        return https_fn.Response(f"Vetoed: Wick too long for {tier['label']} tier ({wick_percentage}%)")

    # 7. Place Order
    try:
        order_id = place_sniper_order(symbol, tier['qty'])
        print(f"Tradier Order ID: {order_id}")
    except Exception as e:
        print(f"Execution Error: {str(e)}")
        return https_fn.Response(f"Execution Failed: {str(e)}", status=500)

    # 8. Sync to MCH Dashboard & Global Audit
    # Spoke Alignment: bot_status/futures_sniper
    spoke_ref = db.collection("bot_status").document("futures_sniper")
    spoke_ref.set({
        "status": "POSITION_OPEN",
        "metrics": {
            "last_trade_pnl": 0, # To be updated on exit
            "active_symbol": symbol,
            "last_action": action
        },
        "last_heartbeat": firestore.SERVER_TIMESTAMP,
        "rejection_mode_active": rejection_mode
    }, merge=True)

    # Log event to useSystemStore audit trail
    db.collection("system_status").document("futures_audit").set({
        "last_event": f"{tier['label']} {action} executed on {symbol}",
        "timestamp": firestore.SERVER_TIMESTAMP,
        "type": "trade"
    }, merge=True)

    # NEW: Report to Alpha Command Intelligence Stream
    report_id = f"futures-{datetime.now().timestamp()}"
    db.collection("bot_analysis_reports").document(report_id).set({
        "timestamp": firestore.SERVER_TIMESTAMP,
        "metadata": {
            "request_id": report_id,
            "timestamp": datetime.now().timestamp() * 1000,
            "bot_origin": "futures_sniper",
            "domain": "futures",
            "target_asset": symbol,
            "status": "EXECUTED"
        },
        "synthesis": {
            "overall_conviction_score": 90 if tier['label'] == 'MAX_CONVICTION' else (75 if tier['label'] == 'SCALING' else 55),
            "regime_type": "ATH_REJECTION" if rejection_mode else "TREND_FOLLOWING",
            "veto_flag": False,
            "recommended_sizing": tier['label'],
            "stop_strategy": "DYNAMIC_TRAILING",
            "key_takeaway": f"Sniper order sent: {tier['qty']} contracts. Wick Def: {wick_percentage}%",
            "macro_context": f"Nasdaq Proximity: {nasdaq_proximity}%"
        }
    })

    # Also update the legacy agent ref if needed for other components
    agent_ref.set({
        "daily_trades": daily_count + 1,
        "last_seen": firestore.SERVER_TIMESTAMP
    }, merge=True)

    return https_fn.Response(f"Order Sent: {tier['label']} {action} {tier['qty']} {symbol}. MCH Updated.")

@scheduler_fn.on_schedule(schedule="every 5 minutes")
def market_heartbeat(event: scheduler_fn.ScheduledEvent) -> None:
    """Updates the Futures Spoke heartbeat to show it's online in MCH."""
    try:
        spoke_ref = db.collection("bot_status").document("futures_sniper")
        spoke_ref.set({
            "last_heartbeat": firestore.SERVER_TIMESTAMP,
            "status": "IDLE"
        }, merge=True)
        print("Futures Heartbeat Sent.")
    except Exception as e:
        print(f"Heartbeat Error: {str(e)}")

