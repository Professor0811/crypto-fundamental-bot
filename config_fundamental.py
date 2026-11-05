# ==============================================================================
# CONFIG FUNDAMENTAL: Institutional Macro & On-Chain Parameters
# ==============================================================================
import os

# Research Synthesis Intervals
SYNTHESIS_INTERVAL = 60                   # Complete research cycle every 60s
SENTIMENT_POLL_INTERVAL = 60              # Sentiment worker alias
MACRO_POLL_INTERVAL = 300                 # Macro calendar alias
MACRO_CALENDAR_POLL_INTERVAL = 300        # Macro calendar poll interval
DERIVATIVES_POLL_INTERVAL = 60            # Derivatives interval
ONCHAIN_POLL_INTERVAL = 60                # On-chain poll interval

# 4-Pillar Quantitative Weights (Sum = 100%)
WEIGHT_DERIVATIVES = 0.35   # 35% Bybit V5 Funding + Open Interest
WEIGHT_SENTIMENT = 0.35     # 35% Fear & Greed + Live News RSS NLP
WEIGHT_DOMINANCE = 0.15     # 15% BTC Dominance & Altcoin Liquidity Flow
WEIGHT_MACRO = 0.15         # 15% Macro Economic Calendar Safety

# Telegram Credentials (Read from Render Environment Variables)
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# Real-Time News NLP Scoring Keywords
BULLISH_KEYWORDS = [
    "etf", "inflow", "accumulate", "approval", "bullish", "surge", "rally",
    "adoption", "institutional", "breakout", "buy", "treasury", "upgrade", "partnership"
]

BEARISH_KEYWORDS = [
    "hack", "exploit", "sec", "lawsuit", "ban", "crash", "outflow", "liquidat",
    "delist", "bankrupt", "dump", "investigation", "penalty", "cpi hot", "hawkish"
]

# Critical Keywords that Trigger Instant Token-Specific Blacklisting
BLACKLIST_TRIGGERS = [
    "hack", "exploit", "delist", "rug", "stolen", "insolvent", "suspend"
]

# Tracked Major Pairs for Token-Specific Exploit & Delist Shield
TRACKED_TOKENS = [
    "BTC", "ETH", "SOL", "BNB", "XRP", "DOGE", "ADA", "AVAX", "TRX", "LINK",
    "DOT", "NEAR", "SUI", "LTC", "UNI", "APT", "PEPE", "SHIB", "FET", "RENDER",
    "ARB", "OP", "INJ", "WIF", "BONK", "SEI", "TIA", "AAVE", "PENDLE", "JUP"
]
