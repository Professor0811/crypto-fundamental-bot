# ==============================================================================
# FUNDAMENTAL BOT CLOUD WEB SERVICE & LIVING CYBER-SPIDER AI VISUALIZER v4.0
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
    print("🧠🕷️ [Living Cyber Spider v4.0] Autonomous Neural Loop Started...")
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

app = FastAPI(title="Chama Capital - Living Cyber Spider v4.0", lifespan=lifespan)

@app.api_route("/healthz", methods=["GET", "HEAD"])
@app.api_route("/api/state", methods=["GET", "HEAD"])
async def health_check():
    return JSONResponse(status_code=200, content=_LATEST_STATUS)

@app.api_route("/", methods=["GET", "HEAD"])
async def serve_visual_terminal():
    return HTMLResponse(content=LIVING_SPIDER_HTML, status_code=200)


LIVING_SPIDER_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CHAMA CAPITAL // Living Cyber-Spider Neural Core v4.0</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root {
    --bg: #010308;
    --card: rgba(7, 12, 24, 0.88);
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
    box-shadow: 0 0 30px rgba(0, 242, 254, 0.12);
}
.brand { display: flex; align-items: center; gap: 12px; }
.spider-logo {
    font-size: 26px; filter: drop-shadow(0 0 12px var(--cyan));
    animation: spiderGlow 1.8s infinite alternate;
}
@keyframes spiderGlow {
    0% { transform: scale(0.95); filter: drop-shadow(0 0 6px var(--cyan)); }
    100% { transform: scale(1.1); filter: drop-shadow(0 0 20px var(--cyan)); }
}
.pill {
    padding: 5px 12px; border-radius: 999px; font-size: 11px; font-weight: 700;
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(0, 242, 254, 0.06); border: 1px solid rgba(0, 242, 254, 0.25);
}
.dot { width: 8px; height: 8px; border-radius: 50%; background: var(--green); box-shadow: 0 0 8px var(--green); animation: blink 1s infinite; }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.25; } }

/* ========================================================================= */
/* LIVING CYBER-SPIDER ARENA                                                 */
/* ========================================================================= */
.arena-container {
    position: relative;
    width: 100%;
    height: 570px;
    background: radial-gradient(circle at 50% 46%, #071936 0%, #020816 55%, #010308 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 14px;
    box-shadow: inset 0 0 100px rgba(0, 242, 254, 0.1), 0 0 40px rgba(0, 0, 0, 0.95);
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
    background: rgba(5, 10, 22, 0.88);
    border: 1px solid rgba(0, 242, 254, 0.28);
    border-radius: 12px;
    padding: 12px 16px;
    backdrop-filter: blur(14px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.85);
    pointer-events: none;
    transition: all 0.3s ease;
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

/* Live Neural Activity Log Overlay (Top Center) */
.neural-thought-bar {
    position: absolute;
    top: 16px; left: 50%;
    transform: translateX(-50%);
    z-index: 5;
    background: rgba(3, 8, 20, 0.85);
    border: 1px solid rgba(0, 242, 254, 0.3);
    padding: 6px 18px;
    border-radius: 999px;
    font-size: 11px;
    color: var(--cyan);
    pointer-events: none;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 20px rgba(0, 242, 254, 0.15);
    white-space: nowrap;
}

/* Center Score HUD (Below the Spider) */
.center-hud {
    position: absolute;
    bottom: 24px; left: 50%;
    transform: translateX(-50%);
    z-index: 6;
    text-align: center;
    pointer-events: none;
    background: rgba(4, 9, 20, 0.78);
    border: 1px solid rgba(0, 242, 254, 0.25);
    padding: 10px 28px;
    border-radius: 16px;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 35px rgba(0, 0, 0, 0.8);
}
.bias-badge {
    padding: 3px 14px; border-radius: 999px; font-size: 11px; font-weight: 800;
    letter-spacing: 1.5px; display: inline-block; margin-bottom: 2px;
}
.score-display {
    font-size: 46px; font-weight: 900; line-height: 1.05;
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
            <div style="font-size: 11px; color: var(--cyan);" class="mono">AUTONOMOUS QUANT CYBER SPIDER // LIVING NEURAL WEB v4.0</div>
        </div>
    </div>
    <div style="display: flex; gap: 10px; align-items: center;">
        <div class="pill"><span class="dot"></span> <span id="sync-status">SUPABASE IPC: SYNCED</span></div>
        <div class="pill mono" id="last-sync">SYNCING...</div>
    </div>
</div>

<!-- ========================================================================= -->
<!-- LIVING CYBER SPIDER ARENA                                                 -->
<!-- ========================================================================= -->
<div class="arena-container">
    <canvas id="spiderCanvas"></canvas>

    <!-- Top Center Neural Status Stream -->
    <div class="neural-thought-bar mono" id="spiderThought">
        ⚡ SPIDER NEURAL CORE: SCANNING BYBIT V5 DERIVATIVES & GLOBAL RSS FEEDS...
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
            <span class="mono" style="font-size:10px; color:var(--cyan);">Interactive: Move or Click on Spider Web Above</span>
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
<!-- LIVING CYBER-SPIDER PHYSICS & HOLOGRAPHIC ENGINE                          -->
<!-- ========================================================================= -->
<script>
const canvas = document.getElementById('spiderCanvas');
const ctx = canvas.getContext('2d');
let W, H;
let mouse = { x: null, y: null, clicked: false };

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
    mouse.clicked = true;
    if (mouse.x && mouse.y) triggerShockwave(mouse.x, mouse.y, '#c084fc', 220);
});
resizeCanvas();

function getCorners() {
    return [
        { x: 155, y: 75, color: '#00f2fe', label: 'BYBIT OI/FUNDING' },
        { x: W - 155, y: 75, color: '#c084fc', label: 'RSS NLP STREAM' },
        { x: 155, y: H - 75, color: '#f59e0b', label: 'BTC DOMINANCE' },
        { x: W - 155, y: H - 75, color: '#10b981', label: 'MACRO SHIELD' }
    ];
}

// 1. Background Ambient Matrix Cyber Particles
let bgStars = [];
for (let i = 0; i < 65; i++) {
    bgStars.push({
        x: Math.random() * 1600,
        y: Math.random() * 700,
        r: Math.random() * 1.6 + 0.4,
        vx: (Math.random() - 0.5) * 0.35,
        vy: (Math.random() - 0.5) * 0.35,
        alpha: Math.random() * 0.6 + 0.15
    });
}

// 2. Caught Prey Data Nodes on the Web (Crypto Tickers & Signals)
const preyLabels = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'FUNDING', 'OPEN INT', 'FEAR/GREED', 'COINDesk', 'BTC.D %', 'ALT FLOW', 'CPI GUARD', 'FOMC', 'EXPLOIT SHIELD'];
let preyNodes = [];
for (let i = 0; i < preyLabels.length; i++) {
    const angle = (i / preyLabels.length) * Math.PI * 2 + 0.25;
    const distRatio = 0.42 + (i % 3) * 0.22;
    preyNodes.push({
        label: preyLabels[i],
        angle: angle,
        distRatio: distRatio,
        pulse: Math.random() * Math.PI * 2,
        activeLaser: 0
    });
}

