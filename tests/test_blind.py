"""
Test Suite for Stage 13 (Phase 33): Quantum Detector Blinding & Spatial-Mode Side-Channel Watchtower (Q-BLIND)
Validates DC bias current monitoring, Geiger-to-linear mode transitions,
spatial beam displacement via quadrant sensors, and inter-arrival timing entropy.
"""

import pytest
import numpy as np

from security.blind import (
    DetectorTelemetry,
    BlindingDetectionResult,
    DetectorBlindingWatcher,
)
from security.detector import ThreatCategory


class TestDetectorBlindingWatcher:
    """
    Unit and side-channel vulnerability tests for Phase 33 Q-BLIND watchtower.
    """

    def test_nominal_geiger_mode_operation(self):
        """
        Validates that an uncompromised APD operating in Geiger mode with nominal dark current
        and Poissonian timing is classified as LEGITIMATE.
        """
        watcher = DetectorBlindingWatcher(current_threshold_ua=5.0, max_spatial_displacement_um=2.5)

        # Generate true exponential Poissonian arrival intervals
        np.random.seed(42)
        intervals = list(np.random.exponential(scale=25.0, size=200))
        intervals = [max(1.5, t) for t in intervals]  # Above dead time (1.0 us)

        telemetry = DetectorTelemetry(
            channel_id="APD_0",
            bias_current_ua=0.35,  # 350 nA (well below 5 uA threshold)
            spatial_offset_x_um=0.3,
            spatial_offset_y_um=-0.2,
            inter_arrival_times_us=intervals,
            double_click_count=1,
            total_clicks=200
        )

        result = watcher.evaluate_detector_state(telemetry)

        assert result.verdict == ThreatCategory.LEGITIMATE
        assert not result.blinding_detected
        assert not result.spatial_breach
        assert not result.dead_time_violation
        assert result.bias_current_ua < 1.0
        assert "Geiger Mode" in result.operating_mode
        assert result.attack_classification == "NOMINAL_GEIGER_OPERATION"

    def test_cw_bright_light_blinding_attack_detected(self):
        """
        Tests detection of continuous-wave (CW) bright illumination driving APD into linear mode.
        """
        watcher = DetectorBlindingWatcher(current_threshold_ua=5.0)

        intervals = list(np.random.normal(5.0, 0.2, 100))

        # Attacker illuminates APD with 15.0 uA DC current
        telemetry = DetectorTelemetry(
            channel_id="APD_0",
            bias_current_ua=16.8,  # Linear mode (> 5 uA)
            spatial_offset_x_um=0.1,
            spatial_offset_y_um=0.1,
            inter_arrival_times_us=intervals,
            double_click_count=2,
            total_clicks=100
        )

        result = watcher.evaluate_detector_state(telemetry)

        assert result.blinding_detected
        assert result.verdict == ThreatCategory.MALICIOUS
        assert "Linear Mode" in result.operating_mode
        assert result.attack_classification == "DETECTOR_BLINDING_CW_ATTACK"
        assert "Anode bias current" in result.cryptanalytic_proof

    def test_spatial_mode_beam_shift_detected(self):
        """
        Tests detection of adversarial spatial beam steering attempting to exploit detector efficiency mismatch.
        """
        watcher = DetectorBlindingWatcher(max_spatial_displacement_um=2.5)

        intervals = list(np.random.exponential(scale=20.0, size=150))
        intervals = [max(1.2, t) for t in intervals]

        # Beam shifted by dx = 3.2 um, dy = 2.5 um -> r = sqrt(3.2^2 + 2.5^2) = 4.06 um > 2.5 um
        telemetry = DetectorTelemetry(
            channel_id="APD_1",
            bias_current_ua=0.40,
            spatial_offset_x_um=3.2,
            spatial_offset_y_um=2.5,
            inter_arrival_times_us=intervals,
            double_click_count=0,
            total_clicks=150
        )

        result = watcher.evaluate_detector_state(telemetry)

        assert result.blinding_detected
        assert result.spatial_breach
        assert result.spatial_displacement_um > 2.5
        assert result.verdict == ThreatCategory.MALICIOUS
        assert result.attack_classification == "SPATIAL_MODE_BEAM_SHIFT_ATTACK"
        assert "Spatial beam displacement" in result.cryptanalytic_proof

    def test_faked_state_timing_attack_detected(self):
        """
        Tests detection of periodic faked-state triggering that produces collapsed entropy
        and dead-time violation clicks.
        """
        watcher = DetectorBlindingWatcher(min_entropy_nats=1.0, detector_dead_time_us=1.0)

        # Rigid deterministic intervals at exactly 2.0 us (zero variance -> entropy collapse)
        # plus a violation at 0.3 us (< 1.0 us dead time)
        intervals = [2.0] * 100
        intervals[0] = 0.3  # Dead-time violation

        telemetry = DetectorTelemetry(
            channel_id="APD_0",
            bias_current_ua=0.8,
            spatial_offset_x_um=0.2,
            spatial_offset_y_um=-0.1,
            inter_arrival_times_us=intervals,
            double_click_count=5,
            total_clicks=100
        )

        result = watcher.evaluate_detector_state(telemetry)

        assert result.blinding_detected
        assert result.dead_time_violation
        assert result.verdict == ThreatCategory.MALICIOUS
        assert result.attack_classification == "FAKED_STATE_TIMING_ATTACK"
        assert "Non-Poissonian arrival statistics detected" in result.cryptanalytic_proof

    def test_simulation_scenarios_diversity(self):
        """
        Tests simulation helper for all four representative operational scenarios.
        """
        watcher = DetectorBlindingWatcher()

        res_honest = watcher.simulate_detector_scan("Honest")
        assert res_honest.verdict == ThreatCategory.LEGITIMATE

        res_blind = watcher.simulate_detector_scan("Blinding CW")
        assert res_blind.verdict == ThreatCategory.MALICIOUS
        assert res_blind.attack_classification == "DETECTOR_BLINDING_CW_ATTACK"

        res_spatial = watcher.simulate_detector_scan("Spatial Shift")
        assert res_spatial.verdict == ThreatCategory.MALICIOUS
        assert res_spatial.attack_classification == "SPATIAL_MODE_BEAM_SHIFT_ATTACK"

        res_faked = watcher.simulate_detector_scan("Faked State Timing")
        assert res_faked.verdict == ThreatCategory.MALICIOUS
        assert res_faked.attack_classification == "FAKED_STATE_TIMING_ATTACK"
