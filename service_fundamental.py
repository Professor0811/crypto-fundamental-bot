# ==============================================================================
# FUNDAMENTAL BOT CLOUD WEB SERVICE & AUTONOMOUS CYBER SPIDER CANVAS ENGINE
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

app = FastAPI(title="Chama Capital - Autonomous Cyber Spider", lifespan=lifespan)

@app.api_route("/healthz", methods=["GET", "HEAD"])
@app.api_route("/api/state", methods=["GET", "HEAD"])
async def health_check():
    return JSONResponse(status_code=200, content=_LATEST_STATUS)

@app.api_route("/", methods=["GET", "HEAD"])
async def serve_visual_terminal():
    return HTMLResponse(content=CYBER_SPIDER_HTML, status_code=200)


CYBER_SPIDER_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CHAMA CAPITAL // Autonomous Cyber Spider Macro Engine</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root {
    --bg: #020617;
    --card: rgba(10, 16, 31, 0.90);
    --border: rgba(0, 242, 254, 0.35);
    --cyan: #00f2fe;
    --green: #10b981;
    --red: #f43f5e;
    --amber: #f59e0b;
    --purple: #c084fc;
    --text: #f8fafc;
    --muted: #94a3b8;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    background: #020617;
    color: var(--text);
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
    padding: 14px;
    overflow-x: hidden;
}
.mono { font-family: 'JetBrains Mono', monospace; }
.scifi { font-family: 'Orbitron', sans-serif; }

/* Top Header */
.header {
    display: flex; justify-content: space-between; align-items: center;
    padding: 12px 20px; background: var(--card); border: 1px solid var(--border);
    border-radius: 12px; margin-bottom: 12px; backdrop-filter: blur(12px);
    box-shadow: 0 0 25px rgba(0, 242, 254, 0.1);
}
.brand { display: flex; align-items: center; gap: 12px; }
.spider-logo {
    font-size: 26px; filter: drop-shadow(0 0 10px var(--cyan));
    animation: spiderPulse 2s infinite alternate;
}
@keyframes spiderPulse {
    0% { transform: scale(0.95); filter: drop-shadow(0 0 6px var(--cyan)); }
    100% { transform: scale(1.08); filter: drop-shadow(0 0 18px var(--cyan)); }
}
.pill {
    padding: 5px 12px; border-radius: 999px; font-size: 11px; font-weight: 700;
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1);
}
.dot { width: 8px; height: 8px; border-radius: 50%; background: var(--green); animation: blink 1.2s infinite; }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

/* ========================================================================= */
/* THE CYBER SPIDER CANVAS STAGE                                             */
/* ========================================================================= */
.arena-container {
    position: relative;
    width: 100%;
    height: 520px;
    background: radial-gradient(circle at center, rgba(15, 23, 42, 0.98) 0%, #01040d 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 14px;
    box-shadow: inset 0 0 70px rgba(0, 242, 254, 0.08), 0 0 35px rgba(0, 0, 0, 0.85);
}
#spiderCanvas {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: 1;
}

/* Floating UI Panels Over Canvas (The 4 Web Anchors) */
.anchor-card {
    position: absolute;
    z-index: 5;
    width: 270px;
    background: rgba(8, 13, 26, 0.92);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 12px 16px;
    backdrop-filter: blur(14px);
    box-shadow: 0 0 22px rgba(0, 0, 0, 0.7);
    pointer-events: none;
    transition: border-color 0.3s;
}
.anc-top-left { top: 16px; left: 16px; border-left: 4px solid var(--cyan); }
.anc-top-right { top: 16px; right: 16px; border-right: 4px solid var(--purple); text-align: right; }
.anc-bottom-left { bottom: 16px; left: 16px; border-left: 4px solid var(--amber); }
.anc-bottom-right { bottom: 16px; right: 16px; border-right: 4px solid var(--green); text-align: right; }

