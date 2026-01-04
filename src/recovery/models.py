from dataclasses import dataclass
from typing import Optional

# ============================================================
# Compatibility State for External Integrations (Sidecars, K8s)
# ============================================================

@dataclass(frozen=True)
class SystemState:
    """
    Compatibility state used by external observers (e.g. watchdog sidecar).

    This mirrors the minimum required fields from StepState but does not
    require internal engine fields like step_hash or t.
    """
    stress: float
    M: float
    beta_eff: float
    C: float
    violations: int

@dataclass(frozen=True)
class RecoveryMetrics:
    """
    Derived recovery debt metrics.
    """
    recovery_margin: float
    debt_slope: float
    steps_to_irreversible: Optional[int]
    confidence: float


@dataclass(frozen=True)
class DetectorReport:
    """
    Final detector output (signable / auditable).
    """
    run_hash: str
    verified: bool
    recovery_margin: float
    debt_slope: float
    steps_to_irreversible: Optional[int]
    confidence: float
    alert_level: str
    detector_version: str
