# ==============================================================================
# FUNDAMENTAL BOT CLOUD WEB SERVICE & ANIMATED QUANT INTELLIGENCE TERMINAL
# ==============================================================================
import os
import asyncio
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
import config_fundamental as cfg
import research_brain as brain

_LATEST_STATUS = {
    "status": "initializing",
    "composite_score": 0.0,
    "bias_label": "INITIALIZING",
    "is_news_freeze": False,
    "active_macro_event": "Syncing...",
    "sentiment_score": 0.0,
    "fng_value": 50,
    "fng_label": "Neutral",
    "bull_news": 0,
    "bear_news": 0,
    "derivatives_score": 0.0,
    "btc_funding": 0.0001,
    "eth_funding": 0.0001,
    "sol_funding": 0.0001,
    "btc_oi_usd": 0.0,
    "squeeze_status": "SYNCING",
    "deriv_source": "Bybit V5 Global",
    "btc_dominance": 55.0,
    "altseason_status": "SCANNING",
    "dom_score": 0.0,
    "blacklisted_tokens": [],
    "headlines": [],
    "supabase_synced": False,
    "last_synced": "Starting..."
}

async def fundamental_background_worker():
    print("🧠 [Fundamental Cloud Worker] 4-Pillar Institutional Loop Started...")
    while True:
        try:
            start_ts = time.time()
            res = await asyncio.to_thread(brain.calculate_composite_bias)
            _LATEST_STATUS.update(res)
            _LATEST_STATUS["status"] = "online"
            _LATEST_STATUS["last_synced"] = time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())

            print(
                f"[{_LATEST_STATUS['last_synced']}] Bias: {_LATEST_STATUS['bias_label']} "
                f"({_LATEST_STATUS['composite_score']:+.1f}) | DB Synced: {_LATEST_STATUS['supabase_synced']}"
            )
            elapsed = time.time() - start_ts
            await asyncio.sleep(max(10.0, cfg.SYNTHESIS_INTERVAL - elapsed))
        except Exception as e:
            print(f"[Fundamental Worker Error]: {e}")
            await asyncio.sleep(10)

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(fundamental_background_worker())
    yield
    task.cancel()

app = FastAPI(title="Chama Capital - Fundamental Macro Intelligence Engine", lifespan=lifespan)

@app.api_route("/healthz", methods=["GET", "HEAD"])
@app.api_route("/api/state", methods=["GET", "HEAD"])
async def health_check():
    return JSONResponse(status_code=200, content=_LATEST_STATUS)

@app.api_route("/", methods=["GET", "HEAD"])
async def serve_visual_terminal():
    return HTMLResponse(content=DASHBOARD_HTML, status_code=200)


DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CHAMA CAPITAL // Fundamental AI & Macro Intelligence Engine</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root {
    --bg: #060911;
    --card: rgba(13, 19, 33, 0.85);
    --border: rgba(56, 189, 248, 0.18);
    --cyan: #00f2fe;
    --green: #10b981;
    --red: #f43f5e;
    --amber: #f59e0b;
    --purple: #a855f7;
    --text: #f1f5f9;
    --muted: #94a3b8;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    background: radial-gradient(circle at 50% 0%, #0f172a 0%, #05070e 100%);
    color: var(--text);
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
    padding: 20px;
    overflow-x: hidden;
}
.mono { font-family: 'JetBrains Mono', monospace; }

