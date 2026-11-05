# ==============================================================================
# MACRO CALENDAR: High-Impact Economic News & Volatility Guard
# ==============================================================================

import time
from datetime import datetime, timezone
import requests
import config_fundamental as cfg

# In-memory Macro State Cache
_MACRO_CACHE = {
    "is_news_freeze": False,
    "active_event": None,
    "minutes_until_event": None,
    "last_checked": 0
}


def check_macro_event_proximity() -> dict:
    """
    Scans upcoming high-impact economic calendar events.
    Returns whether the bot should freeze new trade entries.
    """
    global _MACRO_CACHE
    now_ts = time.time()

    # Rate limiting: Re-evaluate every MACRO_CALENDAR_POLL_INTERVAL
    if (now_ts - _MACRO_CACHE["last_checked"]) < cfg.MACRO_CALENDAR_POLL_INTERVAL:
        return _MACRO_CACHE

    is_freeze = False
    active_event_name = None
    time_diff_mins = None

    try:
        # Public Financial Juice / ForexFactory style macro feed
        # Fallback to structured calendar endpoint
        url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
        res = requests.get(url, timeout=6)

        if res.status_code == 200:
            events = res.json()
            utc_now = datetime.now(timezone.utc)

            for event in events:
                # Target High-Impact USD Events only (they dictate Crypto volatility)
                country = event.get("country", "")
                impact = event.get("impact", "")
                title = event.get("title", "")
                event_date_str = event.get("date", "")

                if country != "USD" or impact != "High":
                    continue

                # Filter by critical keywords (CPI, FOMC, Fed, Payrolls)
                if not any(k.lower() in title.lower() for k in cfg.HIGH_IMPACT_KEYWORDS):
                    continue

                # Parse event datetime (ISO format)
                try:
                    event_dt = datetime.fromisoformat(event_date_str)
                    diff_seconds = (event_dt - utc_now).total_seconds()
                    diff_minutes = diff_seconds / 60.0

                    # Pre-news window: within PRE_NEWS_FREEZE_MINUTES before event
                    # Post-news window: within POST_NEWS_FREEZE_MINUTES after event
                    if -cfg.POST_NEWS_FREEZE_MINUTES <= diff_minutes <= cfg.PRE_NEWS_FREEZE_MINUTES:
                        is_freeze = True
                        active_event_name = title
                        time_diff_mins = round(diff_minutes, 1)
                        break

                except Exception:
                    continue

    except Exception as e:
        print(f"[Macro Calendar Error]: {e}")

    _MACRO_CACHE = {
        "is_news_freeze": is_freeze,
        "active_event": active_event_name,
        "minutes_until_event": time_diff_mins,
        "last_checked": now_ts
    }
    return _MACRO_CACHE


if __name__ == "__main__":
    print("Testing Macro Calendar Guard...")
    data = check_macro_event_proximity()
    print(f"Trading Freeze Status: {'LOCKED ⛔' if data['is_news_freeze'] else 'SAFE TO TRADE ✅'}")
    if data["is_news_freeze"]:
        print(f"Event: {data['active_event']} (in {data['minutes_until_event']} mins)")
    else:
        print("No immediate high-impact USD economic events detected within freeze window.")