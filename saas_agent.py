"""
saas_agent.py

Lightweight agent that customers install on their servers.
Sends metrics to Recovery Watchdog SaaS.
"""

import time
import requests
import socket
from real_collector import RealMetricsCollector


class RecoveryWatchdogAgent:
    """
    SaaS agent for Recovery Watchdog.
    Customers install this on their servers.
    """
    
    def __init__(self, api_key: str, api_url: str = "http://localhost:8000"):
        """
        Args:
            api_key: Organization API key from Recovery Watchdog dashboard
            api_url: SaaS API endpoint
        """
        self.api_key = api_key
        self.api_url = api_url.rstrip('/')
        self.collector = RealMetricsCollector()
        self.agent_id = None
        self.hostname = socket.gethostname()
        
    def register(self):
        """Register this agent with SaaS platform"""
        response = requests.post(
            f"{self.api_url}/api/v1/agents/register",
            headers={'X-API-Key': self.api_key},
            json={'hostname': self.hostname}
        )
        
        if response.status_code == 201:
            data = response.json()
            self.agent_id = data['agent_id']
            print(f"✓ Agent registered: {self.agent_id}")
            print(f"  Hostname: {self.hostname}")
            return True
        else:
            print(f"✗ Registration failed: {response.text}")
            return False
    
    def send_metrics(self):
        """Collect and send metrics to SaaS"""
        if not self.agent_id:
            print("✗ Agent not registered")
            return False
        
        # Collect local metrics
        metrics = self.collector.collect()
        
        # Add agent_id
        metrics['agent_id'] = self.agent_id
        
        # Send to SaaS
        try:
            response = requests.post(
                f"{self.api_url}/api/v1/metrics",
                headers={'X-API-Key': self.api_key},
                json=metrics,
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"✗ Metrics submission failed: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Connection error: {e}")
            return None
    
    def run(self, interval: int = 30):
        """Run monitoring loop"""
        print("=" * 60)
        print("Recovery Watchdog Agent Starting")
        print("=" * 60)
        print(f"API: {self.api_url}")
        print(f"Hostname: {self.hostname}")
        print(f"Interval: {interval}s")
        print("=" * 60)
        print()
        
        # Register agent
        if not self.register():
            print("Failed to register agent. Exiting.")
            return
        
        print()
        print("Monitoring started. Press Ctrl+C to stop.")
        print()
        
        step = 0
        try:
            while True:
                step += 1
                
                result = self.send_metrics()
                
                if result:
                    alert_symbol = {
                        'GREEN': '✓',
                        'YELLOW': '⚠',
                        'RED': '✗'
                    }.get(result['alert_level'], '?')
                    
                    print(f"[{step:04d}] C={result['coherence']:.3f} | "
                          f"M={result['recovery_margin']:.3f} | "
                          f"{alert_symbol} {result['alert_level']}")
                else:
                    print(f"[{step:04d}] ✗ Failed to send metrics")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n" + "=" * 60)
            print("Monitoring stopped")
            print("=" * 60)


# Example usage
if __name__ == "__main__":
    # Customer gets this API key from Recovery Watchdog dashboard
    API_KEY = "rwk_YvS7E1UKK6MyKpbAyqC5S1Ii1Hy3ayqlADi1yQcXV6A"
    API_URL = "http://localhost:8000"  # Change to production URL
    
    agent = RecoveryWatchdogAgent(API_KEY, API_URL)
    agent.run(interval=30)