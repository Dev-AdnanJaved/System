# Detect Cross
# ema_periods = [7, 25, 50, 99, 200]

# from modules.binance_client.binance_client import get_futures_client
# from modules.market_data.market_data import fetch_klines_multiple
# from modules.indicators.ema import get_ema_all_timeframes
# from strategies.Ema_Volume_Rsi_Adx.Ema_Cross_Detection.Ema_Volume import get_recent_ema_cross

# client = get_futures_client()
# data_dict_for_multiple_intervals = fetch_klines_multiple(client, 'WAXPUSDT', intervals=None)


# ema_data = get_ema_all_timeframes(data_dict_for_multiple_intervals, ema_periods)
# data = get_recent_ema_cross(ema_data, timeframe='15m', lookback_candles=192 )
# print(data)

# WORKED

# -----------------------------------------------------------------------------------------------------------------------------------

#RSI
# from modules.indicators.rsi import get_latest_rsi
# from modules.binance_client.binance_client import get_futures_client
# from modules.market_data.market_data import fetch_klines_multiple
# from strategies.Ema_Volume_Rsi_Adx.RSI.rsi import get_rsi_signal

# client = get_futures_client()
# data_dict_for_multiple_intervals = fetch_klines_multiple(client, 'WAXPUSDT', intervals=None)

# rsi_data = get_latest_rsi(data_dict_for_multiple_intervals)
# signal = get_rsi_signal(rsi_data)
# print(signal)


# WORKED

# -----------------------------------------------------------------------------------------------------------------------------------



#ADX

# from modules.indicators.adx import calculate_adx_multi_intervals
# from modules.binance_client.binance_client import get_futures_client
# from modules.market_data.market_data import fetch_klines_multiple
# from strategies.Ema_Volume_Rsi_Adx.ADX.adx import get_adx_strength

# client = get_futures_client()
# data_dict_for_multiple_intervals = fetch_klines_multiple(client, 'WAXPUSDT', intervals=None)

# adx_dict = calculate_adx_multi_intervals(data_dict_for_multiple_intervals)
# signal = get_adx_strength(adx_dict)
# print(signal)

# WORKED

# -----------------------------------------------------------------------------------------------------------------------------------



#Volume Spike Detection


from modules.indicators.volume import get_last_n_volume_with_pressure
from modules.binance_client.binance_client import get_futures_client
from modules.market_data.market_data import fetch_klines_multiple
from strategies.Ema_Volume_Rsi_Adx.Volume_Detection.volume_detection import volume_analysis_report


client = get_futures_client()
data_dict_for_multiple_intervals = fetch_klines_multiple(client, 'JASMYUSDT', intervals=None)


volume_data = get_last_n_volume_with_pressure(data_dict_for_multiple_intervals, last_n=500)
volume_report = volume_analysis_report(volume_data, lookback=15, surge_len=4, base_mult=1.35)
print(volume_report)




    # Worked 
    



# -----------------------------------------------------------------------------------------------------------------------------------