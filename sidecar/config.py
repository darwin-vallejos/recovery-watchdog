"""Configuration for Recovery Debt Watchdog"""

class WatchdogConfig:
    # Detector parameters
    BETA_BASE = 1.1
    HISTORY_SIZE = 200
    WINDOW_SIZE = 20
    
    # Irreversibility detection
    MARGIN_THRESHOLD = 0.01
    SUSTAINED_WINDOW = 5
    
    # Timing
    POLL_INTERVAL_SEC = 1.0
    
    # Actions
    KILL_ON_IRREVERSIBLE = True
    
    # Logging
    LOG_LEVEL = "INFO"
