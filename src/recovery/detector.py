from dataclasses import dataclass


@dataclass
class Metrics:
    recovery_margin: float


class RecoveryDebtDetector:
    """
    Stable, stateless recovery-debt engine.
    """

    def __init__(self, beta_base: float = 1.1, c_baseline: float = 0.6):
        self.beta_base = beta_base
        self.c_baseline = c_baseline

    def update(self, C: float, beta: float):
        """
        Compute recovery margin and alert level.
        """

        margin = (C - self.c_baseline) / self.c_baseline
        margin = max(0.0, margin)

        if margin == 0.0:
            alert = "RED"
        elif beta > self.beta_base:
            alert = "YELLOW"
        else:
            alert = "GREEN"

        return Metrics(recovery_margin=margin), alert