.anchor-title { font-size: 10px; color: var(--cyan); text-transform: uppercase; font-weight: 800; letter-spacing: 1px; }
.anchor-name { font-size: 13px; font-weight: 800; margin: 3px 0; color: #fff; }
.anchor-stat { font-size: 11px; color: #cbd5e1; }

/* Center HUD (Output Score) */
.center-hud {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    z-index: 6;
    text-align: center;
    pointer-events: none;
    margin-top: 65px;
}
.bias-badge {
    padding: 4px 16px; border-radius: 999px; font-size: 12px; font-weight: 800;
    letter-spacing: 1.5px; display: inline-block; margin-bottom: 4px;
}
.score-display {
    font-size: 46px; font-weight: 900; line-height: 1;
    text-shadow: 0 0 25px rgba(0, 242, 254, 0.6);
}

/* ========================================================================= */
/* BOTTOM TELEMETRY PANELS                                                   */
/* ========================================================================= */
.bottom-grid {
    display: grid; grid-template-columns: 1.4fr 1fr; gap: 14px;
}
.panel {
    background: var(--card); border: 1px solid var(--border); border-radius: 12px;
    padding: 16px; backdrop-filter: blur(12px);
}
.panel-header {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid rgba(255,255,255,0.06);
}
.panel-title { font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; color: #cbd5e1; }

.news-list { display: flex; flex-direction: column; gap: 8px; max-height: 190px; overflow-y: auto; }
.news-item {
    display: flex; justify-content: space-between; align-items: center; gap: 10px;
    padding: 8px 12px; background: rgba(255,255,255,0.025);
    border-left: 3px solid var(--cyan); border-radius: 6px; font-size: 12px;
}
.news-tag { padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 700; white-space: nowrap; }

.gate-box {
    display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 12px;
}
.gate-card {
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 8px; padding: 10px; text-align: center;
}
.gate-title { font-size: 10px; color: var(--muted); margin-bottom: 2px; }
.gate-status { font-size: 13px; font-weight: 800; }

@media (max-width: 950px) {
    .arena-container { height: 600px; }
    .bottom-grid { grid-template-columns: 1fr; }
    .anchor-card { width: 220px; }
    .anc-top-right, .anc-bottom-right { text-align: left; border-right: none; border-left: 4px solid var(--purple); }
}
</style>
</head>
<body>

<div class="header">
    <div class="brand">
        <div class="spider-logo">🕷️</div>
        <div>
            <div style="font-size: 15px; font-weight: 800; letter-spacing: 0.5px;" class="scifi">CHAMA CAPITAL MANAGEMENT</div>
            <div style="font-size: 11px; color: var(--cyan);" class="mono">AUTONOMOUS QUANT CYBER SPIDER // NEURAL WEB ENGINE v3.0</div>
        </div>
    </div>
    <div style="display: flex; gap: 10px;">
        <div class="pill"><span class="dot"></span> <span id="sync-status">SUPABASE IPC: SYNCED</span></div>
        <div class="pill mono" id="last-sync">SYNCING...</div>
    </div>
</div>

<!-- ========================================================================= -->
<!-- SPIDER CANVAS ARENA                                                       -->
<!-- ========================================================================= -->
<div class="arena-container">
    <canvas id="spiderCanvas"></canvas>

    <!-- Node 1: Derivatives (Top-Left) -->
    <div class="anchor-card anc-top-left">
        <div class="anchor-title">Silk Anchor 1 • 35% Weight</div>
        <div class="anchor-name">Bybit V5 Derivatives & OI</div>
        <div class="anchor-stat mono" id="ui-deriv">Score: +0 | Funding: 0.010%</div>
    </div>

    <!-- Node 2: News NLP & Sentiment (Top-Right) -->
    <div class="anchor-card anc-top-right">
        <div class="anchor-title" style="color:var(--purple);">Silk Anchor 2 • 35% Weight</div>
        <div class="anchor-name">News NLP & Sentiment Engine</div>
        <div class="anchor-stat mono" id="ui-sent">F&G: 50 | RSS: 0B / 0Br</div>
    </div>

    <!-- Node 3: BTC Dominance Radar (Bottom-Left) -->
    <div class="anchor-card anc-bottom-left">
        <div class="anchor-title" style="color:var(--amber);">Silk Anchor 3 • 15% Weight</div>
        <div class="anchor-name">BTC Dominance & Capital Flow</div>
        <div class="anchor-stat mono" id="ui-dom">BTC.D: 55.4% | Alt Flow: STABLE</div>
    </div>

    <!-- Node 4: Macro Freeze Guard (Bottom-Right) -->
    <div class="anchor-card anc-bottom-right">
        <div class="anchor-title" style="color:var(--green);">Silk Anchor 4 • 15% Weight</div>
        <div class="anchor-name">Macro Economic Guard</div>
        <div class="anchor-stat mono" id="ui-macro">Freeze: CLEAR | Fed Safe</div>
    </div>

    <!-- Center HUD (Output Score) -->
    <div class="center-hud">
        <div id="biasBadge" class="bias-badge mono" style="background:rgba(0,242,254,0.18); color:var(--cyan);">SYNCHRONIZING</div>
        <div id="compositeScore" class="score-display scifi mono">+0.0</div>
        <div style="font-size:10px; color:var(--muted); letter-spacing:1px; margin-top:2px;">SYNTHESIZED MACRO SCORE (-100 to +100)</div>
    </div>
</div>

<!-- Bottom Telemetry -->
<div class="bottom-grid">
    <div class="panel">
        <div class="panel-header">
            <span class="panel-title">📰 Real-Time RSS Stream (Spider Prey Caught in Web)</span>
            <span class="mono" style="font-size:10px; color:var(--muted);">Auto-Ingested Every 60s</span>
        </div>
        <div class="news-list" id="newsBox">
            <div class="news-item"><span>Spider scanning CoinTelegraph & CoinDesk live RSS...</span></div>
        </div>
    </div>

    <div class="panel">
        <div class="panel-header">
            <span class="panel-title">🛡️ Bybit 10x Futures Bot Execution Guard</span>
            <span class="mono" style="font-size:10px; color:var(--green);">POSTGRESQL IPC ACTIVE</span>
        </div>
        <div class="gate-box">
            <div class="gate-card">
                <div class="gate-title">LONG ORDERS</div>
                <div id="longGate" class="gate-status" style="color:var(--green);">ALLOWED ✅</div>
            </div>
            <div class="gate-card">
                <div class="gate-title">SHORT ORDERS</div>
                <div id="shortGate" class="gate-status" style="color:var(--green);">ALLOWED ✅</div>
            </div>
        </div>
        <div id="blacklistCard" style="background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.3); padding:12px; border-radius:8px; text-align:center;">
            <div style="font-size:12px; font-weight:800; color:var(--green);">✅ ZERO BLACKLISTED PAIRS</div>
            <div style="font-size:10px; color:var(--muted); margin-top:2px;">Exploit & Delist Shield active across 675 Perpetual pairs</div>
        </div>
    </div>
</div>

<!-- ========================================================================= -->
<!-- CYBER SPIDER CANVAS ANIMATION ENGINE                                      -->
<!-- ========================================================================= -->
<script>
const canvas = document.getElementById('spiderCanvas');
const ctx = canvas.getContext('2d');
let W, H;
let mouse = { x: null, y: null };

function resizeCanvas() {
    const rect = canvas.parentElement.getBoundingClientRect();
    W = canvas.width = rect.width;
    H = canvas.height = rect.height;
}
window.addEventListener('resize', resizeCanvas);
canvas.parentElement.addEventListener('mousemove', e => {
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
});
canvas.parentElement.addEventListener('mouseleave', () => { mouse.x = null; mouse.y = null; });
resizeCanvas();

// Traveling Energy Prey Particles
let particles = [];
for (let i = 0; i < 32; i++) {
    particles.push({
        targetCorner: Math.floor(Math.random() * 4), // 0: TL, 1: TR, 2: BL, 3: BR
        progress: Math.random(),
        speed: 0.005 + Math.random() * 0.008,
        size: Math.random() * 3 + 2.5
    });
}

function getCorners() {
    return [
        { x: 140, y: 65, color: '#00f2fe' },          // 0: Top-Left (Derivatives)
        { x: W - 140, y: 65, color: '#c084fc' },      // 1: Top-Right (Sentiment)
        { x: 140, y: H - 65, color: '#f59e0b' },      // 2: Bottom-Left (Dominance)
        { x: W - 140, y: H - 65, color: '#10b981' }   // 3: Bottom-Right (Macro)
    ];
}

let tick = 0;

// Draw Concentric Spider Web Rings
function drawConcentricWeb(cx, cy, maxRadius) {
    const rings = 6;
    const spokes = 16;

    ctx.save();
    ctx.lineWidth = 0.7;

    // Draw Spokes
    for (let s = 0; s < spokes; s++) {
        const angle = (s / spokes) * Math.PI * 2;
        ctx.strokeStyle = 'rgba(0, 242, 254, 0.12)';
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(cx + Math.cos(angle) * maxRadius, cy + Math.sin(angle) * maxRadius);
        ctx.stroke();
    }

    // Draw Concentric Rings
    for (let r = 1; r <= rings; r++) {
        const radius = (r / rings) * maxRadius;
        ctx.strokeStyle = `rgba(0, 242, 254, ${0.06 + (r / rings) * 0.14})`;
        ctx.beginPath();
        for (let s = 0; s <= spokes; s++) {
            const angle = (s / spokes) * Math.PI * 2;
            const wobble = Math.sin(tick * 0.03 + r + s) * 2.5;
            const px = cx + Math.cos(angle) * (radius + wobble);
            const py = cy + Math.sin(angle) * (radius + wobble);
            if (s === 0) ctx.moveTo(px, py);
            else ctx.lineTo(px, py);
        }
        ctx.stroke();
    }
    ctx.restore();
}

// Draw the Glowing Cybernetic Spider
function drawCyberSpider(cx, cy, color) {
    ctx.save();

    // 1. Cyber Abdomen / Core Glow
    ctx.shadowBlur = 30;
    ctx.shadowColor = color;

    // Rear Abdomen
    ctx.beginPath();
    ctx.ellipse(cx, cy - 8, 14, 20, 0, 0, Math.PI * 2);
    ctx.fillStyle = '#050b18';
    ctx.fill();
    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    ctx.stroke();

    // Cephalothorax (Front Body)
    ctx.beginPath();
    ctx.arc(cx, cy + 12, 11, 0, Math.PI * 2);
    ctx.fillStyle = '#09152e';
    ctx.fill();
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 1.8;
    ctx.stroke();

    // Glowing Chelicerae / Fangs
    ctx.strokeStyle = color;
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(cx - 4, cy + 22);
    ctx.lineTo(cx - 6, cy + 28);
    ctx.moveTo(cx + 4, cy + 22);
    ctx.lineTo(cx + 6, cy + 28);
    ctx.stroke();

    // Cybernetic Multiple Eyes (8 Eyes)
    ctx.fillStyle = color;
    ctx.shadowBlur = 10;
    ctx.beginPath();
    ctx.arc(cx - 4, cy + 9, 2, 0, Math.PI * 2);
    ctx.arc(cx + 4, cy + 9, 2, 0, Math.PI * 2);
    ctx.arc(cx - 7, cy + 13, 1.6, 0, Math.PI * 2);
    ctx.arc(cx + 7, cy + 13, 1.6, 0, Math.PI * 2);
    ctx.fill();

    // 2. Spider 8 Articulated Legs (Procedural IK Walking Animation)
    ctx.strokeStyle = color;
    ctx.lineWidth = 2.2;
    ctx.shadowBlur = 14;

    const legAngles = [
        -0.85, -0.45, -0.15, 0.20,             // Left 4 legs
        Math.PI + 0.85, Math.PI + 0.45, Math.PI + 0.15, Math.PI - 0.20 // Right 4 legs
    ];

    for (let i = 0; i < legAngles.length; i++) {
        let baseAngle = legAngles[i];
        let wobble = Math.sin(tick * 0.05 + i * 0.8) * 0.15;
        let currentAngle = baseAngle + wobble;

        let joint1Dist = 32;
        let joint2Dist = 26;

        let j1x = cx + Math.cos(currentAngle) * joint1Dist;
        let j1y = cy + Math.sin(currentAngle) * joint1Dist - 6;

        let kneeBend = (i < 4) ? -0.8 : 0.8;
        let j2x = j1x + Math.cos(currentAngle + kneeBend) * joint2Dist;
        let j2y = j1y + Math.sin(currentAngle + kneeBend) * joint2Dist + 12;

        ctx.beginPath();
        ctx.moveTo(cx + Math.cos(currentAngle) * 10, cy + Math.sin(currentAngle) * 10);
        ctx.lineTo(j1x, j1y);
        ctx.lineTo(j2x, j2y);
        ctx.stroke();
    }
    ctx.restore();
}

function renderScene() {
    tick++;
    ctx.clearRect(0, 0, W, H);

    const cx = W / 2;
    const cy = H / 2 - 25;
    const corners = getCorners();

    // 1. Draw Geometric Web Background
    drawConcentricWeb(cx, cy, Math.min(W, H) * 0.48);

    // 2. Draw 4 Major Silk Beams (Connecting Corners to Spider)
    for (let i = 0; i < corners.length; i++) {
        let c = corners[i];
        ctx.save();
        ctx.strokeStyle = c.color;
        ctx.lineWidth = 1.8;
        ctx.shadowBlur = 15;
        ctx.shadowColor = c.color;

        ctx.beginPath();
        ctx.moveTo(cx, cy);
        let midX = (cx + c.x) / 2 + Math.sin(tick * 0.03 + i) * 20;
        let midY = (cy + c.y) / 2 + Math.cos(tick * 0.03 + i) * 15;
        ctx.quadraticCurveTo(midX, midY, c.x, c.y);
        ctx.stroke();
        ctx.restore();
    }

    // 3. Draw Traveling Data Particles (Prey Ingestion along silk threads)
    for (let p of particles) {
        p.progress += p.speed;
        if (p.progress >= 1.0) {
            p.progress = 0;
            p.targetCorner = Math.floor(Math.random() * 4);
        }

        let c = corners[p.targetCorner];
        let px = c.x + (cx - c.x) * p.progress;
        let py = c.y + (cy - c.y) * p.progress;

        ctx.save();
        ctx.fillStyle = '#fff';
        ctx.shadowBlur = 14;
        ctx.shadowColor = c.color;
        ctx.beginPath();
        ctx.arc(px, py, p.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }

    // 4. Mouse Interactive Web Thread
    if (mouse.x && mouse.y) {
        ctx.save();
        ctx.strokeStyle = 'rgba(192, 132, 252, 0.6)';
        ctx.lineWidth = 1.4;
        ctx.setLineDash([4, 4]);
        ctx.shadowBlur = 10;
        ctx.shadowColor = '#c084fc';
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(mouse.x, mouse.y);
        ctx.stroke();
        ctx.restore();
    }

    // 5. Draw the Autonomous Spider at Center
    let currentColor = '#00f2fe';
    const scoreVal = parseFloat(document.getElementById('compositeScore').textContent || '0');
    if (scoreVal >= 15) currentColor = '#10b981';
    else if (scoreVal <= -15) currentColor = '#f43f5e';

    drawCyberSpider(cx, cy, currentColor);

    requestAnimationFrame(renderScene);
}
renderScene();

// =========================================================================
// TELEMETRY POLLER (Every 5s from FastAPI backend)
// =========================================================================
async function fetchBotState() {
    try {
        const res = await fetch('/api/state');
        const d = await res.json();

        const score = parseFloat(d.composite_score || 0);
        const scoreEl = document.getElementById('compositeScore');
        scoreEl.textContent = (score >= 0 ? '+' : '') + score.toFixed(1);

        const badge = document.getElementById('biasBadge');
        badge.textContent = d.bias_label || 'NEUTRAL';
        if (score >= 15) {
            scoreEl.style.color = 'var(--green)';
            badge.style.background = 'rgba(16,185,129,0.2)';
            badge.style.color = 'var(--green)';
        } else if (score <= -15) {
            scoreEl.style.color = 'var(--red)';
            badge.style.background = 'rgba(244,63,94,0.2)';
            badge.style.color = 'var(--red)';
        } else {
            scoreEl.style.color = 'var(--cyan)';
            badge.style.background = 'rgba(0,242,254,0.18)';
            badge.style.color = 'var(--cyan)';
        }

        // Anchors Text
        const bf = (parseFloat(d.btc_funding || 0) * 100).toFixed(4);
        document.getElementById('ui-deriv').textContent = `Score: ${d.derivatives_score >= 0 ? '+' : ''}${d.derivatives_score} | BTC Fund: ${bf}%`;
        document.getElementById('ui-sent').textContent = `F&G: ${d.fng_value} (${d.fng_label}) | RSS: ${d.bull_news}B / ${d.bear_news}Br`;
        document.getElementById('ui-dom').textContent = `BTC.D: ${d.btc_dominance}% | Flow: ${d.altseason_status}`;
        document.getElementById('ui-macro').textContent = `Freeze: ${d.is_news_freeze ? 'ACTIVE 🚨' : 'CLEAR ✅'} | ${d.active_macro_event || 'Safe'}`;

        // Execution Gatekeeper
        const freeze = Boolean(d.is_news_freeze);
        const lg = document.getElementById('longGate');
        const sg = document.getElementById('shortGate');
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
        document.getElementById('sync-status').textContent = d.supabase_synced ? 'SUPABASE IPC: SYNCED ✅' : 'SUPABASE IPC: LOCAL';

        // News Headlines List
        const newsBox = document.getElementById('newsBox');
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
        const blBox = document.getElementById('blacklistCard');
        if (d.blacklisted_tokens && d.blacklisted_tokens.length > 0) {
            blBox.style.background = 'rgba(244,63,94,0.12)';
            blBox.style.borderColor = 'rgba(244,63,94,0.4)';
            blBox.innerHTML = `<div style="font-size:12px; font-weight:800; color:var(--red);">🚨 BLOCKED PAIRS: ${d.blacklisted_tokens.join(', ')}</div>
                               <div style="font-size:10px; color:var(--muted); margin-top:2px;">Protected from High-Risk Exploit/Delist News</div>`;
        }
    } catch (e) {
        console.error(e);
    }
}
fetchBotState();
setInterval(fetchBotState, 5000);
</script>
</body>
</html>
"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("service_fundamental:app", host="0.0.0.0", port=port)
