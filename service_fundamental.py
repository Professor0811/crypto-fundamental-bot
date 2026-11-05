# ==============================================================================
# FUNDAMENTAL BOT CLOUD WEB SERVICE & SPIDER NEURAL TOPOLOGY DASHBOARD
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
    print("🧠🕷️ [Fundamental Spider Core] 4-Pillar Neural Loop Started...")
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

app = FastAPI(title="Chama Capital - Fundamental Spider Engine", lifespan=lifespan)

@app.api_route("/healthz", methods=["GET", "HEAD"])
@app.api_route("/api/state", methods=["GET", "HEAD"])
async def health_check():
    return JSONResponse(status_code=200, content=_LATEST_STATUS)

@app.api_route("/", methods=["GET", "HEAD"])
async def serve_visual_terminal():
    return HTMLResponse(content=SPIDER_DASHBOARD_HTML, status_code=200)


SPIDER_DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CHAMA CAPITAL // Cyber Spider Quant Intelligence Engine</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root {
    --bg: #030712;
    --card: rgba(11, 17, 32, 0.82);
    --border: rgba(0, 242, 254, 0.22);
    --cyan: #00f2fe;
    --green: #10b981;
    --red: #f43f5e;
    --amber: #f59e0b;
    --purple: #a855f7;
    --text: #f8fafc;
    --muted: #94a3b8;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    background: #030712;
    color: var(--text);
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
    padding: 16px;
    position: relative;
    overflow-x: hidden;
}
.mono { font-family: 'JetBrains Mono', monospace; }

/* Background Canvas for Spider Web */
#spider-canvas {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    pointer-events: auto;
}

.content-wrap {
    position: relative;
    z-index: 10;
    max-width: 1400px;
    margin: 0 auto;
}

/* Header */
.header {
    display: flex; justify-content: space-between; align-items: center;
    padding: 14px 22px; background: var(--card); border: 1px solid var(--border);
    border-radius: 14px; backdrop-filter: blur(14px); margin-bottom: 16px;
    box-shadow: 0 0 25px rgba(0, 242, 254, 0.08);
}
.brand { display: flex; align-items: center; gap: 14px; }
.spider-orb {
    width: 44px; height: 44px; border-radius: 12px;
    background: radial-gradient(circle, #00f2fe 10%, #030712 90%);
    border: 1px solid var(--cyan);
    display: flex; align-items: center; justify-content: center;
    font-size: 22px; box-shadow: 0 0 20px rgba(0, 242, 254, 0.6);
    animation: webPulse 2.5s infinite alternate ease-in-out;
}
@keyframes webPulse {
    0% { box-shadow: 0 0 10px rgba(0, 242, 254, 0.4); transform: scale(0.96); }
    100% { box-shadow: 0 0 25px rgba(0, 242, 254, 0.9); transform: scale(1.04); }
}
.status-pills { display: flex; gap: 10px; flex-wrap: wrap; }
.pill {
    padding: 6px 12px; border-radius: 999px; font-size: 11px; font-weight: 700;
    display: flex; align-items: center; gap: 7px;
    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1);
}
.dot { width: 8px; height: 8px; border-radius: 50%; background: var(--green); animation: blink 1.2s infinite; }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

