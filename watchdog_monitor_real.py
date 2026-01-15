"""
watchdog_monitor_real.py

Production monitoring loop using REAL system metrics.
"""

import csv
import time
from datetime import datetime, timezone
from pathlib import Path

from src.recovery.detector import RecoveryDebtDetector
from src.recovery.coherence import compute_coherence_from_pod_metrics, compute_stress_factor
from real_collector import RealMetricsCollector


def main():
    """Main monitoring loop with real metrics"""
    
    # Initialize components
    detector = RecoveryDebtDetector(
        beta_base=1.1,
        c_baseline=0.6
    )
    
    collector = RealMetricsCollector()
    
    # Output file
    output_file = Path("pilot_real.csv")
    
    # Create CSV with headers
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'timestamp', 'coherence_C', 'recovery_margin', 'alert_level',
            'cpu_usage', 'mem_usage', 'error_rate'
        ])
    
    print("=" * 60)
    print("Recovery Watchdog Started (REAL METRICS)")
    print("=" * 60)
    print(f"Monitoring: {Path.cwd()}")
    print(f"Logging to: {output_file.absolute()}")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    print()
    
    try:
        step = 0
        while True:
            step += 1
            
            # Collect REAL metrics
            metrics = collector.collect()
            
            # Compute coherence and stress
            C = compute_coherence_from_pod_metrics(metrics)
            beta = compute_stress_factor(metrics)
            
            # Run detector
            margin_result, alert_level = detector.update(C, beta)
            margin = margin_result.recovery_margin
            
            # Current timestamp
            timestamp = datetime.now(timezone.utc).isoformat()
            
            # Log to CSV
            with open(output_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    timestamp, C, margin, alert_level,
                    metrics['cpu_usage'], metrics['mem_usage'], metrics['error_rate']
                ])
            
            # Print status
            alert_symbol = {
                'GREEN': '✓',
                'YELLOW': '⚠',
                'RED': '✗'
            }
            
            cpu_str = f"CPU={metrics['cpu_usage']:.1f}%"
            mem_str = f"MEM={metrics['mem_usage']:.1f}%"
            
            print(f"[{step:04d}] {timestamp[:19]} | C={C:.3f} | M={margin:.3f} | "
                  f"{alert_symbol.get(alert_level, '?')} {alert_level} | {cpu_str} {mem_str}")
            
            # Sleep 5 seconds (real systems don't need second-by-second monitoring)
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("Monitoring stopped")
        print(f"Real system data saved to: {output_file.absolute()}")
        print("=" * 60)


if __name__ == "__main__":
    main()