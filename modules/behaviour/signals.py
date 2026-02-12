#ema_periods = [7, 25, 50 99, 200]


def add_ema(df, ema_periods):
    for period in ema_periods:
        df[f"ema_{period}"] = df["close"].ewm(
            span=period,
            adjust=False
        ).mean()
    return df



