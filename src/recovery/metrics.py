import math
from typing import Optional


def compute_recovery_margin(C: float, C_baseline: float) -> float:
    """
    Remaining recovery capacity as a percentage.
    """
    if C_baseline <= 0:
        return 0.0
    margin = (C - C_baseline) / C_baseline
    return max(0.0, min(1.0, margin)) * 100.0


def compute_debt_slope(history: list[float]) -> float:
    """
    Rate of recovery margin decline per step.
    Negative slope = worsening.
    """
    if len(history) < 2:
        return 0.0
    return history[-1] - history[-2]


def estimate_steps_to_irreversible(
    current_margin: float,
    slope: float
) -> Optional[int]:
    """
    Predict how many steps remain until margin reaches zero.
    """
    if slope >= 0:
        return None
    if current_margin <= 0:
        return 0
    return int(abs(current_margin / slope))


def compute_confidence(history: list[float]) -> float:
    """
    Confidence based on stability of recent margin changes.
    """
    if len(history) < 5:
        return 0.3
    diffs = [abs(history[i] - history[i - 1]) for i in range(1, len(history))]
    variance = sum(diffs[-5:]) / 5.0
    return max(0.0, min(1.0, 1.0 - variance))
