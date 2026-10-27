# AI Smart Traffic Management System

A production-grade, modular, and real-time AI Smart Traffic Management System integrating computer vision, traffic intelligence, ML forecasting, and safety-verified adaptive signal control.

---

## Key Features
- **AI Vision Pipeline**: YOLOv8 vehicle detection, IoU tracking, lane assignment, and ANPR plate recognition.
- **Traffic Intelligence**: PCU-weighted density, composite congestion levels (LOW, MEDIUM, HIGH, CRITICAL).
- **ML Forecasting**: 5, 10, 15, and 30-minute horizons with 95% confidence intervals.
- **Adaptive Signals**: Density and prediction-assisted signal timing with a strict **Safety Validator** (conflict matrix, min/max green, all-red, starvation prevention).
- **Emergency Priority**: Automatic green corridor preemption for ambulances, fire trucks, and police.
- **Incident & Violation Detection**: Stationary vehicle detection, collision risk, speeding, and red-light violations.
- **Environmental Analytics**: Estimated fuel savings and CO₂ reduction metrics.
- **Interactive UI**: Real-time React + Tailwind dashboard with SVG intersection visualizer and WebSockets.

---

## Quick Start

### 1. Run the Backend & Live Dashboard
```bash
cd ai_smart_traffic_system
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
Open [http://localhost:8000](http://localhost:8000) in your browser.

### 2. Run the 5-Scenario Interactive Demo
```bash
python scripts/run_demo_scenarios.py
```

### 3. Run Automated Tests
```bash
python -m pytest tests/ -v
```

---

## AI/ML Honest Disclosures
- **Pretrained Weights**: `yolov8n.pt` is pretrained on MS-COCO.
- **Synthetic Datasets**: `traffic_history.csv` is synthetic historical data, not physical sensor measurements.
- **Environmental Metrics**: Fuel savings and CO₂ reductions are calculated estimates.
- **DQN Model**: Labeled as a simulated benchmark extension.
