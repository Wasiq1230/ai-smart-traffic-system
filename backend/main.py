import asyncio
import os
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.config import settings
from backend.database import init_db, SessionLocal
from backend.websocket.manager import manager
from backend.services.traffic_service import master_traffic_service
from backend.repositories.traffic_repo import TrafficRepository
from ai_vision.pipeline import VisionPipeline

from backend.routers.health import router as health_router
from backend.routers.auth import router as auth_router
from backend.routers.traffic import router as traffic_router
from backend.routers.signals import router as signal_router
from backend.routers.forecast import router as forecast_router
from backend.routers.emergency import router as emergency_router
from backend.routers.accidents import router as accident_router
from backend.routers.violations import router as violation_router
from backend.routers.analytics import router as analytics_router
from backend.routers.detection import router as detection_router

background_pipeline = None

async def continuous_traffic_simulation():
    global background_pipeline
    background_pipeline = VisionPipeline(video_source=settings.SAMPLE_VIDEO_PATH)
    
    while True:
        try:
            signal_states = master_traffic_service.signal_engine.current_signal_states
            vision_result = background_pipeline.process_next_frame(signal_states=signal_states)
            
            if vision_result:
                payload = master_traffic_service.process_vision_payload(vision_result)
                
                db = SessionLocal()
                try:
                    for lane_name, l_data in vision_result.get("lane_analytics", {}).items():
                        TrafficRepository.log_measurement(db, {
                            "intersection_id": "INT-001",
                            "lane_name": lane_name,
                            "vehicle_count": l_data.get("vehicle_count", 0),
                            "pcu_count": l_data.get("vehicle_count", 0) * 1.2,
                            "density_score": l_data.get("density_score", 0.0),
                            "congestion_level": "MEDIUM" if l_data.get("density_score", 0) > 0.5 else "LOW",
                            "avg_speed_kmh": l_data.get("avg_speed_kmh", 45.0),
                            "queue_length_meters": l_data.get("queue_length_meters", 0.0)
                        })
                    for v in vision_result.get("violations", []):
                        TrafficRepository.log_violation(db, v)
                except Exception:
                    pass
                finally:
                    db.close()

                await manager.broadcast({
                    "event": "traffic_update",
                    "data": payload
                })
        except Exception:
            await manager.broadcast({
                "event": "traffic_update",
                "data": master_traffic_service.last_state
            })
            
        await asyncio.sleep(1.0)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    sim_task = asyncio.create_task(continuous_traffic_simulation())
    yield
    sim_task.cancel()
    if background_pipeline:
        background_pipeline.video_processor.release()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

api_prefix = settings.API_V1_PREFIX
app.include_router(health_router, prefix=api_prefix)
app.include_router(auth_router, prefix=api_prefix)
app.include_router(traffic_router, prefix=api_prefix)
app.include_router(signal_router, prefix=api_prefix)
app.include_router(forecast_router, prefix=api_prefix)
app.include_router(emergency_router, prefix=api_prefix)
app.include_router(accident_router, prefix=api_prefix)
app.include_router(violation_router, prefix=api_prefix)
app.include_router(analytics_router, prefix=api_prefix)
app.include_router(detection_router, prefix=api_prefix)

@app.websocket("/ws/traffic")
async def websocket_traffic_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    if master_traffic_service.last_state:
        await websocket.send_json({"event": "initial_state", "data": master_traffic_service.last_state})
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)

frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")
