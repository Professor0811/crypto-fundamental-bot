# ==============================================================================
# BOT BRIDGE: Verified Supabase Cloud Sync + Telegram Regime Shift Alerts
# ==============================================================================
import os
import json
import requests
import psycopg2
import config_fundamental as cfg

DATABASE_URL = os.environ.get("DATABASE_URL", "")
_LAST_ALERTED_BIAS = None
_LAST_ALERTED_FREEZE = False

def _clean_db_url(url: str) -> str:
    if not url:
        return ""
    url = url.strip()
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url

def send_regime_telegram_alert(message: str):
    token = cfg.TELEGRAM_BOT_TOKEN
    chat_id = cfg.TELEGRAM_CHAT_ID
    if not token or not chat_id:
        return
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}, timeout=5)
    except Exception as e:
        print(f"[Telegram Alert Error]: {e}")

def update_supabase_bias(payload: dict):
    global _LAST_ALERTED_BIAS, _LAST_ALERTED_FREEZE

    db_url = _clean_db_url(DATABASE_URL)
    if not db_url or "[YOUR-PASSWORD]" in db_url:
        print("[Supabase Bridge Warning]: Valid DATABASE_URL not set!")
        return False

    score = float(payload.get("composite_score", 0.0))
    label = str(payload.get("bias_label", "NEUTRAL"))
    freeze = bool(payload.get("is_news_freeze", False))
    event = payload.get("active_macro_event")
    blacklist_str = ",".join(payload.get("blacklisted_tokens", []))
    btc_dom = float(payload.get("btc_dominance", 54.0))
    alt_status = str(payload.get("altseason_status", "NEUTRAL"))
    sent_score = float(payload.get("sentiment_score", 0.0))
    deriv_score = float(payload.get("derivatives_score", 0.0))
    headlines_str = json.dumps(payload.get("headlines", [])[:6])

    try:
        conn = psycopg2.connect(db_url, sslmode="require", connect_timeout=6)
        cursor = conn.cursor()

        query = """
            INSERT INTO public.market_bias (
                id, composite_score, bias_label, is_news_freeze, active_macro_event,
                blacklisted_tokens, btc_dominance, altseason_status,
                sentiment_score, derivatives_score, headlines_json, updated_at
            )
            VALUES (1, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            ON CONFLICT (id) DO UPDATE SET
                composite_score = EXCLUDED.composite_score,
                bias_label = EXCLUDED.bias_label,
                is_news_freeze = EXCLUDED.is_news_freeze,
                active_macro_event = EXCLUDED.active_macro_event,
                blacklisted_tokens = EXCLUDED.blacklisted_tokens,
                btc_dominance = EXCLUDED.btc_dominance,
                altseason_status = EXCLUDED.altseason_status,
                sentiment_score = EXCLUDED.sentiment_score,
                derivatives_score = EXCLUDED.derivatives_score,
                headlines_json = EXCLUDED.headlines_json,
                updated_at = NOW();
        """
        cursor.execute(query, (
            score, label, freeze, event, blacklist_str,
            btc_dom, alt_status, sent_score, deriv_score, headlines_str
        ))
        conn.commit()
        cursor.close()
        conn.close()

        if (_LAST_ALERTED_BIAS is not None and _LAST_ALERTED_BIAS != label) or (_LAST_ALERTED_FREEZE != freeze):
            alert_msg = (
                f"🧠 *Fundamental Regime Shift Detected!*\n"
                f"• New Bias: `{label} ({score:+.1f})`\n"
                f"• News Freeze: `{'⛔ ACTIVE (' + str(event) + ')' if freeze else '✅ CLEAR'}`\n"
                f"• BTC Dominance: `{btc_dom:.1f}% ({alt_status})`\n"
                f"• Blacklisted Coins: `{blacklist_str if blacklist_str else 'None 🛡️'}`"
            )
            send_regime_telegram_alert(alert_msg)

        _LAST_ALERTED_BIAS = label
        _LAST_ALERTED_FREEZE = freeze
        return True
    except Exception as e:
        print(f"[Supabase Push Error]: {e}")
        return False
