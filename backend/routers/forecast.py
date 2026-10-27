from fastapi import APIRouter
from backend.services.traffic_service import master_traffic_service

router = APIRouter(prefix="/forecast", tags=["ML Forecasting"])

@router.get("")
@router.get("/{intersection_id}")
def get_traffic_forecast(intersection_id: str = "INT-001"):
    if master_traffic_service.last_state:
        return master_traffic_service.last_state.get("forecast", {})
    return master_traffic_service.forecaster.forecast(intersection_id=intersection_id)
