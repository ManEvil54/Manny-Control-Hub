import json
import requests
import os
from pathlib import Path

def load_config():
    config_path = Path(__file__).parent.parent / "config" / "tradier_env.json"
    with open(config_path, 'r') as f:
        return json.load(f)

def get_tradier_client():
    config = load_config()
    current = config["environments"][config["active_env"]]
    
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {current['token']}",
        "Accept": "application/json"
    })
    
    return session, current

def place_sniper_order(symbol, qty, order_type="market"):
    session, current = get_tradier_client()
    
    url = f"{current['base_url']}accounts/{current['brokerage_id']}/orders"
    
    payload = {
        "class": "equity",
        "symbol": symbol,
        "side": "buy",
        "quantity": qty,
        "type": order_type,
        "duration": "day"
    }
    
    try:
        response = session.post(url, data=payload)
        response.raise_for_status()
        data = response.json()
        
        if "order" in data and "id" in data["order"]:
            print(f"[Order Success] {qty}x {symbol} filled in {current['mode_label']}. Order ID: {data['order']['id']}")
            return data["order"]["id"]
        else:
            print(f"[Order Warning] Order sent but no ID returned for {symbol}")
            return None
            
    except Exception as e:
        error_detail = response.json() if 'response' in locals() else str(e)
        print(f"[Order Failed] Error in {current['mode_label']}: {error_detail}")
        raise e

if __name__ == "__main__":
    # Test Scout Order in Sandbox
    config = load_config()
    if config["active_env"] == "sandbox":
        print("Firing Test Scout Order in Python Sandbox...")
        try:
            place_sniper_order("/MNQ", 1)
        except:
            pass
