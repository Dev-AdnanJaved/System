import pandas as pd

def volumes_and_closes_all_timeframes(data_dict_of_intervals):
    """
    Returns closes and volumes as Python lists for all timeframes,
    automatically converting Pandas Series, NumPy arrays, or lists to lists.

    Args:
        data_dict_of_intervals (dict): Dictionary containing OHLCV data per timeframe.

    Returns:
        dict: {
            '15m': {'close': [...], 'volume': [...]},
            '1h': {'close': [...], 'volume': [...]},
            ...
        }
    """
    result = {}

    for timeframe, df in data_dict_of_intervals.items():
        # Convert to pandas Series internally (handles lists, arrays, or Series)
        close_series = pd.Series(df['close'])
        volume_series = pd.Series(df['volume'])

        # Convert to Python lists
        closes = close_series.tolist()
        volumes = volume_series.tolist()

        result[timeframe] = {'close': closes, 'volume': volumes}

    return result
