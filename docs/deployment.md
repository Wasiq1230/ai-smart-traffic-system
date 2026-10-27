# Deployment Guide

## Standalone Local Deployment
```bash
cd ai_smart_traffic_system
python -m pip install -r requirements.txt
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

## Docker Deployment
```bash
docker-compose up --build -d
```
