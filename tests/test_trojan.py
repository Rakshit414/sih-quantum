"""
Test Suite for Stage 12 (Phase 32): Quantum Trojan-Horse Watchtower (Q-TROJAN)
Validates T1/T2 memory decoherence simulation, Helstrom information leakage bounds,
optical power thresholding, spectral bandpass gating, and temporal gating.
"""

import pytest
import numpy as np

from security.trojan import (
    QuantumMemoryBuffer,
    TrojanHorseDetector,
    TrojanProbeSignal,
    StoredQubitState,
    TrojanDetectionResult,
)
from security.detector import ThreatCategory


class TestQuantumTrojanDetector:
    """
    Unit and cryptanalytic tests for Phase 32 Q-TROJAN watchtower.
    """

    def test_quantum_memory_buffer_decoherence(self):
        """
        Tests physical Lindblad decoherence model across continuous storage times.
        Ensures trace preservation, fidelity degradation monotonicity, and physical constraints.
        """
        buffer = QuantumMemoryBuffer(t1_us=1000.0, t2_us=200.0)

        # Ground state |0>
        psi_0 = np.array([1.0, 0.0], dtype=complex)

        # Time 0: perfect fidelity
        s0 = buffer.evolve_state(psi_0, elapsed_us=0.0)
        assert np.isclose(s0.memory_fidelity, 1.0, atol=1e-4)
        assert np.isclose(s0.decoherence_error_rate, 0.0, atol=1e-4)
        assert np.isclose(np.trace(s0.current_density_matrix).real, 1.0, atol=1e-6)

        # Superposition state |+> = (|0> + |1>) / sqrt(2)
        psi_plus = np.array([1.0 / np.sqrt(2), 1.0 / np.sqrt(2)], dtype=complex)
        s_100 = buffer.evolve_state(psi_plus, elapsed_us=100.0)
        s_500 = buffer.evolve_state(psi_plus, elapsed_us=500.0)

        assert s_100.memory_fidelity > s_500.memory_fidelity, "Fidelity must decay over storage time"
        assert s_100.decoherence_error_rate < s_500.decoherence_error_rate
        assert np.isclose(np.trace(s_100.current_density_matrix).real, 1.0, atol=1e-6)
        assert np.isclose(np.trace(s_500.current_density_matrix).real, 1.0, atol=1e-6)

        # Test physical constraint validation T2 <= 2*T1
        with pytest.raises(ValueError):
            QuantumMemoryBuffer(t1_us=100.0, t2_us=250.0)

    def test_clean_channel_trojan_detection(self):
        """
        Ensures that an honest quantum channel with zero Trojan probes passes as LEGITIMATE.
        """
        detector = TrojanHorseDetector(safe_power_threshold_uw=0.010)
        result = detector.analyze_probe(probe=None, elapsed_storage_us=50.0)

        assert result.verdict == ThreatCategory.LEGITIMATE
        assert not result.probe_detected
        assert not result.spectral_breach
        assert not result.temporal_breach
        assert result.information_leakage_bits == 0.0
        assert result.attack_classification == "CLEAN_CHANNEL"

    def test_bright_pulse_trojan_horse_detected(self):
        """
        Tests detection of high-intensity optical probe pulses injected to read phase settings.
        """
        detector = TrojanHorseDetector(safe_power_threshold_uw=0.010)

        # Adversary injects 2.0 uW probe pulse at telecom 1550 nm synchronously
        probe = TrojanProbeSignal(
            optical_power_uw=2.0,
            wavelength_nm=1550.0,
            arrival_offset_ns=0.0,
            pulse_duration_ns=1.0,
            internal_reflectivity_r=0.02
        )
        # Reflected power = 2.0 * 0.02 = 0.04 uW > 0.010 uW threshold

        result = detector.analyze_probe(probe=probe, elapsed_storage_us=0.0)

        assert result.probe_detected
        assert result.verdict == ThreatCategory.MALICIOUS
        assert result.attack_classification == "BRIGHT_PULSE_TROJAN_HORSE"
        assert result.information_leakage_bits > 0.01
        assert "High-intensity optical probe detected" in result.cryptanalytic_proof

    def test_spectral_breach_trojan_probe(self):
        """
        Tests detection of out-of-band Trojan probes (e.g. 1310 nm instead of 1550 nm).
        """
        detector = TrojanHorseDetector(passband_center_nm=1550.0, passband_width_nm=10.0)

        # Out-of-band probe at 1310 nm
        probe = TrojanProbeSignal(
            optical_power_uw=0.05,
            wavelength_nm=1310.0,
            arrival_offset_ns=0.0,
            pulse_duration_ns=1.0,
            internal_reflectivity_r=0.01
        )

        result = detector.analyze_probe(probe=probe)

        assert result.spectral_breach
        assert result.verdict == ThreatCategory.MALICIOUS
        assert result.attack_classification == "OUT_OF_BAND_SPECTRAL_PROBE"
        assert "Out-of-band optical injection" in result.cryptanalytic_proof

    def test_temporal_gating_breach_trojan_probe(self):
        """
        Tests detection of asynchronous Trojan probes arriving outside the synchronization gate.
        """
        detector = TrojanHorseDetector(gate_window_ns=1.0)

        # Pulse arriving +3.5 ns late
        probe = TrojanProbeSignal(
            optical_power_uw=0.05,
            wavelength_nm=1550.0,
            arrival_offset_ns=3.5,
            pulse_duration_ns=1.0,
            internal_reflectivity_r=0.01
        )

        result = detector.analyze_probe(probe=probe)

        assert result.temporal_breach
        assert result.verdict == ThreatCategory.MALICIOUS
        assert result.attack_classification == "ASYNC_TIME_DOMAIN_PROBE"
        assert "outside synchronous gate window" in result.cryptanalytic_proof
