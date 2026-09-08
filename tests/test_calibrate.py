"""
Unit Tests for Phase 28: Dynamic Baseline Noise Calibration (Q-CALIBRATE)
"""

import pytest
import time
from security.calibrate import DynamicNoiseCalibrator, CalibrationStatus


class TestDynamicNoiseCalibrator:

    def test_nominal_calibration_steady_state(self):
        """Feeding honest calibration samples near 3% should maintain calibrated p0 ~ 0.03."""
        calibrator = DynamicNoiseCalibrator(nominal_p0=0.03, window_size=5)
        now = time.time()
        status = None
        for i in range(10):
            # 1 error in 33 trials is ~3.0%
            status = calibrator.ingest_pilot_measurement(num_trials=50, n_errors=2, timestamp=now + i * 2)

        assert status is not None
        assert 0.015 <= status.calibrated_p0 <= 0.06
        assert status.is_drift_anomalous is False
        assert status.sample_window_size == 5

    def test_thermal_drift_adaptation(self):
        """When channel naturally degrades to 5%, the calibrator adapts smoothly."""
        calibrator = DynamicNoiseCalibrator(nominal_p0=0.02, window_size=5, alpha_ema=0.3)
        now = time.time()
        for i in range(8):
            # Error rate ~5%
            status = calibrator.ingest_pilot_measurement(num_trials=100, n_errors=5, timestamp=now + i * 5)

        assert status.calibrated_p0 > 0.03
        assert status.confidence_interval_95[0] < status.calibrated_p0 < status.confidence_interval_95[1]

    def test_anomalous_sudden_drift_detection(self):
        """A sudden jump in error within a short time window should trip the drift anomaly alarm."""
        calibrator = DynamicNoiseCalibrator(nominal_p0=0.02, window_size=5, max_allowable_drift_per_min=0.05)
        now = time.time()
        # Normal first
        calibrator.ingest_pilot_measurement(num_trials=100, n_errors=2, timestamp=now)
        # Immediate sudden jump to 25% errors 10 seconds later: drift = (0.25 - 0.02) / 10s * 60s = 1.38/min >> 0.05
        status = calibrator.ingest_pilot_measurement(num_trials=100, n_errors=25, timestamp=now + 10)

        assert status.is_drift_anomalous is True
        assert "Drift Anomaly Alert" in status.status_summary