/* Animated Header */
.header {
    display: flex; justify-content: space-between; align-items: center;
    padding: 16px 24px; background: var(--card); border: 1px solid var(--border);
    border-radius: 14px; backdrop-filter: blur(12px); margin-bottom: 20px;
    box-shadow: 0 0 30px rgba(0, 242, 254, 0.06);
}
.brand { display: flex; align-items: center; gap: 14px; }
.logo-orb {
    width: 42px; height: 42px; border-radius: 10px;
    background: linear-gradient(135deg, #00f2fe, #4facfe);
    display: flex; align-items: center; justify-content: center;
    font-weight: 800; color: #05070e; font-size: 18px;
    box-shadow: 0 0 15px rgba(0, 242, 254, 0.6);
    animation: pulseGlow 3s infinite alternate;
}
@keyframes pulseGlow {
    0% { box-shadow: 0 0 10px rgba(0, 242, 254, 0.4); }
    100% { box-shadow: 0 0 25px rgba(0, 242, 254, 0.9); }
}
.status-pills { display: flex; gap: 10px; flex-wrap: wrap; }
.pill {
    padding: 6px 12px; border-radius: 999px; font-size: 12px; font-weight: 600;
    display: flex; align-items: center; gap: 7px;
    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1);
}
.dot { width: 8px; height: 8px; border-radius: 50%; background: var(--green); animation: blink 1.4s infinite; }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.25; } }

/* Visual Pipeline Flow Banner */
.pipeline-box {
    background: var(--card); border: 1px solid var(--border); border-radius: 14px;
    padding: 18px 24px; margin-bottom: 20px; position: relative; overflow: hidden;
}
.pipeline-title { font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; color: var(--cyan); margin-bottom: 14px; font-weight: 700; }
.pipeline-grid {
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; position: relative;
}
.node {
    background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 10px; padding: 12px 14px; position: relative;
    transition: transform 0.3s ease, border-color 0.3s ease;
}
.node:hover { transform: translateY(-3px); border-color: var(--cyan); }
.node-step { font-size: 10px; color: var(--cyan); font-weight: 700; text-transform: uppercase; }
.node-name { font-size: 14px; font-weight: 700; margin: 4px 0; }
.node-desc { font-size: 11px; color: var(--muted); }
.flow-bar {
    height: 3px; width: 100%; background: rgba(255,255,255,0.06);
    margin-top: 10px; border-radius: 4px; overflow: hidden; position: relative;
}
.flow-beam {
    height: 100%; width: 45%;
    background: linear-gradient(90deg, transparent, var(--cyan), var(--purple), transparent);
    position: absolute; animation: streamFlow 2.2s infinite linear;
}
@keyframes streamFlow { 0% { left: -45%; } 100% { left: 100%; } }

/* Main Grid */
.main-grid { display: grid; grid-template-columns: 1.15fr 1.85fr; gap: 20px; margin-bottom: 20px; }
.panel {
    background: var(--card); border: 1px solid var(--border); border-radius: 14px;
    padding: 20px; backdrop-filter: blur(12px);
}
.panel-header {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 16px; padding-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.06);
}
.panel-title { font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #cbd5e1; }

/* Dial / Score Centerpiece */
.score-center { text-align: center; padding: 12px 0; }
.score-big { font-size: 56px; font-weight: 800; line-height: 1; margin: 10px 0; text-shadow: 0 0 25px rgba(0,242,254,0.3); }
.bias-badge {
    display: inline-block; padding: 6px 18px; border-radius: 999px;
    font-size: 14px; font-weight: 800; letter-spacing: 1px; margin-bottom: 14px;
}
.meter-track {
    height: 14px; width: 100%; border-radius: 999px;
    background: linear-gradient(90deg, #f43f5e 0%, #f59e0b 50%, #10b981 100%);
    position: relative; margin: 18px 0 8px 0;
}
.meter-pointer {
    width: 18px; height: 24px; background: #fff; border: 3px solid #05070e;
    border-radius: 4px; position: absolute; top: -5px; transform: translateX(-50%);
    transition: left 0.8s cubic-bezier(0.22, 1, 0.36, 1);
    box-shadow: 0 0 12px #fff;
}
.meter-labels { display: flex; justify-content: space-between; font-size: 11px; color: var(--muted); }

/* Execution Gatekeeper Box */
.gate-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 18px; }
.gate-card {
    padding: 12px; border-radius: 10px; background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08); text-align: center;
}
.gate-title { font-size: 11px; color: var(--muted); margin-bottom: 4px; }
.gate-val { font-size: 14px; font-weight: 800; }

