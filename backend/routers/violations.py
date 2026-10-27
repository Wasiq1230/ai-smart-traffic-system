from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.repositories.traffic_repo import TrafficRepository
from backend.services.traffic_service import master_traffic_service

router = APIRouter(prefix="/violations", tags=["Violations"])

@router.get("")
@router.get("/list")
def get_violations(db: Session = Depends(get_db)):
    db_viols = TrafficRepository.get_violations(db, limit=50)
    live_viols = master_traffic_service.last_state.get("violations", [])
    return {
        "recent_live_violations": live_viols,
        "stored_violations": [
            {
                "violation_id": v.violation_id,
                "type": v.violation_type,
                "vehicle_type": v.vehicle_type,
                "lane": v.lane,
                "speed_kmh": v.speed_kmh,
                "timestamp": v.timestamp.isoformat() if v.timestamp else None
            }
            for v in db_viols
        ]
    }
