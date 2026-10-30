"""Historical floor-rank percentile definition; MIT project code."""
def _percentile(sorted_values: list[float], q: float) -> float:
    if not sorted_values:
        return float("nan")
    idx = int(q * (len(sorted_values) - 1))
    return sorted_values[idx]
