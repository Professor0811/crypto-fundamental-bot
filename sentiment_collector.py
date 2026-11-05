# ==============================================================================
# SENTIMENT & NEWS ENGINE: Fear & Greed + Live RSS Headlines + Exploit Shield
# ==============================================================================
import requests
import xml.etree.ElementTree as ET
import config_fundamental as cfg

def fetch_fear_and_greed() -> dict:
    try:
        res = requests.get("https://api.alternative.me/fng/?limit=1", timeout=5)
        if res.status_code == 200:
            data = res.json().get("data", [])
            if data:
                val = int(data[0].get("value", 50))
                label = data[0].get("value_classification", "Neutral")
                norm_score = (val - 50) * 2.0
                return {"fng_value": val, "fng_label": label, "fng_score": norm_score}
    except Exception as e:
        print(f"[F&G Fetch Error]: {e}")
    return {"fng_value": 50, "fng_label": "Neutral", "fng_score": 0.0}

def fetch_live_crypto_news_and_blacklist() -> dict:
    rss_urls = [
        "https://cointelegraph.com/rss",
        "https://www.coindesk.com/arc/outboundfeeds/rss/"
    ]
    headlines = []
    bull_hits = 0
    bear_hits = 0
    blacklisted = set()
    headers = {"User-Agent": "Mozilla/5.0 (compatible; ChamaQuantBot/2.0)"}

    for url in rss_urls:
        try:
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                root = ET.fromstring(res.content)
                for item in root.findall(".//item")[:12]:
                    title_el = item.find("title")
                    if title_el is not None and title_el.text:
                        title = title_el.text.strip()
                        title_lower = title.lower()

                        item_tag = "NEUTRAL"
                        if any(k in title_lower for k in cfg.BULLISH_KEYWORDS):
                            bull_hits += 1
                            item_tag = "BULLISH"
                        if any(k in title_lower for k in cfg.BEARISH_KEYWORDS):
                            bear_hits += 1
                            item_tag = "BEARISH"

                        if any(trig in title_lower for trig in cfg.BLACKLIST_TRIGGERS):
                            for tok in cfg.TRACKED_TOKENS:
                                if f" {tok.lower()} " in f" {title_lower} " or f"({tok.lower()})" in title_lower:
                                    if tok not in ["BTC", "ETH"]:
                                        blacklisted.add(f"{tok}USDT")
                                        item_tag = f"🚨 BLACKLIST ({tok})"

                        if len(headlines) < 10:
                            headlines.append({"title": title[:95], "tag": item_tag})
        except Exception:
            continue

    total_hits = bull_hits + bear_hits
    news_score = ((bull_hits - bear_hits) / total_hits) * 75.0 if total_hits > 0 else 0.0

    return {
        "news_score": round(news_score, 1),
        "bull_count": bull_hits,
        "bear_count": bear_hits,
        "blacklisted_tokens": list(blacklisted),
        "headlines": headlines
    }

def get_combined_sentiment() -> dict:
    fng = fetch_fear_and_greed()
    news = fetch_live_crypto_news_and_blacklist()
    combined_score = (fng["fng_score"] * 0.40) + (news["news_score"] * 0.60)
    return {
        "sentiment_score": round(max(-100.0, min(100.0, combined_score)), 1),
        "fng_value": fng["fng_value"],
        "fng_label": fng["fng_label"],
        "news_score": news["news_score"],
        "bull_news": news["bull_count"],
        "bear_news": news["bear_count"],
        "blacklisted_tokens": news["blacklisted_tokens"],
        "headlines": news["headlines"]
    }
