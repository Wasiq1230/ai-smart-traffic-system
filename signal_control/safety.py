from typing import Dict, List, Any, Tuple

class SafetyViolationException(Exception):
    pass

class SafetyValidator:
    CONFLICT_PAIRS = [
        ("Northbound", "Eastbound"),
        ("Northbound", "Westbound"),
        ("Southbound", "Eastbound"),
        ("Southbound", "Westbound")
    ]

    MIN_GREEN_SEC = 10
    MAX_GREEN_SEC = 65
    YELLOW_SEC = 3
    ALL_RED_SEC = 2
    MAX_STARVATION_CYCLES = 3

    def validate_plan(
        self,
        green_allocations: Dict[str, int],
        active_lane: str,
        starvation_counters: Dict[str, int]
    ) -> Tuple[bool, str, Dict[str, int]]:
        adjusted = {}
        for lane, g_time in green_allocations.items():
            safe_green = max(self.MIN_GREEN_SEC, min(self.MAX_GREEN_SEC, int(g_time)))
            if starvation_counters.get(lane, 0) >= self.MAX_STARVATION_CYCLES:
                safe_green = max(safe_green, self.MIN_GREEN_SEC + 5)
            adjusted[lane] = safe_green

        if active_lane not in green_allocations:
            return False, f"Invalid active green lane: {active_lane}", adjusted

        return True, "SAFETY_PASSED", adjusted
