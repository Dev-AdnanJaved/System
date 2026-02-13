import pandas as pd
import time
from config import REQUEST_DELAY_SECONDS, MAX_RETRIES, RETRY_DELAY,CANDLE_LIMIT
limit = CANDLE_LIMIT

def fetch_klines_single(client, symbol, interval="15m", limit = CANDLE_LIMIT):
    """
    Fetch candlestick data for a single interval with retries.
    Returns a DataFrame.
    """
    for attempt in range(MAX_RETRIES):
        try:
            klines = client.futures_klines(symbol=symbol, interval=interval, limit=limit)
            df = pd.DataFrame(klines, columns=[
                "time","open","high","low","close","volume",
                "close_time","qav","num_trades",
                "taker_base_vol","taker_quote_vol","ignore"
            ])
            # Convert types
            df["open"] = df["open"].astype(float)
            df["high"] = df["high"].astype(float)
            df["low"] = df["low"].astype(float)
            df["close"] = df["close"].astype(float)
            df["volume"] = df["volume"].astype(float)
            df["time"] = pd.to_datetime(df["time"], unit="ms")
            df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")
            time.sleep(REQUEST_DELAY_SECONDS)
            return df
        except Exception as e:
            print(f"Klines fetch error for {symbol} ({interval}) attempt {attempt+1}/{MAX_RETRIES}: {e}")
            time.sleep(RETRY_DELAY)
    return pd.DataFrame()

#For multiple Intervals
def fetch_klines_multiple(client, symbol, intervals=None, limit=CANDLE_LIMIT):
    """
    Fetch candlestick data for multiple intervals.
    Returns a dictionary: {interval: DataFrame}
    """
    if intervals is None:
        intervals = ["5m", "15m", "1h", "4h", "1d"]  # default intervals

    data = {}
    for interval in intervals:
        df = fetch_klines_single(client, symbol, interval=interval, limit=limit)
        if not df.empty:
            data[interval] = df
        else:
            print(f"No data fetched for {symbol} at interval {interval}")
    return data
