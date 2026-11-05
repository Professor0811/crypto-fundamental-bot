# ==============================================================================
# CRYPTO FUNDAMENTAL RESEARCH & MACRO BIAS ENGINE CONFIGURATION
# ==============================================================================

import os

# --- 1. DATA REFRESH INTERVALS (Seconds) ---
SENTIMENT_POLL_INTERVAL = 300       # Fear & Greed Index fetch interval (Every 5 mins)
MACRO_CALENDAR_POLL_INTERVAL = 900  # Economic calendar scan (Every 15 mins)
FUNDING_RATE_POLL_INTERVAL = 180    # Derivatives Funding & OI check (Every 3 mins)
SYNTHESIS_INTERVAL = 60             # Composite score recalculation loop (Every 1 min)

# --- 2. SHARED STATE / IPC BRIDGE ---
# Execution Bot එකට මේ bias file එක කියවලා trade decisions filter කරන්න පුළුවන්
MARKET_BIAS_FILE_PATH = os.environ.get("MARKET_BIAS_FILE_PATH", "market_bias.json")

# --- 3. HIGH-IMPACT MACRO VOLATILITY LOCKS (CPI, FOMC, NFP) ---
# High impact economic news එකකට පෙර සහ පසු trading freeze කරන කාලය (මිනිත්තු වලින්)
PRE_NEWS_FREEZE_MINUTES = 30        # Freeze new entries 30 mins before major news
POST_NEWS_FREEZE_MINUTES = 15       # Keep frozen for 15 mins after news to let dust settle

# Target High-Impact Events to automatically guard against
HIGH_IMPACT_KEYWORDS = [
    "CPI", "FOMC", "Interest Rate Decision", "Fed Chair Press Conference",
    "Non-Farm Payrolls", "Unemployment Rate", "GDP Annualized"
]

# --- 4. SENTIMENT SCORING BOUNDARIES (Fear & Greed Index: 0 - 100) ---
EXTREME_FEAR_THRESHOLD = 25.0       # < 25: Extreme Fear
FEAR_THRESHOLD = 45.0               # 25 - 45: Fear
NEUTRAL_MIN = 46.0                  # 46 - 54: Neutral Chop
GREED_THRESHOLD = 55.0              # 55 - 75: Greed
EXTREME_GREED_THRESHOLD = 75.0      # > 75: Extreme Greed

# --- 5. DERIVATIVES & ON-CHAIN THRESHOLDS (Binance Futures) ---
EXTREME_NEGATIVE_FUNDING = -0.02    # -0.02% or lower per 8h -> High squeeze probability (Lean Long)
EXTREME_POSITIVE_FUNDING = 0.05     # +0.05% or higher per 8h -> Overheated Longs (Lean Short/Caution)

# --- 6. AGGREGATED BIAS WEIGHTS (Total Weight = 1.0) ---
WEIGHT_FEAR_GREED = 0.35            # Fear & Greed Index weight (35%)
WEIGHT_DERIVATIVES = 0.40           # Funding Rates & Open Interest momentum (40%)
WEIGHT_MACRO_CALENDAR = 0.25        # Economic Calendar proximity & impact (25%)

# --- 7. TELEGRAM ALERTS ---
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")