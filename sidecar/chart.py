#!/usr/bin/env python3

import csv
import matplotlib
matplotlib.use('Agg')  # Fix for recursion issue
import matplotlib.pyplot as plt
from datetime import datetime

CSV_PATH = "pilot.csv"

timestamps = []
coherence = []
margin = []

with open(CSV_PATH, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        timestamps.append(datetime.fromisoformat(row["timestamp"]))
        coherence.append(float(row["coherence_C"]))
        margin.append(float(row["recovery_margin"]))

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

ax1.plot(timestamps, coherence, 'b-', linewidth=2)
ax1.axhline(0.6, linestyle="--", color="red", alpha=0.5)
ax1.set_ylabel("Coherence C")
ax1.grid(True, alpha=0.3)
ax1.set_title("Recovery Watchdog - System Health")

ax2.plot(timestamps, margin, 'orange', linewidth=2)
ax2.axhline(0.0, linestyle="--", color="black", alpha=0.5)
ax2.set_ylabel("Recovery Margin")
ax2.set_xlabel("Time")
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("watchdog_report.png", dpi=150)
print("Chart saved to: watchdog_report.png")