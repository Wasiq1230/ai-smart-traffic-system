"""
Accident & Incident Detection Module.
"""

import time
from typing import List, Dict, Any
from ai_vision.tracker import TrackedObject
from ai_vision.utils import calculate_iou


class AccidentDetector:
    def __init__(self, stop_time_threshold: float = 6.0, overlap_iou_thresh: float = 0.25):
        self.stop_time_threshold = stop_time_threshold
        self.overlap_iou_thresh = overlap_iou_thresh
        self.incidents: Dict[str, Dict[str, Any]] = {}

    def detect(self, tracked_objects: List[TrackedObject]) -> List[Dict[str, Any]]:
        detected = []
        now = time.time()

        for obj in tracked_objects:
            if obj.is_stopped and obj.stopped_duration >= self.stop_time_threshold:
                inc_id = f"INC-STOP-{obj.track_id}"
                incident = {
                    "incident_id": inc_id,
                    "type": "STATIONARY_VEHICLE_OBSTRUCTION",
                    "severity": "HIGH" if obj.stopped_duration > 15.0 else "MEDIUM",
                    "status": "CONFIRMED" if obj.stopped_duration > 10.0 else "SUSPECTED",
                    "lane": obj.lane,
                    "track_ids": [obj.track_id],
                    "duration_sec": round(obj.stopped_duration, 1),
                    "location": [obj.cx, obj.cy],
                    "confidence": 0.88,
                    "timestamp": now,
                    "description": f"Vehicle {obj.track_id} stopped for {round(obj.stopped_duration, 1)}s in {obj.lane}"
                }
                detected.append(incident)
                self.incidents[inc_id] = incident

        n = len(tracked_objects)
        for i in range(n):
            for j in range(i + 1, n):
                v1 = tracked_objects[i]
                v2 = tracked_objects[j]
                iou = calculate_iou(v1.bbox, v2.bbox)
                if iou > self.overlap_iou_thresh and (v1.is_stopped or v2.is_stopped):
                    inc_id = f"INC-COL-{min(v1.track_id, v2.track_id)}-{max(v1.track_id, v2.track_id)}"
                    incident = {
                        "incident_id": inc_id,
                        "type": "POTENTIAL_COLLISION_OVERLAP",
                        "severity": "CRITICAL",
                        "status": "CONFIRMED",
                        "lane": v1.lane,
                        "track_ids": [v1.track_id, v2.track_id],
                        "duration_sec": max(v1.stopped_duration, v2.stopped_duration),
                        "location": [int((v1.cx + v2.cx) / 2), int((v1.cy + v2.cy) / 2)],
                        "confidence": 0.92,
                        "timestamp": now,
                        "description": f"Collision overlap (IoU {iou:.2f}) between vehicle {v1.track_id} and {v2.track_id}"
                    }
                    detected.append(incident)
                    self.incidents[inc_id] = incident

        return detected
