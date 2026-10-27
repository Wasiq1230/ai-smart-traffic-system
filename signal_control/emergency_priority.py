import time
from typing import Dict, List, Any, Optional

class EmergencyPriorityManager:
    def __init__(self):
        self.active_preemption: Optional[Dict[str, Any]] = None
        self.preemption_history: List[Dict[str, Any]] = []

    def request_priority(self, emergency_alert: Dict[str, Any]) -> Dict[str, Any]:
        target_lane = emergency_alert.get("lane", "Northbound")
        now = time.time()

        plan = {
            "preemption_id": f"PREEMPT-{int(now)}",
            "emergency_alert_id": emergency_alert.get("alert_id", "UNKNOWN"),
            "vehicle_type": emergency_alert.get("vehicle_type", "ambulance"),
            "green_lane": target_lane,
            "preemption_status": "ACTIVE",
            "clearance_green_seconds": 30,
            "started_at": now,
            "is_emergency_override": True
        }
        self.active_preemption = plan
        return plan

    def clear_preemption(self, note: str = "Emergency vehicle cleared intersection"):
        if self.active_preemption:
            self.active_preemption["preemption_status"] = "CLEARED"
            self.active_preemption["cleared_at"] = time.time()
            self.active_preemption["note"] = note
            self.preemption_history.append(self.active_preemption)
            self.active_preemption = None
