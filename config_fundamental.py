# ==============================================================================
# CONFIG FUNDAMENTAL: Institutional Macro & On-Chain Parameters
# ==============================================================================
import os

SYNTHESIS_INTERVAL = 60  # Run research cycle every 60 seconds

# Pillar Weights (Sum = 100%)
WEIGHT_DERIVATIVES = 0.35   # 35% Bybit V5 Funding + Open Interest
WEIGHT_SENTIMENT = 0.35     # 35% Fear & Greed + Live News RSS NLP
WEIGHT_DOMINANCE = 0.15     # 15% BTC Dominance & Altcoin Liquidity Flow
WEIGHT_MACRO = 0.15         # 15% Macro Economic Calendar Safety

# Telegram Credentials (Read from Render Environment)
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# Keywords for Real-Time News NLP Scoring
BULLISH_KEYWORDS = [
    "etf", "inflow", "accumulate", "approval", "bullish", "surge", "rally",
    "adoption", "institutional", "breakout", "buy", "treasury", "upgrade", "partnership"
]

BEARISH_KEYWORDS = [
    "hack", "exploit", "sec", "lawsuit", "ban", "crash", "outflow", "liquidat",
    "delist", "bankrupt", "dump", "investigation", "penalty", "cpi hot", "hawkish"
]

# Critical Keywords that trigger Token-Specific Blacklisting
BLACKLIST_TRIGGERS = ["hack", "exploit", "delist", "rug", "stolen", "insolvent", "suspend"]

# Tracked Major Tickers for Blacklist & News Extraction
TRACKED_TOKENS = [
    "BTC", "ETH", "SOL", "BNB", "XRP", "DOGE", "ADA", "AVAX", "TRX", "LINK",
    "DOT", "NEAR", "SUI", "LTC", "UNI", "APT", "PEPE", "SHIB", "FET", "RENDER",
    "ARB", "OP", "INJ", "WIF", "BONK", "SEI", "TIA", "AAVE", "PENDLE", "JUP"
]
