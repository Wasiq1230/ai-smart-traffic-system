from typing import Dict, List, Any

PCU_FACTORS = {
    "car": 1.0,
    "bus": 2.5,
    "truck": 2.0,
    "motorcycle": 0.5,
    "pedestrian": 0.2,
    "bicycle": 0.3
}

class DensityCalculator:
    def __init__(self, lane_capacity_pcu: float = 25.0):
        self.lane_capacity_pcu = lane_capacity_pcu

    def calculate_lane_density(self, vehicles: List[Dict[str, Any]], lane_length_meters: float = 150.0) -> Dict[str, Any]:
        total_pcu = 0.0
        stopped_pcu = 0.0
        type_breakdown: Dict[str, int] = {}

        for v in vehicles:
            lbl = v.get("label", "car").lower()
            factor = PCU_FACTORS.get(lbl, 1.0)
            total_pcu += factor
            type_breakdown[lbl] = type_breakdown.get(lbl, 0) + 1
            if v.get("is_stopped", False):
                stopped_pcu += factor

        density_score = min(1.0, total_pcu / max(1.0, self.lane_capacity_pcu))
        queue_meters = stopped_pcu * 6.5

        return {
            "total_vehicles": len(vehicles),
            "total_pcu": round(total_pcu, 1),
            "stopped_pcu": round(stopped_pcu, 1),
            "density_score": round(density_score, 3),
            "queue_meters": round(queue_meters, 1),
            "type_breakdown": type_breakdown
        }
