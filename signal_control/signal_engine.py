import time
from typing import Dict, Any, List, Optional

from signal_control.safety import SafetyValidator
from signal_control.emergency_priority import EmergencyPriorityManager

class SignalEngine:
    def __init__(self, intersection_id: str = "INT-001"):
        self.intersection_id = intersection_id
        self.safety_validator = SafetyValidator()
        self.emergency_mgr = EmergencyPriorityManager()
        self.lanes = ["Northbound", "Southbound", "Eastbound", "Westbound"]
        self.current_phase_index = 0
        self.current_signal_states = {lane: "RED" for lane in self.lanes}
        self.current_signal_states["Northbound"] = "GREEN"
        self.starvation_counters = {lane: 0 for lane in self.lanes}
        self.last_phase_change = time.time()
        self.current_green_duration = 25

    def compute_optimal_timings(
        self,
        lane_densities: Dict[str, float],
        forecast_densities: Optional[Dict[str, float]] = None,
        emergency_alerts: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        now = time.time()

        if emergency_alerts:
            em = emergency_alerts[0]
            preempt_plan = self.emergency_mgr.request_priority(em)
            target_lane = preempt_plan["green_lane"]

            signals = {l: "RED" for l in self.lanes}
            signals[target_lane] = "GREEN"
            self.current_signal_states = signals

            return {
                "intersection_id": self.intersection_id,
                "mode": "EMERGENCY_PREEMPTION",
                "active_green_lane": target_lane,
                "allocated_green_seconds": 30,
                "yellow_seconds": 3,
                "all_red_seconds": 2,
                "signal_states": signals,
                "safety_status": "SAFETY_PASSED_EMERGENCY_OVERRIDE",
                "is_emergency_active": True,
                "reason": f"Emergency Priority Corridor granted to {em.get('vehicle_type', 'emergency')}"
            }

        if self.emergency_mgr.active_preemption:
            self.emergency_mgr.clear_preemption()

        raw_allocations = {}
        total_d = sum(lane_densities.get(l, 0.2) for l in self.lanes) or 1.0

        for lane in self.lanes:
            current_d = lane_densities.get(lane, 0.2)
            forecast_d = forecast_densities.get(lane, current_d) if forecast_densities else current_d
            combined_weight = 0.65 * current_d + 0.35 * forecast_d

            allocated_sec = int(15 + (combined_weight / total_d) * 45)
            raw_allocations[lane] = allocated_sec

        best_lane = max(self.lanes, key=lambda l: lane_densities.get(l, 0.0) + (0.1 * self.starvation_counters.get(l, 0)))

        ok, msg, safe_allocations = self.safety_validator.validate_plan(
            raw_allocations,
            best_lane,
            self.starvation_counters
        )

        for l in self.lanes:
            if l == best_lane:
                self.starvation_counters[l] = 0
            else:
                self.starvation_counters[l] += 1

        signals = {l: "RED" for l in self.lanes}
        signals[best_lane] = "GREEN"
        self.current_signal_states = signals
        self.current_green_duration = safe_allocations[best_lane]
        self.last_phase_change = now

        return {
            "intersection_id": self.intersection_id,
            "mode": "ADAPTIVE_DENSITY_FORECAST",
            "active_green_lane": best_lane,
            "allocated_green_seconds": safe_allocations[best_lane],
            "lane_green_allocations": safe_allocations,
            "yellow_seconds": 3,
            "all_red_seconds": 2,
            "signal_states": signals,
            "safety_status": msg,
            "is_emergency_active": False,
            "reason": f"Allocated {safe_allocations[best_lane]}s green to {best_lane} (Density: {lane_densities.get(best_lane, 0):.2f})"
        }
