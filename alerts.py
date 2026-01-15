"""
alerts.py

Send alerts via email or Slack when RED alert is triggered.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from datetime import datetime


class AlertManager:
    """
    Manages alert delivery via multiple channels.
    """
    
    def __init__(self, config: dict = None):
        """
        Initialize alert manager with configuration.
        
        Args:
            config: Dictionary with alert settings
                {
                    'email': {
                        'enabled': True,
                        'smtp_server': 'smtp.gmail.com',
                        'smtp_port': 587,
                        'sender': 'your-email@gmail.com',
                        'password': 'your-app-password',
                        'recipients': ['alert@company.com']
                    },
                    'slack': {
                        'enabled': True,
                        'webhook_url': 'https://hooks.slack.com/services/...'
                    }
                }
        """
        self.config = config or {}
        self.last_alert_time = {}
        
    def should_send_alert(self, alert_level: str, cooldown_seconds: int = 300) -> bool:
        """
        Check if enough time has passed since last alert.
        Prevents alert spam.
        """
        if alert_level not in self.last_alert_time:
            return True
        
        elapsed = (datetime.now() - self.last_alert_time[alert_level]).total_seconds()
        return elapsed > cooldown_seconds
    
    def send_alert(self, alert_level: str, message: str, metrics: dict = None):
        """
        Send alert through configured channels.
        """
        if not self.should_send_alert(alert_level):
            print(f"  [Alert cooldown active for {alert_level}]")
            return
        
        self.last_alert_time[alert_level] = datetime.now()
        
        # Email
        if self.config.get('email', {}).get('enabled'):
            try:
                self._send_email(alert_level, message, metrics)
                print(f"  [✓ Email alert sent]")
            except Exception as e:
                print(f"  [✗ Email failed: {e}]")
        
        # Slack
        if self.config.get('slack', {}).get('enabled'):
            try:
                self._send_slack(alert_level, message, metrics)
                print(f"  [✓ Slack alert sent]")
            except Exception as e:
                print(f"  [✗ Slack failed: {e}]")
    
    def _send_email(self, alert_level: str, message: str, metrics: dict):
        """Send email alert"""
        email_config = self.config['email']
        
        msg = MIMEMultipart()
        msg['From'] = email_config['sender']
        msg['To'] = ', '.join(email_config['recipients'])
        msg['Subject'] = f"[{alert_level}] Recovery Watchdog Alert"
        
        body = f"""
Recovery Watchdog Alert

Status: {alert_level}
Time: {datetime.now().isoformat()}

Message: {message}

System Metrics:
- Coherence: {metrics.get('coherence', 'N/A'):.3f}
- Recovery Margin: {metrics.get('margin', 'N/A'):.3f}
- CPU: {metrics.get('cpu_usage', 'N/A'):.1f}%
- Memory: {metrics.get('mem_usage', 'N/A'):.1f}%

---
Recovery Watchdog v0.1.0
"""
        
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
            server.starttls()
            server.login(email_config['sender'], email_config['password'])
            server.send_message(msg)
    
    def _send_slack(self, alert_level: str, message: str, metrics: dict):
        """Send Slack alert"""
        slack_config = self.config['slack']
        
        color = {
            'GREEN': 'good',
            'YELLOW': 'warning',
            'RED': 'danger'
        }.get(alert_level, 'danger')
        
        payload = {
            "attachments": [{
                "color": color,
                "title": f"Recovery Watchdog Alert: {alert_level}",
                "text": message,
                "fields": [
                    {
                        "title": "Coherence",
                        "value": f"{metrics.get('coherence', 0):.3f}",
                        "short": True
                    },
                    {
                        "title": "Recovery Margin",
                        "value": f"{metrics.get('margin', 0):.3f}",
                        "short": True
                    },
                    {
                        "title": "CPU Usage",
                        "value": f"{metrics.get('cpu_usage', 0):.1f}%",
                        "short": True
                    },
                    {
                        "title": "Memory Usage",
                        "value": f"{metrics.get('mem_usage', 0):.1f}%",
                        "short": True
                    }
                ],
                "footer": "Recovery Watchdog v0.1.0",
                "ts": int(datetime.now().timestamp())
            }]
        }
        
        response = requests.post(slack_config['webhook_url'], json=payload)
        response.raise_for_status()


# Example usage
if __name__ == "__main__":
    # Test configuration (replace with your actual credentials)
    config = {
        'email': {
            'enabled': False,  # Set to True and configure
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'sender': 'your-email@gmail.com',
            'password': 'your-app-password',
            'recipients': ['alert@company.com']
        },
        'slack': {
            'enabled': False,  # Set to True and configure
            'webhook_url': 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'
        }
    }
    
    alert_manager = AlertManager(config)
    
    # Test alert
    print("Testing alert system...")
    alert_manager.send_alert(
        'RED',
        'System coherence has dropped below critical threshold!',
        {
            'coherence': 0.45,
            'margin': 0.01,
            'cpu_usage': 95.2,
            'mem_usage': 87.3
        }
    )
    print("Test complete")