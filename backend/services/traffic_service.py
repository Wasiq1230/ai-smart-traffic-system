from typing import Dict, Any, List
from traffic.traffic_engine import TrafficEngine
from signal_control.signal_engine import SignalEngine
from ml.inference.forecaster import TrafficForecaster

class MasterTrafficService:
    def __init__(self):
        self.traffic_engine = TrafficEngine(intersection_id="INT-001")
        self.signal_engine = SignalEngine(intersection_id="INT-001")
        self.forecaster = TrafficForecaster()
        self.last_state: Dict[str, Any] = {}

    def process_vision_payload(self, vision_payload: Dict[str, Any]) -> Dict[str, Any]:
        traffic_info = self.traffic_engine.process_vision_data(vision_payload)
        
        lane_densities = {
            lane: data["density_score"] 
            for lane, data in traffic_info["lanes"].items()
        }
        
        lane_counts = {
            lane: data["vehicle_count"] 
            for lane, data in traffic_info["lanes"].items()
        }
        forecast_info = self.forecaster.forecast(lane_counts, intersection_id="INT-001")
        
        forecast_densities = {
            lane: f_data["predicted_density_5min"]
            for lane, f_data in forecast_info["lane_forecasts"].items()
        }
        
        signal_decision = self.signal_engine.compute_optimal_timings(
            lane_densities=lane_densities,
            forecast_densities=forecast_densities,
            emergency_alerts=vision_payload.get("emergency_alerts", [])
        )
        
        combined_payload = {
            "traffic": traffic_info,
            "signals": signal_decision,
            "forecast": forecast_info,
            "violations": vision_payload.get("violations", []),
            "accidents": vision_payload.get("accidents", []),
            "emergency_alerts": vision_payload.get("emergency_alerts", []),
            "system_health": vision_payload.get("system_health", {"status": "HEALTHY", "fps": 15.0})
        }
        self.last_state = combined_payload
        return combined_payload

master_traffic_service = MasterTrafficService()
