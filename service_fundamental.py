# ==============================================================================
# FUNDAMENTAL BOT CLOUD WEB SERVICE & SENTIENT CYBER-SPIDER MATRIX v5.0
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
    print("🧠🕷️ [Sentient Cyber Spider v5.0] Autonomous Hunting Loop Started...")
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

app = FastAPI(title="Chama Capital - Sentient Cyber Spider v5.0", lifespan=lifespan)

NO_CACHE_HEADERS = {
    "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
    "Pragma": "no-cache",
    "Expires": "0"
}

@app.api_route("/healthz", methods=["GET", "HEAD"])
@app.api_route("/api/state", methods=["GET", "HEAD"])
async def health_check():
    return JSONResponse(status_code=200, content=_LATEST_STATUS, headers=NO_CACHE_HEADERS)

@app.api_route("/", methods=["GET", "HEAD"])
async def serve_visual_terminal():
    return HTMLResponse(content=SENTIENT_SPIDER_HTML, status_code=200, headers=NO_CACHE_HEADERS)


SENTIENT_SPIDER_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CHAMA CAPITAL // Sentient Cyber-Spider Neural Core v5.0</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root {
    --bg: #010308;
    --card: rgba(6, 11, 24, 0.88);
    --border: rgba(0, 242, 254, 0.38);
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
    background: #010308;
    color: var(--text);
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
    padding: 12px 16px;
    overflow-x: hidden;
}
.mono { font-family: 'JetBrains Mono', monospace; }
.scifi { font-family: 'Orbitron', sans-serif; }

/* Header */
.header {
    display: flex; justify-content: space-between; align-items: center;
    padding: 10px 20px; background: var(--card); border: 1px solid var(--border);
    border-radius: 12px; margin-bottom: 12px; backdrop-filter: blur(16px);
    box-shadow: 0 0 30px rgba(0, 242, 254, 0.14);
}
.brand { display: flex; align-items: center; gap: 12px; }
.spider-logo {
    font-size: 26px; filter: drop-shadow(0 0 12px var(--cyan));
    animation: spiderGlow 1.5s infinite alternate;
}
@keyframes spiderGlow {
    0% { transform: scale(0.92); filter: drop-shadow(0 0 6px var(--cyan)); }
    100% { transform: scale(1.12); filter: drop-shadow(0 0 22px var(--cyan)); }
}
.pill {
    padding: 5px 12px; border-radius: 999px; font-size: 11px; font-weight: 700;
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(0, 242, 254, 0.08); border: 1px solid rgba(0, 242, 254, 0.3);
}
.dot { width: 8px; height: 8px; border-radius: 50%; background: var(--green); box-shadow: 0 0 10px var(--green); animation: blink 1s infinite; }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.25; } }

/* ========================================================================= */
/* SENTIENT CYBER-SPIDER ARENA                                               */
/* ========================================================================= */
.arena-container {
    position: relative;
    width: 100%;
    height: 580px;
    background: radial-gradient(circle at 50% 45%, #081d3d 0%, #030918 55%, #010308 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 14px;
    box-shadow: inset 0 0 110px rgba(0, 242, 254, 0.12), 0 0 45px rgba(0, 0, 0, 0.95);
    cursor: crosshair;
}
#spiderCanvas {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: 1;
}

/* Corner Anchor HUD Panels */
.anchor-card {
    position: absolute;
    z-index: 5;
    width: 285px;
    background: rgba(4, 9, 20, 0.88);
    border: 1px solid rgba(0, 242, 254, 0.32);
    border-radius: 12px;
    padding: 12px 16px;
    backdrop-filter: blur(14px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.85);
    pointer-events: none;
}
.anc-top-left { top: 16px; left: 16px; border-left: 4px solid var(--cyan); }
.anc-top-right { top: 16px; right: 16px; border-right: 4px solid var(--purple); text-align: right; }
.anc-bottom-left { bottom: 16px; left: 16px; border-left: 4px solid var(--amber); }
.anc-bottom-right { bottom: 16px; right: 16px; border-right: 4px solid var(--green); text-align: right; }

