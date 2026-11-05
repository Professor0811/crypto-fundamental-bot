# ==============================================================================
# ON-CHAIN & DERIVATIVES ENGINE: Bybit V5 Global Mirror (Zero US Geo-Block)
# ==============================================================================
import requests

def fetch_derivatives_metrics() -> dict:
    result = {
        "btc_funding": 0.0001,
        "eth_funding": 0.0001,
        "sol_funding": 0.0001,
        "btc_oi_usd": 0.0,
        "derivatives_score": 0.0,
        "squeeze_status": "BALANCED",
        "source": "Bybit V5 Global"
    }

    endpoints = [
        "https://api.bytick.com/v5/market/tickers?category=linear",
        "https://api.bybit.com/v5/market/tickers?category=linear"
    ]

    tickers_map = {}
    for url in endpoints:
        try:
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                data = res.json()
                items = data.get("result", {}).get("list", [])
                if items:
                    for item in items:
                        sym = item.get("symbol", "")
                        if sym in ["BTCUSDT", "ETHUSDT", "SOLUSDT"]:
                            tickers_map[sym] = {
                                "funding": float(item.get("fundingRate", 0.0001) or 0.0001),
                                "oi_val": float(item.get("openInterestValue", 0.0) or 0.0),
                                "change_24h": float(item.get("price24hPcnt", 0.0) or 0.0) * 100.0
                            }
                    if tickers_map:
                        break
        except Exception:
            continue

    if not tickers_map:
        try:
            res = requests.get("https://www.okx.com/api/v5/public/funding-rate?instId=BTC-USDT-SWAP", timeout=5)
            if res.status_code == 200:
                d = res.json().get("data", [])
                if d:
                    f_rate = float(d[0].get("fundingRate", 0.0001))
                    tickers_map["BTCUSDT"] = {"funding": f_rate, "oi_val": 1500000000.0, "change_24h": 0.5}
                    result["source"] = "OKX Swap Backup"
        except Exception as e:
            print(f"[Derivatives Fallback Warning]: {e}")

    btc = tickers_map.get("BTCUSDT", {"funding": 0.0001, "oi_val": 0.0, "change_24h": 0.0})
    eth = tickers_map.get("ETHUSDT", {"funding": 0.0001, "oi_val": 0.0, "change_24h": 0.0})
    sol = tickers_map.get("SOLUSDT", {"funding": 0.0001, "oi_val": 0.0, "change_24h": 0.0})

    result["btc_funding"] = btc["funding"]
    result["eth_funding"] = eth["funding"]
    result["sol_funding"] = sol["funding"]
    result["btc_oi_usd"] = round(btc["oi_val"] / 1_000_000, 2)

    avg_funding_pct = ((btc["funding"] + eth["funding"]) / 2.0) * 100.0
    btc_chg = btc["change_24h"]

    score = 0.0
    if avg_funding_pct < 0 and btc_chg >= 0:
        score = 65.0
        result["squeeze_status"] = "SHORT SQUEEZE IMMINENT 🚀"
    elif avg_funding_pct < -0.02 and btc_chg < -1.0:
        score = -45.0
        result["squeeze_status"] = "HEAVY SHORT PRESSURE 🩸"
    elif avg_funding_pct > 0.04:
        score = -55.0
        result["squeeze_status"] = "OVERHEATED LONGS (TRAP) ⚠️"
    elif 0.0 <= avg_funding_pct <= 0.025 and btc_chg > 0.5:
        score = 40.0
        result["squeeze_status"] = "INSTITUTIONAL ACCUMULATION 🟢"
    elif btc_chg < -2.0:
        score = -35.0
        result["squeeze_status"] = "LONG UNWINDING 🔴"
    else:
        score = 12.0
        result["squeeze_status"] = "HEALTHY NEUTRAL CARRY ⚡"

    result["derivatives_score"] = round(max(-100.0, min(100.0, score)), 1)
    return result
