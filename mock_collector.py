"""
mock_collector.py

Simulates collecting metrics from a real system.
Generates realistic metric patterns including gradual degradation.
"""

import time
import random
import math


class MockMetricsCollector:
    """
    Simulates a system that gradually degrades over time.
    """
    
    def __init__(self, degradation_rate=0.01):
        """
        Args:
            degradation_rate: How fast the system degrades (0.01 = slow, 0.1 = fast)
        """
        self.degradation_rate = degradation_rate
        self.time_step = 0
        self.base_cpu = 30.0
        self.base_mem = 40.0
        self.restart_count = 0
        
    def collect(self) -> dict:
        """
        Collect current metrics snapshot.
        
        Returns:
            dict: Current system metrics
        """
        self.time_step += 1
        
        # Simulate gradual degradation
        degradation = self.time_step * self.degradation_rate
        
        # CPU usage increases over time with noise
        cpu = self.base_cpu + (degradation * 50) + random.uniform(-5, 5)
        cpu = max(0, min(100, cpu))  # Clamp to 0-100
        
        # Memory usage increases similarly
        mem = self.base_mem + (degradation * 40) + random.uniform(-5, 5)
        mem = max(0, min(100, mem))
        
        # Error rate increases as system degrades
        error_rate = max(0, (degradation * 0.1) + random.uniform(-0.01, 0.01))
        
        # Response time increases exponentially as system degrades
        response_p95 = 100 + (degradation * 1000) + random.uniform(-50, 50)
        response_p95 = max(0, response_p95)
        
        # Restarts happen when CPU > 95% or memory > 95%
        if cpu > 95 or mem > 95:
            if random.random() < 0.1:  # 10% chance per check
                self.restart_count += 1
        
        return {
            'cpu_usage': cpu,
            'mem_usage': mem,
            'error_rate': error_rate,
            'response_p95': response_p95,
            'restart_count': self.restart_count
        }
    
    def reset(self):
        """Reset to healthy state (simulate recovery)"""
        self.time_step = 0
        self.base_cpu = 30.0
        self.base_mem = 40.0
        self.restart_count = 0


# Test the collector
if __name__ == "__main__":
    collector = MockMetricsCollector(degradation_rate=0.05)
    
    print("Simulating system degradation over 20 steps:")
    print()
    
    for i in range(20):
        metrics = collector.collect()
        print(f"Step {i+1}:")
        print(f"  CPU: {metrics['cpu_usage']:.1f}%")
        print(f"  Memory: {metrics['mem_usage']:.1f}%")
        print(f"  Errors: {metrics['error_rate']:.4f}/sec")
        print(f"  P95 Latency: {metrics['response_p95']:.0f}ms")
        print(f"  Restarts: {metrics['restart_count']}")
        print()
        
        time.sleep(0.1)  # Small delay for readability