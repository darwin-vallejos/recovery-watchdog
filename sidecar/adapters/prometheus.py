import os
import time
import random
import logging
import requests


class PrometheusAdapter:
    """
    Safe Prometheus adapter.

    Rules:
    - NEVER crash
    - Return None if unavailable
    - Support MOCK mode for pilots/demos
    """

    def __init__(
        self,
        prometheus_url="http://localhost:9090",
        query="up",
        timeout=1.0,
    ):
        self.url = prometheus_url.rstrip("/")
        self.query = query
        self.timeout = timeout

        # Enable mock mode via env var
        self.mock = os.getenv("MOCK_PROMETHEUS", "false").lower() == "true"

        self.log = logging.getLogger("prometheus-adapter")

        if self.mock:
            self.log.warning("MOCK_PROMETHEUS enabled — using simulated signal")

    def get_coherence(self):
        """
        Returns:
            float in [0,1]  -> coherence
            None            -> metrics unavailable (SAFE)
        """

        # =========================
        # MOCK MODE (DEMO / PILOT)
        # =========================
        if self.mock:
            # Smooth decay with noise (looks realistic on charts)
            base = max(0.0, 1.0 - (time.time() % 60) / 80.0)
            noise = random.uniform(-0.02, 0.02)
            return max(0.0, min(1.0, base + noise))

        # =========================
        # REAL PROMETHEUS MODE
        # =========================
        try:
            resp = requests.get(
                f"{self.url}/api/v1/query",
                params={"query": self.query},
                timeout=self.timeout,
            )

            if resp.status_code != 200:
                self.log.warning("Prometheus HTTP %s", resp.status_code)
                return None

            data = resp.json()
            if data.get("status") != "success":
                return None

            result = data.get("data", {}).get("result", [])
            if not result:
                return 0.0  # Prometheus up, no targets

            # Extract numeric value
            value = float(result[0]["value"][1])

            # Normalize -> coherence
            # "up" metric: 1 = healthy, 0 = down
            return max(0.0, min(1.0, value))

        except Exception as e:
            # HARD RULE: NEVER CRASH
            self.log.warning("Prometheus unavailable (%s)", str(e))
            return None
