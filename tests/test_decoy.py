"""
Unit Tests for Phase 31: Decoy-State Protocol & Photon Number Splitting (PNS) Detection
"""

import pytest
from security.decoy import DecoyStateAnalyzer, PNSAnalysisResult
from security.detector import ThreatCategory


class TestDecoyStateAndPNS:

    def test_honest_decoy_state_bounds(self):
        """Under honest transmission, decoy-state yield Y1 bound should satisfy channel bounds."""
        analyzer = DecoyStateAnalyzer(mu_signal=0.50, nu_decoy=0.10, channel_transmittance=0.12)
        result = analyzer.simulate_transmission(num_pulses=3000, pns_attack_active=False)

        assert result.pns_attack_detected is False
        assert result.verdict == ThreatCategory.LEGITIMATE
        assert result.lower_bound_Y1 >= 0.05
        assert result.signal_gain_Q_mu > result.decoy_gain_Q_nu
        assert "Decoy-State Bounds Verified" in result.cryptanalytic_proof

    def test_pns_attack_detection_via_decoy_inequality(self):
        """When Eve attempts a Photon Number Splitting attack, Y1 drops drastically and trips alert."""
        analyzer = DecoyStateAnalyzer(mu_signal=0.50, nu_decoy=0.10, channel_transmittance=0.12)
        result = analyzer.simulate_transmission(num_pulses=3000, pns_attack_active=True)

        assert result.pns_attack_detected is True
        assert result.verdict == ThreatCategory.MALICIOUS
        assert "PNS ATTACK DETECTED" in result.cryptanalytic_proof

    def test_gain_monotonicity_vacuum_decoy_signal(self):
        """Physical gains must satisfy Q_0 < Q_nu < Q_mu."""
        analyzer = DecoyStateAnalyzer(mu_signal=0.60, nu_decoy=0.15, channel_transmittance=0.10)
        result = analyzer.simulate_transmission(num_pulses=2500, pns_attack_active=False)

        assert result.vacuum_gain_Q_0 <= result.decoy_gain_Q_nu
        assert result.decoy_gain_Q_nu < result.signal_gain_Q_mu
