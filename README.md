\# Recovery Watchdog



Deterministic, read-only detection of recovery debt in distributed systems.



This project implements a watchdog loop that evaluates system recoverability

using explicit thresholds and produces an auditable evidence trail.



This is \*\*not\*\* an AI system.

This is \*\*not\*\* a predictive system.

All outputs are deterministic and reproducible.



---



\## What It Does



\- Computes a coherence signal (C)

\- Computes a recovery margin

\- Detects sustained recovery exhaustion (phase change)

\- Enforces read-only behavior

\- Produces CSV logs and visual charts



No automated destructive actions are taken.



---



\## Design Principles



\- Deterministic logic only

\- No machine learning

\- No heuristic inference

\- Read-only by default

\- No action under uncertainty

\- Evidence-first output (CSV + chart)



---



\## Evidence



This repository includes:



\- `pilot.csv` — append-only audit log

\- `report/` — pilot report and visualization

\- `sidecar/chart.py` — deterministic chart generator



All behavior can be reproduced locally.



---



\## Safety



\- No secrets stored

\- No customer data

\- No external write actions

\- Graceful degradation when metrics are unavailable



---



\## License



Apache License 2.0



