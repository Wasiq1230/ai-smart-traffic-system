# System Architecture

The AI Smart Traffic Management System implements a closed-loop reactive architecture:

```
PERCEIVE ──► UNDERSTAND ──► PREDICT ──► DECIDE ──► ACT ──► MONITOR ──► LEARN
```

## Layer Overview
1. **Perception (AI Vision)**: Video ingestion, YOLO vehicle detection, multi-object IoU tracking, lane assignment, and ANPR.
2. **Understanding (Traffic Intelligence)**: PCU-weighted density, composite congestion classification, and incident lifecycle management.
3. **Prediction (ML Forecasting)**: Multi-horizon (5, 10, 15, 30 min) predictions with empirical uncertainty intervals.
4. **Decision (Signal Control)**: Dynamic green time optimization bounded by mandatory Safety Validator rules.
5. **Action & Preemption**: Emergency corridor green preemption and alternative route guidance.
6. **Persistence & API**: SQLAlchemy ORM (14 models), versioned REST API (`/api/v1/`), and real-time WebSockets.
7. **Presentation**: React + Tailwind live dashboard with SVG intersection visualizer.
