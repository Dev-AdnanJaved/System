def volume_analysis_report(data,
                           lookback,
                           surge_len,
                           base_mult):
    """
    Volume Surge Analysis using TWO filters:

    OPTION A (Adaptive Absolute Strength)
        - Compares recent volume vs smoothed EMA baseline
        - Adjusts threshold based on volume volatility dynamically
        - Ensures volume is objectively strong

    OPTION B (Relative Expansion)
        - Compares recent volume vs historical average
        - Ensures volume is expanding vs past
        - Protects from entering quiet markets

    Final signal requires BOTH options to pass.

    Returns detailed human-readable explanation.
    """

    # -----------------------------------------------------------
    # Extract 15m volume list from provided data
    # -----------------------------------------------------------
    vols = data['15m']['volume']

    # Safety check → ensure enough candles exist
    if len(vols) < surge_len + 5:
        return {"message": "Not enough candles to evaluate volume."}

    # -----------------------------------------------------------
    # Helper Functions
    # -----------------------------------------------------------

    # --- EMA CALCULATION (for smoothed baseline)
    def ema(values, period):
        k = 2 / (period + 1)          # smoothing factor
        ema_val = values[0]           # starting value
        for v in values[1:]:
            ema_val = v * k + ema_val * (1 - k)
        return ema_val

    # --- Simple mean (average)
    def mean(v):
        return sum(v) / len(v)

    # --- Standard deviation (measure of volume instability)
    def std(v):
        m = mean(v)
        return (sum((x - m) ** 2 for x in v) / len(v)) ** 0.5

    # -----------------------------------------------------------
    # STEP 1 — Define Recent and Historical Windows
    # -----------------------------------------------------------

    # Last N candles → what we want to evaluate (SURGE ZONE)
    recent = vols[-surge_len:]
    avg_recent = mean(recent)

    # Lookback candles → define "normal behaviour"
    look = vols[-lookback:] if len(vols) >= lookback else vols[:-surge_len]

    # Remove recent candles so baseline isn't contaminated
    prev = look[:-surge_len] if len(look) > surge_len else look

    # Historical baseline stats
    avg_prev = mean(prev)

    # Smoothed baseline using EMA
    ema10 = ema(vols[-10:], 10)

    # -----------------------------------------------------------
    # STEP 2 — Measure Volume Volatility and Dynamic Threshold
    # -----------------------------------------------------------
    vol_volatility = std(prev) / max(avg_prev, 1)

    # --- Dynamic multiplier scaling
    multiplier = base_mult + vol_volatility * 3    # scale with volatility
    multiplier = min(multiplier, 1.5)             # cap at 3
    multiplier = max(multiplier, 1.20)            # minimum for stable coins

    threshold = ema10 * multiplier

    # -----------------------------------------------------------
    # ✅ OPTION A — Absolute Strength Filter
    # -----------------------------------------------------------
    optionA_pass = avg_recent > threshold

    # -----------------------------------------------------------
    # ✅ OPTION B — Relative Expansion Filter
    # -----------------------------------------------------------
    spike_ratio = avg_recent / max(avg_prev, 1)
    optionB_pass = spike_ratio > 1.30

    # -----------------------------------------------------------
    # FINAL DECISION (Both filters must agree)
    # -----------------------------------------------------------
    combined_pass = optionA_pass and optionB_pass

    # -----------------------------------------------------------
    # Build Human Explanation Message
    # -----------------------------------------------------------
    msg = (
        f"Volume Analysis Report\n"
        f"---------------------------------\n"
        f"Recent Avg Volume (last {surge_len}): {avg_recent:.2f}\n"
        f"Historical Avg Volume: {avg_prev:.2f}\n"
        f"EMA10 Volume Baseline: {ema10:.2f}\n"
        f"Volume Volatility: {vol_volatility:.3f}\n"
        f"Dynamic Multiplier: {multiplier:.2f}\n"
        f"Option A Threshold: {threshold:.2f}\n\n"
        f"OPTION A — Absolute Strength Check\n"
        f"Result: {'PASS' if optionA_pass else 'FAIL'}\n\n"
        f"OPTION B — Relative Expansion Check\n"
        f"Spike Ratio: {spike_ratio:.2f}\n"
        f"Result: {'PASS' if optionB_pass else 'FAIL'}\n\n"
        f"FINAL VOLUME SIGNAL: "
        f"{'VALID SURGE ✅' if combined_pass else 'NO SURGE ❌'}"
    )

    return {
        "optionA": optionA_pass,
        "optionB": optionB_pass,
        "combined": combined_pass,
        "message": msg
    }
