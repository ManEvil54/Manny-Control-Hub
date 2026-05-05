import firebase_admin
from firebase_admin import credentials, firestore
import requests
import os
import time

# 1. Initialize Firestore spoke
sa_path = "serviceAccountKey.json"
if not os.path.exists(sa_path):
    # Fallback to absolute path if needed
    sa_path = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")

if os.path.exists(sa_path):
    cred = credentials.Certificate(sa_path)
    firebase_admin.initialize_app(cred)
else:
    # Try initializing from default credentials or env if possible
    try:
        firebase_admin.initialize_app()
    except Exception as e:
        print(f"CRITICAL: Firebase initialization failed. No service account at {sa_path}")
        raise e

db = firestore.client()

# Tradovate Configuration
BASE_URL = "https://live.tradovateapi.com/v1"
YOUR_ACCOUNT_ID = os.environ.get("TRADOVATE_ACCOUNT_ID", "YOUR_ACCOUNT_ID")

def get_tradovate_token():
    """Retrieves a fresh Tradovate access token using OAuth2."""
    auth_data = {
        "name": os.environ.get("TRADOVATE_NAME", "YOUR_NAME"),
        "password": os.environ.get("TRADOVATE_PASS", "YOUR_PASSWORD"),
        "appId": "MCH_Sniper",
        "appVersion": "1.0",
        "cid": os.environ.get("TRADOVATE_CID", "YOUR_CID"),
        "sec": os.environ.get("TRADOVATE_SEC", "YOUR_SECRET")
    }
    try:
        print(f"Requesting Tradovate token for {auth_data['name']}...")
        response = requests.post(f"{BASE_URL}/auth/accesstokenrequest", data=auth_data)
        response.raise_for_status()
        token = response.json().get('accessToken')
        print("Tradovate Token acquired successfully.")
        return token
    except Exception as e:
        print(f"Tradovate Auth Failed: {e}")
        return None

def execute_tradovate_order(data):
    """Execution logic moved from bot's 'brain' to MCH command"""
    token = get_tradovate_token()
    if not token:
        print("Aborting execution: Could not retrieve Tradovate token.")
        return

    url = f"{BASE_URL}/order/placeorder"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "accountId": int(YOUR_ACCOUNT_ID) if YOUR_ACCOUNT_ID.isdigit() else YOUR_ACCOUNT_ID,
        "symbol": data.get('contract', data.get('symbol')),
        "action": data.get('action', 'BUY').capitalize(), # Ensure 'Buy' or 'Sell'
        "orderQty": data.get('size', data.get('qty', 1)),
        "orderType": "Market",
        "isAutomated": True
    }
    
    print(f"Sending order to Tradovate: {payload}")
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        res_json = response.json()
        print(f"Executed: {res_json}")
        
        # Log success to system logs
        db.collection('system_logs').add({
            'event': 'FUTURES_ORDER_EXECUTED',
            'symbol': payload['symbol'],
            'action': payload['action'],
            'qty': payload['orderQty'],
            'orderId': res_json.get('orderId'),
            'timestamp': firestore.SERVER_TIMESTAMP,
            'status': 'SUCCESS'
        })
        
        # Update bot status in MCH
        db.collection("bot_status").document("futures_sniper").set({
            "status": "POSITION_OPEN",
            "last_action": payload['action'],
            "last_symbol": payload['symbol'],
            "last_heartbeat": firestore.SERVER_TIMESTAMP
        }, merge=True)

    except Exception as e:
        error_msg = response.text if 'response' in locals() else str(e)
        print(f"Execution Failed: {error_msg}")
        db.collection('system_logs').add({
            'event': 'FUTURES_ORDER_FAILED',
            'error': error_msg,
            'symbol': payload.get('symbol'),
            'timestamp': firestore.SERVER_TIMESTAMP,
            'status': 'FAILED'
        })

# 2. The 'Listener' - This is the spoke connection
def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        signal = doc.to_dict()
        print(f"Signal received: {signal.get('status')}")
        if signal.get('status') == 'ARMED':
            execute_tradovate_order(signal)
            # Mark as EXECUTED to prevent double-firing
            doc.reference.update({'status': 'EXECUTED'})

import threading

def heartbeat():
    """Background thread to signal that the spoke is alive."""
    while True:
        try:
            db.collection("bot_status").document("futures_sniper").set({
                "last_heartbeat": firestore.SERVER_TIMESTAMP,
                "status": "IDLE" if not 'doc_watch' in locals() else "ACTIVE",
                "connection_stable": True,
                "id": "futures_sniper",
                "name": "Futures Sniper",
                "type": "Tradovate Spoke"
            }, merge=True)
            print("Heartbeat sent to MCH.")
        except Exception as e:
            print(f"Heartbeat error: {e}")
        time.sleep(60)

# Start heartbeat thread
threading.Thread(target=heartbeat, daemon=True).start()

# Point to the specific hub-spoke designator
print("Starting Futures Spoke Listener...")
doc_ref = db.collection('mch_signals').document('futures_target')
doc_watch = doc_ref.on_snapshot(on_snapshot)

# Keep the script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping listener...")
