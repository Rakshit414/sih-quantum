"""
Test Suite for Stage 16 (Phase 37): Quantum WDM & Co-propagation Raman Scattering Defense (Q-WDM)
Validates physical spontaneous Raman scattering (SpRS) modeling, effective non-linear interaction length (L_eff),
narrowband FBG optical filtering, signal-to-noise ratio (SNR), and detection of adversarial cross-talk jamming.
"""

import pytest
import numpy as np

from security.wdm import (
    WDMChannelConfig,
    WDMAnalysisResult,
    RamanScatteringModel,
    WDMRamanWatcher,
)
from security.detector import ThreatCategory


class TestWDMRamanWatchtower:
    """
    Unit and cryptanalytic tests for Phase 37 Q-WDM watchtower.
    """

    def test_honest_wdm_co_propagation_secure(self):
        """
        Tests that an honest WDM co-propagation channel (0 dBm / 1 mW classical power, 25 km SMF-28)
        with 20 nm wavelength separation and 0.08 nm FBG filtering achieves SNR >= 15.0
        and induced Raman QBER <= 4.5%, certifying secure co-propagation.
        """
        watcher = WDMRamanWatcher(target_min_snr=12.0, max_tolerable_raman_qber=0.05)
        result = watcher.simulate_wdm_scenario("Honest Co-Propagation (0 dBm Classical)", fiber_length_km=25.0)

        assert result.is_wdm_secure is True
        assert result.verdict == ThreatCategory.LEGITIMATE
        assert result.signal_to_noise_ratio_snr >= 15.0
        assert result.induced_raman_qber <= 0.045
        assert result.attack_classification == "LEGITIMATE_WDM_CO_PROPAGATION"
        assert result.optical_isolation_db > 50.0
        assert "certified secure" in result.cryptanalytic_proof

    def test_adversarial_cross_talk_jamming_detected(self):
        """
        Tests that an adversary injecting +14 dBm (25 mW) classical pump power
        collapses SNR (< 3.0) and drives induced Raman QBER up, triggering a MALICIOUS verdict.
        """
        watcher = WDMRamanWatcher()
        result = watcher.simulate_wdm_scenario("Adversarial Cross-Talk Jamming", fiber_length_km=25.0)

        assert result.is_wdm_secure is False
        assert result.verdict == ThreatCategory.MALICIOUS
        assert result.attack_classification == "ADVERSARIAL_CROSS_TALK_JAMMING"
        assert result.signal_to_noise_ratio_snr < 5.0
        assert "Adversarial cross-talk jamming detected" in result.cryptanalytic_proof

    def test_raman_scattering_saturation_detected(self):
        """
        Tests that high classical power (+8 dBm) at close channel spacing (10 nm)
        saturates the single-photon channel, causing excessive QBER.
        """
        watcher = WDMRamanWatcher()
        result = watcher.simulate_wdm_scenario("Raman Scattering Saturation", fiber_length_km=25.0)

        assert result.is_wdm_secure is False
        assert result.verdict == ThreatCategory.MALICIOUS
        assert result.attack_classification == "RAMAN_SCATTERING_SATURATION"
        assert result.induced_raman_qber > 0.05
        assert "Spontaneous Raman scattering saturation" in result.cryptanalytic_proof

    def test_effective_fiber_length_physics(self):
        """
        Tests physical properties of effective non-linear fiber length:
        L_eff = (1 - exp(-alpha * L)) / alpha
        - For L = 25 km with alpha = 0.20 dB/km: L_eff ~ 14.9 km (< 25 km).
        - For asymptotic L -> inf: L_eff -> 1 / alpha_lin ~ 21.7 km.
        """
        model = RamanScatteringModel()
        l_eff_25 = model.compute_effective_length(25.0, 0.20)
        l_eff_100 = model.compute_effective_length(100.0, 0.20)

        assert 14.0 < l_eff_25 < 16.0, f"Expected L_eff ~ 14.9 km, got {l_eff_25}"
        assert 20.0 < l_eff_100 < 22.0, f"Expected L_eff ~ 21.7 km asymptotic limit, got {l_eff_100}"
        assert l_eff_25 < l_eff_100 < 21.72

    def test_simulation_scenarios_diversity(self):
        """
        Validates that all simulation scenarios provided to the dashboard execute cleanly.
        """
        watcher = WDMRamanWatcher()

        res_honest = watcher.simulate_wdm_scenario("Honest Co-Propagation (0 dBm Classical)")
        assert res_honest.verdict == ThreatCategory.LEGITIMATE

        res_jam = watcher.simulate_wdm_scenario("Adversarial Cross-Talk Jamming")
        assert res_jam.verdict == ThreatCategory.MALICIOUS

        res_sat = watcher.simulate_wdm_scenario("Raman Scattering Saturation")
        assert res_sat.verdict == ThreatCategory.MALICIOUS

        res_noise = watcher.simulate_wdm_scenario("Elevated Co-Propagation Noise")
        assert res_noise.verdict in [ThreatCategory.SUSPICIOUS, ThreatCategory.LEGITIMATE]