import csv
import matplotlib.pyplot as plt

CSV_FILE = "detector_report.csv"

steps = []
margins = []

with open(CSV_FILE, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        t = row.get("t")
        steps.append(int(t) if t not in (None, "", "None") else i)
        margins.append(float(row["recovery_margin"]))

plt.figure(figsize=(10, 4))
plt.plot(steps, margins, label="Recovery Margin")
plt.axhline(0.0, linestyle="--", color="red", alpha=0.5)
plt.xlabel("Step")
plt.ylabel("Recovery Margin")
plt.title("Recovery Margin Over Time")
plt.legend()
plt.tight_layout()
plt.show()
