

def get_last_n_volume_with_pressure(candle_data_dict, last_n, use_quote=False): #buy/sell/base_vol
    """
    Returns volume, buy, and sell volumes for the last N candles per interval.

    Parameters:
    - candle_data_dict : dict {interval: DataFrame} from fetch_klines_multiple
    - last_n : int, how many recent candles to return
    - use_quote : bool, True for quote volume ("qav"), False for base asset volume ("volume")

    Returns:
    - dict : {interval: {"volume": [], "buy": [], "sell": []}}
    """
    volumes = {}

    for interval, df in candle_data_dict.items():
        if df.empty:
            volumes[interval] = {"volume": [], "buy": [], "sell": []}
            continue

        # Choose volume column
        vol_col = "qav" if use_quote else "volume"

        # Get last N candles
        last_candles = df.tail(last_n)

        base_vol = last_candles[vol_col].astype(float).tolist()
        taker_buy = last_candles["taker_base_vol"].astype(float).tolist()
        taker_sell = [b - buy for b, buy in zip(base_vol, taker_buy)]

        volumes[interval] = {"volume": base_vol, "buy": taker_buy, "sell": taker_sell}

    return volumes
