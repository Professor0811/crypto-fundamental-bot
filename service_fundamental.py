# ==============================================================================
# FUNDAMENTAL BOT CLOUD WEB SERVICE (Render Free Tier Compatible)
# Supports both GET and HEAD HTTP methods for UptimeRobot monitoring
# ==============================================================================

import os
import asyncio
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import config_fundamental as cfg
import research_brain as brain

# Shared state in memory for health telemetry
_LATEST_STATUS = {
    "status": "initializing",
    "composite_score": 0.0,
    "bias_label": "NEUTRAL",
    "is_news_freeze": False,
    "last_synced": None
}

async def fundamental_background_worker():
    """Background task running the 24/7 research & macro bias loop."""
    print("🧠 [Fundamental Cloud Worker] Background loop started...")
    while True:
        try:
            start_ts = time.time()
            
            # Run synthesis & auto-push to Supabase via research_brain
            res = await asyncio.to_thread(brain.calculate_composite_bias)
            
            _LATEST_STATUS["status"] = "online"
            _LATEST_STATUS["composite_score"] = res.get("composite_score", 0.0)
            _LATEST_STATUS["bias_label"] = res.get("bias_label", "NEUTRAL")
            _LATEST_STATUS["is_news_freeze"] = res.get("is_news_freeze", False)
            _LATEST_STATUS["last_synced"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            
            print(f"[{_LATEST_STATUS['last_synced']}] Macro Bias Synced: {_LATEST_STATUS['bias_label']} ({_LATEST_STATUS['composite_score']:+.1f}) | Freeze: {_LATEST_STATUS['is_news_freeze']}")
            
            elapsed = time.time() - start_ts
            sleep_duration = max(5.0, cfg.SYNTHESIS_INTERVAL - elapsed)
            await asyncio.sleep(sleep_duration)

        except Exception as e:
            print(f"[Fundamental Cloud Worker Error]: {e}")
            await asyncio.sleep(10)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start background research loop
    task = asyncio.create_task(fundamental_background_worker())
    yield
    # Shutdown
    task.cancel()

app = FastAPI(title="Fundamental Research & Macro Bias Engine", lifespan=lifespan)

# Route handles both GET and HEAD methods across root (/) and /healthz
@app.api_route("/", methods=["GET", "HEAD"])
@app.api_route("/healthz", methods=["GET", "HEAD"])
async def health_check():
    """Health check endpoint supporting both GET and UptimeRobot default HEAD requests."""
    return JSONResponse(status_code=200, content=_LATEST_STATUS)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("service_fundamental:app", host="0.0.0.0", port=port)
