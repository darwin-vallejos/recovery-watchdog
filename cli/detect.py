import argparse
import csv
import json
from pathlib import Path

from recovery.detector import RecoveryDebtDetector


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--run", required=True)
    p.add_argument("--beta-base", type=float, default=1.1)
    p.add_argument("--c-baseline", type=float, default=0.6)
    p.add_argument("--output", default="detector_report.csv")
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args()

    with open(args.run, "r", encoding="utf-8-sig") as f:
        run = json.load(f)

    steps = run.get("step_logs") or run.get("steps")
    if not steps:
        raise SystemExit("Run file missing 'step_logs' or 'steps'")

    detector = RecoveryDebtDetector(
        beta_base=args.beta_base,
        c_baseline=args.c_baseline,
    )

    rows = []

    for step in steps:
        if "C" not in step:
            raise SystemExit("Step missing required key: 'C'")

        C = float(step["C"])
        beta = float(step.get("beta", step.get("beta_eff", args.beta_base)))

        metrics, alert = detector.update(C=C, beta=beta)

        t = step.get("t", step.get("step"))

        if not args.quiet:
            print(t, alert, metrics.recovery_margin)

        rows.append({
            "t": t,
            "alert": alert,
            "recovery_margin": metrics.recovery_margin,
        })

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)

    with open(out, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"OK: wrote {len(rows)} rows → {out}")


if __name__ == "__main__":
    main()
