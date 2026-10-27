"""
Lane Assignment & Intersection Geometry Detector.
"""

from typing import Dict, List, Tuple, Any, Optional
from ai_vision.utils import is_point_in_polygon
from ai_vision.tracker import TrackedObject
from ai_vision.config import DEFAULT_LANE_POLYGONS


class LaneDetector:
    def __init__(self, lane_polygons: Optional[Dict[str, List[Tuple[int, int]]]] = None):
        self.lane_polygons = lane_polygons or DEFAULT_LANE_POLYGONS

    def assign_lanes(self, tracked_objects: List[TrackedObject]) -> Dict[str, Any]:
        lane_assignments: Dict[str, List[TrackedObject]] = {lane: [] for lane in self.lane_polygons}
        unassigned: List[TrackedObject] = []

        for obj in tracked_objects:
            assigned = False
            point = (float(obj.cx), float(obj.cy))
            for lane_name, polygon in self.lane_polygons.items():
                if is_point_in_polygon(point, polygon):
                    obj.lane = lane_name
                    lane_assignments[lane_name].append(obj)
                    assigned = True
                    break
            if not assigned:
                obj.lane = "Unassigned"
                unassigned.append(obj)

        lane_stats = {}
        for lane_name, objs in lane_assignments.items():
            speeds = [o.speed_kmh for o in objs]
            stopped = sum(1 for o in objs if o.is_stopped)
            lane_stats[lane_name] = {
                "vehicle_count": len(objs),
                "stopped_vehicles": stopped,
                "avg_speed_kmh": round(sum(speeds) / len(speeds), 1) if speeds else 45.0,
                "queue_length_meters": stopped * 6.5,
                "density_score": min(1.0, len(objs) / 10.0),
                "vehicles": [o.to_dict() for o in objs]
            }

        return {
            "lanes": lane_stats,
            "unassigned_count": len(unassigned)
        }
