"""
Q-Sentinel: Cryptographic Freshness & Anti-Replay Engine
Stage 4: Phase 11
Maintains a sliding-window nonce and timestamp registry to detect classical
teleportation bit re-injection and stale quantum signature sessions.
"""

from __future__ import annotations
import time
from typing import Set, Dict, Tuple, Optional


class FreshnessRegistry:
    """
    Tracks session nonces, monotonic sequence counters, and UTC timestamps.
    Deterministically intercepts replay attacks.
    """

    def __init__(self, max_time_window_seconds: float = 60.0):
        self.max_time_window: float = max_time_window_seconds
        # Set of observed nonces: { (signer_id, nonce) }
        self.seen_nonces: Set[Tuple[str, str]] = set()
        # Nonce timestamps for window eviction: { (signer_id, nonce): timestamp }
        self.nonce_timestamps: Dict[Tuple[str, str], float] = {}

    def verify_and_register(
        self,
        signer_id: str,
        nonce: str,
        timestamp: float,
        current_time: Optional[float] = None
    ) -> Tuple[bool, str]:
        """
        Validates token freshness:
        1. Checks timestamp freshness within [current_time - max_time_window, current_time + 5s].
        2. Checks if nonce was previously observed for this signer.
        
        Returns: (is_fresh, failure_reason)
        """
        now = current_time if current_time is not None else time.time()
        key = (signer_id, nonce)

        # Evict expired nonces outside time window
        expired_keys = [k for k, ts in self.nonce_timestamps.items() if now - ts > self.max_time_window]
        for k in expired_keys:
            self.seen_nonces.discard(k)
            self.nonce_timestamps.pop(k, None)

        # 1. Stale timestamp check
        if timestamp < (now - self.max_time_window):
            age = now - timestamp
            return False, f"Stale signature timestamp: age {age:.1f}s exceeds window of {self.max_time_window:.1f}s."

        if timestamp > (now + 5.0):
            return False, f"Future timestamp detected (clock skew > 5s): {timestamp - now:.1f}s in future."

        # 2. Replay check (nonce duplication)
        if key in self.seen_nonces:
            return False, f"Replay attack detected: Nonce '{nonce}' has already been processed for signer '{signer_id}'."

        # Register nonce
        self.seen_nonces.add(key)
        self.nonce_timestamps[key] = timestamp
        return True, "Fresh token registered successfully."

    def reset(self) -> None:
        """Clears the registry cache (useful for testing and reset buttons)."""
        self.seen_nonces.clear()
        self.nonce_timestamps.clear()
