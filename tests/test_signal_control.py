import pytest
from signal_control.safety import SafetyValidator
from signal_control.emergency_priority import EmergencyPriorityManager
from signal_control.signal_engine import SignalEngine
from signal_control.dqn_simulation import DQNSimulation

def test_safety_validator_bounds():
    sv = SafetyValidator()
    raw = {"Northbound": 80, "Southbound": 5, "Eastbound": 25, "Westbound": 30}
    ok, msg, adjusted = sv.validate_plan(raw, "Northbound", starvation_counters={"Northbound": 0})
    assert ok is True
    assert adjusted["Northbound"] <= sv.MAX_GREEN_SEC
    assert adjusted["Southbound"] >= sv.MIN_GREEN_SEC

def test_safety_validator_starvation():
    sv = SafetyValidator()
    raw = {"Northbound": 30, "Southbound": 10, "Eastbound": 10, "Westbound": 10}
    starvation = {"Northbound": 0, "Southbound": 4, "Eastbound": 0, "Westbound": 0}
    ok, msg, adjusted = sv.validate_plan(raw, "Northbound", starvation)
    assert ok is True
    assert adjusted["Southbound"] >= sv.MIN_GREEN_SEC + 5

def test_emergency_preemption():
    epm = EmergencyPriorityManager()
    alert = {"alert_id": "EM-101", "vehicle_type": "ambulance", "lane": "Eastbound"}
    plan = epm.request_priority(alert)
    assert plan["green_lane"] == "Eastbound"
    assert plan["is_emergency_override"] is True
    assert epm.active_preemption is not None
    epm.clear_preemption()
    assert epm.active_preemption is None

def test_signal_engine_adaptive():
    se = SignalEngine()
    densities = {"Northbound": 0.8, "Southbound": 0.3, "Eastbound": 0.2, "Westbound": 0.2}
    decision = se.compute_optimal_timings(densities)
    assert decision["active_green_lane"] == "Northbound"
    assert decision["signal_states"]["Northbound"] == "GREEN"
    assert decision["signal_states"]["Eastbound"] == "RED"
    assert decision["safety_status"] == "SAFETY_PASSED"

def test_dqn_simulation_benchmark():
    bm = DQNSimulation.get_benchmark_comparison()
    assert bm["status"] == "SIMULATED_BENCHMARK_PROJECTION"
    assert "adaptive_delay_reduction_pct" in bm["metrics"]
