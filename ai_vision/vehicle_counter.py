"""
Unique Vehicle Counter and Classification Aggregator.
"""

from typing import Dict, List, Set, Any
from ai_vision.tracker import TrackedObject


class VehicleCounter:
    def __init__(self):
        self.seen_track_ids: Set[int] = set()
        self.type_counts: Dict[str, int] = {
            "car": 0,
            "bus": 0,
            "truck": 0,
            "motorcycle": 0,
            "pedestrian": 0,
            "bicycle": 0
        }
        self.lane_cumulative_counts: Dict[str, int] = {}
        self.total_unique_vehicles = 0

    def update(self, tracked_objects: List[TrackedObject]) -> Dict[str, Any]:
        for obj in tracked_objects:
            if obj.track_id not in self.seen_track_ids:
                self.seen_track_ids.add(obj.track_id)
                self.total_unique_vehicles += 1
                lbl = obj.label.lower()
                self.type_counts[lbl] = self.type_counts.get(lbl, 0) + 1

                lane = obj.lane
                if lane and lane != "Unassigned":
                    self.lane_cumulative_counts[lane] = self.lane_cumulative_counts.get(lane, 0) + 1

        active_type_counts = {}
        for obj in tracked_objects:
            lbl = obj.label.lower()
            active_type_counts[lbl] = active_type_counts.get(lbl, 0) + 1

        return {
            "active_vehicle_count": len(tracked_objects),
            "total_unique_count": self.total_unique_vehicles,
            "active_by_type": active_type_counts,
            "cumulative_by_type": self.type_counts.copy(),
            "cumulative_by_lane": self.lane_cumulative_counts.copy()
        }
