#!/usr/bin/env python3

import os
import sys
import time
import logging
import signal

# Ensure local imports work
sys.path.insert(0, os.path.abspath("."))

from sidecar.adapters.prometheus import PrometheusAdapter
from sidecar.exporter import CSVExporter
from recovery.detector import RecoveryDebtDetector


def _coerce_float(x):
    """
    Convert x to float safely.
    Supports:
      - float/int/str numeric
      - objects with .recovery_margin or .margin
      - dict with keys recovery_margin/margin
    Returns None if cannot coerce.
    """
    if x is None:
        return None

    # direct numeric
    if isinstance(x, (int, float)):
        return float(x)

    # numeric string
    if isinstance(x, str):
        try:
            return float(x)
        except Exception:
            return None

    # dict with margin fields
    if isinstance(x, dict):
        v = x.get("recovery_margin", x.get("margin"))
        return _coerce_float(v)

    # object with margin fields
    for attr in ("recovery_margin", "margin"):
        if hasattr(x, attr):
            return _coerce_float(getattr(x, attr))

    # last attempt
    try:
        return float(x)
    except Exception:
        return None


def _parse_detector_output(out):
    """
    Normalize detector output into: (margin: float|None, alert: any)
    Supports:
      - tuple/list: (margin, alert, ...)
      - object: out.recovery_margin + out.alert_level (or .margin/.alert)
      - dict: keys recovery_margin/margin, alert_level/alert
    """
    if out is None:
        return None, None

    # tuple/list
    if isinstance(out, (tuple, list)):
        if len(out) == 0:
            return None, None
        margin = _coerce_float(out[0])
        alert = out[1] if len(out) > 1 else None
        # If alert itself is an object with alert fields, extract
        if alert is not None and not isinstance(alert, (str, int, float, dict, tuple, list)):
            for a_attr in ("alert_level", "alert"):
                if hasattr(alert, a_attr):
                    alert = getattr(alert, a_attr)
                    break
        return margin, alert

    # dict
    if isinstance(out, dict):
        margin = _coerce_float(out.get("recovery_margin", out.get("margin")))
        alert = out.get("alert_level", out.get("alert"))
        return margin, alert

    # object
    margin = None
    for m_attr in ("recovery_margin", "margin"):
        if hasattr(out, m_attr):
            margin = _coerce_float(getattr(out, m_attr))
            break

    alert = None
    for a_attr in ("alert_level", "alert"):
        if hasattr(out, a_attr):
            alert = getattr(out, a_attr)
            break

    return margin, alert


class RecoveryWatchdog:
    """
    Recovery Watchdog
    - READ ONLY
    - Signature safe
    - Metrics-object safe
    - Tuple safe
    - Pilot safe
    """

    def __init__(self):
        # -------------------------
        # CONFIG
        # -------------------------
        self.READ_ONLY = True
        self.SLEEP_SECONDS = 1.0
        self.RED_THRESHOLD = 0.01
        self.RED_COUNT_LIMIT = 5
        self.BETA = 1.1

        # -------------------------
        # LOGGING
        # -------------------------
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
        )
        self.log = logging.getLogger("watchdog")

        # -------------------------
        # ADAPTER
        # -------------------------
        self.adapter = PrometheusAdapter(
            prometheus_url=os.getenv("PROMETHEUS_URL", "http://localhost:9090"),
            query="up",
        )

        # -------------------------
        # DETECTOR
        # -------------------------
        self.detector = RecoveryDebtDetector(beta_base=self.BETA)

        # -------------------------
        # CSV EXPORT
        # -------------------------
        self.exporter = CSVExporter("pilot.csv")

        # -------------------------
        # INTERNAL STATE
        # -------------------------
        self.red_count = 0
        self.phase_triggered = False

        self.log.info("Recovery Watchdog started (READ-ONLY MODE)")

    def _detector_update(self, C):
        """
        Call detector.update with whatever signature it supports.
        """
        try:
            # Try (C, beta)
            return self.detector.update(C, self.BETA)
        except TypeError:
            try:
                # Try (C, beta=)
                return self.detector.update(C, beta=self.BETA)
            except TypeError:
                # Try (C)
                return self.detector.update(C)

    def step(self):
        C = self.adapter.get_coherence()

        if C is None:
            self.log.warning("No metrics available — skipping step")
            return

        # detector
        try:
            out = self._detector_update(C)
        except Exception as e:
            self.log.error(f"Detector failed: {e}")
            return

        # normalize output
        margin, alert = _parse_detector_output(out)

        if margin is None:
            self.log.error("Detector output had no usable recovery_margin/margin")
            return

        alert_level = alert if alert is not None else "UNKNOWN"

        # log (never format non-numeric)
        self.log.info(
            f"C={float(C):.3f} margin={float(margin):.3f} alert={alert_level} red={self.red_count}"
        )

        # csv
        self.exporter.write(
            C=float(C),
            margin=float(margin),
            alert=alert_level,
        )

        # phase tracking
        if margin <= self.RED_THRESHOLD:
            self.red_count += 1
        else:
            self.red_count = 0

        if self.red_count >= self.RED_COUNT_LIMIT and not self.phase_triggered:
            self.phase_triggered = True
            self.trigger_action()

    def trigger_action(self):
        self.log.critical("=" * 60)
        self.log.critical("PHASE CHANGE DETECTED")

        if self.READ_ONLY:
            self.log.critical("READ-ONLY MODE — NO ACTION TAKEN")
            self.log.critical("=" * 60)
            return

        self.log.critical("SENDING SIGTERM TO PID 1")
        self.log.critical("=" * 60)
        time.sleep(2)

        try:
            os.kill(1, signal.SIGTERM)
        except Exception:
            self.log.critical("PID 1 not available — exiting")
            sys.exit(1)

    def run(self):
        while True:
            self.step()
            time.sleep(self.SLEEP_SECONDS)


if __name__ == "__main__":
    RecoveryWatchdog().run()
