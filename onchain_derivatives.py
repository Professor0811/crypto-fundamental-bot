# ==============================================================================
# ON-CHAIN & DERIVATIVES: Funding Rate & Derivatives Bias Tracker
# ==============================================================================

import time
import requests
import config_fundamental as cfg

_DERIVATIVES_CACHE = {
    "funding_rates": {},
    "derivatives_bias_score": 0.0,
    "bias_label": "Neutral",
    "last_checked": 0
}

TARGET_BENCHMARKS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]


def fetch_derivatives_bias() -> dict:
    """
    Binance Futures Public API හරහා Funding Rates fetch කර 
    Derivatives Bias Score එකක් (-100 සිට +100 දක්වා) generate කරයි.
    """
    global _DERIVATIVES_CACHE
    now_ts = time.time()

    if (now_ts - _DERIVATIVES_CACHE["last_checked"]) < cfg.FUNDING_RATE_POLL_INTERVAL:
        return _DERIVATIVES_CACHE

    funding_map = {}
    total_rate = 0.0
    valid_count = 0

    url = "https://fapi.binance.com/fapi/v1/premiumIndex"

    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            # Index into target benchmark pairs
            rate_lookup = {item["symbol"]: float(item.get("lastFundingRate", 0.0)) for item in data if "symbol" in item}

            for sym in TARGET_BENCHMARKS:
                rate = rate_lookup.get(sym, 0.0001)  # standard baseline 0.01%
                funding_pct = rate * 100.0          # convert to percentage
                funding_map[sym] = round(funding_pct, 4)
                total_rate += funding_pct
                valid_count += 1

    except Exception as e:
        print(f"[Derivatives Warning] Binance funding fetch error: {e}")

    # Calculate average benchmark funding rate
    avg_rate = (total_rate / valid_count) if valid_count > 0 else 0.01

    # Bias Logic:
    # 1. Heavily negative funding (< -0.02%) = Short squeeze condition -> Bullish bias (+50 to +80)
    # 2. Overheated positive funding (> 0.05%) = Long squeeze risk -> Bearish / Caution (-50 to -80)
    # 3. Normal / Neutral zone (0.00% to 0.015%) = Stable (+10 to +20)
    if avg_rate <= cfg.EXTREME_NEGATIVE_FUNDING:
        bias_score = 75.0
        label = "Bullish (Short Squeeze Fuel)"
    elif avg_rate >= cfg.EXTREME_POSITIVE_FUNDING:
        bias_score = -75.0
        label = "Bearish (Overheated Longs)"
    elif avg_rate < 0:
        bias_score = 30.0
        label = "Mild Bullish Bias"
    elif avg_rate > 0.02:
        bias_score = -20.0
        label = "Mild Caution"
    else:
        bias_score = 10.0
        label = "Healthy / Neutral"

    _DERIVATIVES_CACHE = {
        "funding_rates": funding_map,
        "average_funding_pct": round(avg_rate, 4),
        "derivatives_bias_score": bias_score,
        "bias_label": label,
        "last_checked": now_ts
    }
    return _DERIVATIVES_CACHE


if __name__ == "__main__":
    print("Testing Derivatives & Funding Rate Tracker...")
    data = fetch_derivatives_bias()
    print("Live Funding Rates (8h):")
    for s, r in data["funding_rates"].items():
        print(f"  • {s}: {r:+.4f}%")
    print(f"Average Benchmark Rate: {data['average_funding_pct']:+.4f}%")
    print(f"Derivatives Bias Score: {data['derivatives_bias_score']} ({data['bias_label']})")