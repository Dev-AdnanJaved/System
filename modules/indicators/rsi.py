
def get_latest_rsi(candle_data_dict, period=14):
    """
    Calculate latest RSI per interval exactly like Binance Futures.

    Returns:
    - dict {interval: latest RSI value (float)}
    """
    latest_rsi = {}

    for interval, df in candle_data_dict.items():
        if df.empty:
            latest_rsi[interval] = None
            continue

        close = df["close"].astype(float)
        delta = close.diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        # First average gain/loss: SMA of first 'period' candles
        avg_gain = gain[:period].mean()
        avg_loss = loss[:period].mean()

        # Recursive calculation for all candles after the first 'period'
        for i in range(period, len(gain)):
            avg_gain = (avg_gain * (period - 1) + gain.iloc[i]) / period
            avg_loss = (avg_loss * (period - 1) + loss.iloc[i]) / period

        # Calculate RSI
        rs = avg_gain / avg_loss if avg_loss != 0 else float('inf')
        rsi = 100 - (100 / (1 + rs))

        latest_rsi[interval] = rsi

    return latest_rsi
