from datetime import datetime, timedelta

def get_recent_ema_cross(ema_data, timeframe, lookback_candles): #lookback_candles=192 for 48 hours
    """
    Detect the most recent EMA50 / EMA200 cross within lookback window,
    and check if EMA200 has been rising (average trend) since the cross.
    
    Returns:
    {
        "type": "bullish"/"bearish",
        "candles_ago": int,
        "hours_ago": float,
        "time": str,
        "ema200_trend": "rising"/"falling"
    }
    or None / "No Cross Happened"
    """

    ema50 = ema_data.get(timeframe, {}).get("ema_50", [])
    ema200 = ema_data.get(timeframe, {}).get("ema_200", [])

    # Safety checks
    if not ema50 or not ema200 or len(ema50) != len(ema200) or len(ema50) < 2:
        
     return {
        "signal": "NO SIGNAL",
        "reason": "Not Enough Candles"
    }

    total_candles = len(ema50)

    # Candle duration in hours
    timeframe_map = {
        "1m": 1/60, "5m": 5/60, "15m": 0.25, "30m": 0.5,
        "1h": 1, "2h": 2, "4h": 4, "6h": 6, "12h": 12, "1d": 24
    }
    candle_hours = timeframe_map.get(timeframe, 0.25)  # default 15m

    # Limit lookback
    max_lookback = min(lookback_candles, total_candles - 1)

    # Scan from most recent → backwards
    for i in range(1, max_lookback + 1):
        current_50 = ema50[-i]
        current_200 = ema200[-i]
        prev_50 = ema50[-i - 1]
        prev_200 = ema200[-i - 1]

        # Bullish cross
        if prev_50 <= prev_200 and current_50 > current_200:
            # Slice EMA200 from cross to now
            ema200_since_cross = ema200[-i:]
            mid = len(ema200_since_cross) // 2
            first_half_avg = sum(ema200_since_cross[:mid]) / max(mid,1)
            second_half_avg = sum(ema200_since_cross[mid:]) / max(len(ema200_since_cross)-mid,1)

            ema200_trend = "rising" if second_half_avg > first_half_avg else "falling"

            cross_time = datetime.now() - timedelta(hours=i * candle_hours)
            cross_time_str = cross_time.strftime("%d %b %Y %H:%M")

            return {
                "type": "bullish",
                "candles_ago": i,
                "hours_ago": round(i * candle_hours, 2),
                "time": cross_time_str,
                "ema200_trend": ema200_trend
            }

        # Bearish cross
        if prev_50 >= prev_200 and current_50 < current_200:
            # Slice EMA200 from cross to now
            ema200_since_cross = ema200[-i:]
            mid = len(ema200_since_cross) // 2
            first_half_avg = sum(ema200_since_cross[:mid]) / max(mid,1)
            second_half_avg = sum(ema200_since_cross[mid:]) / max(len(ema200_since_cross)-mid,1)

            ema200_trend = "falling" if second_half_avg < first_half_avg else "rising"

            cross_time = datetime.now() - timedelta(hours=i * candle_hours)
            cross_time_str = cross_time.strftime("%d %b %Y %H:%M")

            return {
                "type": "bearish",
                "candles_ago": i,
                "hours_ago": round(i * candle_hours, 2),
                "time": cross_time_str,
                "ema200_trend": ema200_trend
            }

    return    {
        "signal": "NO SIGNAL",
        "reason": f"EMA cross returned invalid result"
    }


#Worked

#------------------------------------------------------------------------------------------------------------------------------------
