import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import init_db, SessionLocal
from backend.models import User, Intersection

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    init_db()

@pytest.fixture
def client():
    return TestClient(app)

def test_health_endpoint(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert data["subsystems"]["database"] == "CONNECTED"

def test_traffic_current_endpoint(client):
    response = client.get("/api/v1/traffic/current")
    assert response.status_code == 200
    data = response.json()
    assert "lanes" in data

def test_signals_endpoint(client):
    response = client.get("/api/v1/signals")
    assert response.status_code == 200
    data = response.json()
    assert "signal_states" in data

def test_forecast_endpoint(client):
    response = client.get("/api/v1/forecast")
    assert response.status_code == 200
    data = response.json()
    assert len(data["horizons"]) == 4

def test_analytics_endpoint(client):
    response = client.get("/api/v1/analytics")
    assert response.status_code == 200
    data = response.json()
    assert "environmental_impact" in data

def test_auth_login(client):
    response = client.post("/api/v1/auth/login", json={"username": "admin", "password": "admin123"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["role"] == "ADMIN"
