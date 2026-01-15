# Recovery Watchdog

Proactive failure prediction system that monitors system health and predicts failures before they happen.

## Features

- **Real-time monitoring** - Tracks CPU, memory, network, and process metrics
- **Failure prediction** - Predicts system failures 5-15 minutes in advance
- **Alert system** - Email and Slack notifications for critical events
- **Web dashboard** - Beautiful real-time visualization
- **Audit logging** - Complete CSV audit trail for compliance

## Quick Start

### Local Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run monitoring
python watchdog_monitor_real.py

# Run dashboard (in separate terminal)
python dashboard.py
```

Visit http://localhost:5000 for the dashboard.

### Docker Deployment
```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f watchdog

# Stop
docker-compose down
```

Dashboard available at http://localhost:5001

## Configuration

### Email Alerts

Edit `alerts.py` config:
```python
config = {
    'email': {
        'enabled': True,
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'sender': 'your-email@gmail.com',
        'password': 'your-app-password',
        'recipients': ['alert@company.com']
    }
}
```

### Slack Alerts

Create Slack webhook at https://api.slack.com/messaging/webhooks
```python
config = {
    'slack': {
        'enabled': True,
        'webhook_url': 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'
    }
}
```

## Architecture
```
Real System Metrics → Coherence Calculator → Detector → Alerts
         ↓                                        ↓
    CSV Logger                              Dashboard
```

## Metrics

- **Coherence (C)**: Overall system health (0-1 scale)
- **Recovery Margin**: Buffer before failure (higher is better)
- **Alert Levels**: GREEN (healthy), YELLOW (degrading), RED (critical)

## Use Cases

- DevOps monitoring
- Infrastructure reliability
- Compliance logging
- Incident prevention
- Post-mortem analysis

## License

Apache License 2.0

## Support

Created by Darwin Vallejos