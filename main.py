#EMA_VOLUME_RSI_ADX STRATEGY

import time
from datetime import datetime

#Config Variables
from config import CANDLE_LIMIT, INTERVAL, LOOKBACK_VOLUME_CANDLES, SURGE_LENGTH, BASE_MULTI
from config import EMA_PERIODS, di_period, adx_period, RSI_PERIODS, LOOKBACK_CANDLES
from config import TOP_VOLUME_COINS, LOOP_INTERVAL_SECONDS

#Client and Data
from modules.binance_client.binance_client import get_futures_client
from modules.market_data.market_data import fetch_klines_multiple

#Main Function Which Generates Final Signal
from strategies.Ema_Volume_Rsi_Adx.main import generate_final_signal, print_final_signal_report

#Telegram Notification
from modules.notifications.notifier_telegram import send_telegram

#Indicators
from modules.indicators.ema import get_ema_all_timeframes
from modules.indicators.adx import calculate_adx_multi_intervals
from modules.indicators.rsi import get_latest_rsi
from modules.indicators.volume import get_last_n_volume_with_pressure


def get_all_binance_futures_symbols(client):
    """
    Fetch all available USDT perpetual futures trading pairs from Binance.
    
    Parameters:
        client: Binance futures client
    
    Returns:
        list: List of all USDT perpetual futures symbols
    """
    try:
        print("🔍 Fetching all Binance Futures symbols...")
        
        exchange_info = client.futures_exchange_info()
        
        # Filter for USDT perpetual futures that are actively trading
        symbols = []
        for symbol_info in exchange_info['symbols']:
            # Only get USDT perpetual futures that are trading
            if (symbol_info['symbol'].endswith('USDT') and 
                symbol_info['status'] == 'TRADING' and 
                symbol_info['contractType'] == 'PERPETUAL'):
                symbols.append(symbol_info['symbol'])
        
        symbols.sort()  # Sort alphabetically
        print(f"✅ Found {len(symbols)} USDT perpetual futures pairs")
        
        return symbols
        
    except Exception as e:
        print(f"❌ Error fetching Binance symbols: {str(e)}")
        return []


def get_top_volume_coins(client, top_n):
    """
    Fetch top N coins by 24h trading volume (USDT).
    
    Parameters:
        client: Binance futures client
        top_n: Number of top volume coins to return
    
    Returns:
        list: List of top N symbols by volume
    """
    try:
        print(f"🔍 Fetching top {top_n} coins by 24h volume...")
        
        # Get 24h ticker data for all symbols
        tickers = client.futures_ticker()
        
        # Filter for USDT perpetual futures and sort by quote volume
        usdt_tickers = []
        for ticker in tickers:
            if ticker['symbol'].endswith('USDT'):
                try:
                    volume = float(ticker['quoteVolume'])
                    usdt_tickers.append({
                        'symbol': ticker['symbol'],
                        'volume': volume
                    })
                except (ValueError, KeyError):
                    continue
        
        # Sort by volume (descending) and get top N
        usdt_tickers.sort(key=lambda x: x['volume'], reverse=True)
        top_symbols = [ticker['symbol'] for ticker in usdt_tickers[:top_n]]
        
        print(f"✅ Top {top_n} coins by volume:")
        for i, ticker in enumerate(usdt_tickers[:top_n], 1):
            volume_millions = ticker['volume'] / 1_000_000
            print(f"   {i}. {ticker['symbol']}: ${volume_millions:.2f}M")
        
        return top_symbols
        
    except Exception as e:
        print(f"❌ Error fetching volume data: {str(e)}")
        return []


def process_single_coin(client, symbol):
    """
    Process a single coin and check for trading signals.
    
    Parameters:
        client: Binance futures client
        symbol: Trading pair symbol (e.g., 'BTCUSDT')
    
    Returns:
        signal dict or None
    """
    try:
        print(f"\n{'='*60}")
        print(f"Processing: {symbol}")
        print(f"{'='*60}")
        
        # Fetch market data
        data_dict = fetch_klines_multiple(client, symbol=symbol, intervals=None, limit=CANDLE_LIMIT)
        
        if not data_dict:
            print(f"❌ Failed to fetch data for {symbol}")
            return None
        
        # Calculate all indicators
        ema_data_dict = get_ema_all_timeframes(data_dict, EMA_PERIODS)
        adx_data_dict = calculate_adx_multi_intervals(data_dict, di_period, adx_period)
        rsi_data_dict = get_latest_rsi(data_dict, RSI_PERIODS)
        volume_data_dict = get_last_n_volume_with_pressure(data_dict, CANDLE_LIMIT, use_quote=False)
        
        # Generate Final Signal
        signal = generate_final_signal(
            ema_data_dict, 
            INTERVAL, 
            LOOKBACK_CANDLES, 
            adx_data_dict, 
            rsi_data_dict, 
            volume_data_dict, 
            LOOKBACK_VOLUME_CANDLES, 
            SURGE_LENGTH, 
            BASE_MULTI
        )
        
        if signal:
            print(f"✅ Signal detected for {symbol}: {signal['signal']}")
            return signal
        else:
            print(f"ℹ️ No valid signal for {symbol}")
            return None
            
    except Exception as e:
        print(f"❌ Error processing {symbol}: {str(e)}")
        return None


