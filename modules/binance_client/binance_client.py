from binance.client import Client
from config import BINANCE_API_KEY, BINANCE_API_SECRET

def get_futures_client():
    # Use standard Binance REST API URL for futures
    client = Client(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=False)
    client.API_URL = 'https://api.binance.com/api'
    
    # Set User-Agent and headers to avoid WAF 403
    client.session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-MBX-APIKEY": BINANCE_API_KEY
    })
    
    # Try using a different endpoint or proxy if available, but for now just ensure standard client setup
    return client
