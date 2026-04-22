import requests

def is_near_52wk_high(current_price=None, symbol="NQ"):
    """
    Checks if the Nasdaq (NQ) is within 0.5% of its 52-week high.
    In production, this would fetch real-time data.
    """
    # Placeholder for the 52-week high of NQ (approximate for 2026 scenario)
    # Ideally, this would be fetched from an API
    nasdaq_52wk_high = 21000.0 
    
    if current_price is None:
        # Mocking the current price for demo purposes
        current_price = 20950.0 
        
    proximity = (nasdaq_52wk_high - current_price) / nasdaq_52wk_high
    
    return proximity <= 0.005 # Within 0.5%

def evaluate_rejection_risk(candle):
    """
    LANCE RULE: Rejections at highs are toxic.
    If a wick forms that retraces more than 67% of the breakout candle, the trade is dead.
    """
    wick_size = candle['high'] - max(candle['open'], candle['close'])
    body_size = abs(candle['open'] - candle['close'])
    
    # Avoid division by zero
    total_candle_size = wick_size + body_size
    if total_candle_size == 0:
        return "PROCEED"
        
    wick_percentage = wick_size / total_candle_size

    # LANCE RULE: Rejections at highs are toxic
    if is_near_52wk_high(current_price=candle['close']) and wick_percentage > 0.67:
        return "HARD_VETO: Institutional Rejection Detected"
    
    return "PROCEED"