// 3. Traveling Energy Comets from 4 Corners
let pulses = [];
for (let i = 0; i < 36; i++) {
    pulses.push({
        corner: i % 4,
        progress: Math.random(),
        speed: 0.005 + Math.random() * 0.007,
        width: 2.2 + Math.random() * 2.2
    });
}

// 4. Shockwaves & String Vibrations
let shockwaves = [];
let cornerVibration = [0, 0, 0, 0];

function triggerShockwave(x, y, color, maxR = 160) {
    if (shockwaves.length < 8) {
        shockwaves.push({ x, y, radius: 18, maxRadius: maxR, alpha: 0.85, color });
    }
}

// 5. Autonomous Spider State (Position, Target, Angle, Hunting Behavior)
let spider = {
    x: 0,
    y: 0,
    targetX: 0,
    targetY: 0,
    angle: 0,
    targetAngle: 0,
    walkCycle: 0,
    patrolTimer: 0
};

const thoughts = [
    "⚡ SPIDER CORE: ANALYZING BYBIT V5 PERPETUAL FUNDING RATES...",
    "🕸️ PREY DETECTED: SCRAPING COINTELEGRAPH & COINDESK HEADLINES...",
    "🔬 QUANT BRAIN: EVALUATING BTC DOMINANCE & ALTCOIN LIQUIDITY...",
    "🛡️ SHIELD ACTIVE: CHECKING TOKEN BLACKLIST & EXPLOIT TRIGGERS...",
    "📡 SUPABASE IPC: SYNCHRONIZING MACRO BIAS WITH FUTURES BOT..."
];
let thoughtIdx = 0;
setInterval(() => {
    thoughtIdx = (thoughtIdx + 1) % thoughts.length;
    const el = document.getElementById('spiderThought');
    if (el) el.textContent = thoughts[thoughtIdx];
}, 4000);

let tick = 0;

// Draw Rotating Holographic Sci-Fi Rings + Radar Sweep
function drawHologramHUD(cx, cy, maxR, color) {
    ctx.save();

    // Rotating Radar Sonar Sweep
    const sweepAngle = (tick * 0.015) % (Math.PI * 2);
    let grad = ctx.createRadialGradient(cx, cy, 10, cx, cy, maxR);
    grad.addColorStop(0, 'rgba(0, 242, 254, 0.14)');
    grad.addColorStop(1, 'transparent');

    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.arc(cx, cy, maxR, sweepAngle, sweepAngle + 0.45);
    ctx.closePath();
    ctx.fill();

    // Outer Dashed Telemetry Ring 1
    ctx.translate(cx, cy);
    ctx.rotate(tick * 0.004);
    ctx.strokeStyle = 'rgba(0, 242, 254, 0.22)';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([12, 8, 4, 8]);
    ctx.beginPath();
    ctx.arc(0, 0, maxR * 1.04, 0, Math.PI * 2);
    ctx.stroke();

    // Inner Counter-Rotating Ring 2
    ctx.rotate(-tick * 0.01);
    ctx.strokeStyle = color;
    ctx.globalAlpha = 0.35;
    ctx.lineWidth = 1.2;
    ctx.setLineDash([6, 14]);
    ctx.beginPath();
    ctx.arc(0, 0, 68, 0, Math.PI * 2);
    ctx.stroke();

    ctx.restore();
}

