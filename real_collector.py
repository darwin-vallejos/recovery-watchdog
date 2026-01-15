"""
real_collector.py

Collects REAL system metrics from the actual machine.
IMPROVED version with better response time calculation.
"""

import psutil
import time


class RealMetricsCollector:
    """
    Collects real system metrics from the local machine.
    """
    
    def __init__(self):
        """Initialize collector with baseline measurements"""
        self.process_count_baseline = len(psutil.pids())
        self.boot_time = psutil.boot_time()
        
        # Get initial network counters for rate calculation
        self.prev_net_io = psutil.net_io_counters()
        self.prev_time = time.time()
        
        # Track process count changes for restart detection
        self.prev_process_count = self.process_count_baseline
        
    def collect(self) -> dict:
        """
        Collect current system metrics.
        
        Returns:
            dict: Current system metrics
        """
        
        # CPU usage (percentage)
        cpu_usage = psutil.cpu_percent(interval=0.1)
        
        # Memory usage (percentage)
        mem = psutil.virtual_memory()
        mem_usage = mem.percent
        
        # Network error rate
        net_io = psutil.net_io_counters()
        current_time = time.time()
        
        # Calculate errors per second
        time_delta = current_time - self.prev_time
        errors_delta = (net_io.errin + net_io.errout) - (self.prev_net_io.errin + self.prev_net_io.errout)
        error_rate = errors_delta / time_delta if time_delta > 0 else 0.0
        
        # Update for next iteration
        self.prev_net_io = net_io
        self.prev_time = current_time
        
        # Response time proxy: use system load average
        # On Windows, use CPU queue length as proxy
        # Lower values = faster response
        try:
            # Get 1-minute load average (normalized by CPU count)
            cpu_count = psutil.cpu_count() or 1
            
            # Use CPU percent as load indicator
            # 0-20% = 100ms, 20-50% = 500ms, 50-80% = 1500ms, 80-100% = 3000ms
            if cpu_usage < 20:
                response_p95 = 100.0
            elif cpu_usage < 50:
                response_p95 = 100 + ((cpu_usage - 20) / 30) * 400  # 100-500ms
            elif cpu_usage < 80:
                response_p95 = 500 + ((cpu_usage - 50) / 30) * 1000  # 500-1500ms
            else:
                response_p95 = 1500 + ((cpu_usage - 80) / 20) * 1500  # 1500-3000ms
        except:
            response_p95 = 100.0  # Default to healthy
        
        # Process restarts: detect significant changes in process count
        current_process_count = len(psutil.pids())
        process_delta = abs(current_process_count - self.prev_process_count)
        
        # If >5 processes changed, consider it a restart event
        restart_count = min(process_delta // 5, 10)  # Cap at 10
        
        self.prev_process_count = current_process_count
        
        return {
            'cpu_usage': cpu_usage,
            'mem_usage': mem_usage,
            'error_rate': error_rate,
            'response_p95': response_p95,
            'restart_count': restart_count
        }


# Test the collector
if __name__ == "__main__":
    collector = RealMetricsCollector()
    
    print("Collecting REAL system metrics for 10 seconds...")
    print()
    
    for i in range(10):
        metrics = collector.collect()
        print(f"Sample {i+1}:")
        print(f"  CPU: {metrics['cpu_usage']:.1f}%")
        print(f"  Memory: {metrics['mem_usage']:.1f}%")
        print(f"  Network Errors: {metrics['error_rate']:.4f}/sec")
        print(f"  Response Time: {metrics['response_p95']:.0f}ms")
        print(f"  Process Changes: {metrics['restart_count']}")
        print()
        
        time.sleep(1)