/* SPIDER STAGE CANVAS BANNER */
.spider-stage {
    background: radial-gradient(circle at center, rgba(0, 242, 254, 0.08) 0%, rgba(3, 7, 18, 0.92) 80%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    text-align: center;
    position: relative;
    backdrop-filter: blur(10px);
    box-shadow: inset 0 0 40px rgba(0, 242, 254, 0.04);
}
.spider-title { font-size: 11px; text-transform: uppercase; letter-spacing: 2px; color: var(--cyan); font-weight: 800; margin-bottom: 6px; }
.spider-subtitle { font-size: 13px; color: var(--muted); margin-bottom: 18px; }

/* The Spider Centerpiece */
.spider-core {
    display: inline-flex; flex-direction: column; align-items: center; justify-content: center;
    position: relative; padding: 14px 28px; border-radius: 20px;
    background: rgba(11, 17, 32, 0.9); border: 1px solid var(--cyan);
    box-shadow: 0 0 35px rgba(0, 242, 254, 0.25);
}
.spider-avatar { font-size: 42px; margin-bottom: 4px; filter: drop-shadow(0 0 12px var(--cyan)); }
.score-big { font-size: 48px; font-weight: 800; line-height: 1; }
.bias-badge {
    padding: 5px 16px; border-radius: 999px; font-size: 12px; font-weight: 800;
    letter-spacing: 1px; margin-top: 8px;
}

/* 4 Anchor Nodes connected to Spider */
.spider-legs-grid {
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-top: 22px;
}
.web-anchor {
    background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px; padding: 12px 14px; text-align: left; position: relative;
    transition: transform 0.3s, border-color 0.3s;
}
.web-anchor:hover { transform: translateY(-3px); border-color: var(--cyan); }
.anchor-tag { font-size: 10px; color: var(--cyan); font-weight: 800; text-transform: uppercase; }
.anchor-name { font-size: 13px; font-weight: 700; margin: 3px 0; }
.anchor-val { font-size: 12px; color: #cbd5e1; }

/* Bottom Grid */
.main-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-bottom: 18px; }
.panel {
    background: var(--card); border: 1px solid var(--border); border-radius: 14px;
    padding: 18px; backdrop-filter: blur(12px);
}
.panel-header {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 14px; padding-bottom: 8px; border-bottom: 1px solid rgba(255,255,255,0.06);
}
.panel-title { font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; color: #e2e8f0; }

/* News & Blacklist */
.news-list { display: flex; flex-direction: column; gap: 8px; max-height: 220px; overflow-y: auto; }
.news-item {
    display: flex; justify-content: space-between; align-items: center; gap: 10px;
    padding: 8px 12px; background: rgba(255,255,255,0.025);
    border-left: 3px solid var(--cyan); border-radius: 6px; font-size: 12px;
}
.news-tag { padding: 3px 8px; border-radius: 4px; font-size: 10px; font-weight: 700; white-space: nowrap; }

@media (max-width: 900px) {
    .spider-legs-grid, .main-grid { grid-template-columns: 1fr; }
}
</style>
</head>
<body>

<!-- Animated Spider Web Canvas in Background -->
<canvas id="spider-canvas"></canvas>

<div class="content-wrap">
    <!-- Header -->
    <div class="header">
        <div class="brand">
            <div class="spider-orb">🕷️</div>
            <div>
                <div style="font-size: 16px; font-weight: 800; letter-spacing: 0.5px;">CHAMA CAPITAL MANAGEMENT</div>
                <div style="font-size: 11px; color: var(--cyan);" class="mono">AUTONOMOUS QUANT SPIDER // NEURAL MACRO RADAR v3.0</div>
            </div>
        </div>
        <div class="status-pills">
            <div class="pill"><span class="dot"></span> <span id="sync-status">SUPABASE BRIDGE: SYNCED</span></div>
            <div class="pill mono" id="last-sync">SYNCING...</div>
        </div>
    </div>

    <!-- SPIDER WEB CORE STAGE -->
    <div class="spider-stage">
        <div class="spider-title">Autonomous Spider Intelligence & Web Topology</div>
        <div class="spider-subtitle">Synthesizing live decentralized silk threads into an institutional execution gatekeeper</div>

        <div class="spider-core">
            <div class="spider-avatar">🕷️</div>
            <div id="composite-score" class="score-big mono">+0.0</div>
            <div id="bias-badge" class="bias-badge" style="background:rgba(0,242,254,0.15); color:var(--cyan);">SYNCHRONIZING</div>
        </div>

        <!-- 4 Silk Thread Anchors -->
        <div class="spider-legs-grid">
            <div class="web-anchor">
                <div class="anchor-tag">Silk Thread 1 • 35%</div>
                <div class="anchor-name">Bybit V5 Derivatives</div>
                <div class="anchor-val mono" id="anc-deriv">Score: 0.0 | Funding: 0.0100%</div>
            </div>
            <div class="web-anchor">
                <div class="anchor-tag">Silk Thread 2 • 35%</div>
                <div class="anchor-name">News NLP & Sentiment</div>
                <div class="anchor-val mono" id="anc-sent">F&G: 50 | RSS: 0 Bull / 0 Bear</div>
            </div>
            <div class="web-anchor">
                <div class="anchor-tag">Silk Thread 3 • 15%</div>
                <div class="anchor-name">BTC Dominance Radar</div>
                <div class="anchor-val mono" id="anc-dom">BTC.D: 55.0% | Flow: STABLE</div>
            </div>
            <div class="web-anchor">
                <div class="anchor-tag">Silk Thread 4 • 15%</div>
                <div class="anchor-name">Macro Calendar Shield</div>
                <div class="anchor-val mono" id="anc-macro">Freeze: CLEAR | CPI/Fed Safe</div>
            </div>
        </div>
    </div>

    <!-- Details Grid -->
    <div class="main-grid">
        <!-- Live News NLP Stream -->
        <div class="panel">
            <div class="panel-header">
                <span class="panel-title">🕸️ Real-Time News Stream (Spider Web Prey)</span>
                <span class="mono" style="font-size:11px; color:var(--muted);">Auto-Scanned Every 60s</span>
            </div>
            <div class="news-list" id="news-container">
                <div class="news-item"><span>Spider scanning CoinTelegraph & CoinDesk RSS...</span></div>
            </div>
        </div>

        <!-- Pre-Trade Execution Gatekeeper & Blacklist Shield -->
        <div class="panel">
            <div class="panel-header">
                <span class="panel-title">🛡️ Futures Bot Execution Gatekeeper</span>
                <span class="mono" style="font-size:11px; color:var(--green);">BYBIT 10X SHIELD</span>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:14px;">
                <div style="background:rgba(255,255,255,0.03); padding:12px; border-radius:10px; border:1px solid rgba(255,255,255,0.07); text-align:center;">
                    <div style="font-size:11px; color:var(--muted);">LONG TRADES</div>
                    <div id="long-gate" style="font-size:13px; font-weight:800; color:var(--green); margin-top:4px;">ALLOWED</div>
                </div>
                <div style="background:rgba(255,255,255,0.03); padding:12px; border-radius:10px; border:1px solid rgba(255,255,255,0.07); text-align:center;">
                    <div style="font-size:11px; color:var(--muted);">SHORT TRADES</div>
                    <div id="short-gate" style="font-size:13px; font-weight:800; color:var(--green); margin-top:4px;">ALLOWED</div>
                </div>
            </div>
            <div id="blacklist-box" style="padding:14px; border-radius:10px; background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.3); text-align:center;">
                <div style="font-size:13px; font-weight:800; color:var(--green);">✅ ZERO BLACKLISTED PAIRS</div>
                <div style="font-size:11px; color:var(--muted); margin-top:3px;">Exploit & Delist Shield Active across 675 Bybit Pairs</div>
            </div>
        </div>
    </div>
</div>

<!-- Spider Web Dynamic Particle Simulation Script -->
<script>
const canvas = document.getElementById('spider-canvas');
const ctx = canvas.getContext('2d');
let width, height;
let points = [];
const numPoints = 48;
let mouse = { x: null, y: null };

function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
}
window.addEventListener('resize', resize);
window.addEventListener('mousemove', (e) => { mouse.x = e.clientX; mouse.y = e.clientY; });
window.addEventListener('mouseout', () => { mouse.x = null; mouse.y = null; });
resize();

// Create floating nodes for the web
for (let i = 0; i < numPoints; i++) {
    points.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.8,
        vy: (Math.random() - 0.5) * 0.8,
        radius: Math.random() * 2 + 1.5
    });
}

