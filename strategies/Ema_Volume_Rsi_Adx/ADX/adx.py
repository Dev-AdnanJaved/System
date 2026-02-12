def get_adx_strength(adx_data):
    """
    Check trend strength using ADX 15m and 1h.

    Rules:
        Strong trend: 15m > 25 AND 1h > 25
        Weak trend / warning: 15m > 25 but 1h <= 25 or 15m <= 25
        Very Weak: 15m <= 25 1h <= 25

    Returns:
        dict or None
    """
    adx_15m = adx_data.get('15m')
    adx_1h = adx_data.get('1h')

    if adx_15m is None or adx_1h is None:
        return None

    # Strong trend
    if adx_15m > 25 and adx_1h > 25:
        return {
            "strength": "strong",
            "message": f"Trend is strong. ADX 15m: {adx_15m:.2f}, ADX 1h: {adx_1h:.2f}"
        }

    # Weak trend warning (one of them low)
    if adx_15m > 25 and adx_1h <= 25:
        return {
            "strength": "weak",
            "message": f"Trend is weak. ADX 15m: {adx_15m:.2f}, ADX 1h: {adx_1h:.2f} (Warning: 1h trend weak)"
        }

    # Trend too weak
    if adx_15m <= 25:
        return {
            "strength": "very weak",
            "message": f"Trend is very weak. ADX 15m: {adx_15m:.2f}, ADX 1h: {adx_1h:.2f}"
        }

    return None
