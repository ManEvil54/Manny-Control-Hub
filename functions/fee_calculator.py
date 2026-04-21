# functions/fee_calculator.py

def calculate_net_profit(gross_profit, contract_count, asset_type="micro"):
    """
    Calculates the Net Profit after subtracting Tradier Pro commissions and passthrough fees.
    
    Args:
        gross_profit (float): Total profit before fees.
        contract_count (int): Total number of contracts traded.
        asset_type (str): Type of asset ('micro', 'option', 'index').
        
    Returns:
        float: Net profit after round-trip fees.
    """
    # Tradier Pro Plan 2026 Rates
    commissions = {
        "micro": 0.35,
        "option": 0.75,
        "index": 0.35
    }
    
    # Standard 2026 Passthrough fees (Exchange + NFA + Clearing)
    passthrough_fee = 0.35 
    
    # Round-trip calculation (* 2 for Buy + Sell)
    total_fees = (commissions.get(asset_type, 0.35) + passthrough_fee) * contract_count * 2
    
    return gross_profit - total_fees
