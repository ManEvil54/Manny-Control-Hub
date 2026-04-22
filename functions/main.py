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

    # 2. Extract Signal
    symbol = data.get("symbol")
    action = data.get("action").capitalize()
    wick_percentage = data.get("wick_pct", 0) # Provided by TradingView alert

    # NEW: Advanced Wick Defense (Environment Switch)
    # Construct a candle object for the evaluation
    current_price = data.get("price", 0)
    candle = {
        'high': data.get("high", current_price),
        'low': data.get("low", current_price),
        'open': data.get("open", current_price),
        'close': current_price
    }
    rejection_status = evaluate_rejection_risk(candle)
    if "HARD_VETO" in rejection_status:
        return https_fn.Response(rejection_status)

    # 3. Get Current Bot State from Firestore
    # Canonical Registry Alignment: 'agents/market_command'
    agent_ref = db.collection("agents").document("market_command")
    agent_doc = agent_ref.get()
    agent_data = agent_doc.to_dict() if agent_doc.exists else {"daily_trades": 0}
    daily_count = agent_data.get("daily_trades", 0)

    # 4. Apply Tiered Logic
    tier = get_trade_tier(daily_count)
    
    # 5. Hybrid Veto Logic (Technical & Sentiment)
    research_confirmed = True 
    
    if wick_percentage > tier['wick_max']:
        return https_fn.Response(f"Vetoed: Wick too long for {tier['label']} tier ({wick_percentage}%)")

    if not research_confirmed and tier['qty'] > 1:
        return https_fn.Response(f"Vetoed: Research Bot did not confirm high-conviction environment.")

    # 6. Place Order
    try:
        tradier_cfg = load_config()
        order_id = place_sniper_order(symbol, tier['qty'])
        print(f"Tradier Order ID: {order_id}")
    except Exception as e:
        print(f"Execution Error: {str(e)}")

    # 7. Sync to MCH Dashboard
    update_data = {
        "id": "market_command",
        "name": "Market",
        "type": "Context Analyst",
        "status": "POSITION_OPEN",
        "active_symbol": symbol,
        "last_action": action,
        "daily_trades": daily_count + 1,
        "conviction_level": tier['conviction'],
        "tier_label": tier['label'],
        "last_seen": firestore.SERVER_TIMESTAMP,
        "conviction_metrics": {
            "score": 85 if tier['conviction'] == "HIGH" else (65 if tier['conviction'] == "MEDIUM" else 45),
            "label": tier['conviction']
        }
    }

    # LITTLE RZY LOGIC: Track points and calculate exits
    if tier['label'] == "SCOUT":
        # Point A is the low, Point B is the breakout high
        update_data["point_a"] = data.get("point_a", current_price) 
        update_data["point_b"] = current_price
    elif tier['label'] == "SCALING":
        # Point C is the pullback low
        point_a = agent_data.get("point_a", 0)
        point_b = agent_data.get("point_b", 0)
        point_c = data.get("point_c", current_price)
        
        if point_a and point_b:
            # Target = BreakoutPrice + (ImpulseHigh - ImpulseLow)
            measured_move = (point_b - point_a)
            profit_target = current_price + measured_move
            
            update_data["profit_target"] = profit_target
            update_data["stop_loss"] = point_c # Move SL to Point C
            update_data["point_c"] = point_c
            
            print(f"LITTLE RZY ACTIVE: Target={profit_target}, SL={point_c}")

    # Use set(merge=True) to preserve other metadata like uptime or account history
    agent_ref.set(update_data, merge=True)

    return https_fn.Response(f"Order Sent: {tier['label']} {action} {tier['qty']} {symbol}. MCH Updated.")

@scheduler_fn.on_schedule(schedule="every 5 minutes")
def market_heartbeat(event: scheduler_fn.ScheduledEvent) -> None:
    """Updates the Market agent last_seen to show it's online in MCH."""
    try:
        agent_ref = db.collection("agents").document("market_command")
        agent_ref.set({
            "last_seen": firestore.SERVER_TIMESTAMP,
            "status": "IDLE" # Default status when not in a trade
        }, merge=True)
        print("Market Heartbeat Sent.")
    except Exception as e:
        print(f"Heartbeat Error: {str(e)}")
