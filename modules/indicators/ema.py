def get_ema_all_timeframes(data_dict, ema_periods):
    """
    Returns full EMA series for all candles
    Structure:
    {
        "15m": {
            "ema_7":   [...500 values...],
            "ema_25":  [...],
            "ema_50":  [...],
            "ema_99":  [...],
            "ema_200": [...]
        },
        "1h": {...},
        ...
    }
    """

    ema_result = {}

    for tf, df in data_dict.items():

        # ensure float
        df["close"] = df["close"].astype(float)

        ema_result[tf] = {}

        # calculate EMAs
        for period in ema_periods:
            ema_series = df["close"].ewm(
                span=period,
                adjust=False
            ).mean()

            # store FULL list of values
            ema_result[tf][f"ema_{period}"] = ema_series.tolist()

    return ema_result
