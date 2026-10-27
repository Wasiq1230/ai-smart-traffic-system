from fastapi import APIRouter
from typing import Optional, Dict, Any
from backend.services.traffic_service import master_traffic_service
from backend.schemas import SignalOptimizeRequest, SignalStateOut

router = APIRouter(prefix="/signals", tags=["Adaptive Signals"])

@router.get("")
@router.get("/status/{intersection_id}")
@router.get("/{intersection_id}")
def get_current_signals(intersection_id: str = "INT-001"):
    if master_traffic_service.last_state:
        return master_traffic_service.last_state.get("signals", {})
    return master_traffic_service.signal_engine.compute_optimal_timings(
        lane_densities={"Northbound": 0.4, "Southbound": 0.6, "Eastbound": 0.25, "Westbound": 0.3}
    )

@router.post("/optimize")
@router.post("/calculate")
def optimize_signals(req: Optional[SignalOptimizeRequest] = None):
    return master_traffic_service.signal_engine.compute_optimal_timings(
        lane_densities={"Northbound": 0.5, "Southbound": 0.8, "Eastbound": 0.3, "Westbound": 0.35}
    )

@router.post("/advance-phase")
def advance_phase():
    return master_traffic_service.signal_engine.compute_optimal_timings(
        lane_densities={"Northbound": 0.3, "Southbound": 0.3, "Eastbound": 0.7, "Westbound": 0.6}
    )
