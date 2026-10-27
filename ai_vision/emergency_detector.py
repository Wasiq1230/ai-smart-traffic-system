"""
Emergency Vehicle Detection & Priority Alert Generator.
"""

import time
from typing import List, Dict, Any, Optional
import cv2
import numpy as np

from ai_vision.tracker import TrackedObject


class EmergencyDetector:
    EMERGENCY_TYPES = ["ambulance", "fire truck", "police", "emergency"]

    def __init__(self, confidence_threshold: float = 0.65):
        self.confidence_threshold = confidence_threshold
        self.active_emergencies: Dict[int, Dict[str, Any]] = {}

    def analyze(self, frame: np.ndarray, tracked_objects: List[TrackedObject]) -> List[Dict[str, Any]]:
        detected_alerts = []
        now = time.time()

        for obj in tracked_objects:
            is_emergency = False
            em_type = "emergency"
            conf = 0.0

            if obj.label.lower() in self.EMERGENCY_TYPES:
                is_emergency = True
                em_type = obj.label.lower()
                conf = obj.conf
            elif frame is not None and frame.size > 0:
                crop = self._extract_crop(frame, obj.bbox)
                if crop is not None and crop.size > 0:
                    beacon_conf = self._check_flashing_beacon(crop)
                    if beacon_conf >= self.confidence_threshold:
                        is_emergency = True
                        em_type = "ambulance" if obj.label in ["bus", "truck"] else "police"
                        conf = beacon_conf

            if is_emergency:
                alert = {
                    "alert_id": f"EM-{obj.track_id}-{int(now)}",
                    "track_id": obj.track_id,
                    "vehicle_type": em_type,
                    "confidence": round(conf, 2),
                    "lane": obj.lane,
                    "speed_kmh": obj.speed_kmh,
                    "position": [obj.cx, obj.cy],
                    "timestamp": now,
                    "priority_status": "ACTIVE_PREEMPTION",
                    "recommended_action": f"CLEAR_{obj.lane.upper()}_CORRIDOR"
                }
                detected_alerts.append(alert)
                self.active_emergencies[obj.track_id] = alert

        active_tids = {obj.track_id for obj in tracked_objects}
        for tid in list(self.active_emergencies.keys()):
            if tid not in active_tids:
                del self.active_emergencies[tid]

        return detected_alerts

    def _extract_crop(self, frame: np.ndarray, bbox: List[float]) -> Optional[np.ndarray]:
        h, w = frame.shape[:2]
        x1 = max(0, int(bbox[0]))
        y1 = max(0, int(bbox[1]))
        x2 = min(w, int(bbox[2]))
        y2 = min(h, int(bbox[3]))
        if x2 > x1 and y2 > y1:
            return frame[y1:y2, x1:x2]
        return None

    def _check_flashing_beacon(self, crop: np.ndarray) -> float:
        h, w = crop.shape[:2]
        top_crop = crop[:int(h * 0.4), :]
        if top_crop.size == 0:
            return 0.0

        hsv = cv2.cvtColor(top_crop, cv2.COLOR_BGR2HSV)
        lower_red1 = np.array([0, 120, 120])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 120, 120])
        upper_red2 = np.array([180, 255, 255])
        mask_r = cv2.inRange(hsv, lower_red1, upper_red1) | cv2.inRange(hsv, lower_red2, upper_red2)

        lower_blue = np.array([100, 150, 120])
        upper_blue = np.array([140, 255, 255])
        mask_b = cv2.inRange(hsv, lower_blue, upper_blue)

        beacon_ratio = (np.count_nonzero(mask_r) + np.count_nonzero(mask_b)) / float(top_crop.shape[0] * top_crop.shape[1])
        if beacon_ratio > 0.08:
            return min(0.95, 0.5 + beacon_ratio * 3.0)
        return 0.0
