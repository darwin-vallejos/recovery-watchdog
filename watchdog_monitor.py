"""
watchdog_monitor.py

Main monitoring loop that:
1. Collects metrics
2. Computes coherence
3. Runs detector
4. Logs to CSV
"""

import csv
import time
from datetime import datetime, timezone
from pathlib import Path

from src.recovery.detector import RecoveryDebtDetector
from src.recovery.coherence import compute_coherence_from_pod_metrics, compute_stress_factor
from mock_collector import MockMetricsCollector


def main():
    """Main monitoring loop"""
    
    # Initialize components
    detector = RecoveryDebtDetector(
        beta_base=1.1,
        c_baseline=0.6
    )
    
    collector = MockMetricsCollector(degradation_rate=0.02)
    
    # Output file
    output_file = Path("pilot.csv")
    
    # Create CSV with headers
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'coherence_C', 'recovery_margin', 'alert_level'])
    
    print("Recovery Watchdog Started")
    print("=" * 60)
    print(f"Logging to: {output_file.absolute()}")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    print()
    
    try:
        step = 0
        while True:
            step += 1
            
            # Collect metrics
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
                writer.writerow([timestamp, C, margin, alert_level])
            
            # Print status
            alert_symbol = {
                'GREEN': '✓',
                'YELLOW': '⚠',
                'RED': '✗'
            }
            
            print(f"[{step:04d}] {timestamp[:19]} | C={C:.3f} | Margin={margin:.3f} | {alert_symbol.get(alert_level, '?')} {alert_level}")
            
            # Sleep 1 second
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("Monitoring stopped")
        print(f"Data saved to: {output_file.absolute()}")
        print("=" * 60)


if __name__ == "__main__":
    main()