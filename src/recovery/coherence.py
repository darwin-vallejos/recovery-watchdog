"""
coherence.py

Converts observable system metrics into coherence score C.
IMPROVED for real system monitoring.
"""

def compute_coherence_from_pod_metrics(metrics: dict) -> float:
    """
    Convert system metrics into coherence score C (0-1 scale)
    
    Args:
        metrics: Dictionary with keys:
            - cpu_usage: float (0-100, percentage)
            - mem_usage: float (0-100, percentage)
            - error_rate: float (0-1, errors per second)
            - response_p95: float (milliseconds) - OPTIONAL
            - restart_count: int (number of restarts) - OPTIONAL
    
    Returns:
        float: Coherence score C (0-1)
    """
    
    # Normalize each metric to health score (0-1)
    # Higher health = better
    
    # CPU health: 100% usage = 0 health, 0% usage = 1 health
    cpu_usage = metrics.get('cpu_usage', 0)
    cpu_health = max(0.0, 1.0 - (cpu_usage / 100.0))
    
    # Memory health: same logic
    mem_usage = metrics.get('mem_usage', 0)
    mem_health = max(0.0, 1.0 - (mem_usage / 100.0))
    
    # Error health: exponential penalty
    # 0 errors = 1.0 health, 0.1 errors/sec = 0 health
    error_rate = metrics.get('error_rate', 0)
    error_health = max(0.0, 1.0 - (error_rate * 10.0))
    
    # Latency health (optional): normalize to 5000ms max
    response_p95 = metrics.get('response_p95', 100.0)  # Default to healthy 100ms
    # Cap at reasonable values
    response_p95 = min(response_p95, 5000.0)
    latency_health = max(0.0, 1.0 - (response_p95 / 5000.0))
    
    # Restart health (optional): 10+ restarts = 0 health
    restart_count = metrics.get('restart_count', 0)
    restart_health = max(0.0, 1.0 - (restart_count / 10.0))
    
    # Weighted geometric mean
    # CPU and Memory are most important (weight 2x)
    # Errors, latency, restarts are secondary (weight 1x)
    weights = [2.0, 2.0, 1.0, 1.0, 1.0]
    values = [cpu_health, mem_health, error_health, latency_health, restart_health]
    
    # Weighted geometric mean formula
    product = 1.0
    total_weight = sum(weights)
    
    for value, weight in zip(values, weights):
        # Ensure value is positive to avoid math errors
        value = max(0.001, value)
        product *= value ** (weight / total_weight)
    
    C = product
    
    # Ensure C is in valid range
    C = max(0.0, min(1.0, C))
    
    return C


def compute_stress_factor(metrics: dict) -> float:
    """
    Compute stress factor beta from system load
    
    Args:
        metrics: Same dictionary as above
    
    Returns:
        float: Beta stress factor (typically 0.5-2.0)
    """
    
    # Base stress from CPU and memory
    cpu_stress = metrics.get('cpu_usage', 0) / 100.0
    mem_stress = metrics.get('mem_usage', 0) / 100.0
    
    # Average stress
    base_stress = (cpu_stress + mem_stress) / 2.0
    
    # Scale to beta range (0.5 = low stress, 2.0 = high stress)
    beta = 0.5 + (base_stress * 1.5)
    
    return beta


# Test function
if __name__ == "__main__":
    # Test with healthy system
    healthy_metrics = {
        'cpu_usage': 20.0,
        'mem_usage': 30.0,
        'error_rate': 0.0,
        'response_p95': 150.0,
        'restart_count': 0
    }
    
    C = compute_coherence_from_pod_metrics(healthy_metrics)
    beta = compute_stress_factor(healthy_metrics)
    
    print("Healthy system:")
    print(f"  Coherence C: {C:.4f}")
    print(f"  Stress beta: {beta:.4f}")
    print()
    
    # Test with stressed system
    stressed_metrics = {
        'cpu_usage': 85.0,
        'mem_usage': 75.0,
        'error_rate': 0.05,
        'response_p95': 2000.0,
        'restart_count': 2
    }
    
    C_stressed = compute_coherence_from_pod_metrics(stressed_metrics)
    beta_stressed = compute_stress_factor(stressed_metrics)
    
    print("Stressed system:")
    print(f"  Coherence C: {C_stressed:.4f}")
    print(f"  Stress beta: {beta_stressed:.4f}")
    print()
    
    # Test with current real metrics (low CPU/MEM)
    current_metrics = {
        'cpu_usage': 6.1,
        'mem_usage': 53.6,
        'error_rate': 0.0,
        'response_p95': 100.0,
        'restart_count': 0
    }
    
    C_current = compute_coherence_from_pod_metrics(current_metrics)
    beta_current = compute_stress_factor(current_metrics)
    
    print("Your current system:")
    print(f"  Coherence C: {C_current:.4f}")
    print(f"  Stress beta: {beta_current:.4f}")