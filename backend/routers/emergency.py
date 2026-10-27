from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from backend.database import get_db
from backend.models import EmergencyEvent
from backend.schemas import EmergencyAlertCreate
from backend.services.traffic_service import master_traffic_service
from backend.repositories.traffic_repo import TrafficRepository

router = APIRouter(prefix="/emergency", tags=["Emergency System"])

@router.get("")
@router.get("/active")
def get_emergency_alerts(db: Session = Depends(get_db)):
    events = TrafficRepository.get_emergency_events(db)
    active = [e for e in events if e.preemption_status == "ACTIVE"]
    return active or events

@router.post("/priority")
@router.post("/override")
def request_emergency_priority(req: EmergencyAlertCreate, db: Session = Depends(get_db)):
    alert_dict = {
        "alert_id": f"EM-MANUAL-{req.vehicle_type}",
        "vehicle_type": req.vehicle_type,
        "lane": req.approach_lane,
        "confidence": req.confidence
    }
    decision = master_traffic_service.signal_engine.compute_optimal_timings(
        lane_densities={"Northbound": 0.3, "Southbound": 0.3, "Eastbound": 0.3, "Westbound": 0.3},
        emergency_alerts=[alert_dict]
    )
    em_db = EmergencyEvent(
        alert_id=alert_dict["alert_id"],
        intersection_id=req.intersection_id,
        vehicle_type=req.vehicle_type,
        approach_lane=req.approach_lane,
        confidence=req.confidence,
        preemption_status="ACTIVE"
    )
    db.add(em_db)
    db.commit()
    return decision

@router.post("/clear")
def clear_emergency():
    master_traffic_service.signal_engine.emergency_mgr.clear_preemption()
    return {"message": "Emergency preemption cleared"}
