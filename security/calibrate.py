"""
Q-Sentinel: Dynamic Baseline Noise Auto-Calibration Engine (Q-CALIBRATE)
Stage 9: Phase 28
Monitors ambient optical decoherence and physical thermal drift across quantum channels.
Continuously updates baseline error floor p0(t) using sliding-window pilot frames,
preventing false alarms while detecting stealthy adversarial channel drift.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple, Optional
import numpy as np
import time


@dataclass
class CalibrationSample:
    """
    Individual pilot probe measurement sample.
    """
    timestamp: float
    num_trials: int
    n_errors: int
    empirical_error: float


@dataclass
class CalibrationStatus:
    """
    Current health, noise baseline estimate, and drift assessment of the quantum channel.
    """
    calibrated_p0: float
    confidence_interval_95: Tuple[float, float]
    sample_window_size: int
    drift_rate_per_min: float
    is_drift_anomalous: bool
    status_summary: str


class DynamicNoiseCalibrator:
    """
    Sliding-window Kalman-inspired auto-calibration engine for baseline channel noise floor.
    """

    def __init__(
        self,
        nominal_p0: float = 0.03,
        window_size: int = 10,
        max_allowable_drift_per_min: float = 0.04,
        alpha_ema: float = 0.25
    ):
        self.nominal_p0: float = nominal_p0
        self.window_size: int = window_size
        self.max_allowable_drift: float = max_allowable_drift_per_min
        self.alpha_ema: float = alpha_ema
        self.history: List[CalibrationSample] = []
        self.current_calibrated_p0: float = nominal_p0

    def ingest_pilot_measurement(self, num_trials: int, n_errors: int, timestamp: Optional[float] = None) -> CalibrationStatus:
        """
        Ingests a reference calibration pulse measurement and updates running noise baseline.
        """
        ts = timestamp or time.time()
        emp_err = n_errors / max(1, num_trials)
        sample = CalibrationSample(timestamp=ts, num_trials=num_trials, n_errors=n_errors, empirical_error=emp_err)
        self.history.append(sample)

        # Maintain sliding window
        if len(self.history) > self.window_size:
            self.history = self.history[-self.window_size:]

        # Calculate Exponential Moving Average (EMA) of noise floor
        prev_p0 = self.current_calibrated_p0
        self.current_calibrated_p0 = (self.alpha_ema * emp_err) + ((1.0 - self.alpha_ema) * self.current_calibrated_p0)
        # Ensure non-zero physical floor
        self.current_calibrated_p0 = float(np.clip(self.current_calibrated_p0, 0.005, 0.20))

        # Compute 95% Wilson score / normal confidence interval
        total_n = sum(s.num_trials for s in self.history)
        se = float(np.sqrt(self.current_calibrated_p0 * (1.0 - self.current_calibrated_p0) / max(10, total_n)))
        ci_lower = float(max(0.0, self.current_calibrated_p0 - 1.96 * se))
        ci_upper = float(min(1.0, self.current_calibrated_p0 + 1.96 * se))

        # Compute drift rate per minute
        drift_rate_per_min = 0.0
        if len(self.history) >= 2:
            time_delta_sec = self.history[-1].timestamp - self.history[0].timestamp
            err_delta = self.history[-1].empirical_error - self.history[0].empirical_error
            if time_delta_sec > 0.01:
                drift_rate_per_min = float((err_delta / time_delta_sec) * 60.0)

        is_drift_anomalous = abs(drift_rate_per_min) > self.max_allowable_drift

        if is_drift_anomalous:
            status_summary = (
                f"Drift Anomaly Alert: Channel error rate changing at {drift_rate_per_min*100:+.2f}%/min, "
                f"exceeding physical thermal bounds ({self.max_allowable_drift*100:.1f}%/min). Possible active tampering."
            )
        else:
            status_summary = (
                f"Channel Stable: Adaptive baseline calibrated to {self.current_calibrated_p0*100:.2f}% "
                f"(95% CI: [{ci_lower*100:.1f}%, {ci_upper*100:.1f}%])."
            )

        return CalibrationStatus(
            calibrated_p0=round(self.current_calibrated_p0, 4),
            confidence_interval_95=(round(ci_lower, 4), round(ci_upper, 4)),
            sample_window_size=len(self.history),
            drift_rate_per_min=round(drift_rate_per_min, 4),
            is_drift_anomalous=is_drift_anomalous,
            status_summary=status_summary
        )

    def get_current_baseline(self) -> float:
        """Returns the currently active calibrated noise floor p0."""
        return self.current_calibrated_p0

    def reset(self):
        """Resets calibration history back to nominal defaults."""
        self.history.clear()
        self.current_calibrated_p0 = self.nominal_p0