/* 4-Pillar Cards */
.pillars-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.pillar-card {
    background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px; padding: 15px;
}
.pillar-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.pillar-name { font-size: 13px; font-weight: 700; color: var(--cyan); }
.pillar-weight { font-size: 11px; color: var(--muted); background: rgba(255,255,255,0.05); padding: 2px 8px; border-radius: 6px; }
.metric-row { display: flex; justify-content: space-between; font-size: 12px; margin: 6px 0; color: #cbd5e1; }

/* Bottom Grid: Live News & Blacklist */
.bottom-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; }
.news-list { display: flex; flex-direction: column; gap: 8px; max-height: 240px; overflow-y: auto; }
.news-item {
    display: flex; justify-content: space-between; align-items: center; gap: 12px;
    padding: 10px 14px; background: rgba(255,255,255,0.025);
    border-left: 3px solid var(--cyan); border-radius: 6px; font-size: 12px;
}
.news-tag { padding: 3px 8px; border-radius: 4px; font-size: 10px; font-weight: 700; white-space: nowrap; }

@media (max-width: 950px) {
    .pipeline-grid, .main-grid, .pillars-grid, .bottom-grid { grid-template-columns: 1fr; }
}
</style>
</head>
<body>

<div class="header">
    <div class="brand">
        <div class="logo-orb">🧠</div>
        <div>
            <div style="font-size: 16px; font-weight: 800; letter-spacing: 0.5px;">CHAMA CAPITAL MANAGEMENT</div>
            <div style="font-size: 11px; color: var(--cyan);" class="mono">INSTITUTIONAL FUNDAMENTAL & MACRO BIAS ENGINE v2.0</div>
        </div>
    </div>
    <div class="status-pills">
        <div class="pill"><span class="dot"></span> <span id="sync-status">SUPABASE BRIDGE: ONLINE</span></div>
        <div class="pill mono" id="last-sync">SYNCING...</div>
    </div>
</div>

<!-- HOW THE BOT WORKS: LIVE NEURAL PIPELINE -->
<div class="pipeline-box">
    <div class="pipeline-title">⚡ Real-Time Autonomous Decision Pipeline (How the Fundamental Brain Operates)</div>
    <div class="pipeline-grid">
        <div class="node">
            <div class="node-step">Stage 1 • Data Ingestion</div>
            <div class="node-name">Multi-Source Collectors</div>
            <div class="node-desc">Bybit V5 Linear OI/Funding, CoinGecko BTC.D, F&G, Live RSS News</div>
            <div class="flow-bar"><div class="flow-beam"></div></div>
        </div>
        <div class="node">
            <div class="node-step">Stage 2 • NLP & Quant Filter</div>
            <div class="node-name">4-Pillar Synthesis Brain</div>
            <div class="node-desc">Weights: 35% Deriv + 35% Sentiment + 15% BTC.D + 15% Macro</div>
            <div class="flow-bar"><div class="flow-beam"></div></div>
        </div>
        <div class="node">
            <div class="node-step">Stage 3 • Cloud State Sync</div>
            <div class="node-name">Supabase PostgreSQL IPC</div>
            <div class="node-desc">Pushes Composite Score, News Freeze & Token Blacklist every 60s</div>
            <div class="flow-bar"><div class="flow-beam"></div></div>
        </div>
        <div class="node">
            <div class="node-step">Stage 4 • Execution Guard</div>
            <div class="node-name">Bybit 10x Futures Bot</div>
            <div class="node-desc">Blocks counter-bias trades & halts execution during CPI/FOMC</div>
            <div class="flow-bar"><div class="flow-beam"></div></div>
        </div>
    </div>
</div>

