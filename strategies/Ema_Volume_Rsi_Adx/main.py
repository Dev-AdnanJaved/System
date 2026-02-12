"""
Final Signal Generator
Combines all strategy components to generate a final bullish/bearish trading signal.
Only returns a signal when ALL criteria are met, otherwise returns None.
"""

from .Ema_Cross_Detection.Ema_Volume import get_recent_ema_cross
from .ADX.adx import get_adx_strength
from .RSI.rsi import get_rsi_signal
from .Volume_Detection.volume_detection import volume_analysis_report





def generate_final_signal(
    ema_data_dict,
    timeframe,
    lookback_candles,
    adx_data_dict,
    rsi_data_dict,
    volume_data_dict,
    volume_lookback=20,
    surge_len=4,
    base_mult=1.5
):
    """
    Generate final trading signal by combining all strategy components.
    
    Signal Criteria (ALL must be met):
    1. EMA Cross detected within 48 hours
    2. EMA200 trend aligned with cross type (rising for bullish, falling for bearish)
    3. ADX check (weak or strong - both acceptable with warnings)
    4. RSI confirmation (strict or warning mode)
    5. Volume surge (BOTH Option A and Option B must pass)
    
    Parameters:
        ema_data_dict: EMA data for cross detection
        timeframe: Timeframe for EMA analysis
        lookback_candles: Lookback period for EMA cross
        adx_data_dict: ADX data for trend strength
        rsi_data_dict: RSI data for momentum
        volume_data_dict: Volume data for surge analysis
        volume_lookback: Lookback period for volume analysis
        surge_len: Recent candles to check for volume surge
        base_mult: Base multiplier for volume threshold
    
    Returns:
        dict: Final signal with all components if ALL criteria met
        None: If any criteria not met
    """
    
    # ========== STEP 1: EMA CROSS DETECTION ==========
    # print("=" * 60)
    # print("STEP 1: CHECKING EMA CROSS")
    # print("=" * 60)
    
    cross_result = get_recent_ema_cross(ema_data_dict, timeframe, lookback_candles)
    
    if not cross_result or cross_result == "No Cross Happened":
        # print("❌ NO EMA CROSS DETECTED - Signal Generation Stopped")
        return None
    
    # Check if cross happened within 48 hours
    hours_ago = cross_result.get('hours_ago', float('inf'))
    if hours_ago > 48:
        # print(f"❌ EMA CROSS TOO OLD ({hours_ago:.1f} hours ago) - Signal Generation Stopped")
        return None
    
    cross_type = cross_result.get('type')
    ema200_trend = cross_result.get('ema200_trend')
    
    # print(f"✓ Cross Type: {cross_type.upper()}")
    # print(f"✓ Cross Time: {cross_result.get('time')} ({hours_ago:.1f} hours ago)")
    # print(f"✓ EMA200 Trend: {ema200_trend}")
    
    # ========== STEP 2: EMA200 TREND VALIDATION ==========
    # print("\n" + "=" * 60)
    # print("STEP 2: VALIDATING EMA200 TREND")
    # print("=" * 60)
    
    trend_valid = False
    if cross_type == 'bullish' and ema200_trend == 'rising':
        # print("✓ BULLISH CROSS with RISING EMA200 - Trend Aligned")
        trend_valid = True
    elif cross_type == 'bearish' and ema200_trend == 'falling':
        # print("✓ BEARISH CROSS with FALLING EMA200 - Trend Aligned")
        trend_valid = True
    else:
        # print(f"❌ TREND MISMATCH: {cross_type} cross but EMA200 is {ema200_trend}")
        return None
    
    # ========== STEP 3: ADX STRENGTH CHECK ==========
    # print("\n" + "=" * 60)
    # print("STEP 3: CHECKING ADX TREND STRENGTH")
    # print("=" * 60)
    
    adx_result = get_adx_strength(adx_data_dict)
    
    if not adx_result:
        # print("❌ ADX DATA NOT AVAILABLE")
        return None
    
    adx_strength = adx_result.get('strength')
    adx_message = adx_result.get('message')
    
    # print(f"ADX Strength: {adx_strength.upper()}")
    # print(f"Message: {adx_message}")
    
    # ADX is acceptable at any strength (will be flagged in final signal)
    adx_warning = ""
    if adx_strength == "very weak":
        adx_warning = "⚠️ WARNING: Very weak trend - proceed with caution"
    elif adx_strength == "weak":
        adx_warning = "⚠️ WARNING: Weak trend - monitor closely"
    
    # ========== STEP 4: RSI MOMENTUM CHECK ==========
    # print("\n" + "=" * 60)
    # print("STEP 4: CHECKING RSI MOMENTUM")
    # print("=" * 60)
    
    rsi_result = get_rsi_signal(rsi_data_dict)
    
    if not rsi_result:
        # print("❌ RSI DATA NOT AVAILABLE")
        return None
    
    rsi_type = rsi_result.get('type')
    rsi_strength = rsi_result.get('strength')
    rsi_message = rsi_result.get('message')
    
    # print(f"RSI Signal: {rsi_type.upper()} ({rsi_strength})")
    # print(f"Message: {rsi_message}")
    
    # RSI validation (warning signals are acceptable)
    rsi_valid = False
    rsi_warning = ""
    
    if cross_type == rsi_type:
        if rsi_strength == 'strong':
            # print(f"✓ RSI CONFIRMS {cross_type.upper()} signal strongly")
            rsi_valid = True
        elif rsi_strength == 'weak':
            # print(f"⚠️ RSI CONFIRMS {cross_type.upper()} signal but with weakness")
            rsi_valid = True
            rsi_warning = f"⚠️ WARNING: RSI shows weak {rsi_type} signal"
    else:
        # print(f"❌ RSI CONFLICT: Cross is {cross_type} but RSI shows {rsi_type}")
        return None
    
    # ========== STEP 5: VOLUME SURGE VALIDATION ==========
    # print("\n" + "=" * 60)
    # print("STEP 5: VALIDATING VOLUME SURGE")
    # print("=" * 60)
    
    volume_result = volume_analysis_report(
        volume_data_dict,
        lookback=volume_lookback,
        surge_len=surge_len,
        base_mult=base_mult
    )
    
    if not volume_result:
        # print("❌ VOLUME DATA NOT AVAILABLE")
        return None
    
    volume_combined = volume_result.get('combined', False)
    volume_message = volume_result.get('message', '')
    
    # print(volume_message)
    
    if not volume_combined:
        # print("\n❌ VOLUME SURGE NOT CONFIRMED - Both Option A and B must pass")
        return None
    
    # print("\n✓ VOLUME SURGE CONFIRMED - Both options passed")
    
    # ========== FINAL SIGNAL GENERATION ==========
    # print("\n" + "=" * 60)
    # print("FINAL SIGNAL GENERATION")
    # print("=" * 60)
    
    # Extract RSI values from message
    rsi_15m = None
    rsi_1h = None
    try:
        # Parse RSI message: "RSI 15m is XX.XX and RSI 1h is XX.XX"
        parts = rsi_message.split()
        for i, part in enumerate(parts):
            if part == "is" and i > 0:
                if "15m" in parts[i-1]:
                    rsi_15m = float(parts[i+1])
                elif "1h" in parts[i-1]:
                    rsi_1h = float(parts[i+1])
    except:
        pass
    
    # Extract ADX values from message
    adx_15m = None
    adx_1h = None
    try:
        # Parse ADX message: "ADX 15m: XX.XX, ADX 1h: XX.XX"
        parts = adx_message.split()
        for i, part in enumerate(parts):
            if "15m:" in part:
                adx_15m = float(parts[i+1].rstrip(','))
            elif "1h:" in part:
                adx_1h = float(parts[i+1])
    except:
        pass
    
    # Compile final signal
    final_signal = {
        "signal": cross_type.upper(),
        "status": "VALID SIGNAL",
        
        # Cross Information
        "cross": {
            "type": cross_type,
            "time": cross_result.get('time'),
            "hours_ago": hours_ago,
            "candles_ago": cross_result.get('candles_ago')
        },
        
        # EMA200 Trend
        "ema200_trend": ema200_trend,
        
        # RSI Details
        "rsi": {
            "type": rsi_type,
            "strength": rsi_strength,
            "rsi_15m": rsi_15m,
            "rsi_1h": rsi_1h,
            "message": rsi_message
        },
        
        # ADX Details
        "adx": {
            "strength": adx_strength,
            "adx_15m": adx_15m,
            "adx_1h": adx_1h,
            "message": adx_message
        },
        
        # Volume Details
        "volume": {
            "surge_confirmed": volume_combined,
            "optionA": volume_result.get('optionA'),
            "optionB": volume_result.get('optionB'),
            "recent_avg_volume": volume_result.get('recent_avg_volume'),
            "historical_avg_volume": volume_result.get('historical_avg_volume'),
            "ema10_baseline": volume_result.get('ema10_baseline'),
            "volatility": volume_result.get('volatility'),
            "dynamic_multiplier": volume_result.get('dynamic_multiplier'),
            "spike_ratio": volume_result.get('spike_ratio'),
            "full_message": volume_message
        },
        
        # Warnings
        "warnings": []
    }
    
    # Add warnings if any
    if adx_warning:
        final_signal["warnings"].append(adx_warning)
    if rsi_warning:
        final_signal["warnings"].append(rsi_warning)
    
    # Print final signal summary
    # print(f"\n🎯 FINAL SIGNAL: {cross_type.upper()}")
    # print(f"   Cross Time: {cross_result.get('time')} ({hours_ago:.1f}h ago)")
    # print(f"   EMA200 Trend: {ema200_trend}")
    # print(f"   RSI: {rsi_type} ({rsi_strength}) | 15m: {rsi_15m}, 1h: {rsi_1h}")
    # print(f"   ADX: {adx_strength} | 15m: {adx_15m}, 1h: {adx_1h}")
    # print(f"   Volume: SURGE CONFIRMED ✓")
    
    # if final_signal["warnings"]:
    #     print(f"\n⚠️  WARNINGS:")
    #     for warning in final_signal["warnings"]:
    #         print(f"   {warning}")
    
    # print("=" * 60)
    
    return final_signal


