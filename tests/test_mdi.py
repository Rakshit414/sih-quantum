"""
Test Suite for Stage 15 (Phase 36): Measurement-Device-Independent (MDI) QDS & Untrusted Relay Watchtower (Q-MDI)
Validates Hong-Ou-Mandel two-photon interference visibility, symmetric coincidence prohibition (Z-error),
untrusted relay tampering detection, distinguishable photon spoofing, and detector side-channel immunity.
"""

import pytest
import numpy as np

from security.mdi import (
    MDIEvent,
    MDIAnalysisResult,
    MDIQuantumRelay,
    MDIRelayWatcher,
)
from security.detector import ThreatCategory


class TestMDIQuantumRelayWatchtower:
    """
    Unit and cryptanalytic tests for Phase 36 Q-MDI watchtower.
    """

    def test_honest_untrusted_relay_certified(self):
        """
        Tests that an honest untrusted relay yields high HOM visibility (V_HOM >= 70%)
        and low forbidden coincidence rate (e_Z <= 8%), certifying relay honesty
        and confirming detector side-channel immunity.
        """
        watcher = MDIRelayWatcher(min_hom_visibility=0.70, max_z_error_rate=0.08)
        result = watcher.simulate_mdi_session("Honest Untrusted Relay", num_trials=1200)

        assert result.detector_immune is True
        assert result.verdict == ThreatCategory.LEGITIMATE
        assert result.hom_visibility >= 0.70
        assert result.z_basis_error_rate <= 0.08
        assert result.attack_classification == "CERTIFIED_MDI_RELAY_HONEST"
        assert "Untrusted relay verified honest" in result.cryptanalytic_proof

    def test_distinguishable_photon_spoof_malicious(self):
        """
        Tests that distinguishable photon injection causes HOM interference collapse
        (V_HOM < 40%), resulting in a MALICIOUS verdict with DISTINGUISHABLE_PHOTON_SPOOF classification.
        """
        watcher = MDIRelayWatcher(min_hom_visibility=0.70, max_z_error_rate=0.08)
        result = watcher.simulate_mdi_session("Distinguishable Photon Spoofing", num_trials=1200)

        assert result.verdict == ThreatCategory.MALICIOUS
        assert result.hom_visibility < 0.40
        assert result.attack_classification == "DISTINGUISHABLE_PHOTON_SPOOF"
        assert "Two-photon interference collapsed" in result.cryptanalytic_proof

    def test_untrusted_relay_tampering_malicious(self):
        """
        Tests that an untrusted relay fabricating coincidence announcements exhibits
        elevated symmetric state error rate (e_Z > 8%), triggering MALICIOUS verdict.
        """
        watcher = MDIRelayWatcher(min_hom_visibility=0.70, max_z_error_rate=0.08)
        result = watcher.simulate_mdi_session("Compromised Untrusted Relay", num_trials=1200)

        assert result.verdict == ThreatCategory.MALICIOUS
        assert result.z_basis_error_rate > 0.08
        assert result.attack_classification == "UNTRUSTED_RELAY_TAMPERING"
        assert "Forbidden symmetric coincidence error" in result.cryptanalytic_proof

    def test_hong_ou_mandel_coincidence_physics(self):
        """
        Tests underlying Hong-Ou-Mandel physics simulation:
        - Symmetric states (|00>) exhibit near-zero coincidences due to photon bunching.
        - Anti-symmetric states (|01>) exhibit high coincidence rates ~ 46% (with nominal V_HOM=0.92).
        """
        relay = MDIQuantumRelay(nominal_hom_visibility=0.95, dark_count_prob=1e-4)

        # 500 symmetric trials |00>
        sym_clicks = sum(
            relay.simulate_bsm_trial(alice_bit=0, alice_basis='Z', bob_bit=0, bob_basis='Z')
            for _ in range(500)
        )
        # 500 anti-symmetric trials |01>
        anti_clicks = sum(
            relay.simulate_bsm_trial(alice_bit=0, alice_basis='Z', bob_bit=1, bob_basis='Z')
            for _ in range(500)
        )

        sym_rate = sym_clicks / 500.0
        anti_rate = anti_clicks / 500.0

        assert sym_rate < 0.05, f"Symmetric coincidence rate should be suppressed (<5%), got {sym_rate}"
        assert anti_rate > 0.35, f"Anti-symmetric coincidence rate should be high (>35%), got {anti_rate}"

    def test_empty_events_raises_error(self):
        """
        Tests that passing an empty list of MDI events raises ValueError.
        """
        watcher = MDIRelayWatcher()
        with pytest.raises(ValueError, match="at least 1 trial"):
            watcher.analyze_mdi_session([])