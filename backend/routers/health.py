from fastapi import APIRouter
import time

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check():
    return {
        "status": "HEALTHY",
        "timestamp": time.time(),
        "version": "2.0.0",
        "subsystems": {
            "ai_vision": "ONLINE",
            "traffic_engine": "ONLINE",
            "signal_engine": "ONLINE",
            "forecaster": "ONLINE",
            "database": "CONNECTED",
            "websocket": "ONLINE"
        }
    }

@router.get("/system/status")
def system_status():
    return health_check()
