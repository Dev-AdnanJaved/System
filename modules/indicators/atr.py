import pandas as pd
# from config import ATR_VALUE

def calculate_atr_multi_intervals(data_dict, atr_period):  #No need to give spearte time intervals because it will auto detetct from data dict from multiple k line functon
    """
    Calculate ATR for multiple intervals (timeframes) from a dict of OHLCV DataFrames.

    Parameters:
    - data_dict: dict of DataFrames, e.g.,
        {
            "15m": df_15m,
            "1h": df_1h,
            "4h": df_4h,
            "1d": df_1d
        }
      Each df must have columns: ['high','low','close']
    - atr_period: int, ATR period (Wilder's smoothing)

    Returns:
    - dict: latest ATR per timeframe
      {
        "15m": 523.12345,
        "1h": 540.67890,
        "4h": 512.23456,
        "1d": 495.98765
      }
    """

    atr_result = {}

    for interval, df in data_dict.items():
        # Ensure numeric
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)
        df["close"] = df["close"].astype(float)

        # True Range
        df["prev_close"] = df["close"].shift(1)
        df["tr"] = pd.concat([
            df["high"] - df["low"],
            (df["high"] - df["prev_close"]).abs(),
            (df["low"] - df["prev_close"]).abs()
        ], axis=1).max(axis=1)

        # ATR using Wilder's smoothing
        df["atr"] = df["tr"].ewm(alpha=1/atr_period, adjust=False).mean()

        # Latest ATR
        atr_result[interval] = round(df["atr"].iloc[-1], 5)

    return atr_result
