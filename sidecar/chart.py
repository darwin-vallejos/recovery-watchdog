#!/usr/bin/env python3

import csv
import sys
from datetime import datetime
import matplotlib.pyplot as plt


CSV_PATH = "pilot.csv"


def load_csv(path):
    timestamps = []
    coherence = []
    margin = []

    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            timestamps.append(
                datetime.fromisoformat(row["timestamp"])
            )
            coherence.append(float(row["coherence_C"]))
            margin.append(float(row["recovery_margin"]))

    return timestamps, coherence, margin


def plot():
    try:
        ts, C, m = load_csv(CSV_PATH)
    except FileNotFoundError:
        print("pilot.csv not found")
        sys.exit(1)

    if not ts:
        print("No data rows yet — chart will appear once metrics exist.")
        sys.exit(0)

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

    ax1.plot(ts, C, label="Coherence C")
    ax1.set_ylabel("C")
    ax1.legend()
    ax1.grid(True)

    ax2.plot(ts, m, color="red", label="Recovery Margin")
    ax2.axhline(0.01, linestyle="--", color="black")
    ax2.set_ylabel("Margin")
    ax2.legend()
    ax2.grid(True)

    plt.xlabel("Time")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot()