def send_signal_notification(symbol, signal):
    """
    Send Telegram notification for a detected signal.
    
    Parameters:
        symbol: Trading pair symbol
        signal: Signal dictionary from generate_final_signal
    """
    signal_type = signal['signal']
    
    # Prepare warnings text
    warnings_text = ""
    if signal['warnings']:
        warnings_text = "\n\n⚠️ WARNINGS:\n" + "\n".join([f"  • {w}" for w in signal['warnings']])
    
    # Choose emoji based on signal type
    if signal_type == 'BULLISH':
        emoji = "🟢"
        trend_emoji = "📈"
    else:
        emoji = "🔴"
        trend_emoji = "📉"
    
    message = f"""
{emoji} **{signal_type} SIGNAL DETECTED** {emoji}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Symbol: {symbol}
Timeframe: {INTERVAL}
Status: {signal['status']}

📊 **EMA CROSS DETAILS**
  • Type: {signal['cross']['type'].upper()}
  • Time: {signal['cross']['time']}
  • Hours Ago: {signal['cross']['hours_ago']:.1f}h
  • Candles Ago: {signal['cross']['candles_ago']}
  • EMA200 Trend: {signal['ema200_trend'].upper()} ✅

{trend_emoji} **RSI MOMENTUM**
  • Signal: {signal['rsi']['type'].upper()} ({signal['rsi']['strength']})
  • RSI 15m: {signal['rsi']['rsi_15m']}
  • RSI 1h: {signal['rsi']['rsi_1h']}

💪 **ADX TREND STRENGTH**
  • Strength: {signal['adx']['strength'].upper()}
  • ADX 15m: {signal['adx']['adx_15m']}
  • ADX 1h: {signal['adx']['adx_1h']}

📊 **VOLUME ANALYSIS**
  • Surge Confirmed: YES ✅
  • Option A: {'PASS ✓' if signal['volume']['optionA'] else 'FAIL ✗'}
  • Option B: {'PASS ✓' if signal['volume']['optionB'] else 'FAIL ✗'}
  • Recent Avg: {signal['volume'].get('recent_avg_volume', 'N/A')}
  • Historical Avg: {signal['volume'].get('historical_avg_volume', 'N/A')}
  • Spike Ratio: {signal['volume'].get('spike_ratio', 'N/A')}{warnings_text}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    send_telegram(message)
    print(f"✅ {signal_type} signal sent to Telegram for {symbol}")


def main():
    """
    Main function to run the trading signal scanner.
    Filters coins by volume and continuously checks them for signals.
    """
    print("\n" + "="*60)
    print("EMA VOLUME RSI ADX STRATEGY - MULTI-COIN SCANNER")
    print("="*60)
    
    # Initialize Binance client
    client = get_futures_client()
    
    # Determine which coins to check based on volume filter
    if TOP_VOLUME_COINS is None or not isinstance(TOP_VOLUME_COINS, int):
        # No volume filter - get all coins
        print("📡 Mode: ALL COINS (No volume filter)")
        coins_list = get_all_binance_futures_symbols(client)
        if not coins_list:
            print("❌ Failed to fetch symbols. Exiting...")
            return
        volume_filtered = False
    else:
        # Volume filter enabled - get top N coins by volume
        print(f"📡 Mode: TOP {TOP_VOLUME_COINS} COINS BY VOLUME")
        coins_list = get_top_volume_coins(client, TOP_VOLUME_COINS)
        if not coins_list:
            print("❌ Failed to fetch top volume coins. Exiting...")
            return
        volume_filtered = True
    
    print(f"\nCoins to monitor: {len(coins_list)}")
    if volume_filtered:
        print(f"Volume Filter: Top {TOP_VOLUME_COINS} by 24h volume")
        print(f"Coins: {', '.join(coins_list)}")
    else:
        print(f"Volume Filter: DISABLED (All coins)")
        print(f"First 10: {', '.join(coins_list[:10])}...")
    
    print(f"Loop interval: {LOOP_INTERVAL_SECONDS} seconds ({LOOP_INTERVAL_SECONDS/60:.1f} minutes)")
    print(f"Timeframe: {INTERVAL}")
    print("="*60)
    
    iteration = 0
    
    while True:
        iteration += 1
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\n{'#'*60}")
        print(f"ITERATION #{iteration} - {current_time}")
        print(f"{'#'*60}")
        
        # Refresh coin list periodically
        if iteration % 10 == 0:  # Refresh every 10 iterations
            print("🔄 Refreshing coin list...")
            if volume_filtered:
                new_coins_list = get_top_volume_coins(client, TOP_VOLUME_COINS)
            else:
                new_coins_list = get_all_binance_futures_symbols(client)
            
            if new_coins_list:
                coins_list = new_coins_list
        
        signals_found = 0
        
        # Process each coin
        for idx, symbol in enumerate(coins_list, 1):
            print(f"\n[{idx}/{len(coins_list)}] Checking {symbol}...")
            
            signal = process_single_coin(client, symbol)
            
            if signal:
                signals_found += 1
                send_signal_notification(symbol, signal)
                # Optional: Print detailed report to console
                # print_final_signal_report(signal)
            
            # Small delay between API calls to avoid rate limits
            time.sleep(0.5)
        
        # Summary
        print(f"\n{'='*60}")
        print(f"Iteration #{iteration} Summary:")
        print(f"  • Coins scanned: {len(coins_list)}")
        print(f"  • Signals found: {signals_found}")
        if volume_filtered:
            print(f"  • Volume filter: Top {TOP_VOLUME_COINS}")
        print(f"  • Next scan in: {LOOP_INTERVAL_SECONDS} seconds ({LOOP_INTERVAL_SECONDS/60:.1f} minutes)")
        print(f"{'='*60}")
        
        # Wait before next iteration
        print(f"\n⏳ Waiting {LOOP_INTERVAL_SECONDS} seconds before next scan...")
        time.sleep(LOOP_INTERVAL_SECONDS)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Scanner stopped by user (Ctrl+C)")
        print("Exiting gracefully...")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()