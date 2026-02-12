def get_rsi_signal(rsi_data):
    """
    Check RSI for bullish or bearish conditions using 15m and 1h RSI.
    
    Rules:
        Bullish: 15m > 50 AND 1h > 50 → strong bullish
        Bearish: 15m < 50 AND 1h < 50 → strong bearish
        Warning: 15m confirms but 1h opposite → weak signal
    
    Returns:
        dict or None
    """
    rsi_15m = rsi_data.get('15m')
    rsi_1h = rsi_data.get('1h')

    if rsi_15m is None or rsi_1h is None:
        return None

    # Strong Bullish
    if rsi_15m > 50 and rsi_1h > 50:
        return {
            "type": "bullish",
            "strength": "strong",
            "message": f"RSI 15m is {rsi_15m:.2f} and RSI 1h is {rsi_1h:.2f}"
        }

    # Strong Bearish
    if rsi_15m < 50 and rsi_1h < 50:
        return {
            "type": "bearish",
            "strength": "strong",
            "message": f"RSI 15m is {rsi_15m:.2f} and RSI 1h is {rsi_1h:.2f}"
        }

    # Weak/Warning Bullish (15m > 50 but 1h <= 50)
    if rsi_15m > 50 and rsi_1h <= 50:
        return {
            "type": "bullish",
            "strength": "weak",
            "message": f"RSI 15m is {rsi_15m:.2f} but RSI 1h is {rsi_1h:.2f} (Warning: 1h below 50)"
        }

    # Weak/Warning Bearish (15m < 50 but 1h >= 50)
    if rsi_15m < 50 and rsi_1h >= 50:
        return {
            "type": "bearish",
            "strength": "weak",
            "message": f"RSI 15m is {rsi_15m:.2f} but RSI 1h is {rsi_1h:.2f} (Warning: 1h above 50)"
        }

    # Neutral
    return None
