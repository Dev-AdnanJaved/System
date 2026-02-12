#ATR
# from config import ATR_VALUE
# from modules.indicators.atr import calculate_atr_multi_intervals
# from modules.market_data.market_data import fetch_klines_multiple
# from modules.binance_client.binance_client import get_futures_client
# client = get_futures_client()

# data_dict = fetch_klines_multiple(client, 'BTCUSDT', intervals=None)

# atr_for_all_intervals = calculate_atr_multi_intervals(data_dict,ATR_VALUE )
# atr_15 = atr_for_all_intervals['15m']
# print(atr_15)


# WORKED

# -----------------------------------------------------------------------------------------------------------------------------------


#EMA for [] all time frames = [15m, 1h, 4h, 1d] for all ema_periods

# ema_periods = [7, 25, 50, 99, 200]

# from modules.binance_client.binance_client import get_futures_client
# from modules.market_data.market_data import fetch_klines_multiple
# from modules.indicators.ema import get_ema_all_timeframes

# client = get_futures_client()
# data_dict_for_multiple_intervals = fetch_klines_multiple(client, 'BTCUSDT', intervals=None)

# ema_data = get_ema_all_timeframes(data_dict_for_multiple_intervals, ema_periods)

# print (ema_data)



# ema_50_1h = ema_data["1h"]["ema_50"]
# ema_200_1h = ema_data["1h"]["ema_200"]
# print(f"EMA_50 of 1H: {ema_50_1h}, EMA_200 of 1H: {ema_200_1h}")


    
    # Worked 
    



# -----------------------------------------------------------------------------------------------------------------------------------

#Volume Indicator
# from config import CANDLE_LIMIT
# from modules.binance_client.binance_client import get_futures_client
# from modules.market_data.market_data import fetch_klines_multiple
# from modules.indicators.volume import get_last_n_volume_with_pressure

# client = get_futures_client()
# data_dict = fetch_klines_multiple(client, symbol='SOLUSDT', intervals=None, limit=500)

# volumes = get_last_n_volume_with_pressure(data_dict, last_n=10, use_quote=False)

# print(volumes)

# print(volumes['1h']['volume'])
# print(volumes['1h']['buy'])
# print(volumes['1h']['sell'])







    # Worked 
    

# -----------------------------------------------------------------------------------------------------------------------------------



#RSI

# from modules.binance_client.binance_client import get_futures_client
# from modules.market_data.market_data import fetch_klines_multiple
# from modules.indicators.rsi import get_latest_rsi
# from config import RSI_PERIODS as period

# client = get_futures_client()
# data_dict = fetch_klines_multiple(client, symbol='SOLUSDT', intervals=None, limit=500)

# RSI = get_latest_rsi(data_dict, period )
# print(RSI)
# print(f"RSI_15m: {RSI['15m']}")
# print(f"RSI_1h: {RSI['1h']}")
# print(f"RSI_4h: {RSI['4h']}")
# print(f"RSI_1d: {RSI['1d']}")


 # Worked 
    



# -----------------------------------------------------------------------------------------------------------------------------------




#MACD

# from modules.binance_client.binance_client import get_futures_client
# from modules.market_data.market_data import fetch_klines_multiple
# from modules.indicators.macd import get_latest_macd

# from config import MACD_VALUES

# client = get_futures_client()
# data_dict = fetch_klines_multiple(client, symbol='SOLUSDT', intervals=None, limit=500)
# macd = get_latest_macd(data_dict, MACD_VALUES)
# print(macd['15m'])
# print(macd['1h'])
# print(macd['4h'])


 # Worked 
    



# -----------------------------------------------------------------------------------------------------------------------------------


#ADX
# from config import ADX_VALUE
# from modules.indicators.adx import calculate_adx_multi_intervals
# from modules.market_data.market_data import fetch_klines_multiple
# from modules.binance_client.binance_client import get_futures_client
# client = get_futures_client()

# data_dict = fetch_klines_multiple(client, 'WAXPUSDT', intervals=None)

# adx_for_all_intervals = calculate_adx_multi_intervals(data_dict,ADX_VALUE )
# print(adx_for_all_intervals)



# WORKED

# -----------------------------------------------------------------------------------------------------------------------------------