<div class="main-grid">
    <div class="panel">
        <div class="panel-header">
            <span class="panel-title">🎯 Synthesized Composite Market Bias</span>
            <span class="mono" style="font-size:11px; color:var(--muted);">Scale: -100 to +100</span>
        </div>
        <div class="score-center">
            <div id="bias-badge" class="bias-badge" style="background:rgba(56,189,248,0.15); color:var(--cyan);">NEUTRAL</div>
            <div id="composite-score" class="score-big mono">+0.0</div>
            <div style="font-size:12px; color:var(--muted);">Institutional Macro & On-Chain Conviction Score</div>

            <div class="meter-track">
                <div id="meter-pointer" class="meter-pointer" style="left: 50%;"></div>
            </div>
            <div class="meter-labels mono">
                <span>-100 (MAX BEAR)</span>
                <span>0 (NEUTRAL)</span>
                <span>+100 (MAX BULL)</span>
            </div>
        </div>

        <div class="gate-grid">
            <div class="gate-card">
                <div class="gate-title">LONG TRADES GATEKEEPER</div>
                <div id="long-gate" class="gate-val" style="color:var(--green);">✅ ALLOWED</div>
            </div>
            <div class="gate-card">
                <div class="gate-title">SHORT TRADES GATEKEEPER</div>
                <div id="short-gate" class="gate-val" style="color:var(--green);">✅ ALLOWED</div>
            </div>
        </div>
    </div>

    <div class="panel">
        <div class="panel-header">
            <span class="panel-title">🔬 4-Pillar Institutional Intelligence Breakdown</span>
            <span class="mono" style="font-size:11px; color:var(--cyan);" id="deriv-src">Feed: Bybit V5 Global</span>
        </div>
        <div class="pillars-grid">
            <div class="pillar-card">
                <div class="pillar-top">
                    <span class="pillar-name">1. Derivatives & OI Flow</span>
                    <span class="pillar-weight">Weight: 35%</span>
                </div>
                <div class="metric-row"><span>Pillar Score:</span> <strong class="mono" id="p-deriv-score">0.0</strong></div>
                <div class="metric-row"><span>BTC / ETH Funding:</span> <span class="mono" id="p-funding">0.0100% / 0.0100%</span></div>
                <div class="metric-row"><span>BTC Open Interest:</span> <span class="mono" id="p-oi">$0M</span></div>
                <div class="metric-row"><span>Regime Signal:</span> <strong id="p-squeeze" style="color:var(--cyan);">BALANCED</strong></div>
            </div>

            <div class="pillar-card">
                <div class="pillar-top">
                    <span class="pillar-name">2. News NLP & Sentiment</span>
                    <span class="pillar-weight">Weight: 35%</span>
                </div>
                <div class="metric-row"><span>Pillar Score:</span> <strong class="mono" id="p-sent-score">0.0</strong></div>
                <div class="metric-row"><span>Fear & Greed Index:</span> <span class="mono" id="p-fng">50 (Neutral)</span></div>
                <div class="metric-row"><span>Live RSS Headlines:</span> <span class="mono" id="p-news-counts">0 Bull / 0 Bear</span></div>
                <div class="metric-row"><span>NLP Feed Status:</span> <strong style="color:var(--green);">ACTIVE (CoinDesk/CT)</strong></div>
            </div>

            <div class="pillar-card">
                <div class="pillar-top">
                    <span class="pillar-name">3. BTC Dominance Radar</span>
                    <span class="pillar-weight">Weight: 15%</span>
                </div>
                <div class="metric-row"><span>Pillar Score:</span> <strong class="mono" id="p-dom-score">0.0</strong></div>
                <div class="metric-row"><span>BTC Dominance (BTC.D):</span> <strong class="mono" id="p-btcd">55.0%</strong></div>
                <div class="metric-row"><span>Altcoin Liquidity:</span> <strong id="p-altseason" style="color:var(--amber);">STABLE</strong></div>
            </div>

            <div class="pillar-card">
                <div class="pillar-top">
                    <span class="pillar-name">4. Macro Economic Guard</span>
                    <span class="pillar-weight">Weight: 15%</span>
                </div>
                <div class="metric-row"><span>Kill-Switch Freeze:</span> <strong id="p-freeze" style="color:var(--green);">FALSE (SAFE)</strong></div>
                <div class="metric-row"><span>Active Macro Event:</span> <span id="p-macro-event" class="mono">None</span></div>
                <div class="metric-row"><span>Protection Policy:</span> <span>Auto-Blocks Trades on CPI/Fed</span></div>
            </div>
        </div>
    </div>