// Draw Concentric Living Hexagonal Web
function drawLivingSpiderWeb(cx, cy, maxR) {
    const rings = 8;
    const spokes = 16;

    ctx.save();
    for (let s = 0; s < spokes; s++) {
        const angle = (s / spokes) * Math.PI * 2;
        ctx.strokeStyle = 'rgba(0, 242, 254, 0.13)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        let endX = cx + Math.cos(angle) * maxR;
        let endY = cy + Math.sin(angle) * maxR;
        let midX = (cx + endX) / 2 + Math.sin(tick * 0.03 + s) * 5;
        let midY = (cy + endY) / 2 + Math.cos(tick * 0.03 + s) * 5;
        ctx.quadraticCurveTo(midX, midY, endX, endY);
        ctx.stroke();
    }

    for (let r = 1; r <= rings; r++) {
        const radius = (r / rings) * maxR;
        const ringAlpha = 0.07 + (r / rings) * 0.15;
        ctx.strokeStyle = `rgba(0, 242, 254, ${ringAlpha})`;
        ctx.lineWidth = 1.1;

        ctx.beginPath();
        for (let s = 0; s <= spokes; s++) {
            const angle = (s / spokes) * Math.PI * 2;
            const wobble = Math.sin(tick * 0.04 + r * 1.4 + s) * 3.2;
            const px = cx + Math.cos(angle) * (radius + wobble);
            const py = cy + Math.sin(angle) * (radius + wobble);
            if (s === 0) ctx.moveTo(px, py);
            else ctx.lineTo(px, py);
        }
        ctx.stroke();
    }
    ctx.restore();
}

// Draw Floating Prey Nodes on the Web & Neural Lightning
function drawPreyNodes(cx, cy, maxR, sx, sy, mainColor) {
    ctx.save();
    ctx.font = '600 10px "JetBrains Mono", monospace';

    for (let i = 0; i < preyNodes.length; i++) {
        let n = preyNodes[i];
        n.pulse += 0.05;

        let r = maxR * n.distRatio + Math.sin(n.pulse) * 4;
        let nx = cx + Math.cos(n.angle) * r;
        let ny = cy + Math.sin(n.angle) * r;

        // Randomly fire neural lightning from Spider to Prey node
        if (Math.random() < 0.008 && n.activeLaser <= 0) {
            n.activeLaser = 22;
        }

        if (n.activeLaser > 0) {
            n.activeLaser--;
            ctx.save();
            ctx.strokeStyle = '#00f2fe';
            ctx.lineWidth = 1.6;
            ctx.shadowBlur = 12;
            ctx.shadowColor = '#00f2fe';
            ctx.beginPath();
            ctx.moveTo(sx, sy);
            // Jagged electric lightning midpoint
            let mx = (sx + nx) / 2 + (Math.random() - 0.5) * 18;
            let my = (sy + ny) / 2 + (Math.random() - 0.5) * 18;
            ctx.lineTo(mx, my);
            ctx.lineTo(nx, ny);
            ctx.stroke();
            ctx.restore();
        }

        // Node Orb
        ctx.fillStyle = n.activeLaser > 0 ? '#fff' : mainColor;
        ctx.shadowBlur = n.activeLaser > 0 ? 16 : 8;
        ctx.shadowColor = mainColor;
        ctx.beginPath();
        ctx.arc(nx, ny, n.activeLaser > 0 ? 5 : 3.2, 0, Math.PI * 2);
        ctx.fill();

        // Node Label
        ctx.shadowBlur = 0;
        ctx.fillStyle = n.activeLaser > 0 ? '#fff' : 'rgba(203, 213, 225, 0.78)';
        ctx.fillText(n.label, nx + 7, ny + 3);
    }
    ctx.restore();
}

// Draw Articulated Hunting Cyber Spider
function drawHuntingSpider(sx, sy, angle, walkCycle, color) {
    ctx.save();
    ctx.translate(sx, sy);
    ctx.rotate(angle);

    // 1. Spider Legs (8 Articulated 3-Segment IK Legs)
    ctx.strokeStyle = color;
    ctx.lineWidth = 2.5;
    ctx.shadowBlur = 16;
    ctx.shadowColor = color;

    const leftAngles = [-1.05, -0.60, -0.15, 0.35];
    const rightAngles = [Math.PI + 1.05, Math.PI + 0.60, Math.PI + 0.15, Math.PI - 0.35];
    const allLegs = [...leftAngles, ...rightAngles];

    for (let i = 0; i < allLegs.length; i++) {
        let baseA = allLegs[i];
        let phase = (i % 2 === 0 ? 1 : -1) * Math.sin(walkCycle + i * 0.7) * 0.22;
        let a = baseA + phase;

        let rX = Math.cos(a) * 12;
        let rY = Math.sin(a) * 12;

        let kX = rX + Math.cos(a) * 32;
        let kY = rY + Math.sin(a) * 32;

        let bend = (i < 4) ? -0.75 : 0.75;
        let fX = kX + Math.cos(a + bend) * 28;
        let fY = kY + Math.sin(a + bend) * 28;

        ctx.beginPath();
        ctx.moveTo(rX, rY);
        ctx.lineTo(kX, kY);
        ctx.lineTo(fX, fY);
        ctx.stroke();

        // Glowing Claw Joint & Tip
        ctx.fillStyle = '#fff';
        ctx.beginPath();
        ctx.arc(kX, kY, 1.8, 0, Math.PI * 2);
        ctx.arc(fX, fY, 2.2, 0, Math.PI * 2);
        ctx.fill();
    }

    // 2. Abdomen (Rear Reactor Core)
    ctx.shadowBlur = 30;
    ctx.shadowColor = color;
    ctx.beginPath();
    ctx.ellipse(0, -14, 17, 23, 0, 0, Math.PI * 2);
    ctx.fillStyle = '#030917';
    ctx.fill();
    ctx.strokeStyle = color;
    ctx.lineWidth = 2.6;
    ctx.stroke();

    // Glowing Reactor Core inside Abdomen
    let pulseR = 6 + Math.sin(tick * 0.1) * 2.5;
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(0, -14, pulseR, 0, Math.PI * 2);
    ctx.fill();

    // 3. Cephalothorax (Armored Head)
    ctx.beginPath();
    ctx.arc(0, 12, 13, 0, Math.PI * 2);
    ctx.fillStyle = '#07142b';
    ctx.fill();
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 2;
    ctx.stroke();

    // 4. Cybernetic Fangs (Animated Pincers)
    let fangPinch = Math.sin(tick * 0.08) * 2;
    ctx.strokeStyle = color;
    ctx.lineWidth = 2.6;
    ctx.beginPath();
    ctx.moveTo(-5, 22);
    ctx.lineTo(-7 + fangPinch, 33);
    ctx.moveTo(5, 22);
    ctx.lineTo(7 - fangPinch, 33);
    ctx.stroke();

    // 5. Glowing Eyes (Laser Optics)
    ctx.fillStyle = '#fff';
    ctx.shadowBlur = 12;
    ctx.shadowColor = '#fff';
    ctx.beginPath();
    ctx.arc(-4.5, 16, 2.5, 0, Math.PI * 2);
    ctx.arc(4.5, 16, 2.5, 0, Math.PI * 2);
    ctx.arc(-8.5, 12, 1.7, 0, Math.PI * 2);
    ctx.arc(8.5, 12, 1.7, 0, Math.PI * 2);
    ctx.fill();

    ctx.restore();
}

