import os
from dotenv import load_dotenv

load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET", "")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Bot settings
INTERVAL = "15m"
CANDLE_LIMIT = 500

TOP_VOLUME_COINS = 600
LOOP_INTERVAL_SECONDS = 1200

STATE_FILE = "data/state.json"

# Rate limit safety
REQUEST_DELAY_SECONDS = 0.5  # ~2 req/sec
MAX_RETRIES = 5              # retry API calls if 403 / timeout
RETRY_DELAY = 5               # seconds between retries


# Indicators settings
ATR_VALUE = 14
ADX_VALUE = 14
di_period=14
adx_period=14

RSI_PERIODS = 14
MACD_VALUES = {"fast": 12, "slow": 26, "signal": 9}
EMA_PERIODS = [7, 25, 50, 99, 200]


#For Cross Detection Detection
LOOKBACK_CANDLES = 96  #For cross detection in 48 hours as 192/15=48

#For Volume Detection
LOOKBACK_VOLUME_CANDLES = 10  # Last 20 Candles Volume to compare with Surge Candles Volume
SURGE_LENGTH = 4    # Number Of Recent Candles to compare with LookBack Candles of Volume
BASE_MULTI = 1.35     # The percentage of increase in volume, which triggers passed 

