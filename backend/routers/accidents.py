from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Incident
from backend.repositories.traffic_repo import TrafficRepository
from backend.services.traffic_service import master_traffic_service

router = APIRouter(prefix="/accidents", tags=["Accidents & Incidents"])

@router.get("")
@router.get("/active")
def get_active_accidents(db: Session = Depends(get_db)):
    return master_traffic_service.traffic_engine.incident_mgr.get_active()

@router.get("/history")
def get_accident_history(db: Session = Depends(get_db)):
    db_incidents = TrafficRepository.get_incidents(db)
    return [
        {
            "id": inc.id,
            "incident_id": inc.incident_id,
            "type": inc.incident_type,
            "severity": inc.severity,
            "status": inc.status,
            "lane": inc.lane,
            "description": inc.description,
            "timestamp": inc.timestamp.isoformat() if inc.timestamp else None
        }
        for inc in db_incidents
    ]

@router.post("/resolve/{incident_id}")
def resolve_incident(incident_id: str, db: Session = Depends(get_db)):
    res = master_traffic_service.traffic_engine.incident_mgr.resolve_incident(incident_id)
    db_inc = db.query(Incident).filter(Incident.incident_id == incident_id).first()
    if db_inc:
        db_inc.status = "RESOLVED"
        db.commit()
    return res or {"message": f"Incident {incident_id} resolved"}