function renderScene() {
    tick++;
    ctx.clearRect(0, 0, W, H);

    const cx = W / 2;
    const cy = H / 2 - 28;
    const corners = getCorners();
    const maxR = Math.min(W, H) * 0.45;

    let activeColor = '#00f2fe';
    const scoreVal = parseFloat(document.getElementById('compositeScore').textContent || '0');
    if (scoreVal >= 15) activeColor = '#10b981';
    else if (scoreVal <= -15) activeColor = '#f43f5e';

    // 1. Draw Ambient Cyber Stars
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

    // 2. Update Autonomous Spider Movement & Hunting Patrol
    if (spider.x === 0) { spider.x = cx; spider.y = cy; spider.targetX = cx; spider.targetY = cy; }

    if (mouse.x && mouse.y) {
        // Look towards mouse and stalk slightly
        let dx = mouse.x - cx;
        let dy = mouse.y - cy;
        let dist = Math.hypot(dx, dy);
        let maxStalk = 55;
        spider.targetX = cx + (dx / (dist || 1)) * Math.min(dist * 0.25, maxStalk);
        spider.targetY = cy + (dy / (dist || 1)) * Math.min(dist * 0.25, maxStalk);
        spider.targetAngle = Math.atan2(mouse.y - spider.y, mouse.x - spider.x) - Math.PI / 2;
    } else {
        // Autonomous Hunting Patrol around center web
        spider.patrolTimer++;
        if (spider.patrolTimer % 140 === 0) {
            let randAngle = Math.random() * Math.PI * 2;
            let randDist = Math.random() * 38;
            spider.targetX = cx + Math.cos(randAngle) * randDist;
            spider.targetY = cy + Math.sin(randAngle) * randDist;
            spider.targetAngle = randAngle - Math.PI / 2;
        } else if (spider.patrolTimer % 280 === 0) {
            spider.targetX = cx;
            spider.targetY = cy;
        }
    }

    // Smooth interpolation for Spider position & rotation
    let moveDX = spider.targetX - spider.x;
    let moveDY = spider.targetY - spider.y;
    let moveSpeed = Math.hypot(moveDX, moveDY);
    spider.x += moveDX * 0.05;
    spider.y += moveDY * 0.05;

    // Normalize angle difference for smooth turning
    let angleDiff = spider.targetAngle - spider.angle;
    while (angleDiff > Math.PI) angleDiff -= Math.PI * 2;
    while (angleDiff < -Math.PI) angleDiff += Math.PI * 2;
    spider.angle += angleDiff * 0.06;

    // Leg walking speed scales with movement speed + idle breathing
    spider.walkCycle += 0.06 + Math.min(0.22, moveSpeed * 0.04);

    // 3. Draw Holographic HUD & Radar Sweep
    drawHologramHUD(cx, cy, maxR, activeColor);

    // 4. Draw Concentric Spider Web
    drawLivingSpiderWeb(cx, cy, maxR);

    // 5. Draw 4 Main Silk Anchor Beams (with plucked vibration physics)
    for (let i = 0; i < corners.length; i++) {
        let c = corners[i];
        cornerVibration[i] *= 0.92; // Dampen vibration

        ctx.save();
        ctx.strokeStyle = c.color;
        ctx.lineWidth = 2.4;
        ctx.shadowBlur = 18;
        ctx.shadowColor = c.color;

        ctx.beginPath();
        ctx.moveTo(spider.x, spider.y);
        let vib = Math.sin(tick * 0.5) * cornerVibration[i];
        let midX = (spider.x + c.x) / 2 + Math.sin(tick * 0.03 + i) * 18 + vib;
        let midY = (spider.y + c.y) / 2 + Math.cos(tick * 0.03 + i) * 14 + vib;
        ctx.quadraticCurveTo(midX, midY, c.x, c.y);
        ctx.stroke();
        ctx.restore();
    }

    // 6. Draw Prey Data Nodes & Spider Neural Lightning
    drawPreyNodes(cx, cy, maxR, spider.x, spider.y, activeColor);

    // 7. Draw Traveling Data Comets along the 4 Silk Beams
    for (let p of pulses) {
        p.progress += p.speed;
        if (p.progress >= 1.0) {
            p.progress = 0;
            cornerVibration[p.corner] = 14; // Pluck string!
            triggerShockwave(spider.x, spider.y, corners[p.corner].color, 130);
            p.corner = Math.floor(Math.random() * 4);
        }

        let c = corners[p.corner];
        let px = c.x + (spider.x - c.x) * p.progress;
        let py = c.y + (spider.y - c.y) * p.progress;

        let tailProg = Math.max(0, p.progress - 0.08);
        let tx = c.x + (spider.x - c.x) * tailProg;
        let ty = c.y + (spider.y - c.y) * tailProg;

        ctx.save();
        let grad = ctx.createLinearGradient(tx, ty, px, py);
        grad.addColorStop(0, 'transparent');
        grad.addColorStop(1, c.color);

        ctx.strokeStyle = grad;
        ctx.lineWidth = p.width;
        ctx.shadowBlur = 15;
        ctx.shadowColor = c.color;
        ctx.beginPath();
        ctx.moveTo(tx, ty);
        ctx.lineTo(px, py);
        ctx.stroke();

        ctx.fillStyle = '#fff';
        ctx.beginPath();
        ctx.arc(px, py, p.width * 1.25, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }

    // 8. Draw Energy Shockwaves
    for (let i = shockwaves.length - 1; i >= 0; i--) {
        let sw = shockwaves[i];
        sw.radius += 3.8;
        sw.alpha -= 0.022;
        if (sw.alpha <= 0 || sw.radius >= sw.maxRadius) {
            shockwaves.splice(i, 1);
            continue;
        }
        ctx.save();
        ctx.strokeStyle = sw.color;
        ctx.lineWidth = 2;
        ctx.globalAlpha = sw.alpha;
        ctx.shadowBlur = 14;
        ctx.shadowColor = sw.color;
        ctx.beginPath();
        ctx.arc(sw.x, sw.y, sw.radius, 0, Math.PI * 2);
        ctx.stroke();
        ctx.restore();
    }

    // 9. Mouse Laser Tether
    if (mouse.x && mouse.y) {
        ctx.save();
        ctx.strokeStyle = '#c084fc';
        ctx.lineWidth = 1.8;
        ctx.setLineDash([5, 5]);
        ctx.shadowBlur = 12;
        ctx.shadowColor = '#c084fc';
        ctx.beginPath();
        ctx.moveTo(spider.x, spider.y);
        ctx.lineTo(mouse.x, mouse.y);
        ctx.stroke();

        ctx.fillStyle = '#c084fc';
        ctx.beginPath();
        ctx.arc(mouse.x, mouse.y, 4, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }

    // 10. Draw Hunting Cyber Spider
    drawHuntingSpider(spider.x, spider.y, spider.angle, spider.walkCycle, activeColor);

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

        // Anchors Text & Mini Progress Bars
        const bf = (parseFloat(d.btc_funding || 0) * 100).toFixed(4);
        document.getElementById('ui-deriv').textContent = `Score: ${d.derivatives_score >= 0 ? '+' : ''}${d.derivatives_score} | BTC Fund: ${bf}%`;
        document.getElementById('ui-sent').textContent = `F&G: ${d.fng_value} (${d.fng_label}) | RSS: ${d.bull_news}B / ${d.bear_news}Br`;
        document.getElementById('ui-dom').textContent = `BTC.D: ${d.btc_dominance}% | Flow: ${d.altseason_status}`;
        document.getElementById('ui-macro').textContent = `Freeze: ${d.is_news_freeze ? 'ACTIVE 🚨' : 'CLEAR ✅'} | ${d.active_macro_event || 'Safe'}`;

        document.getElementById('bar-deriv').style.width = Math.min(100, Math.max(15, (parseFloat(d.derivatives_score || 0) + 100) / 2)) + '%';
        document.getElementById('bar-sent').style.width = Math.min(100, Math.max(15, (parseFloat(d.sentiment_score || 0) + 100) / 2)) + '%';
        document.getElementById('bar-dom').style.width = Math.min(100, Math.max(15, parseFloat(d.btc_dominance || 55))) + '%';

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
    uvicorn.run("service_fundamental:app", host="0.0.0.0", port=port)# ==============================================================================
# FUNDAMENTAL BOT CLOUD WEB SERVICE & FULL LIVE CYBER SPIDER VISUALIZATION
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
    print("🧠🕷️ [Full Live Cyber Spider] Autonomous Neural Loop Started...")
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

app = FastAPI(title="Chama Capital - Cyber Spider Visual Terminal", lifespan=lifespan)

@app.api_route("/healthz", methods=["GET", "HEAD"])
@app.api_route("/api/state", methods=["GET", "HEAD"])
async def health_check():
    return JSONResponse(status_code=200, content=_LATEST_STATUS)

@app.api_route("/", methods=["GET", "HEAD"])
async def serve_visual_terminal():
    return HTMLResponse(content=FULL_LIVE_SPIDER_HTML, status_code=200)


FULL_LIVE_SPIDER_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CHAMA CAPITAL // Autonomous Cyber Spider Macro Terminal</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root {
    --bg: #01040a;
    --card: rgba(8, 14, 28, 0.88);
    --border: rgba(0, 242, 254, 0.32);
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
    background: #01040a;
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
    border-radius: 12px; margin-bottom: 12px; backdrop-filter: blur(14px);
    box-shadow: 0 0 30px rgba(0, 242, 254, 0.08);
}
.brand { display: flex; align-items: center; gap: 12px; }
.spider-logo {
    font-size: 26px; filter: drop-shadow(0 0 10px var(--cyan));
    animation: corePulse 2s infinite alternate;
}
@keyframes corePulse {
    0% { transform: scale(0.96); filter: drop-shadow(0 0 6px var(--cyan)); }
    100% { transform: scale(1.06); filter: drop-shadow(0 0 18px var(--cyan)); }
}
.pill {
    padding: 5px 12px; border-radius: 999px; font-size: 11px; font-weight: 700;
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1);
}
.dot { width: 8px; height: 8px; border-radius: 50%; background: var(--green); animation: blink 1.2s infinite; }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

/* ========================================================================= */
/* THE FULL-SCREEN CYBER SPIDER ARENA                                        */
/* ========================================================================= */
.arena-container {
    position: relative;
    width: 100%;
    height: 560px;
    background: radial-gradient(circle at 50% 45%, #051026 0%, #020712 60%, #01040a 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 14px;
    box-shadow: inset 0 0 80px rgba(0, 242, 254, 0.06), 0 0 40px rgba(0, 0, 0, 0.9);
}
#spiderCanvas {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: 1;
}

/* Floating Web Anchor Cards (Corner Nodes) */
.anchor-card {
    position: absolute;
    z-index: 5;
    width: 270px;
    background: rgba(6, 11, 24, 0.92);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 12px 16px;
    backdrop-filter: blur(14px);
    box-shadow: 0 0 25px rgba(0, 0, 0, 0.8);
    pointer-events: none;
    transition: transform 0.3s ease, border-color 0.3s ease;
}
.anc-top-left { top: 16px; left: 16px; border-left: 4px solid var(--cyan); }
.anc-top-right { top: 16px; right: 16px; border-right: 4px solid var(--purple); text-align: right; }
.anc-bottom-left { bottom: 16px; left: 16px; border-left: 4px solid var(--amber); }
.anc-bottom-right { bottom: 16px; right: 16px; border-right: 4px solid var(--green); text-align: right; }

.anchor-title { font-size: 10px; color: var(--cyan); text-transform: uppercase; font-weight: 800; letter-spacing: 1px; }
.anchor-name { font-size: 13px; font-weight: 800; margin: 3px 0; color: #fff; }
.anchor-stat { font-size: 11px; color: #cbd5e1; }

/* Center HUD Sits Below the Spider */
.center-hud {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    z-index: 6;
    text-align: center;
    pointer-events: none;
    margin-top: 85px; /* Sits below the animated spider */
}
.bias-badge {
    padding: 5px 18px; border-radius: 999px; font-size: 12px; font-weight: 800;
    letter-spacing: 1.5px; display: inline-block; margin-bottom: 4px;
}
.score-display {
    font-size: 52px; font-weight: 900; line-height: 1;
    text-shadow: 0 0 30px rgba(0, 242, 254, 0.6);
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
    .arena-container { height: 620px; }
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
    <div class="anchor-card anc-top-left" id="card-0">
        <div class="anchor-title">Silk Anchor 1 • 35% Weight</div>
        <div class="anchor-name">Bybit V5 Derivatives & OI</div>
        <div class="anchor-stat mono" id="ui-deriv">Score: +0 | Funding: 0.010%</div>
    </div>

    <!-- Node 2: News NLP & Sentiment (Top-Right) -->
    <div class="anchor-card anc-top-right" id="card-1">
        <div class="anchor-title" style="color:var(--purple);">Silk Anchor 2 • 35% Weight</div>
        <div class="anchor-name">News NLP & Sentiment Engine</div>
        <div class="anchor-stat mono" id="ui-sent">F&G: 50 | RSS: 0B / 0Br</div>
    </div>

    <!-- Node 3: BTC Dominance Radar (Bottom-Left) -->
    <div class="anchor-card anc-bottom-left" id="card-2">
        <div class="anchor-title" style="color:var(--amber);">Silk Anchor 3 • 15% Weight</div>
        <div class="anchor-name">BTC Dominance & Capital Flow</div>
        <div class="anchor-stat mono" id="ui-dom">BTC.D: 55.4% | Alt Flow: STABLE</div>
    </div>

    <!-- Node 4: Macro Freeze Guard (Bottom-Right) -->
    <div class="anchor-card anc-bottom-right" id="card-3">
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
<!-- ADVANCED FULL LIVE CYBER SPIDER SIMULATION SCRIPT                        -->
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

function getCorners() {
    return [
        { x: 140, y: 70, color: '#00f2fe' },          // 0: Top-Left (Derivatives)
        { x: W - 140, y: 70, color: '#c084fc' },      // 1: Top-Right (Sentiment)
        { x: 140, y: H - 70, color: '#f59e0b' },      // 2: Bottom-Left (Dominance)
        { x: W - 140, y: H - 70, color: '#10b981' }   // 3: Bottom-Right (Macro)
    ];
}

// Data Pulses (Prey Traveling to the Spider Core)
let pulses = [];
for (let i = 0; i < 40; i++) {
    pulses.push({
        corner: Math.floor(Math.random() * 4),
        progress: Math.random(),
        speed: 0.005 + Math.random() * 0.008,
        length: 18 + Math.random() * 22,
        width: 2 + Math.random() * 2
    });
}

// Shockwave Energy Rings emitted from Spider on Data Ingestion
let shockwaves = [];
function triggerShockwave(x, y, color) {
    if (shockwaves.length < 5) {
        shockwaves.push({ x, y, radius: 25, maxRadius: 180, alpha: 0.8, color });
    }
}

let tick = 0;

// Draw Complex Procedural Concentric Hexagonal Spider Web
function drawLivingSpiderWeb(cx, cy, maxR, mainColor) {
    const rings = 8;
    const spokes = 16;

    ctx.save();
    // 1. Spokes (Radial Silk Threads)
    for (let s = 0; s < spokes; s++) {
        const angle = (s / spokes) * Math.PI * 2;
        ctx.strokeStyle = 'rgba(0, 242, 254, 0.12)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(cx, cy);

        // Organic thread wave
        let endX = cx + Math.cos(angle) * maxR;
        let endY = cy + Math.sin(angle) * maxR;
        let midX = (cx + endX) / 2 + Math.sin(tick * 0.03 + s) * 6;
        let midY = (cy + endY) / 2 + Math.cos(tick * 0.03 + s) * 6;

        ctx.quadraticCurveTo(midX, midY, endX, endY);
        ctx.stroke();
    }

    // 2. Concentric Web Rings (Spiraling Network)
    for (let r = 1; r <= rings; r++) {
        const radius = (r / rings) * maxR;
        const ringAlpha = 0.06 + (r / rings) * 0.14;
        ctx.strokeStyle = `rgba(0, 242, 254, ${ringAlpha})`;
        ctx.lineWidth = 1.1;

        ctx.beginPath();
        for (let s = 0; s <= spokes; s++) {
            const angle = (s / spokes) * Math.PI * 2;
            const wobble = Math.sin(tick * 0.04 + r * 1.5 + s) * 3;
            const px = cx + Math.cos(angle) * (radius + wobble);
            const py = cy + Math.sin(angle) * (radius + wobble);

            if (s === 0) ctx.moveTo(px, py);
            else ctx.lineTo(px, py);
        }
        ctx.stroke();
    }
    ctx.restore();
}

// Procedural Articulated Cyber Spider (Inverse Kinematics Body & Legs)
function drawCyberSpider(cx, cy, color) {
    ctx.save();

    // Subtle breathing displacement
    let breathe = Math.sin(tick * 0.06) * 2;
    let spiderY = cy + breathe;

    // 1. Abdomen & Core Glow (Rear)
    ctx.shadowBlur = 32;
    ctx.shadowColor = color;

    ctx.beginPath();
    ctx.ellipse(cx, spiderY - 10, 16, 24, 0, 0, Math.PI * 2);
    ctx.fillStyle = '#040b18';
    ctx.fill();
    ctx.strokeStyle = color;
    ctx.lineWidth = 2.5;
    ctx.stroke();

    // Core Circuitry Inside Abdomen
    ctx.strokeStyle = 'rgba(255,255,255,0.6)';
    ctx.lineWidth = 1.2;
    ctx.beginPath();
    ctx.moveTo(cx, spiderY - 26);
    ctx.lineTo(cx, spiderY + 2);
    ctx.moveTo(cx - 8, spiderY - 12);
    ctx.lineTo(cx + 8, spiderY - 12);
    ctx.stroke();

    // 2. Cephalothorax (Front Head)
    ctx.beginPath();
    ctx.arc(cx, spiderY + 14, 13, 0, Math.PI * 2);
    ctx.fillStyle = '#071530';
    ctx.fill();
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 2;
    ctx.stroke();

    // 3. Glowing Cybernetic Multi-Eyes (8 Eyes)
    ctx.fillStyle = color;
    ctx.shadowBlur = 12;
    ctx.beginPath();
    ctx.arc(cx - 5, spiderY + 11, 2.5, 0, Math.PI * 2);
    ctx.arc(cx + 5, spiderY + 11, 2.5, 0, Math.PI * 2);
    ctx.arc(cx - 9, spiderY + 15, 1.8, 0, Math.PI * 2);
    ctx.arc(cx + 9, spiderY + 15, 1.8, 0, Math.PI * 2);
    ctx.arc(cx - 3, spiderY + 17, 1.5, 0, Math.PI * 2);
    ctx.arc(cx + 3, spiderY + 17, 1.5, 0, Math.PI * 2);
    ctx.fill();

    // 4. Chelicerae / Fangs (Mouthparts)
    ctx.strokeStyle = color;
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(cx - 4, spiderY + 25);
    ctx.lineTo(cx - 7, spiderY + 33);
    ctx.moveTo(cx + 4, spiderY + 25);
    ctx.lineTo(cx + 7, spiderY + 33);
    ctx.stroke();

    // 5. Procedural 8 Articulated Legs (Realistic Creepy-Crawly Movement)
    ctx.strokeStyle = color;
    ctx.lineWidth = 2.4;
    ctx.shadowBlur = 16;

    // Angles for the 8 legs
    const leftAngles = [-0.95, -0.55, -0.15, 0.25];
    const rightAngles = [Math.PI + 0.95, Math.PI + 0.55, Math.PI + 0.15, Math.PI - 0.25];
    const allLegs = [...leftAngles, ...rightAngles];

    for (let i = 0; i < allLegs.length; i++) {
        let baseAngle = allLegs[i];
        let walkOffset = Math.sin(tick * 0.05 + i * 1.1) * 0.18;
        let legAngle = baseAngle + walkOffset;

        let coxaDist = 12;      // Body connection
        let femurDist = 34;     // Upper leg
        let tibiaDist = 28;     // Lower leg

        let rootX = cx + Math.cos(legAngle) * coxaDist;
        let rootY = spiderY + Math.sin(legAngle) * coxaDist;

        let kneeX = rootX + Math.cos(legAngle) * femurDist;
        let kneeY = rootY + Math.sin(legAngle) * femurDist - 8;

        let kneeBend = (i < 4) ? -0.85 : 0.85;
        let footX = kneeX + Math.cos(legAngle + kneeBend) * tibiaDist;
        let footY = kneeY + Math.sin(legAngle + kneeBend) * tibiaDist + 14;

        ctx.beginPath();
        ctx.moveTo(rootX, rootY);
        ctx.lineTo(kneeX, kneeY);
        ctx.lineTo(footX, footY);
        ctx.stroke();

        // Glowing Foot Tip
        ctx.fillStyle = '#fff';
        ctx.beginPath();
        ctx.arc(footX, footY, 1.8, 0, Math.PI * 2);
        ctx.fill();
    }
    ctx.restore();
}

function renderScene() {
    tick++;
    ctx.clearRect(0, 0, W, H);

    const cx = W / 2;
    const cy = H / 2 - 25;
    const corners = getCorners();

    // Detect Core Status Color
    let activeColor = '#00f2fe';
    const scoreVal = parseFloat(document.getElementById('compositeScore').textContent || '0');
    if (scoreVal >= 15) activeColor = '#10b981';
    else if (scoreVal <= -15) activeColor = '#f43f5e';

    // 1. Draw Living Geometric Spider Web
    drawLivingSpiderWeb(cx, cy, Math.min(W, H) * 0.48, activeColor);

    // 2. Draw 4 Main Glowing Silk Laser Beams (Connecting Corners)
    for (let i = 0; i < corners.length; i++) {
        let c = corners[i];
        ctx.save();
        ctx.strokeStyle = c.color;
        ctx.lineWidth = 2.2;
        ctx.shadowBlur = 18;
        ctx.shadowColor = c.color;

        ctx.beginPath();
        ctx.moveTo(cx, cy);
        let midX = (cx + c.x) / 2 + Math.sin(tick * 0.03 + i) * 22;
        let midY = (cy + c.y) / 2 + Math.cos(tick * 0.03 + i) * 16;
        ctx.quadraticCurveTo(midX, midY, c.x, c.y);
        ctx.stroke();
        ctx.restore();
    }

    // 3. Draw Traveling Data Comets (Prey Packets with Laser Tails)
    for (let p of pulses) {
        p.progress += p.speed;
        if (p.progress >= 1.0) {
            p.progress = 0;
            p.corner = Math.floor(Math.random() * 4);
            // Trigger shockwave on hitting spider core
            triggerShockwave(cx, cy, activeColor);
        }

        let c = corners[p.corner];
        let px = c.x + (cx - c.x) * p.progress;
        let py = c.y + (cy - c.y) * p.progress;

        // Tail calculation
        let tailProg = Math.max(0, p.progress - 0.06);
        let tx = c.x + (cx - c.x) * tailProg;
        let ty = c.y + (cy - c.y) * tailProg;

        ctx.save();
        let grad = ctx.createLinearGradient(tx, ty, px, py);
        grad.addColorStop(0, 'transparent');
        grad.addColorStop(1, c.color);

        ctx.strokeStyle = grad;
        ctx.lineWidth = p.width;
        ctx.shadowBlur = 14;
        ctx.shadowColor = c.color;

        ctx.beginPath();
        ctx.moveTo(tx, ty);
        ctx.lineTo(px, py);
        ctx.stroke();

        // Bright Head
        ctx.fillStyle = '#fff';
        ctx.beginPath();
        ctx.arc(px, py, p.width * 1.2, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }

    // 4. Draw Radial Energy Shockwaves on Data Ingestion
    for (let i = shockwaves.length - 1; i >= 0; i--) {
        let sw = shockwaves[i];
        sw.radius += 3.5;
        sw.alpha -= 0.02;

        if (sw.alpha <= 0 || sw.radius >= sw.maxRadius) {
            shockwaves.splice(i, 1);
            continue;
        }

        ctx.save();
        ctx.strokeStyle = sw.color;
        ctx.lineWidth = 2;
        ctx.globalAlpha = sw.alpha;
        ctx.shadowBlur = 15;
        ctx.shadowColor = sw.color;
        ctx.beginPath();
        ctx.arc(sw.x, sw.y, sw.radius, 0, Math.PI * 2);
        ctx.stroke();
        ctx.restore();
    }

    // 5. Mouse Magnetic Web Thread Interaction
    if (mouse.x && mouse.y) {
        ctx.save();
        ctx.strokeStyle = 'rgba(192, 132, 252, 0.7)';
        ctx.lineWidth = 1.6;
        ctx.setLineDash([4, 4]);
        ctx.shadowBlur = 12;
        ctx.shadowColor = '#c084fc';
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(mouse.x, mouse.y);
        ctx.stroke();
        ctx.restore();
    }

    // 6. Draw Living Cyber Spider at Center
    drawCyberSpider(cx, cy, activeColor);

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
