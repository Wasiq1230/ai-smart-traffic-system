from typing import Dict, List, Any

class RoutingService:
    def __init__(self):
        self.topology = {
            "Northbound": ["Eastbound", "Westbound"],
            "Southbound": ["Westbound", "Eastbound"],
            "Eastbound":  ["Northbound", "Southbound"],
            "Westbound":  ["Southbound", "Northbound"]
        }

    def recommend_reroute(self, lane_congestions: Dict[str, str]) -> List[Dict[str, Any]]:
        recommendations = []
        for lane, level in lane_congestions.items():
            if level in ["HIGH", "CRITICAL"]:
                alternatives = self.topology.get(lane, [])
                best_alt = None
                for alt in alternatives:
                    if lane_congestions.get(alt, "LOW") in ["LOW", "MEDIUM"]:
                        best_alt = alt
                        break

                if best_alt:
                    recommendations.append({
                        "origin_lane": lane,
                        "current_congestion": level,
                        "recommended_detour": best_alt,
                        "detour_congestion": lane_congestions.get(best_alt, "LOW"),
                        "estimated_time_saving_min": 4.5 if level == "HIGH" else 8.0,
                        "confidence": 0.85,
                        "is_simulated": True
                    })
        return recommendations
