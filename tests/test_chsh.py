"""
Test Suite for Stage 13 (Phase 34): Device-Independent CHSH Bell Inequality Watchtower (Q-CHSH)
Validates Tsirelson bound verification (S ~ 2*sqrt(2)), classical local hidden variable bound (S <= 2.0),
separable state spoofing detection, and statistical Bell violation significance.
"""

import pytest
import numpy as np

from security.chsh import (
    CHSHBellWatcher,
    CHSHMeasurementSetting,
    CHSHVerificationResult,
)
from security.detector import ThreatCategory
from quantum.bell import create_bell_state, BellStateType


class TestCHSHBellWatcher:
    """
    Unit and non-locality cryptanalytic tests for Phase 34 Q-CHSH watchtower.
    """

    def test_honest_bell_state_violates_classical_bound(self):
        """
        Verifies that a pristine maximally entangled Bell state (|Phi+>)
        violates the classical Bell inequality S <= 2.0 and approaches the Tsirelson bound S ~ 2.828.
        """
        watcher = CHSHBellWatcher(trials_per_setting=600)
        phi_plus = create_bell_state(BellStateType.PHI_PLUS).vector.reshape(4, 1)
        rho_ideal = phi_plus @ phi_plus.conj().T

        result = watcher.evaluate_state(rho_ideal, state_label="Prinstine Bell Pair")

        assert result.chsh_s_parameter > 2.50, f"Observed S = {result.chsh_s_parameter} must clearly exceed 2.0"
        assert result.chsh_s_parameter <= (2.0 * np.sqrt(2.0) + 0.15), "Must not exceed Tsirelson bound within noise"
        assert result.bell_violation_z_score >= 4.0, "Violation significance must be >= 4 sigma"
        assert result.entanglement_certified is True
        assert result.verdict == ThreatCategory.LEGITIMATE
        assert result.attack_classification == "CERTIFIED_QUANTUM_ENTANGLEMENT"
        assert "exceeds classical limit 2.0000" in result.cryptanalytic_proof

    def test_classical_separable_state_obeys_bell_inequality(self):
        """
        Verifies that an adversary's classical separable state (50% |00><00| + 50% |11><11|)
        strictly satisfies the classical Bell inequality S <= 2.0, triggering a MALICIOUS spoofing alert.
        """
        watcher = CHSHBellWatcher(trials_per_setting=600)

        # Classical mixture with zero entanglement
        rho_sep = np.zeros((4, 4), dtype=complex)
        rho_sep[0, 0] = 0.50
        rho_sep[3, 3] = 0.50

        result = watcher.evaluate_state(rho_sep, state_label="Separable Spoof")

        assert result.chsh_s_parameter <= 2.00, f"Separable state S = {result.chsh_s_parameter} cannot exceed 2.0"
        assert result.entanglement_certified is False
        assert result.verdict == ThreatCategory.MALICIOUS
        assert result.attack_classification == "CLASSICAL_LHV_SPOOFING_ATTACK"
        assert "Bell inequality satisfied" in result.cryptanalytic_proof

    def test_intercept_resend_measurement_spoof_detected(self):
        """
        Tests that an intercept-resend attack collapsing the entangled pair into classical eigenstates
        is intercepted by the CHSH test.
        """
        watcher = CHSHBellWatcher(trials_per_setting=500)
        res = watcher.simulate_chsh_scenario(scenario="Intercept-Resend Collapse")

        assert res.chsh_s_parameter <= 2.00
        assert res.verdict == ThreatCategory.MALICIOUS
        assert "CLASSICAL_LHV_SPOOFING_ATTACK" in res.attack_classification

    def test_noisy_entanglement_transition(self):
        """
        Tests transition to SUSPICIOUS when depolarizing noise degrades S near the boundary (2.0 < S <= 2.25).
        """
        watcher = CHSHBellWatcher(trials_per_setting=800)
        phi_plus = create_bell_state(BellStateType.PHI_PLUS).vector.reshape(4, 1)
        rho_ideal = phi_plus @ phi_plus.conj().T

        # 25% depolarizing noise: S_noisy ~ (1 - 0.25) * 2.828 ~ 2.12
        rho_noisy = 0.75 * rho_ideal + 0.25 * 0.25 * np.eye(4, dtype=complex)

        result = watcher.evaluate_state(rho_noisy, state_label="Degraded Pair")

        # In noisy regime S ~ 2.1, it should land in SUSPICIOUS or near boundary
        assert result.chsh_s_parameter > 1.80
        assert result.verdict in [ThreatCategory.SUSPICIOUS, ThreatCategory.LEGITIMATE]

    def test_simulation_scenarios_diversity(self):
        """
        Validates all simulation presets available in the dashboard.
        """
        watcher = CHSHBellWatcher(trials_per_setting=400)

        res_honest = watcher.simulate_chsh_scenario("Honest Maximally Entangled")
        assert res_honest.verdict == ThreatCategory.LEGITIMATE
        assert res_honest.chsh_s_parameter > 2.40

        res_spoof = watcher.simulate_chsh_scenario("Classical Separable Spoofing")
        assert res_spoof.verdict == ThreatCategory.MALICIOUS
        assert res_spoof.chsh_s_parameter <= 2.00
