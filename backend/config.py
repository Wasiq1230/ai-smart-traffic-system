import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Smart Traffic Management System"
    VERSION: str = "2.0.0"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: List[str] = ["*"]
    DATABASE_URL: str = "sqlite:///./data/db/traffic.db"
    SECRET_KEY: str = "antigravity-ai-traffic-production-secret-key-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    SAMPLE_VIDEO_PATH: str = "./data/videos/sample_traffic_640x480.mp4"
    YOLO_MODEL_PATH: str = "./models/yolov8n.pt"
    LSTM_WEIGHTS_PATH: str = "./models/lstm_traffic_weights.json"
    DEFAULT_INTERSECTION_ID: str = "INT-001"
    DEFAULT_INTERSECTION_NAME: str = "Grand Central & 5th Ave"
    LANE_CAPACITY: int = 25
    SPEED_LIMIT_KMH: float = 60.0

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
