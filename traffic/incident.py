import time
from typing import Dict, List, Any, Optional

class IncidentManager:
    def __init__(self):
        self.active_incidents: Dict[str, Dict[str, Any]] = {}
        self.incident_history: List[Dict[str, Any]] = []

    def register_or_update(self, incident: Dict[str, Any]) -> Dict[str, Any]:
        inc_id = incident["incident_id"]
        now = time.time()

        if inc_id in self.active_incidents:
            existing = self.active_incidents[inc_id]
            existing.update(incident)
            existing["last_updated"] = now
            return existing
        else:
            incident["first_detected"] = now
            incident["last_updated"] = now
            self.active_incidents[inc_id] = incident
            return incident

    def resolve_incident(self, incident_id: str, note: str = "Cleared by operator") -> Optional[Dict[str, Any]]:
        if incident_id in self.active_incidents:
            inc = self.active_incidents.pop(incident_id)
            inc["status"] = "RESOLVED"
            inc["resolved_at"] = time.time()
            inc["resolution_note"] = note
            self.incident_history.append(inc)
            return inc
        return None

    def get_active(self) -> List[Dict[str, Any]]:
        return list(self.active_incidents.values())