function drawSpiderWeb() {
    ctx.clearRect(0, 0, width, height);

    // Update & draw nodes
    for (let i = 0; i < points.length; i++) {
        let p = points[i];
        p.x += p.vx;
        p.y += p.vy;

        if (p.x < 0 || p.x > width) p.vx *= -1;
        if (p.y < 0 || p.y > height) p.vy *= -1;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(0, 242, 254, 0.5)';
        ctx.fill();

        // Connect nodes within proximity (The Silk Web)
        for (let j = i + 1; j < points.length; j++) {
            let p2 = points[j];
            let dist = Math.hypot(p.x - p2.x, p.y - p2.y);
            if (dist < 130) {
                ctx.beginPath();
                ctx.moveTo(p.x, p.y);
                ctx.lineTo(p2.x, p2.y);
                let alpha = (1 - dist / 130) * 0.25;
                ctx.strokeStyle = `rgba(0, 242, 254, ${alpha})`;
                ctx.lineWidth = 0.8;
                ctx.stroke();
            }
        }

        // Connect to mouse interaction
        if (mouse.x && mouse.y) {
            let mDist = Math.hypot(p.x - mouse.x, p.y - mouse.y);
            if (mDist < 160) {
                ctx.beginPath();
                ctx.moveTo(p.x, p.y);
                ctx.lineTo(mouse.x, mouse.y);
                ctx.strokeStyle = `rgba(168, 85, 247, ${0.4 * (1 - mDist / 160)})`;
                ctx.lineWidth = 1;
                ctx.stroke();
            }
        }
    }
    requestAnimationFrame(drawSpiderWeb);
}
drawSpiderWeb();

