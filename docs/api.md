# REST API & WebSocket Specification

## Base URL
`http://localhost:8000/api/v1`

## Key Endpoints
- `GET /health`: Overall system health and subsystem status.
- `POST /auth/login`: Authenticate and obtain JWT access token.
- `POST /auth/register`: Register operator account.
- `GET /traffic/current`: Current live density, speed, queue lengths, and congestion status.
- `GET /traffic/history`: Historical traffic measurements.
- `GET /signals`: Current adaptive signal phase states and green durations.
- `POST /signals/optimize`: Trigger adaptive signal re-evaluation.
- `GET /forecast`: Multi-horizon traffic predictions (+5, +10, +15, +30 min).
- `GET /emergency`: Logged emergency vehicle alerts and preemption records.
- `POST /emergency/priority`: Request manual or automated green corridor preemption.
- `GET /accidents`: Active and resolved traffic incidents.
- `POST /accidents/{id}/resolve`: Resolve an active incident.
- `GET /violations`: Speeding and red-light violation logs.
- `GET /analytics`: Aggregated throughput and environmental impact statistics.
- `GET /detection/status`: Vision pipeline frame count, FPS, and model backend.

## WebSocket Real-Time Stream
- `WS /ws/traffic`: Emits `traffic_update` JSON packets every second.
