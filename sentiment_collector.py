# ==============================================================================
# SENTIMENT COLLECTOR: Fear & Greed Index & Breaking News Analyzer
# ==============================================================================

import time
import requests
import config_fundamental as cfg

# In-memory sentiment cache
_SENTIMENT_CACHE = {
    "fear_greed_raw": 50,
    "sentiment_label": "Neutral",
    "normalized_score": 0.0,
    "last_updated": 0
}


def fetch_fear_and_greed() -> dict:
    """
    Alternative.me API එක හරහා Crypto Fear & Greed Index එක ලබා ගනී.
    Cache එකක් භාවිතා කර polling interval එකට අනුකූලව run වේ.
    """
    global _SENTIMENT_CACHE
    now = time.time()

    # Cache check (re-use within polling interval to prevent rate limit)
    if (now - _SENTIMENT_CACHE["last_updated"]) < cfg.SENTIMENT_POLL_INTERVAL:
        return _SENTIMENT_CACHE

    url = "https://api.alternative.me/fng/?limit=1"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json().get("data", [])[0]
            val = float(data.get("value", 50))
            label = data.get("value_classification", "Neutral")

            # 0..100 අගය -100..+100 standard score එකකට පරිවර්තනය කිරීම
            # Formula: (value - 50) * 2
            normalized = (val - 50.0) * 2.0

            _SENTIMENT_CACHE = {
                "fear_greed_raw": int(val),
                "sentiment_label": label,
                "normalized_score": round(normalized, 1),
                "last_updated": now
            }
            return _SENTIMENT_CACHE
    except Exception as e:
        print(f"[Sentiment Error] Fear & Greed fetch failed: {e}")

    return _SENTIMENT_CACHE


def score_news_headline(headline: str) -> float:
    """
    Crypto headlines සරලව scan කර sentiment score එකක් (-1.0 සිට +1.0) ලබා දෙයි.
    """
    bullish_keywords = [
        "etf", "approval", "partnership", "surge", "rally", "all-time high",
        "accumulate", "inflow", "upgrade", "bullish", "launch", "breakout"
    ]
    bearish_keywords = [
        "hack", "scam", "lawsuit", "sec", "ban", "dump", "crash",
        "outflow", "liquidation", "insolvent", "bearish", "investigation"
    ]

    h_lower = headline.lower()
    score = 0.0

    for word in bullish_keywords:
        if word in h_lower:
            score += 0.3
    for word in bearish_keywords:
        if word in h_lower:
            score -= 0.4

    # Bound within -1.0 to +1.0
    return max(-1.0, min(1.0, score))


if __name__ == "__main__":
    print("Testing Sentiment Collector...")
    data = fetch_fear_and_greed()
    print(f"Fear & Greed Index: {data['fear_greed_raw']} ({data['sentiment_label']})")
    print(f"Normalized Bias Score: {data['normalized_score']} / 100")