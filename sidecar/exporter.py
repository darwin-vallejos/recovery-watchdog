import csv
import os
import time
from datetime import datetime


class CSVExporter:
    """
    Safe, deterministic CSV exporter.
    Creates the file immediately and appends rows defensively.
    """

    def __init__(self, path: str):
        self.path = os.path.abspath(path)
        self._ensure_file()

    def _ensure_file(self):
        # Create file + header if missing
        if not os.path.exists(self.path):
            with open(self.path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp",
                    "coherence_C",
                    "recovery_margin",
                    "alert_level",
                ])

    def write(self, C: float, margin: float, alert: str):
        # Append one row
        with open(self.path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.utcnow().isoformat(),
                round(C, 6),
                round(margin, 6),
                alert,
            ])