// Telemetry Poller
async function updateTelemetry() {
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

        // Anchors
        const bf = (parseFloat(d.btc_funding || 0) * 100).toFixed(4);
        document.getElementById('anc-deriv').textContent = `Score: ${d.derivatives_score >= 0 ? '+' : ''}${d.derivatives_score} | BTC Fund: ${bf}%`;
        document.getElementById('anc-sent').textContent = `F&G: ${d.fng_value} (${d.fng_label}) | News: ${d.bull_news}B / ${d.bear_news}Br`;
        document.getElementById('anc-dom').textContent = `BTC.D: ${d.btc_dominance}% | Flow: ${d.altseason_status}`;
        document.getElementById('anc-macro').textContent = `Freeze: ${d.is_news_freeze ? 'ACTIVE 🚨' : 'CLEAR ✅'} | ${d.active_macro_event || 'Safe'}`;

        // Gatekeeper
        const freeze = Boolean(d.is_news_freeze);
        const lg = document.getElementById('long-gate');
        const sg = document.getElementById('short-gate');
        if (freeze) {
            lg.textContent = '⛔ BLOCKED (FREEZE)'; lg.style.color = 'var(--red)';
            sg.textContent = '⛔ BLOCKED (FREEZE)'; sg.style.color = 'var(--red)';
        } else {
            lg.textContent = score <= -50 ? '⛔ BLOCKED (BEAR)' : 'ALLOWED ✅';
            lg.style.color = score <= -50 ? 'var(--red)' : 'var(--green)';
            sg.textContent = score >= 50 ? '⛔ BLOCKED (BULL)' : 'ALLOWED ✅';
            sg.style.color = score >= 50 ? 'var(--red)' : 'var(--green)';
        }

        document.getElementById('last-sync').textContent = 'LAST SYNC: ' + (d.last_synced || '');
        document.getElementById('sync-status').textContent = d.supabase_synced ? 'SUPABASE BRIDGE: SYNCED ✅' : 'SUPABASE BRIDGE: LOCAL';

        // News List
        const newsBox = document.getElementById('news-container');
        if (d.headlines && d.headlines.length > 0) {
            newsBox.innerHTML = d.headlines.map(h => {
                let col = h.tag === 'BULLISH' ? 'var(--green)' : (h.tag.includes('BEARISH') || h.tag.includes('BLACKLIST') ? 'var(--red)' : 'var(--cyan)');
                return `<div class="news-item">
                    <span>${h.title}</span>
                    <span class="news-tag mono" style="background:rgba(255,255,255,0.06); color:${col};">${h.tag}</span>
                </div>`;
            }).join('');
        }

        // Blacklist Box
        const blBox = document.getElementById('blacklist-box');
        if (d.blacklisted_tokens && d.blacklisted_tokens.length > 0) {
            blBox.style.background = 'rgba(244,63,94,0.12)';
            blBox.style.borderColor = 'rgba(244,63,94,0.4)';
            blBox.innerHTML = `<div style="font-size:13px; font-weight:800; color:var(--red);">🚨 BLOCKED PAIRS: ${d.blacklisted_tokens.join(', ')}</div>
                               <div style="font-size:11px; color:var(--muted); margin-top:3px;">Protected from High-Risk Exploit/Delist News</div>`;
        }
    } catch (e) {
        console.error(e);
    }
}
updateTelemetry();
setInterval(updateTelemetry, 5000);
</script>
</body>
</html>
"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("service_fundamental:app", host="0.0.0.0", port=port)
