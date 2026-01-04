"""
crypto.py

This module is intentionally disabled in the Recovery Watchdog pilot.

Reason:
- Recovery Watchdog is a read-only, deterministic monitoring system.
- No cryptographic signing, key generation, or verification is required.
- No private keys, secrets, or credentials are used or stored.

This file exists only to preserve package structure.
"""

def crypto_disabled(*args, **kwargs):
    raise NotImplementedError(
        "Cryptographic functionality is intentionally disabled "
        "in the Recovery Watchdog pilot release."
    )
