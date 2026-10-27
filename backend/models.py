from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Index
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Intersection(Base):
    __tablename__ = "intersections"
    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    num_lanes = Column(Integer, default=4)
    lane_config = Column(Text, nullable=True)
    signal_config = Column(Text, nullable=True)
    status = Column(String(20), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

    lanes = relationship("Lane", back_populates="intersection", cascade="all, delete-orphan")
    cameras = relationship("Camera", back_populates="intersection")
    measurements = relationship("TrafficMeasurement", back_populates="intersection")
    signal_states = relationship("SignalState", back_populates="intersection")

class Lane(Base):
    __tablename__ = "lanes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    intersection_id = Column(String(50), ForeignKey("intersections.id"), nullable=False)
    lane_name = Column(String(50), nullable=False)
    direction = Column(String(20), nullable=False)
    speed_limit_kmh = Column(Float, default=60.0)
    polygon_coords = Column(Text, nullable=True)
    intersection = relationship("Intersection", back_populates="lanes")

class Camera(Base):
    __tablename__ = "cameras"
    id = Column(String(50), primary_key=True)
    intersection_id = Column(String(50), ForeignKey("intersections.id"), nullable=False)
    camera_name = Column(String(100), nullable=False)
    rtsp_url = Column(String(255), nullable=True)
    status = Column(String(20), default="ONLINE")
    intersection = relationship("Intersection", back_populates="cameras")

class Detection(Base):
    __tablename__ = "detections"
    id = Column(Integer, primary_key=True, autoincrement=True)
    intersection_id = Column(String(50), nullable=False)
    frame_number = Column(Integer, default=0)
    object_class = Column(String(30), nullable=False)
    confidence = Column(Float, nullable=False)
    bbox_x1 = Column(Float, nullable=False)
    bbox_y1 = Column(Float, nullable=False)
    bbox_x2 = Column(Float, nullable=False)
    bbox_y2 = Column(Float, nullable=False)
    track_id = Column(Integer, nullable=True)
    lane_assigned = Column(String(50), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

class VehicleTrack(Base):
    __tablename__ = "vehicle_tracks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    track_id = Column(Integer, nullable=False)
    intersection_id = Column(String(50), nullable=False)
    vehicle_class = Column(String(30), nullable=False)
    avg_speed_kmh = Column(Float, default=0.0)
    lane = Column(String(50), nullable=True)
    direction = Column(String(20), nullable=True)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)

class TrafficMeasurement(Base):
    __tablename__ = "traffic_measurements"
    id = Column(Integer, primary_key=True, autoincrement=True)
    intersection_id = Column(String(50), ForeignKey("intersections.id"), nullable=False, index=True)
    lane_name = Column(String(50), nullable=False)
    vehicle_count = Column(Integer, default=0)
    pcu_count = Column(Float, default=0.0)
    density_score = Column(Float, default=0.0)
    congestion_level = Column(String(20), default="LOW")
    avg_speed_kmh = Column(Float, default=45.0)
    queue_length_meters = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    intersection = relationship("Intersection", back_populates="measurements")

class Forecast(Base):
    __tablename__ = "forecasts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    intersection_id = Column(String(50), nullable=False, index=True)
    horizon_minutes = Column(Integer, nullable=False)
    predicted_vehicle_count = Column(Float, nullable=False)
    predicted_density = Column(Float, nullable=False)
    predicted_congestion = Column(String(20), default="LOW")
    confidence_score = Column(Float, default=0.90)
    model_version = Column(String(50), default="v2.1")
    generated_at = Column(DateTime, default=datetime.utcnow)

class SignalState(Base):
    __tablename__ = "signal_states"
    id = Column(Integer, primary_key=True, autoincrement=True)
    intersection_id = Column(String(50), ForeignKey("intersections.id"), nullable=False, index=True)
    active_lane = Column(String(50), nullable=False)
    north_state = Column(String(10), default="RED")
    south_state = Column(String(10), default="RED")
    east_state = Column(String(10), default="RED")
    west_state = Column(String(10), default="RED")
    green_duration_sec = Column(Integer, default=30)
    is_emergency_preemption = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    intersection = relationship("Intersection", back_populates="signal_states")

class SignalDecision(Base):
    __tablename__ = "signal_decisions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    intersection_id = Column(String(50), nullable=False)
    selected_lane = Column(String(50), nullable=False)
    green_time_sec = Column(Integer, nullable=False)
    decision_mode = Column(String(50), default="ADAPTIVE")
    reason = Column(Text, nullable=True)
    safety_status = Column(String(50), default="SAFETY_PASSED")
    timestamp = Column(DateTime, default=datetime.utcnow)

class EmergencyEvent(Base):
    __tablename__ = "emergency_events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    alert_id = Column(String(50), unique=True, nullable=False)
    intersection_id = Column(String(50), nullable=False)
    vehicle_type = Column(String(50), default="ambulance")
    approach_lane = Column(String(50), nullable=False)
    confidence = Column(Float, default=0.95)
    preemption_status = Column(String(30), default="ACTIVE")
    timestamp = Column(DateTime, default=datetime.utcnow)

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True, autoincrement=True)
    incident_id = Column(String(50), unique=True, nullable=False)
    intersection_id = Column(String(50), nullable=False)
    incident_type = Column(String(50), nullable=False)
    severity = Column(String(20), default="MEDIUM")
    status = Column(String(20), default="CONFIRMED")
    lane = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Violation(Base):
    __tablename__ = "violations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    violation_id = Column(String(50), unique=True, nullable=False)
    intersection_id = Column(String(50), nullable=False)
    violation_type = Column(String(50), nullable=False)
    vehicle_type = Column(String(30), default="car")
    lane = Column(String(50), nullable=True)
    speed_kmh = Column(Float, nullable=True)
    evidence_image_path = Column(String(255), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    role = Column(String(20), default="OPERATOR")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class AuditEvent(Base):
    __tablename__ = "audit_events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    action = Column(String(100), nullable=False)
    user_id = Column(Integer, nullable=True)
    username = Column(String(50), nullable=True)
    details = Column(Text, nullable=True)
    ip_address = Column(String(50), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class SystemMetric(Base):
    __tablename__ = "system_metrics"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cpu_percent = Column(Float, default=0.0)
    memory_percent = Column(Float, default=0.0)
    vision_fps = Column(Float, default=0.0)
    active_ws_connections = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)
