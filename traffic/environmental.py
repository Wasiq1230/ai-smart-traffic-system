from typing import Dict, Any

class EnvironmentalEstimator:
    KG_CO2_PER_LITER_GASOLINE = 2.31
    LITERS_FUEL_PER_IDLE_HOUR = 0.85

    def calculate(self, total_vehicles_served: int, avg_delay_reduction_seconds: float = 14.5) -> Dict[str, Any]:
        total_idle_sec_saved = total_vehicles_served * max(0.0, avg_delay_reduction_seconds)
        idle_hours_saved = total_idle_sec_saved / 3600.0

        fuel_saved_liters = round(idle_hours_saved * self.LITERS_FUEL_PER_IDLE_HOUR, 2)
        co2_reduced_kg = round(fuel_saved_liters * self.KG_CO2_PER_LITER_GASOLINE, 2)

        return {
            "total_vehicles_served": total_vehicles_served,
            "idle_time_saved_seconds": round(total_idle_sec_saved, 1),
            "idle_hours_saved": round(idle_hours_saved, 2),
            "estimated_fuel_saved_liters": fuel_saved_liters,
            "estimated_co2_reduced_kg": co2_reduced_kg,
            "is_estimate": True,
            "emission_factor_co2_kg_per_l": self.KG_CO2_PER_LITER_GASOLINE
        }
