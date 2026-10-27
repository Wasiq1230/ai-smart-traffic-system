"""
Multimodal Traffic & Vulnerable Road User (VRU) Module.
"""

from typing import List, Dict, Any
from ai_vision.tracker import TrackedObject


class MultimodalDetector:
    def __init__(self):
        pass

    def analyze(self, tracked_objects: List[TrackedObject]) -> Dict[str, Any]:
        pedestrians = [o for o in tracked_objects if o.label.lower() in ["pedestrian", "person"]]
        cyclists = [o for o in tracked_objects if o.label.lower() in ["bicycle", "motorcycle"]]

        crosswalk_occupied = len(pedestrians) > 0
        return {
            "pedestrian_count": len(pedestrians),
            "cyclist_count": len(cyclists),
            "crosswalk_occupied": crosswalk_occupied,
            "vru_safety_clearance_required": crosswalk_occupied
        }
