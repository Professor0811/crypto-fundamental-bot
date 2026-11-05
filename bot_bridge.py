# ==============================================================================
# BOT BRIDGE: Connects Fundamental Research Bot to Futures Execution Bot
# ==============================================================================

import json
import os
import config_fundamental as cfg

def get_current_market_bias() -> dict:
    """
    Fundamental Bot එක මඟින් save කරන ලද market_bias.json file එක කියවා 
    Futures Bot එකට අවශ්‍ය current macro bias සහ freeze status එක ලබා දෙයි.
    """
    default_bias = {
        "composite_score": 0.0,
        "bias_label": "NEUTRAL",
        "is_news_freeze": False,
        "active_macro_event": None
    }

    if not os.path.exists(cfg.MARKET_BIAS_FILE_PATH):
        return default_bias

    try:
        with open(cfg.MARKET_BIAS_FILE_PATH, "r") as f:
            data = json.load(f)
            return data
    except Exception as e:
        print(f"[Bot Bridge Error] Failed to read bias state: {e}")
        return default_bias

def should_block_trade(side: str) -> tuple[bool, str]:
    """
    Futures Bot එකෙන් trade එකක් (LONG හෝ SHORT) open කරන්න කලින් 
    fundamental conditions මඟින් එය block කළ යුතුදැයි පරීක්ෂා කරයි.
    """
    bias_data = get_current_market_bias()
    
    # 1. Macro News Freeze Check (CPI, FOMC වැනි වෙලාවන් වලදී trades සම්පූර්ණයෙන්ම block කරයි)
    if bias_data.get("is_news_freeze", False):
        event_name = bias_data.get("active_macro_event", "High-Impact Macro Event")
        return True, f"Blocked by Macro Freeze: {event_name}"

    score = bias_data.get("composite_score", 0.0)

    # 2. Heavy Bearish condition එකකදී LONG trades දැමීම වළක්වයි
    if side.upper() == "LONG" and score <= -50.0:
        return True, f"Blocked Long: Market is Strongly Bearish (Score: {score})"

    # 3. Heavy Bullish condition එකකදී SHORT trades දැමීම වළක්වයි
    if side.upper() == "SHORT" and score >= 50.0:
        return True, f"Blocked Short: Market is Strongly Bullish (Score: {score})"

    return False, "Allowed"

if __name__ == "__main__":
    print("Testing Bot Bridge...")
    bias = get_current_market_bias()
    print(f"Current Bias State: {bias.get('bias_label')} (Score: {bias.get('composite_score')})")
    print(f"Is News Freeze: {bias.get('is_news_freeze')}")
    
    # Test sample blocks
    blocked, reason = should_block_trade("LONG")
    print(f"Sample LONG Trade Check -> Blocked: {blocked} | Reason: {reason}")