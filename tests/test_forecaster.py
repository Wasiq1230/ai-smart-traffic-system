import pytest
from ml.inference.forecaster import TrafficForecaster
from ml.evaluation.metrics import evaluate_forecast_metrics

def test_forecaster_horizons():
    fc = TrafficForecaster()
    counts = {"Northbound": 15, "Southbound": 25, "Eastbound": 10, "Westbound": 12}
    res = fc.forecast(counts)
    assert res["intersection_id"] == "INT-001"
    assert len(res["horizons"]) == 4
    horizons = [h["horizon_minutes"] for h in res["horizons"]]
    assert horizons == [5, 10, 15, 30]
    for h in res["horizons"]:
        assert h["lower_bound_95"] <= h["predicted_vehicle_count"] <= h["upper_bound_95"]

def test_evaluation_metrics():
    y_true = [20.0, 30.0, 40.0, 50.0]
    y_pred = [22.0, 28.0, 39.0, 51.0]
    metrics = evaluate_forecast_metrics(y_true, y_pred)
    assert metrics["mae"] > 0
    assert metrics["rmse"] > 0
    assert metrics["mape"] > 0
    assert 0.8 <= metrics["r2_score"] <= 1.0