.anchor-title { font-size: 10px; color: var(--cyan); text-transform: uppercase; font-weight: 800; letter-spacing: 1.2px; }
.anchor-name { font-size: 13px; font-weight: 800; margin: 3px 0; color: #fff; }
.anchor-stat { font-size: 11px; color: #cbd5e1; }
.mini-bar-bg { height: 4px; width: 100%; background: rgba(255,255,255,0.08); border-radius: 4px; margin-top: 7px; overflow: hidden; }
.mini-bar-fill { height: 100%; width: 65%; background: var(--cyan); transition: width 0.6s ease; }

/* Top Center Neural Telemetry & Target Tracker */
.neural-thought-bar {
    position: absolute;
    top: 16px; left: 50%;
    transform: translateX(-50%);
    z-index: 5;
    background: rgba(3, 8, 20, 0.9);
    border: 1px solid rgba(0, 242, 254, 0.4);
    padding: 6px 20px;
    border-radius: 999px;
    font-size: 11px;
    color: var(--cyan);
    pointer-events: none;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 25px rgba(0, 242, 254, 0.2);
    white-space: nowrap;
}

/* Center Score HUD (Bottom Center inside Arena) */
.center-hud {
    position: absolute;
    bottom: 18px; left: 50%;
    transform: translateX(-50%);
    z-index: 6;
    text-align: center;
    pointer-events: none;
    background: rgba(4, 9, 22, 0.85);
    border: 1px solid rgba(0, 242, 254, 0.35);
    padding: 8px 30px;
    border-radius: 16px;
    backdrop-filter: blur(12px);
    box-shadow: 0 0 35px rgba(0, 242, 254, 0.15);
}
.bias-badge {
    padding: 3px 14px; border-radius: 999px; font-size: 11px; font-weight: 800;
    letter-spacing: 1.5px; display: inline-block; margin-bottom: 2px;
}
.score-display {
    font-size: 44px; font-weight: 900; line-height: 1.05;
    text-shadow: 0 0 25px rgba(0, 242, 254, 0.7);
}

/* Bottom Grid */
.bottom-grid {
    display: grid; grid-template-columns: 1.4fr 1fr; gap: 14px;
}
.panel {
    background: var(--card); border: 1px solid var(--border); border-radius: 12px;
    padding: 16px; backdrop-filter: blur(14px);
}
.panel-header {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid rgba(255,255,255,0.06);
}
.panel-title { font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; color: #cbd5e1; }

.news-list { display: flex; flex-direction: column; gap: 8px; max-height: 190px; overflow-y: auto; }
.news-item {
    display: flex; justify-content: space-between; align-items: center; gap: 10px;
    padding: 8px 12px; background: rgba(255,255,255,0.03);
    border-left: 3px solid var(--cyan); border-radius: 6px; font-size: 12px;
}
.news-tag { padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 700; white-space: nowrap; }

.gate-box { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 12px; }
.gate-card {
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px; padding: 10px; text-align: center;
}
.gate-title { font-size: 10px; color: var(--muted); margin-bottom: 2px; }
.gate-status { font-size: 13px; font-weight: 800; }

@media (max-width: 950px) {
    .arena-container { height: 640px; }
    .bottom-grid { grid-template-columns: 1fr; }
    .anchor-card { width: 215px; }
    .neural-thought-bar { display: none; }
}
</style>
</head>
<body>

<div class="header">
    <div class="brand">
        <div class="spider-logo">🕷️</div>
        <div>
            <div style="font-size: 15px; font-weight: 900; letter-spacing: 0.8px;" class="scifi">CHAMA CAPITAL MANAGEMENT</div>
            <div style="font-size: 11px; color: var(--cyan);" class="mono">SENTIENT CYBER-SPIDER // AUTONOMOUS NEURAL MATRIX v5.0</div>
        </div>
    </div>
    <div style="display: flex; gap: 10px; align-items: center;">
        <div class="pill"><span class="dot"></span> <span id="sync-status">SUPABASE IPC: SYNCED</span></div>
        <div class="pill mono" id="last-sync">SYNCING...</div>
    </div>
</div>

<!-- ========================================================================= -->
<!-- SENTIENT CYBER SPIDER ARENA                                               -->
<!-- ========================================================================= -->
<div class="arena-container">
    <canvas id="spiderCanvas"></canvas>

    <!-- Top Center Neural Status Stream -->
    <div class="neural-thought-bar mono" id="spiderThought">
        ⚡ SPIDER HUNTER LOCKED ON: [BTCUSDT PERP] — EXTRACTING LIVE FUNDING & OI...
    </div>

    <!-- Node 1: Derivatives (Top-Left) -->
    <div class="anchor-card anc-top-left">
        <div class="anchor-title">Silk Anchor 1 • 35% Weight</div>
        <div class="anchor-name">Bybit V5 Derivatives & OI</div>
        <div class="anchor-stat mono" id="ui-deriv">Score: +0 | Funding: 0.010%</div>
        <div class="mini-bar-bg"><div class="mini-bar-fill" id="bar-deriv" style="background:var(--cyan);"></div></div>
    </div>

    <!-- Node 2: News NLP & Sentiment (Top-Right) -->
    <div class="anchor-card anc-top-right">
        <div class="anchor-title" style="color:var(--purple);">Silk Anchor 2 • 35% Weight</div>
        <div class="anchor-name">News NLP & Sentiment Engine</div>
        <div class="anchor-stat mono" id="ui-sent">F&G: 50 | RSS: 0B / 0Br</div>
        <div class="mini-bar-bg"><div class="mini-bar-fill" id="bar-sent" style="background:var(--purple);"></div></div>
    </div>

    <!-- Node 3: BTC Dominance Radar (Bottom-Left) -->
    <div class="anchor-card anc-bottom-left">
        <div class="anchor-title" style="color:var(--amber);">Silk Anchor 3 • 15% Weight</div>
        <div class="anchor-name">BTC Dominance & Capital Flow</div>
        <div class="anchor-stat mono" id="ui-dom">BTC.D: 55.4% | Alt Flow: STABLE</div>
        <div class="mini-bar-bg"><div class="mini-bar-fill" id="bar-dom" style="background:var(--amber);"></div></div>
    </div>

    <!-- Node 4: Macro Freeze Guard (Bottom-Right) -->
    <div class="anchor-card anc-bottom-right">
        <div class="anchor-title" style="color:var(--green);">Silk Anchor 4 • 15% Weight</div>
        <div class="anchor-name">Macro Economic Guard</div>
        <div class="anchor-stat mono" id="ui-macro">Freeze: CLEAR | Fed Safe</div>
        <div class="mini-bar-bg"><div class="mini-bar-fill" id="bar-macro" style="background:var(--green); width:100%;"></div></div>
    </div>

    <!-- Center HUD (Output Score) -->
    <div class="center-hud">
        <div id="biasBadge" class="bias-badge mono" style="background:rgba(0,242,254,0.18); color:var(--cyan);">SYNCHRONIZING</div>
        <div id="compositeScore" class="score-display scifi mono">+0.0</div>
        <div style="font-size:9px; color:var(--muted); letter-spacing:1.5px; margin-top:2px;">SYNTHESIZED MACRO BIAS (-100 to +100)</div>
    </div>
</div>

<!-- Bottom Telemetry -->
<div class="bottom-grid">
    <div class="panel">
        <div class="panel-header">
            <span class="panel-title">📰 Real-Time RSS Stream (Spider Prey Caught in Web)</span>
            <span class="mono" style="font-size:10px; color:var(--cyan);">Move Mouse or Click Web to Command Spider</span>
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
<!-- v5.0 SENTIENT CYBER-SPIDER ENGINE                                         -->
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
canvas.parentElement.addEventListener('mousedown', () => {
    if (mouse.x && mouse.y) {
        triggerShockwave(mouse.x, mouse.y, '#c084fc', 240);
        spider.targetX = mouse.x;
        spider.targetY = mouse.y;
    }
});
resizeCanvas();

function getCorners() {
    return [
        { x: 155, y: 78, color: '#00f2fe', label: 'BYBIT OI/FUNDING' },
        { x: W - 155, y: 78, color: '#c084fc', label: 'RSS NLP STREAM' },
        { x: 155, y: H - 78, color: '#f59e0b', label: 'BTC DOMINANCE' },
        { x: W - 155, y: H - 78, color: '#10b981', label: 'MACRO SHIELD' }
    ];
}

// 1. Cyber Matrix Background Floating Particles
let bgStars = [];
for (let i = 0; i < 75; i++) {
    bgStars.push({
        x: Math.random() * 1600,
        y: Math.random() * 700,
        r: Math.random() * 1.8 + 0.5,
        vx: (Math.random() - 0.5) * 0.45,
        vy: (Math.random() - 0.5) * 0.45,
        alpha: Math.random() * 0.65 + 0.15
    });
}

// 2. Caught Prey Data Nodes on the Web (Spider actually walks to hunt these!)
const preyData = [
    { label: 'BTCUSDT', color: '#00f2fe' },
    { label: 'ETHUSDT', color: '#00f2fe' },
    { label: 'SOLUSDT', color: '#00f2fe' },
    { label: 'FUNDING RATE', color: '#10b981' },
    { label: 'OPEN INTEREST', color: '#10b981' },
    { label: 'FEAR & GREED', color: '#c084fc' },
    { label: 'COINDESK NLP', color: '#c084fc' },
    { label: 'BTC.D RADAR', color: '#f59e0b' },
    { label: 'ALT LIQUIDITY', color: '#f59e0b' },
    { label: 'CPI / FOMC', color: '#f43f5e' },
    { label: 'EXPLOIT GUARD', color: '#10b981' },
    { label: 'SUPABASE IPC', color: '#00f2fe' }
];
let preyNodes = [];
for (let i = 0; i < preyData.length; i++) {
    const angle = (i / preyData.length) * Math.PI * 2 + 0.2;
    const distRatio = 0.36 + (i % 3) * 0.20;
    preyNodes.push({
        label: preyData[i].label,
        color: preyData[i].color,
        angle: angle,
        distRatio: distRatio,
        x: 0,
        y: 0,
        pulse: Math.random() * Math.PI * 2,
        beingAnalyzed: 0
    });
}

// 3. High-Speed Traveling Data Comets along the 4 Anchor Beams
let pulses = [];
for (let i = 0; i < 44; i++) {
    pulses.push({
        corner: i % 4,
        progress: Math.random(),
        speed: 0.006 + Math.random() * 0.009,
        width: 2.2 + Math.random() * 2.5
    });
}

// 4. Shockwaves & String Vibrations
let shockwaves = [];
let cornerVibration = [0, 0, 0, 0];

function triggerShockwave(x, y, color, maxR = 165) {
    if (shockwaves.length < 10) {
        shockwaves.push({ x, y, radius: 14, maxRadius: maxR, alpha: 0.9, color });
    }
}

// 5. Autonomous Hunting Spider State
let spider = {
    x: 0,
    y: 0,
    targetX: 0,
    targetY: 0,
    angle: 0,
    targetAngle: 0,
    walkCycle: 0,
    huntTimer: 0,
    currentPreyIdx: 0,
    laserTimer: 0
};

let tick = 0;

// Draw Rotating Holographic Sci-Fi Rings + 360 Radar Sweep
function drawHologramHUD(cx, cy, maxR, color) {
    ctx.save();

    // 360 Rotating Radar Sonar Sweep
    const sweepAngle = (tick * 0.018) % (Math.PI * 2);
    let grad = ctx.createRadialGradient(cx, cy, 10, cx, cy, maxR * 1.1);
    grad.addColorStop(0, 'rgba(0, 242, 254, 0.18)');
    grad.addColorStop(1, 'transparent');

    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.arc(cx, cy, maxR * 1.1, sweepAngle, sweepAngle + 0.55);
    ctx.closePath();
    ctx.fill();

    // Outer Dashed Telemetry Ring 1
    ctx.translate(cx, cy);
    ctx.rotate(tick * 0.005);
    ctx.strokeStyle = 'rgba(0, 242, 254, 0.28)';
    ctx.lineWidth = 1.6;
    ctx.setLineDash([14, 8, 4, 8]);
    ctx.beginPath();
    ctx.arc(0, 0, maxR * 1.02, 0, Math.PI * 2);
    ctx.stroke();

    // Middle Counter-Rotating Ring 2
    ctx.rotate(-tick * 0.012);
    ctx.strokeStyle = 'rgba(192, 132, 252, 0.25)';
    ctx.lineWidth = 1.2;
    ctx.setLineDash([20, 15]);
    ctx.beginPath();
    ctx.arc(0, 0, maxR * 0.68, 0, Math.PI * 2);
    ctx.stroke();

    // Inner Core Ring 3
    ctx.rotate(tick * 0.02);
    ctx.strokeStyle = color;
    ctx.globalAlpha = 0.4;
    ctx.lineWidth = 1.5;
    ctx.setLineDash([6, 10]);
    ctx.beginPath();
    ctx.arc(0, 0, 58, 0, Math.PI * 2);
    ctx.stroke();

    ctx.restore();
}

// Draw Concentric Living Hexagonal Web (Centered at Arena Core)
function drawLivingSpiderWeb(cx, cy, maxR) {
    const rings = 8;
    const spokes = 16;

    ctx.save();
    for (let s = 0; s < spokes; s++) {
        const angle = (s / spokes) * Math.PI * 2;
        ctx.strokeStyle = 'rgba(0, 242, 254, 0.15)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        let endX = cx + Math.cos(angle) * maxR;
        let endY = cy + Math.sin(angle) * maxR;
        let midX = (cx + endX) / 2 + Math.sin(tick * 0.03 + s) * 6;
        let midY = (cy + endY) / 2 + Math.cos(tick * 0.03 + s) * 6;
        ctx.quadraticCurveTo(midX, midY, endX, endY);
        ctx.stroke();
    }

    for (let r = 1; r <= rings; r++) {
        const radius = (r / rings) * maxR;
        const ringAlpha = 0.08 + (r / rings) * 0.16;
        ctx.strokeStyle = `rgba(0, 242, 254, ${ringAlpha})`;
        ctx.lineWidth = 1.15;

        ctx.beginPath();
        for (let s = 0; s <= spokes; s++) {
            const angle = (s / spokes) * Math.PI * 2;
            const wobble = Math.sin(tick * 0.045 + r * 1.4 + s) * 3.5;
            const px = cx + Math.cos(angle) * (radius + wobble);
            const py = cy + Math.sin(angle) * (radius + wobble);
            if (s === 0) ctx.moveTo(px, py);
            else ctx.lineTo(px, py);
        }
        ctx.stroke();
    }
    ctx.restore();
}

// Update & Draw Floating Prey Nodes on the Web
function updateAndDrawPreyNodes(cx, cy, maxR) {
    ctx.save();
    ctx.font = '700 10px "JetBrains Mono", monospace';

    for (let i = 0; i < preyNodes.length; i++) {
        let n = preyNodes[i];
        n.pulse += 0.06;

        let r = maxR * n.distRatio + Math.sin(n.pulse) * 4;
        n.x = cx + Math.cos(n.angle) * r;
        n.y = cy + Math.sin(n.angle) * r;

        const isTarget = (i === spider.currentPreyIdx);

        // Outer target reticle if spider is hunting this node
        if (isTarget) {
            ctx.save();
            ctx.strokeStyle = n.color;
            ctx.lineWidth = 1.5;
            ctx.setLineDash([3, 3]);
            ctx.beginPath();
            ctx.arc(n.x, n.y, 12 + Math.sin(tick * 0.15) * 3, 0, Math.PI * 2);
            ctx.stroke();
            ctx.restore();
        }

        // Node Orb
        ctx.fillStyle = isTarget ? '#fff' : n.color;
        ctx.shadowBlur = isTarget ? 18 : 10;
        ctx.shadowColor = n.color;
        ctx.beginPath();
        ctx.arc(n.x, n.y, isTarget ? 5.5 : 3.5, 0, Math.PI * 2);
        ctx.fill();

        // Node Label
        ctx.shadowBlur = 0;
        ctx.fillStyle = isTarget ? '#00f2fe' : 'rgba(226, 232, 240, 0.85)';
        ctx.fillText(n.label, n.x + 9, n.y + 3);
    }
    ctx.restore();
}

// Draw Electric Plasma Extraction Beam between Spider and Prey
function drawElectricBeam(x1, y1, x2, y2, color) {
    ctx.save();
    ctx.strokeStyle = color;
    ctx.lineWidth = 2.2;
    ctx.shadowBlur = 16;
    ctx.shadowColor = color;

    ctx.beginPath();
    ctx.moveTo(x1, y1);
    const segments = 6;
    for (let i = 1; i < segments; i++) {
        let t = i / segments;
        let bx = x1 + (x2 - x1) * t + (Math.random() - 0.5) * 18;
        let by = y1 + (y2 - y1) * t + (Math.random() - 0.5) * 18;
        ctx.lineTo(bx, by);
    }
    ctx.lineTo(x2, y2);
    ctx.stroke();

    // Inner white hot core
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 1;
    ctx.stroke();
    ctx.restore();
}

// Draw Articulated Hunting Cyber Spider
function drawHuntingSpider(sx, sy, angle, walkCycle, color) {
    ctx.save();
    ctx.translate(sx, sy);
    ctx.rotate(angle);

    // 1. Spider Legs (8 Articulated 3-Segment IK Legs)
    ctx.strokeStyle = color;
    ctx.lineWidth = 2.6;
    ctx.shadowBlur = 16;
    ctx.shadowColor = color;

    const leftAngles = [-1.05, -0.60, -0.15, 0.35];
    const rightAngles = [Math.PI + 1.05, Math.PI + 0.60, Math.PI + 0.15, Math.PI - 0.35];
    const allLegs = [...leftAngles, ...rightAngles];

    for (let i = 0; i < allLegs.length; i++) {
        let baseA = allLegs[i];
        let phase = (i % 2 === 0 ? 1 : -1) * Math.sin(walkCycle + i * 0.75) * 0.26;
        let a = baseA + phase;

        let rX = Math.cos(a) * 12;
        let rY = Math.sin(a) * 12;

        let kX = rX + Math.cos(a) * 34;
        let kY = rY + Math.sin(a) * 34;

        let bend = (i < 4) ? -0.78 : 0.78;
        let fX = kX + Math.cos(a + bend) * 30;
        let fY = kY + Math.sin(a + bend) * 30;

        ctx.beginPath();
        ctx.moveTo(rX, rY);
        ctx.lineTo(kX, kY);
        ctx.lineTo(fX, fY);
        ctx.stroke();

        // Glowing Claw Joint & Tip
        ctx.fillStyle = '#fff';
        ctx.beginPath();
        ctx.arc(kX, kY, 2, 0, Math.PI * 2);
        ctx.arc(fX, fY, 2.4, 0, Math.PI * 2);
        ctx.fill();
    }

    // 2. Abdomen (Rear Reactor Core)
    ctx.shadowBlur = 32;
    ctx.shadowColor = color;
    ctx.beginPath();
    ctx.ellipse(0, -15, 18, 24, 0, 0, Math.PI * 2);
    ctx.fillStyle = '#030917';
    ctx.fill();
    ctx.strokeStyle = color;
    ctx.lineWidth = 2.8;
    ctx.stroke();

    // Glowing Reactor Core inside Abdomen
    let pulseR = 6.5 + Math.sin(tick * 0.12) * 2.8;
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(0, -15, pulseR, 0, Math.PI * 2);
    ctx.fill();

    // 3. Cephalothorax (Armored Head)
    ctx.beginPath();
    ctx.arc(0, 12, 13.5, 0, Math.PI * 2);
    ctx.fillStyle = '#07142b';
    ctx.fill();
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 2.2;
    ctx.stroke();

    // 4. Cybernetic Fangs (Animated Pincers)
    let fangPinch = Math.sin(tick * 0.1) * 2.5;
    ctx.strokeStyle = color;
    ctx.lineWidth = 2.8;
    ctx.beginPath();
    ctx.moveTo(-5, 22);
    ctx.lineTo(-7 + fangPinch, 34);
    ctx.moveTo(5, 22);
    ctx.lineTo(7 - fangPinch, 34);
    ctx.stroke();

    // 5. Glowing Eyes (Laser Optics)
    ctx.fillStyle = '#fff';
    ctx.shadowBlur = 14;
    ctx.shadowColor = '#fff';
    ctx.beginPath();
    ctx.arc(-4.5, 16, 2.6, 0, Math.PI * 2);
    ctx.arc(4.5, 16, 2.6, 0, Math.PI * 2);
    ctx.arc(-8.5, 12, 1.8, 0, Math.PI * 2);
    ctx.arc(8.5, 12, 1.8, 0, Math.PI * 2);
    ctx.fill();

    ctx.restore();
}

function renderScene() {
    tick++;
    ctx.clearRect(0, 0, W, H);

    const cx = W / 2;
    const cy = H / 2 - 20;
    const corners = getCorners();
    const maxR = Math.min(W, H) * 0.44;

    let activeColor = '#00f2fe';
    const scoreVal = parseFloat(document.getElementById('compositeScore').textContent || '0');
    if (scoreVal >= 15) activeColor = '#10b981';
    else if (scoreVal <= -15) activeColor = '#f43f5e';

    // 1. Ambient Matrix Stars
    ctx.save();
    for (let st of bgStars) {
        st.x += st.vx; st.y += st.vy;
        if (st.x < 0) st.x = W; if (st.x > W) st.x = 0;
        if (st.y < 0) st.y = H; if (st.y > H) st.y = 0;
        ctx.fillStyle = `rgba(0, 242, 254, ${st.alpha})`;
        ctx.beginPath();
        ctx.arc(st.x, st.y, st.r, 0, Math.PI * 2);
        ctx.fill();
    }
    ctx.restore();

    // 2. Holographic HUD & Radar Sweep
    drawHologramHUD(cx, cy, maxR, activeColor);

    // 3. Living Concentric Spider Web
    drawLivingSpiderWeb(cx, cy, maxR);

    // 4. Update & Draw Prey Nodes
    updateAndDrawPreyNodes(cx, cy, maxR);

    // 5. Autonomous Spider Hunting AI Logic
    if (spider.x === 0) { spider.x = cx; spider.y = cy; spider.targetX = cx; spider.targetY = cy; }

    let activePrey = preyNodes[spider.currentPreyIdx];

    if (mouse.x && mouse.y) {
        // Follow user mouse when hovering inside arena
        let dx = mouse.x - cx;
        let dy = mouse.y - cy;
        let dist = Math.hypot(dx, dy);
        spider.targetX = cx + (dx / (dist || 1)) * Math.min(dist * 0.55, maxR * 0.65);
        spider.targetY = cy + (dy / (dist || 1)) * Math.min(dist * 0.55, maxR * 0.65);
        spider.targetAngle = Math.atan2(mouse.y - spider.y, mouse.x - spider.x) - Math.PI / 2;
    } else {
        // Hunt from Prey Node to Prey Node across the Web!
        spider.huntTimer++;
        if (spider.huntTimer % 150 === 0) {
            spider.currentPreyIdx = (spider.currentPreyIdx + 1) % preyNodes.length;
            activePrey = preyNodes[spider.currentPreyIdx];
            // Walk 60% of the way toward that prey node
            spider.targetX = cx + (activePrey.x - cx) * 0.58;
            spider.targetY = cy + (activePrey.y - cy) * 0.58;
            spider.laserTimer = 45; // Fire extraction beam!

            const thEl = document.getElementById('spiderThought');
            if (thEl) {
                thEl.textContent = `⚡ SPIDER HUNTER LOCKED ON: [${activePrey.label}] — EXTRACTING REAL-TIME TELEMETRY...`;
            }
        }
        spider.targetAngle = Math.atan2(activePrey.y - spider.y, activePrey.x - spider.x) - Math.PI / 2;
    }

    // Smooth Spider Movement & Rotation
    let moveDX = spider.targetX - spider.x;
    let moveDY = spider.targetY - spider.y;
    let moveSpeed = Math.hypot(moveDX, moveDY);
    spider.x += moveDX * 0.045;
    spider.y += moveDY * 0.045;

    let angleDiff = spider.targetAngle - spider.angle;
    while (angleDiff > Math.PI) angleDiff -= Math.PI * 2;
    while (angleDiff < -Math.PI) angleDiff += Math.PI * 2;
    spider.angle += angleDiff * 0.08;

    // Walk cycle speeds up when walking!
    spider.walkCycle += 0.07 + Math.min(0.32, moveSpeed * 0.05);

    // 6. Draw 4 Main Silk Anchor Beams Connected to Spider
