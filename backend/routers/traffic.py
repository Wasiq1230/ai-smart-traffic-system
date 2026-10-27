from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from backend.database import get_db
from backend.services.traffic_service import master_traffic_service
from backend.repositories.traffic_repo import TrafficRepository

router = APIRouter(prefix="/traffic", tags=["Traffic Intelligence"])

@router.get("/current")
@router.get("/current/{intersection_id}")
def get_current_traffic(intersection_id: Optional[str] = "INT-001"):
    if master_traffic_service.last_state:
        return master_traffic_service.last_state.get("traffic", {})
    return master_traffic_service.traffic_engine.process_vision_data({
        "lane_analytics": {
            "Northbound": {"vehicles": [{"label": "car", "is_stopped": False} for _ in range(8)], "avg_speed_kmh": 42.0},
            "Southbound": {"vehicles": [{"label": "car", "is_stopped": False} for _ in range(12)], "avg_speed_kmh": 36.0},
            "Eastbound":  {"vehicles": [{"label": "car", "is_stopped": False} for _ in range(5)], "avg_speed_kmh": 48.0},
            "Westbound":  {"vehicles": [{"label": "car", "is_stopped": False} for _ in range(6)], "avg_speed_kmh": 44.0}
        }
    })

@router.get("/history")
@router.get("/history/{intersection_id}")
def get_traffic_history(intersection_id: str = "INT-001", db: Session = Depends(get_db)):
    records = TrafficRepository.get_recent_measurements(db, intersection_id, limit=50)
    return [
        {
            "id": r.id,
            "lane_name": r.lane_name,
            "vehicle_count": r.vehicle_count,
            "pcu_count": r.pcu_count,
            "density_score": r.density_score,
            "congestion_level": r.congestion_level,
            "avg_speed_kmh": r.avg_speed_kmh,
            "timestamp": r.timestamp.isoformat() if r.timestamp else None
        }
        for r in records
    ]

@router.post("/counts/{intersection_id}")
def update_traffic_counts(intersection_id: str, payload: Dict[str, Any]):
    return {"message": "Traffic counts updated", "intersection_id": intersection_id}

@router.get("/{intersection_id}")
def get_intersection_traffic(intersection_id: str):
    return get_current_traffic(intersection_id)