def print_final_signal_report(signal):
    """
    Print a formatted report of the final signal.
    
    Parameters:
        signal: Output from generate_final_signal() or None
    """
    if not signal:
        print("\n" + "=" * 60)
        print("NO TRADING SIGNAL GENERATED")
        print("=" * 60)
        print("All criteria were not met. No valid signal at this time.")
        return
    
    print("\n" + "=" * 70)
    print(f"{'FINAL TRADING SIGNAL':^70}")
    print("=" * 70)
    
    print(f"\n🎯 SIGNAL TYPE: {signal['signal']}")
    print(f"   Status: {signal['status']}")
    
    print(f"\n📊 EMA CROSS DETAILS")
    print(f"   Type: {signal['cross']['type'].upper()}")
    print(f"   Time: {signal['cross']['time']}")
    print(f"   Hours Ago: {signal['cross']['hours_ago']:.1f}h")
    print(f"   Candles Ago: {signal['cross']['candles_ago']}")
    print(f"   EMA200 Trend: {signal['ema200_trend'].upper()}")
    
    print(f"\n📈 RSI MOMENTUM")
    print(f"   Signal: {signal['rsi']['type'].upper()} ({signal['rsi']['strength']})")
    print(f"   RSI 15m: {signal['rsi']['rsi_15m']}")
    print(f"   RSI 1h: {signal['rsi']['rsi_1h']}")
    
    print(f"\n💪 ADX TREND STRENGTH")
    print(f"   Strength: {signal['adx']['strength'].upper()}")
    print(f"   ADX 15m: {signal['adx']['adx_15m']}")
    print(f"   ADX 1h: {signal['adx']['adx_1h']}")
    
    print(f"\n📊 VOLUME ANALYSIS")
    print(f"   Surge Confirmed: {'YES ✓' if signal['volume']['surge_confirmed'] else 'NO ✗'}")
    print(f"   Option A (Absolute Strength): {'PASS ✓' if signal['volume']['optionA'] else 'FAIL ✗'}")
    print(f"   Option B (Relative Expansion): {'PASS ✓' if signal['volume']['optionB'] else 'FAIL ✗'}")
    print(f"   Recent Avg Volume: {signal['volume'].get('recent_avg_volume', 'N/A')}")
    print(f"   Historical Avg Volume: {signal['volume'].get('historical_avg_volume', 'N/A')}")
    print(f"   Volatility: {signal['volume'].get('volatility', 'N/A')}")
    
    if signal['warnings']:
        print(f"\n⚠️  WARNINGS:")
        for warning in signal['warnings']:
            print(f"   {warning}")
    
    print("\n" + "=" * 70)


# Example usage
if __name__ == "__main__":
    # This is example code - you'll need to pass actual data dictionaries
    
    print("Final Signal Generator Module Loaded")
    print("\nUsage:")
    print("------")
    print("from final_signal_generator import generate_final_signal, print_final_signal_report")
    print()
    print("signal = generate_final_signal(")
    print("    ema_data_dict=your_ema_data,")
    print("    timeframe='15m',")
    print("    lookback_candles=200,")
    print("    adx_data_dict=your_adx_data,")
    print("    rsi_data_dict=your_rsi_data,")
    print("    volume_data_dict=your_volume_data")
    print(")")
    print()
    print("if signal:")
    print("    print_final_signal_report(signal)")
    print("    # Execute trade based on signal['signal'] (BULLISH or BEARISH)")
    print("else:")
    print("    print('No valid signal - criteria not met')")