# ==============================================================================
# RESEARCH BRAIN: 4-Pillar Institutional Synthesis & BTC Dominance Engine
# ==============================================================================
import requests
import config_fundamental as cfg
import sentiment_collector as sentiment
import onchain_derivatives as derivatives
import macro_calendar as macro
import bot_bridge

def fetch_btc_dominance_and_altseason() -> dict:
    try:
        res = requests.get("https://api.coingecko.com/api/v3/global", timeout=5)
        if res.status_code == 200:
            data = res.json().get("data", {})
            mcap_pct = data.get("market_cap_percentage", {})
            btc_d = float(mcap_pct.get("btc", 54.0))
            eth_d = float(mcap_pct.get("eth", 13.0))
            mcap_chg = float(data.get("market_cap_change_percentage_24h_usd", 0.0))

            if btc_d > 58.0 and mcap_chg < -1.5:
                return {"btc_d": round(btc_d, 2), "eth_d": round(eth_d, 2), "dom_score": -40.0, "alt_status": "ALTCOIN BLEED ⚠️"}
            elif btc_d < 52.0 and mcap_chg > 0.5:
                return {"btc_d": round(btc_d, 2), "eth_d": round(eth_d, 2), "dom_score": 45.0, "alt_status": "ALTCOIN SEASON 🚀"}
            elif mcap_chg >= 1.0:
                return {"btc_d": round(btc_d, 2), "eth_d": round(eth_d, 2), "dom_score": 25.0, "alt_status": "RISK-ON INFLOW 🟢"}
            elif mcap_chg <= -2.0:
                return {"btc_d": round(btc_d, 2), "eth_d": round(eth_d, 2), "dom_score": -35.0, "alt_status": "RISK-OFF OUTFLOW 🔴"}
            else:
                return {"btc_d": round(btc_d, 2), "eth_d": round(eth_d, 2), "dom_score": 10.0, "alt_status": "ROTATION STABLE ⚡"}
    except Exception as e:
        print(f"[BTC Dominance Fetch Warning]: {e}")

    return {"btc_d": 55.4, "eth_d": 13.2, "dom_score": 5.0, "alt_status": "STABLE FLOW ⚡"}

def calculate_composite_bias() -> dict:
    deriv_data = derivatives.fetch_derivatives_metrics()
    deriv_score = deriv_data.get("derivatives_score", 0.0)

    sent_data = sentiment.get_combined_sentiment()
    sent_score = sent_data.get("sentiment_score", 0.0)

    dom_data = fetch_btc_dominance_and_altseason()
    dom_score = dom_data.get("dom_score", 0.0)

    try:
        macro_data = macro.check_macro_safety()
    except Exception:
        macro_data = {"is_freeze": False, "active_event": None, "macro_score": 10.0}

    is_freeze = bool(macro_data.get("is_freeze", False))
    macro_score = -80.0 if is_freeze else float(macro_data.get("macro_score", 10.0))

    composite = (
        (deriv_score * cfg.WEIGHT_DERIVATIVES) +
        (sent_score * cfg.WEIGHT_SENTIMENT) +
        (dom_score * cfg.WEIGHT_DOMINANCE) +
        (macro_score * cfg.WEIGHT_MACRO)
    )
    composite_score = round(max(-100.0, min(100.0, composite)), 1)

    if is_freeze:
        bias_label = "MACRO_FREEZE"
    elif composite_score >= 45.0:
        bias_label = "STRONG_BULLISH"
    elif composite_score >= 15.0:
        bias_label = "BULLISH"
    elif composite_score <= -45.0:
        bias_label = "STRONG_BEARISH"
    elif composite_score <= -15.0:
        bias_label = "BEARISH"
    else:
        bias_label = "NEUTRAL"

    payload = {
        "composite_score": composite_score,
        "bias_label": bias_label,
        "is_news_freeze": is_freeze,
        "active_macro_event": macro_data.get("active_event") or "None (Clear Trading Window)",
        "sentiment_score": sent_score,
        "fng_value": sent_data.get("fng_value", 50),
        "fng_label": sent_data.get("fng_label", "Neutral"),
        "bull_news": sent_data.get("bull_news", 0),
        "bear_news": sent_data.get("bear_news", 0),
        "derivatives_score": deriv_score,
        "btc_funding": deriv_data.get("btc_funding", 0.0001),
        "eth_funding": deriv_data.get("eth_funding", 0.0001),
        "sol_funding": deriv_data.get("sol_funding", 0.0001),
        "btc_oi_usd": deriv_data.get("btc_oi_usd", 0.0),
        "squeeze_status": deriv_data.get("squeeze_status", "BALANCED"),
        "deriv_source": deriv_data.get("source", "Bybit V5"),
        "btc_dominance": dom_data.get("btc_d", 55.0),
        "altseason_status": dom_data.get("alt_status", "STABLE"),
        "dom_score": dom_score,
        "blacklisted_tokens": sent_data.get("blacklisted_tokens", []),
        "headlines": sent_data.get("headlines", [])
    }

    synced = bot_bridge.update_supabase_bias(payload)
    payload["supabase_synced"] = synced
    return payload
