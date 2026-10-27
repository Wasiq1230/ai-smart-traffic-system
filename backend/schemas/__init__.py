from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    username: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None
    role: Optional[str] = "OPERATOR"

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str]
    role: str
    is_active: bool

class LaneTrafficOut(BaseModel):
    vehicle_count: int
    pcu_count: float
    density_score: float
    queue_length_meters: float
    avg_speed_kmh: float
    congestion_level: str
    congestion_index: float

class LiveTrafficResponse(BaseModel):
    intersection_id: str
    timestamp: float
    overall_congestion: str
    overall_density: float
    total_active_vehicles: int
    total_pcu: float
    lanes: Dict[str, LaneTrafficOut]
    active_incidents: List[Dict[str, Any]]
    routing_recommendations: List[Dict[str, Any]]
    environmental_impact: Dict[str, Any]

class SignalStateOut(BaseModel):
    intersection_id: str
    active_green_lane: str
    allocated_green_seconds: int
    yellow_seconds: int = 3
    all_red_seconds: int = 2
    signal_states: Dict[str, str]
    safety_status: str
    is_emergency_active: bool = False
    reason: Optional[str] = None

class SignalOptimizeRequest(BaseModel):
    intersection_id: str = "INT-001"
    force_lane: Optional[str] = None

class ForecastHorizonOut(BaseModel):
    horizon_minutes: int
    predicted_timestamp: float
    predicted_vehicle_count: float
    lower_bound_95: float
    upper_bound_95: float
    predicted_density: float
    predicted_congestion: str
    confidence_score: float

class ForecastResponse(BaseModel):
    intersection_id: str
    generated_at: float
    model_version: str
    metrics: Dict[str, Any]
    data_source_type: str
    horizons: List[ForecastHorizonOut]
    lane_forecasts: Dict[str, Any]

class EmergencyAlertCreate(BaseModel):
    intersection_id: str = "INT-001"
    vehicle_type: str = "ambulance"
    approach_lane: str = "Northbound"
    confidence: float = 0.95

class EmergencyAlertOut(BaseModel):
    alert_id: str
    vehicle_type: str
    lane: str
    confidence: float
    priority_status: str
    recommended_action: str

class IncidentCreate(BaseModel):
    intersection_id: str = "INT-001"
    incident_type: str
    severity: str = "MEDIUM"
    lane: Optional[str] = "Northbound"
    description: Optional[str] = None

class IncidentOut(BaseModel):
    incident_id: str
    type: str
    severity: str
    status: str
    lane: Optional[str]
    description: Optional[str]
    confidence: float

class ViolationOut(BaseModel):
    violation_id: str
    type: str
    track_id: int
    vehicle_type: str
    lane: Optional[str]
    speed_kmh: Optional[float]
    confidence: float
    timestamp: float
