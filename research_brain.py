# ==============================================================================
# RESEARCH BRAIN: Composite Fundamental & Macro Bias Engine
# ==============================================================================

import time
import json
import os
import config_fundamental as cfg
import sentiment_collector as sent
import macro_calendar as macro
import onchain_derivatives as deriv

def calculate_composite_bias() -> dict:
    """
    Fear & Greed, Macro Calendar, සහ Derivatives data එකතු කර 
    අවසාන Composite Bias Score එක (-100 සිට +100 දක්වා) ගණනය කරයි.
    """
    # 1. Gather raw data from modules
    fng_data = sent.fetch_fear_and_greed()
    macro_data = macro.check_macro_event_proximity()
    deriv_data = deriv.fetch_derivatives_bias()

    # 2. Extract normalized scores
    fng_score = fng_data.get("normalized_score", 0.0)       # Range: -100 to +100
    deriv_score = deriv_data.get("derivatives_bias_score", 0.0) # Range: -100 to +100

    # Macro calendar score adjustment: 
    # If high-impact news is coming, score goes to 0 (Neutral / Freeze) and sets freeze flag
    is_freeze = macro_data.get("is_news_freeze", False)
    macro_score = 0.0 if not is_freeze else -50.0  # Caution state during macro events

    # 3. Calculate Weighted Composite Score
    # Weights from config: Fear/Greed (35%), Derivatives (40%), Macro Proximity (25%)
    composite_score = (
        (fng_score * cfg.WEIGHT_FEAR_GREED) +
        (deriv_score * cfg.WEIGHT_DERIVATIVES) +
        (macro_score * cfg.WEIGHT_MACRO_CALENDAR)
    )
    composite_score = round(composite_score, 1)

    # 4. Assign Final Bias Label
    if is_freeze:
        bias_label = "FREEZE_TRADING (High-Impact Macro Event)"
    elif composite_score >= 50.0:
        bias_label = "STRONG_BULLISH"
    elif 20.0 <= composite_score < 50.0:
        bias_label = "LEAN_BULLISH"
    elif -20.0 < composite_score < 20.0:
        bias_label = "NEUTRAL"
    elif -50.0 <= composite_score <= -20.0:
        bias_label = "LEAN_BEARISH"
    else:
        bias_label = "STRONG_BEARISH"

    result = {
        "timestamp": time.time(),
        "composite_score": composite_score,
        "bias_label": bias_label,
        "is_news_freeze": is_freeze,
        "active_macro_event": macro_data.get("active_event"),
        "details": {
            "fear_greed": fng_data,
            "derivatives": deriv_data,
            "macro": macro_data
        }
    }

    # 5. Save State to JSON (IPC Bridge for our Futures Execution Bot)
    try:
        with open(cfg.MARKET_BIAS_FILE_PATH, "w") as f:
            json.dump(result, f, indent=4)
    except Exception as e:
        print(f"[Research Brain Error] Failed to write bias state file: {e}")

    return result


if __name__ == "__main__":
    print("Running Research Brain Synthesis...")
    res = calculate_composite_bias()
    print("==================================================")
    print(f" FINAL COMPOSITE SCORE: {res['composite_score']} / 100")
    print(f" MARKET BIAS LABEL    : {res['bias_label']}")
    print(f" NEWS FREEZE ACTIVE   : {res['is_news_freeze']}")
    print("==================================================")