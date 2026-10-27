import pytest
from traffic.density import DensityCalculator
from traffic.congestion import CongestionAnalyzer
from traffic.incident import IncidentManager
from traffic.routing import RoutingService
from traffic.environmental import EnvironmentalEstimator
from traffic.traffic_engine import TrafficEngine

def test_density_calculator():
    dc = DensityCalculator(lane_capacity_pcu=20.0)
    vehicles = [
        {"label": "car", "is_stopped": False},
        {"label": "bus", "is_stopped": True},  # 2.5 PCU
        {"label": "motorcycle", "is_stopped": False}  # 0.5 PCU
    ]
    res = dc.calculate_lane_density(vehicles)
    assert res["total_vehicles"] == 3
    assert res["total_pcu"] == 4.0
    assert res["stopped_pcu"] == 2.5
    assert res["density_score"] == 0.2

def test_congestion_analyzer():
    ca = CongestionAnalyzer(free_flow_speed_kmh=50.0)
    level_low, idx_low = ca.evaluate_lane(density_score=0.1, avg_speed_kmh=48.0, queue_meters=0.0)
    assert level_low == "LOW"
    
    level_crit, idx_crit = ca.evaluate_lane(density_score=0.9, avg_speed_kmh=10.0, queue_meters=80.0)
    assert level_crit in ["HIGH", "CRITICAL"]

def test_environmental_estimator():
    ee = EnvironmentalEstimator()
    res = ee.calculate(total_vehicles_served=1000, avg_delay_reduction_seconds=15.0)
    assert res["total_vehicles_served"] == 1000
    assert res["is_estimate"] is True
    assert res["estimated_fuel_saved_liters"] > 0
    assert res["estimated_co2_reduced_kg"] > 0

def test_routing_service():
    rs = RoutingService()
    congestions = {"Northbound": "CRITICAL", "Eastbound": "LOW", "Westbound": "LOW", "Southbound": "MEDIUM"}
    routes = rs.recommend_reroute(congestions)
    assert len(routes) >= 1
    assert routes[0]["origin_lane"] == "Northbound"
    assert routes[0]["is_simulated"] is True

def test_traffic_engine():
    te = TrafficEngine()
    vision_mock = {
        "lane_analytics": {
            "Northbound": {"vehicles": [{"label": "car", "is_stopped": False} for _ in range(5)], "avg_speed_kmh": 45.0},
            "Southbound": {"vehicles": [{"label": "bus", "is_stopped": True} for _ in range(3)], "avg_speed_kmh": 20.0}
        },
        "accidents": [],
        "total_unique_count": 8
    }
    res = te.process_vision_data(vision_mock)
    assert res["intersection_id"] == "INT-001"
    assert "Northbound" in res["lanes"]
    assert "environmental_impact" in res
