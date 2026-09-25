"""
Test Suite for Stage 26 (Phase 47): Dynamic Noise Calibrator Integration into Sequential Null Hypothesis

Verifies:
1. DynamicNoiseCalibrator integration into SequentialQStat (pulling p0(t) from calibrator).
2. Natural channel decoherence drift adaptation prevents false alarms.
3. Abrupt uncalibrated adversarial noise step triggers CUSUM / SPRT alarm.
4. QStatDetector batch integration with DynamicNoiseCalibrator.
"""

import pytest
import numpy as np

from security.detector import ThreatCategory, QStatDetector
from security.calibrate import DynamicNoiseCalibrator, CalibrationStatus
from security.sequential import SequentialQStat, SequentialVerdict


class TestSequentialCalibration:
    """Verifies adaptive null hypothesis calibration and drift resilience."""

    def test_dynamic_calibrator_updates_baseline_null_hypothesis(self):
        """
        Tests that when thermal drift shifts channel error from 3% to 5.5%,
        DynamicNoiseCalibrator adapts baseline p0, and SequentialQStat pulls it,
        preventing false alarms.
        """
        calibrator = DynamicNoiseCalibrator(nominal_p0=0.03, window_size=5)
        detector = SequentialQStat(
            baseline_p0=0.03,
            alt_p1=0.20,
            calibrator=calibrator,
            calibration_interval_trials=20
        )

        # Ingest pilot measurements indicating gradual drift to ~5.5%
        for i in range(5):
            calibrator.ingest_pilot_measurement(num_trials=100, n_errors=6)

        assert calibrator.get_current_baseline() > 0.045

        # Run 100 trials with Bernoulli(p=0.05)
        # Because baseline adapted, it must NOT false alarm
        np.random.seed(42)
        trials = np.random.choice([0, 1], size=100, p=[0.95, 0.05])
        for t in trials:
            v = detector.update(int(t))
            assert v.verdict != ThreatCategory.MALICIOUS

        assert detector.p0 > 0.045

    def test_ingest_pilot_frame_recalibration(self):
        """
        Tests convenience method ingest_pilot_frame() directly on SequentialQStat.
        """
        detector = SequentialQStat(baseline_p0=0.03, alt_p1=0.20)
        assert detector.p0 == pytest.approx(0.03, abs=1e-4)

        status = detector.ingest_pilot_frame(num_trials=200, n_errors=14)
        assert isinstance(status, CalibrationStatus)
        # Baseline should have adapted toward 7%
        assert detector.p0 > 0.035
        # LLR increments should have been recomputed
        assert detector.llr_1 < 1.89  # ln(0.20 / new_p0) decreases as new_p0 increases

    def test_abrupt_uncalibrated_drift_detected_as_tampering(self):
        """
        Tests that if error rate jumps abruptly to 35% without pilot calibration,
        SequentialQStat detects it as an active attack.
        """
        detector = SequentialQStat(baseline_p0=0.03, alt_p1=0.20)
        np.random.seed(1337)
        trials = np.random.choice([0, 1], size=50, p=[0.65, 0.35])

        detected = False
        for t in trials:
            v = detector.update(int(t))
            if v.verdict == ThreatCategory.MALICIOUS:
                detected = True
                break

        assert detected is True

    def test_batch_detector_calibrator_integration(self):
        """
        Tests QStatDetector backwards-compatible integration with DynamicNoiseCalibrator.
        """
        calibrator = DynamicNoiseCalibrator(nominal_p0=0.03)
        # Ingest high baseline pilot
        calibrator.ingest_pilot_measurement(num_trials=100, n_errors=8)

        detector = QStatDetector(baseline_noise_p0=0.03, calibrator=calibrator)
        assessment = detector.evaluate(
            error_count=8,
            total_trials=100,
            signer_id="Alice",
            nonce="CALIBRATED-NONCE-1",
            timestamp=1000.0,
            current_time=1000.0
        )
        assert assessment.baseline_noise_p0 > 0.035
