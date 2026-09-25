"""
Test Suite for Stage 25 (Phase 46): MDI Selectable Session Mode & Untrusted Relay Watchtower

Verifies:
1. TRUSTED_DETECTOR vs MDI_RELAY session mode selection.
2. Honest MDI session achieves certified detector immunity and ThreatCategory.LEGITIMATE.
3. Untrusted relay tampering / distinguishable photon spoofing triggers ThreatCategory.MALICIOUS.
4. Coincidence error stream correctly maps to SequentialQStat Bernoulli trials.
5. Trust trade-off documentation integrity (Puthoor et al. 2016, Yin et al. 2017).
"""

import pytest
import numpy as np

from security.detector import ThreatCategory
from security.session_mode import SessionMode, SessionModeCoordinator, SessionModeResult
from security.mdi import MDIQuantumRelay, MDIEvent


class TestMDISessionMode:
    """Rigorous verification of MDI session coordinator and detector immunity guarantees."""

    def test_trusted_detector_session_pass(self):
        """Tests standard TRUSTED_DETECTOR verification session."""
        coord = SessionModeCoordinator(baseline_p0=0.03, alt_p1=0.20)
        # 100 legitimate trials
        trials = [0]*97 + [1]*3
        res = coord.verify_trusted_detector_session(trials)

        assert res.mode == SessionMode.TRUSTED_DETECTOR
        assert res.verdict == ThreatCategory.LEGITIMATE
        assert res.detector_immune is False
        assert "TRUSTED_DETECTOR Mode Active" in res.tradeoff_explanation

    def test_honest_mdi_session_certified_immune(self):
        """
        Tests honest MDI session through untrusted relay:
        Validates 100% detector side-channel immunity and ThreatCategory.LEGITIMATE.
        """
        coord = SessionModeCoordinator(baseline_p0=0.03, alt_p1=0.20)
        events = coord.generate_mdi_events("Honest Untrusted Relay", num_trials=500)
        res = coord.verify_mdi_session(events)

        assert res.mode == SessionMode.MDI_RELAY
        assert res.verdict == ThreatCategory.LEGITIMATE
        assert res.detector_immune is True
        assert res.mdi_analysis is not None
        assert res.mdi_analysis.hom_visibility >= 0.70
        assert "Puthoor et al. 2016" in res.tradeoff_explanation

    def test_untrusted_relay_tampering_caught(self):
        """
        Tests that an untrusted relay tampering with Bell-state announcements
        is caught and classified as MALICIOUS in MDI mode.
        """
        coord = SessionModeCoordinator(baseline_p0=0.03, alt_p1=0.20)
        events = coord.generate_mdi_events("Compromised Untrusted Relay", num_trials=500)
        res = coord.verify_mdi_session(events)

        assert res.mode == SessionMode.MDI_RELAY
        assert res.verdict == ThreatCategory.MALICIOUS
        assert res.mdi_analysis.z_basis_error_rate > 0.08
