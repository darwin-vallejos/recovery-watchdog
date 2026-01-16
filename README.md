# Recovery Watchdog

**🚀 LIVE DEMO:** https://web-production-b0dba.up.railway.app/api/v1/health

## Predict Infrastructure Failures 10-15 Minutes Early

Recovery Watchdog uses coherence-based analysis to detect system degradation **before** critical thresholds breach - giving you time to prevent outages instead of reacting to them.

[![GitHub release](https://img.shields.io/github/v/release/darwin-vallejos/recovery-watchdog)](https://github.com/darwin-vallejos/recovery-watchdog/releases)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18004196.svg)](https://doi.org/10.5281/zenodo.18004196)

---

## The Problem

**Traditional monitoring is reactive:**
- CPU hits 90% → Alert fires → Engineers scramble → Too late
- Customers complain → You investigate → Outage already happened

**Recovery Watchdog is predictive:**
- System coherence drops to 0.65 → Alert fires 12 minutes early → Engineers intervene → Crisis prevented

---

## How It Works
```
Traditional:    [Everything fine] → [SUDDEN FAILURE] → [Alert] → [Fix]
                                    ↑ You are here when alerted

Recovery:       [Early Warning] → [Time to Act] → [Prevent Failure]
                ↑ You are here (10-15 min early)
```

**Coherence Analysis:**
- Monitors CPU, memory, network, error rates simultaneously
- Detects patterns of degradation before individual thresholds breach
- Calculates "recovery margin" - time until system failure
- Progressive alerts: GREEN → YELLOW → RED

---

## Quick Start

### Try It Now
```bash
# Check if service is running
curl https://web-production-b0dba.up.railway.app/api/v1/health
```

### Start Free 30-Day Trial

Email: darwin90betanco@gmail.com
- No credit card required
- Full access to all features
- 30-minute setup assistance

---

## Features

- ✅ **Predictive alerts** - 10-15 minute early warning
- ✅ **Multi-tenant SaaS** - Secure organization isolation
- ✅ **Agent-based monitoring** - Lightweight, low overhead
- ✅ **REST API** - Standard HTTP/JSON
- ✅ **Open source** - Apache 2.0 license
- ✅ **Published research** - Peer-reviewed methodology

---

## Pricing

| Plan | Price | Agents | Support | Retention |
|------|-------|--------|---------|-----------|
| **Trial** | $0 | 3 | Email | 7 days |
| **Starter** | $99/mo | 10 | Email | 30 days |
| **Professional** | $299/mo | 50 | Priority | 90 days |
| **Enterprise** | Custom | Unlimited | Phone | Custom |

Early adopter discount: 33% off first year

---

## Real Results

**Recent Test:**
- Alert fired: 2:45 AM
- System failure: 2:58 AM
- **Early warning: 12 minutes**

Traditional monitoring would have alerted AFTER failure.

---

## Research

Published on Zenodo: [DOI 10.5281/zenodo.18004196](https://doi.org/10.5281/zenodo.18004196)

Based on Bootstrap Intelligence Protocol (BIP) framework demonstrating 24% capital preservation improvement through coherence-based analysis.

---

## Installation

### For Customers (Managed SaaS)

1. Email darwin90betanco@gmail.com for trial
2. Receive API key
3. Install agent:
```bash
wget https://raw.githubusercontent.com/darwin-vallejos/recovery-watchdog/main/saas_agent.py
# Edit file, add your API key
python saas_agent.py
```

### For Self-Hosting (Advanced)
```bash
git clone https://github.com/darwin-vallejos/recovery-watchdog.git
cd recovery-watchdog
pip install -r requirements.txt
python saas_api.py
```

---

## Use Cases

**E-commerce:**
- Prevent checkout failures during peak traffic
- Avoid revenue loss from downtime

**SaaS Companies:**
- Maintain SLA guarantees
- Reduce customer churn from outages

**Financial Services:**
- Meet regulatory uptime requirements
- Prevent trading disruptions

**Gaming:**
- Keep servers online during launches
- Maintain player experience

---

## Architecture
```
Customer Infrastructure
    ↓ (HTTPS)
Recovery Watchdog Agent (Python)
    ↓ (Metrics every 30s)
Recovery Watchdog API (Flask)
    ↓ (Coherence calculation)
Database (SQLite/PostgreSQL)
    ↓ (Alerts)
Slack, Email, PagerDuty
```

---

## FAQ

**Q: How is this different from Datadog/New Relic?**
A: They monitor metrics. We predict failures. Use both - they're complementary.

**Q: What if it gives false positives?**
A: Tune thresholds during the trial. Typical accuracy: 85-95%.

**Q: Does it slow down my systems?**
A: No. Agent uses <1% CPU, <50MB memory.

**Q: Can I self-host?**
A: Yes! It's open source. But managed SaaS includes support and updates.

**Q: What about GDPR compliance?**
A: We only collect system metrics, no personal data. Privacy policy available.

---

## Support

- **Community:** GitHub Issues
- **Email:** darwin90betanco@gmail.com
- **Documentation:** Coming soon
- **Status:** https://web-production-b0dba.up.railway.app/api/v1/health

---

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## License

Apache License 2.0 - See [LICENSE](LICENSE)

---

## About

Built by Darwin Vallejos, independent researcher and protocol engineer.

**Other Projects:**
- Bootstrap Intelligence Protocol (BIP)
- Witness Receipt Protocol (WRP)
- Persistence-Weighted General Relativity (PWGR)

---

**Start your free 30-day trial:** darwin90betanco@gmail.com