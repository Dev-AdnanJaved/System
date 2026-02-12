import pandas as pd
from config import MACD_VALUES


def get_latest_macd(candle_data_dict, macd_config = MACD_VALUES):
    """
    Calculate latest MACD per interval exactly like Binance/TradingView.

    Parameters:
    - candle_data_dict: dict {interval: DataFrame} from fetch_klines_multiple
    - macd_config: dict {"fast": int, "slow": int, "signal": int}

    Returns:
    - dict: {interval: {"macd": float, "signal": float, "hist": float}}
    """
    latest_macd = {}
    
    fast = macd_config.get("fast", 12)
    slow = macd_config.get("slow", 26)
    signal = macd_config.get("signal", 9)

    for interval, df in candle_data_dict.items():
        if df.empty:
            latest_macd[interval] = {"macd": None, "signal": None, "hist": None}
            continue

        close = df["close"].astype(float)

        # MACD calculation
        ema_fast = close.ewm(span=fast, adjust=False).mean()
        ema_slow = close.ewm(span=slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        hist = macd_line - signal_line

        latest_macd[interval] = {
            "macd": float(macd_line.iloc[-1]),
            "signal": float(signal_line.iloc[-1]),
            "hist": float(hist.iloc[-1])
        }

    return latest_macd
