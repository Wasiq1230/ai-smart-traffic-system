"""
Traffic Violation Detection Module.
"""

import time
from typing import List, Dict, Any, Optional
from ai_vision.tracker import TrackedObject


class ViolationDetector:
    def __init__(self, speed_limit_kmh: float = 60.0, speed_tolerance: float = 10.0):
        self.speed_limit_kmh = speed_limit_kmh
        self.speed_tolerance = speed_tolerance
        self.violations: List[Dict[str, Any]] = []

    def check_violations(
        self,
        tracked_objects: List[TrackedObject],
        signal_states: Optional[Dict[str, str]] = None
    ) -> List[Dict[str, Any]]:
        new_violations = []
        signals = signal_states or {"Northbound": "RED", "Southbound": "GREEN", "Eastbound": "RED", "Westbound": "RED"}
        now = time.time()

        for obj in tracked_objects:
            effective_limit = self.speed_limit_kmh + self.speed_tolerance
            if obj.speed_kmh > effective_limit:
                v_id = f"VIOL-SPEED-{obj.track_id}-{int(now)}"
                viol = {
                    "violation_id": v_id,
                    "type": "SPEEDING",
                    "track_id": obj.track_id,
                    "vehicle_type": obj.label,
                    "lane": obj.lane,
                    "speed_kmh": obj.speed_kmh,
                    "speed_limit_kmh": self.speed_limit_kmh,
                    "excess_speed_kmh": round(obj.speed_kmh - self.speed_limit_kmh, 1),
                    "confidence": 0.91,
                    "timestamp": now,
                    "evidence_location": [obj.cx, obj.cy]
                }
                new_violations.append(viol)
                self.violations.append(viol)

            lane_signal = signals.get(obj.lane, "GREEN")
            if lane_signal == "RED" and obj.speed_kmh > 15.0:
                v_id = f"VIOL-RED-{obj.track_id}-{int(now)}"
                viol = {
                    "violation_id": v_id,
                    "type": "RED_LIGHT_RUNNING",
                    "track_id": obj.track_id,
                    "vehicle_type": obj.label,
                    "lane": obj.lane,
                    "speed_kmh": obj.speed_kmh,
                    "signal_state": "RED",
                    "confidence": 0.89,
                    "timestamp": now,
                    "evidence_location": [obj.cx, obj.cy]
                }
                new_violations.append(viol)
                self.violations.append(viol)

        return new_violations
