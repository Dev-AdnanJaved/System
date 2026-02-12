import pandas as pd
import numpy as np

#Exact same to Trading view Others are same to Binance
def rma_tv(series, period):
    """TradingView-style RMA (Wilder's Moving Average)."""
    series = series.copy()
    result = pd.Series(np.nan, index=series.index)
    result.iloc[period-1] = series.iloc[:period].mean()  # first value = mean
    for i in range(period, len(series)):
        result.iloc[i] = (result.iloc[i-1]*(period-1) + series.iloc[i])/period
    return result

def calculate_adx_multi_intervals(data_dict, di_period=14, adx_period=14):
    adx_result = {}
    
    for interval, df in data_dict.items():
        df = df.copy()
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)
        df["close"] = df["close"].astype(float)

        up = df["high"].diff()
        down = -df["low"].diff()

        plus_dm = up.where((up > down) & (up > 0), 0.0)
        minus_dm = down.where((down > up) & (down > 0), 0.0)

        tr = pd.concat([
            df["high"] - df["low"],
            (df["high"] - df["close"].shift(1)).abs(),
            (df["low"] - df["close"].shift(1)).abs()
        ], axis=1).max(axis=1)

        # Smooth using RMA (Wilder's MA)
        tr_rma = rma_tv(tr, di_period)
        plus_rma = rma_tv(plus_dm, di_period)
        minus_rma = rma_tv(minus_dm, di_period)

        # +DI and -DI
        plus_di = 100 * (plus_rma / tr_rma)
        minus_di = 100 * (minus_rma / tr_rma)

        # DX
        dx = (plus_di - minus_di).abs() / (plus_di + minus_di)
        dx.fillna(0, inplace=True)

        # ADX smoothing
        adx_series = rma_tv(dx, adx_period) * 100  # scale after smoothing

        # Drop initial NaNs (unstable values)
        adx_valid = adx_series.dropna()
        if len(adx_valid) == 0:
            adx_result[interval] = np.nan
        else:
            adx_result[interval] = round(adx_valid.iloc[-1], 2)

    return adx_result