</div>

<div class="bottom-grid">
    <div class="panel">
        <div class="panel-header">
            <span class="panel-title">📰 Real-Time Institutional News NLP Stream</span>
            <span class="mono" style="font-size:11px; color:var(--muted);">Auto-Parsed Every 60s</span>
        </div>
        <div class="news-list" id="news-container">
            <div class="news-item"><span>Scanning global crypto RSS feeds...</span></div>
        </div>
    </div>

    <div class="panel">
        <div class="panel-header">
            <span class="panel-title">🛡️ Token Exploit & Delist Shield</span>
            <span class="mono" style="font-size:11px; color:var(--green);">ACTIVE GUARD</span>
        </div>
        <p style="font-size:12px; color:var(--muted); margin-bottom:14px;">
            Automatically scans breaking news for <code class="mono">hack</code>, <code class="mono">exploit</code>, or <code class="mono">delist</code> events and blocks affected pairs on the Futures Bot.
        </p>
        <div id="blacklist-box" style="padding:16px; border-radius:10px; background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.3); text-align:center;">
            <div style="font-size:14px; font-weight:800; color:var(--green);">✅ ZERO BLACKLISTED TOKENS</div>
            <div style="font-size:11px; color:var(--muted); margin-top:4px;">All 600+ Bybit Perpetual Pairs Approved for Trading</div>
        </div>
    </div>
</div>

