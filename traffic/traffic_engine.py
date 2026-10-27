import time
from typing import Dict, Any, List, Optional

from traffic.density import DensityCalculator
from traffic.congestion import CongestionAnalyzer
from traffic.incident import IncidentManager
from traffic.routing import RoutingService
from traffic.environmental import EnvironmentalEstimator

class TrafficEngine:
    def __init__(self, intersection_id: str = "INT-001"):
        self.intersection_id = intersection_id
        self.density_calc = DensityCalculator()
        self.congestion_calc = CongestionAnalyzer()
        self.incident_mgr = IncidentManager()
        self.routing_svc = RoutingService()
        self.env_estimator = EnvironmentalEstimator()

    def process_vision_data(self, vision_data: Dict[str, Any]) -> Dict[str, Any]:
        lane_analytics = vision_data.get("lane_analytics", {})
        processed_lanes = {}
        lane_congestions = {}
        total_pcu_sum = 0.0
        total_vehicles_active = 0

        for lane_name, l_data in lane_analytics.items():
            vehicles = l_data.get("vehicles", [])
            avg_speed = l_data.get("avg_speed_kmh", 45.0)

            density_info = self.density_calc.calculate_lane_density(vehicles)
            total_pcu_sum += density_info["total_pcu"]
            total_vehicles_active += density_info["total_vehicles"]

            level, c_index = self.congestion_calc.evaluate_lane(
                density_info["density_score"],
                avg_speed,
                density_info["queue_meters"]
            )
            lane_congestions[lane_name] = level

            processed_lanes[lane_name] = {
                "vehicle_count": density_info["total_vehicles"],
                "pcu_count": density_info["total_pcu"],
                "density_score": density_info["density_score"],
                "queue_length_meters": density_info["queue_meters"],
                "avg_speed_kmh": avg_speed,
                "congestion_level": level,
                "congestion_index": c_index
            }

        for inc in vision_data.get("accidents", []):
            self.incident_mgr.register_or_update(inc)

        detour_recommendations = self.routing_svc.recommend_reroute(lane_congestions)
        env_impact = self.env_estimator.calculate(
            total_vehicles_served=vision_data.get("total_unique_count", total_vehicles_active)
        )

        overall_density = min(1.0, total_pcu_sum / 80.0)
        overall_congestion = "CRITICAL" if any(c == "CRITICAL" for c in lane_congestions.values()) else (
            "HIGH" if any(c == "HIGH" for c in lane_congestions.values()) else (
                "MEDIUM" if any(c == "MEDIUM" for c in lane_congestions.values()) else "LOW"
            )
        )

        return {
            "intersection_id": self.intersection_id,
            "timestamp": time.time(),
            "overall_congestion": overall_congestion,
            "overall_density": round(overall_density, 3),
            "total_active_vehicles": total_vehicles_active,
            "total_pcu": round(total_pcu_sum, 1),
            "lanes": processed_lanes,
            "active_incidents": self.incident_mgr.get_active(),
            "routing_recommendations": detour_recommendations,
            "environmental_impact": env_impact
        }
