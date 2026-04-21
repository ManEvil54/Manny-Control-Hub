def check_hammer_conditions(ticker_data):
    """
    Oracle Agent logic to handle the math for the Hammer scale-in.
    Coordinates MASI, CRAIG, MARCI, and LANCE agents.
    """
    # 1. Check Masi's Sync (VWAP relationship between /ES and /NQ)
    if not masi_sync_is_green(ticker_data):
        return "WAIT: MASI_DIVERGENCE"
        
    # 2. Check Craig's FVG Midpoint
    fvg = detect_fvg(ticker_data)
    if not fvg:
        return "WAIT: NO_FVG_FOOTPRINT"
    
    current_price = ticker_data[-1]['close']
    if current_price > fvg['midpoint']:
        return "WAIT: ABOVE_GOLDEN_ZONE"
    
    # 3. Check Marci's Trendline (Little RZY)
    if not rzy_trendline_broken(ticker_data):
        return "WAIT: TRENDLINE_INTACT"
        
    # 4. Check Lance's Volume (Urgency)
    vol_delta = volume_delta(ticker_data)
    if vol_delta < 1.2: # 20% increase required
        return "VETO: LOW_URGENCY"
        
    return "FIRE_THE_HAMMER"

def masi_sync_is_green(ticker_data):
    """
    Monitors /ES and /NQ VWAP relationship.
    Indices must both be on the same side of VWAP.
    """
    # In a real implementation, this would fetch /ES and /NQ data
    # For now, we assume data is passed in or fetched via bridge
    es_above = ticker_data[-1].get('es_vwap_dist', 0) > 0
    nq_above = ticker_data[-1].get('nq_vwap_dist', 0) > 0
    return es_above == nq_above

def detect_fvg(ticker_data):
    """
    Identifies Fair Value Gaps on the 1m chart.
    Bullish FVG: Candle 1 High < Candle 3 Low.
    """
    if len(ticker_data) < 3:
        return None
    
    # Look at the most recent 3-candle sequence
    c1 = ticker_data[-3]
    c3 = ticker_data[-1]
    
    if c1['high'] < c3['low']:
        gap_top = c3['low']
        gap_bottom = c1['high']
        return {
            'top': gap_top,
            'bottom': gap_bottom,
            'midpoint': (gap_top + gap_bottom) / 2
        }
    return None

def rzy_trendline_broken(ticker_data):
    """
    Projects the Little RZY Measured Move and checks for trendline break.
    """
    # Simplified logic: If last candle closed above the previous candle's high 
    # during a pullback, we consider it a 'break' for this prototype.
    return ticker_data[-1]['close'] > ticker_data[-2]['high']

def volume_delta(ticker_data):
    """
    Measures Volume-per-Minute during the trendline break.
    """
    curr_vol = ticker_data[-1]['volume']
    avg_vol = sum(d['volume'] for d in ticker_data[-5:-1]) / 4
    return curr_vol / avg_vol if avg_vol > 0 else 1.0