<script>
async function refreshTelemetry() {
    try {
        const res = await fetch('/api/state');
        const d = await res.json();

        const score = parseFloat(d.composite_score || 0);
        const scoreEl = document.getElementById('composite-score');
        scoreEl.textContent = (score >= 0 ? '+' : '') + score.toFixed(1);

        const badge = document.getElementById('bias-badge');
        badge.textContent = d.bias_label || 'NEUTRAL';
        if (score >= 15) {
            scoreEl.style.color = 'var(--green)';
            badge.style.background = 'rgba(16,185,129,0.18)';
            badge.style.color = 'var(--green)';
        } else if (score <= -15) {
            scoreEl.style.color = 'var(--red)';
            badge.style.background = 'rgba(244,63,94,0.18)';
            badge.style.color = 'var(--red)';
        } else {
            scoreEl.style.color = 'var(--cyan)';
            badge.style.background = 'rgba(0,242,254,0.15)';
            badge.style.color = 'var(--cyan)';
        }

        const pct = Math.max(2, Math.min(98, ((score + 100) / 200) * 100));
        document.getElementById('meter-pointer').style.left = pct + '%';

        const freeze = Boolean(d.is_news_freeze);
        const longGate = document.getElementById('long-gate');
        const shortGate = document.getElementById('short-gate');

        if (freeze) {
            longGate.textContent = '⛔ BLOCKED (MACRO FREEZE)';
            longGate.style.color = 'var(--red)';
            shortGate.textContent = '⛔ BLOCKED (MACRO FREEZE)';
            shortGate.style.color = 'var(--red)';
        } else {
            if (score <= -50) {
                longGate.textContent = '⛔ BLOCKED (HEAVY BEAR)';
                longGate.style.color = 'var(--red)';
            } else {
                longGate.textContent = '✅ ALLOWED';
                longGate.style.color = 'var(--green)';
            }
            if (score >= 50) {
                shortGate.textContent = '⛔ BLOCKED (HEAVY BULL)';
                shortGate.style.color = 'var(--red)';
            } else {
                shortGate.textContent = '✅ ALLOWED';
                shortGate.style.color = 'var(--green)';
            }
        }

        document.getElementById('deriv-src').textContent = 'Feed: ' + (d.deriv_source || 'Bybit V5');
        document.getElementById('p-deriv-score').textContent = (d.derivatives_score >= 0 ? '+' : '') + d.derivatives_score;
        const bf = (parseFloat(d.btc_funding || 0) * 100).toFixed(4);
        const ef = (parseFloat(d.eth_funding || 0) * 100).toFixed(4);
        document.getElementById('p-funding').textContent = bf + '% / ' + ef + '%';
        document.getElementById('p-oi').textContent = '$' + (d.btc_oi_usd || 0) + 'M';
        document.getElementById('p-squeeze').textContent = d.squeeze_status || 'BALANCED';

        document.getElementById('p-sent-score').textContent = (d.sentiment_score >= 0 ? '+' : '') + d.sentiment_score;
        document.getElementById('p-fng').textContent = (d.fng_value || 50) + ' (' + (d.fng_label || 'Neutral') + ')';
        document.getElementById('p-news-counts').textContent = (d.bull_news || 0) + ' Bullish / ' + (d.bear_news || 0) + ' Bearish';

        document.getElementById('p-dom-score').textContent = (d.dom_score >= 0 ? '+' : '') + (d.dom_score || 0);
        document.getElementById('p-btcd').textContent = (d.btc_dominance || 55.0) + '%';
        document.getElementById('p-altseason').textContent = d.altseason_status || 'STABLE';

        const freezeEl = document.getElementById('p-freeze');
        freezeEl.textContent = freeze ? '🚨 ACTIVE FREEZE' : 'FALSE (CLEAR)';
        freezeEl.style.color = freeze ? 'var(--red)' : 'var(--green)';
        document.getElementById('p-macro-event').textContent = d.active_macro_event || 'None';

        document.getElementById('last-sync').textContent = 'LAST SYNC: ' + (d.last_synced || '');
        document.getElementById('sync-status').textContent = d.supabase_synced ? 'SUPABASE BRIDGE: SYNCED ✅' : 'SUPABASE BRIDGE: LOCAL MODE';

        const newsBox = document.getElementById('news-container');
        if (d.headlines && d.headlines.length > 0) {
            newsBox.innerHTML = d.headlines.map(h => {
                let tagColor = 'rgba(0,242,254,0.15)';
                let textCol = 'var(--cyan)';
                if (h.tag === 'BULLISH') { tagColor = 'rgba(16,185,129,0.2)'; textCol = 'var(--green)'; }
                else if (h.tag === 'BEARISH' || h.tag.includes('BLACKLIST')) { tagColor = 'rgba(244,63,94,0.2)'; textCol = 'var(--red)'; }
                return `<div class="news-item">
                    <span>${h.title}</span>
                    <span class="news-tag mono" style="background:${tagColor}; color:${textCol};">${h.tag}</span>
                </div>`;
            }).join('');
        }

        const blBox = document.getElementById('blacklist-box');
        if (d.blacklisted_tokens && d.blacklisted_tokens.length > 0) {
            blBox.style.background = 'rgba(244,63,94,0.12)';
            blBox.style.borderColor = 'rgba(244,63,94,0.4)';
            blBox.innerHTML = `<div style="font-size:14px; font-weight:800; color:var(--red);">🚨 BLOCKED PAIRS: ${d.blacklisted_tokens.join(', ')}</div>
                               <div style="font-size:11px; color:var(--muted); margin-top:4px;">Protected from High-Risk Exploit/Delist News</div>`;
        }
    } catch (e) {
        console.error(e);
    }
}
refreshTelemetry();
setInterval(refreshTelemetry, 5000);
</script>
</body>
</html>
"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("service_fundamental:app", host="0.0.0.0", port=port)
