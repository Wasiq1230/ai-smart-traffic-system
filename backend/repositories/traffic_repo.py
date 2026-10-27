from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from backend.models import (
    Intersection, TrafficMeasurement, Forecast, SignalDecision,
    EmergencyEvent, Incident, Violation, User, AuditEvent
)

class TrafficRepository:
    @staticmethod
    def log_measurement(db: Session, data: Dict[str, Any]) -> TrafficMeasurement:
        m = TrafficMeasurement(
            intersection_id=data.get("intersection_id", "INT-001"),
            lane_name=data.get("lane_name", "Northbound"),
            vehicle_count=data.get("vehicle_count", 0),
            pcu_count=data.get("pcu_count", 0.0),
            density_score=data.get("density_score", 0.0),
            congestion_level=data.get("congestion_level", "LOW"),
            avg_speed_kmh=data.get("avg_speed_kmh", 45.0),
            queue_length_meters=data.get("queue_length_meters", 0.0)
        )
        db.add(m)
        db.commit()
        db.refresh(m)
        return m

    @staticmethod
    def get_recent_measurements(db: Session, intersection_id: str, limit: int = 50) -> List[TrafficMeasurement]:
        return db.query(TrafficMeasurement).filter(
            TrafficMeasurement.intersection_id == intersection_id
        ).order_by(TrafficMeasurement.timestamp.desc()).limit(limit).all()

    @staticmethod
    def log_violation(db: Session, data: Dict[str, Any]) -> Violation:
        v = Violation(
            violation_id=data.get("violation_id", "VIOL-001"),
            intersection_id=data.get("intersection_id", "INT-001"),
            violation_type=data.get("type", "SPEEDING"),
            vehicle_type=data.get("vehicle_type", "car"),
            lane=data.get("lane", "Northbound"),
            speed_kmh=data.get("speed_kmh", 0.0)
        )
        db.add(v)
        db.commit()
        db.refresh(v)
        return v

    @staticmethod
    def get_violations(db: Session, limit: int = 50) -> List[Violation]:
        return db.query(Violation).order_by(Violation.timestamp.desc()).limit(limit).all()

    @staticmethod
    def get_incidents(db: Session, limit: int = 50) -> List[Incident]:
        return db.query(Incident).order_by(Incident.timestamp.desc()).limit(limit).all()

    @staticmethod
    def get_emergency_events(db: Session, limit: int = 50) -> List[EmergencyEvent]:
        return db.query(EmergencyEvent).order_by(EmergencyEvent.timestamp.desc()).limit(limit).all()
