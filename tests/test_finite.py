"""
Test Suite for Stage 14 (Phase 35): Finite-Size Security Analysis & Serfling Bound Watchtower (Q-FINITE)
Validates Serfling Martingale large-deviation bound, smooth min-entropy privacy amplification penalty,
finite-block starvation detection, and composable epsilon-security (eps <= 10^-10).
"""

import pytest
import numpy as np

from security.finite import (
    FiniteKeyParameters,
    FiniteSecurityResult,
    FiniteSizeSecurityAnalyzer,
)
from security.detector import ThreatCategory


class TestFiniteSizeSecurityAnalyzer:
    """
    Unit and cryptanalytic tests for Phase 35 Q-FINITE watchtower.
    """

    def test_honest_production_finite_block_secure(self):
        """
        Tests that an honest production session with sufficient block size (N = 1600, n = 533)
        and nominal error rate (~2.5%) yields certified positive extractable signature length
        with composable security epsilon <= 10^-10.
        """
        analyzer = FiniteSizeSecurityAnalyzer(f_ec=1.16, target_epsilon_sec=1e-10)

        # 1600 total qubits, 533 sampled for parameter estimation, 13 errors (~2.4%)
        params = FiniteKeyParameters(
            total_qubits_N=1600,
            sample_qubits_n=533,
            observed_sample_errors=13,
            target_epsilon_sec=1e-10
        )

        result = analyzer.evaluate_session_security(params)

        assert result.is_composably_secure is True
        assert result.verdict == ThreatCategory.LEGITIMATE
        assert result.extractable_signature_length > 0
        assert result.distillation_rate > 0.0
        assert result.composable_epsilon <= 1e-10
        assert result.attack_classification == "COMPOSABLY_SECURE_FINITE_SESSION"
        assert "Composable finite-key security certified" in result.cryptanalytic_proof

    def test_finite_block_size_starvation(self):
        """
        Tests that a session with very small block size (N = 200, n = 60)
        cannot extract secret signature bits even with low physical error (e ~ 1.6%)
        because finite-sampling Serfling penalties exhaust the raw length.
        """
        analyzer = FiniteSizeSecurityAnalyzer(f_ec=1.16, target_epsilon_sec=1e-10)

        params = FiniteKeyParameters(
            total_qubits_N=200,
            sample_qubits_n=60,
            observed_sample_errors=1,  # 1.6% physical error
            target_epsilon_sec=1e-10
        )

        result = analyzer.evaluate_session_security(params)

        assert result.is_composably_secure is False
        assert result.extractable_signature_length == 0
        assert result.verdict == ThreatCategory.SUSPICIOUS
        assert result.attack_classification == "FINITE_BLOCK_SIZE_STARVATION"
        assert "Finite-size block starvation" in result.cryptanalytic_proof

    def test_excessive_disturbance_finite_collapse(self):
        """
        Tests that high adversarial noise (e.g. 14% QBER) on a finite block
        causes upper bound phase error to exceed the distillation threshold, triggering MALICIOUS.
        """
        analyzer = FiniteSizeSecurityAnalyzer(f_ec=1.16, max_tolerable_error=0.11)

        params = FiniteKeyParameters(
            total_qubits_N=1600,
            sample_qubits_n=533,
            observed_sample_errors=75,  # 14% error
            target_epsilon_sec=1e-10
        )

        result = analyzer.evaluate_session_security(params)

        assert result.is_composably_secure is False
        assert result.extractable_signature_length == 0
        assert result.upper_bound_phase_error > 0.11
        assert result.verdict == ThreatCategory.MALICIOUS
        assert result.attack_classification == "FINITE_SIZE_SECURITY_COLLAPSE"
        assert "Finite-size security failure" in result.cryptanalytic_proof

    def test_serfling_deviation_properties(self):
        """
        Verifies mathematical properties of Serfling's inequality:
        As sample size n increases for a fixed block size N, deviation cutoff xi decreases monotonically.
        """
        analyzer = FiniteSizeSecurityAnalyzer()

        xi_100 = analyzer.compute_serfling_deviation(total_N=2000, sample_n=100)
        xi_500 = analyzer.compute_serfling_deviation(total_N=2000, sample_n=500)
        xi_1000 = analyzer.compute_serfling_deviation(total_N=2000, sample_n=1000)

        assert xi_100 > xi_500 > xi_1000, "Serfling deviation must decrease monotonically with sample size"
        assert 0.0 < xi_1000 < 0.15

    def test_simulation_scenarios_diversity(self):
        """
        Validates all simulation scenarios provided to the dashboard.
        """
        analyzer = FiniteSizeSecurityAnalyzer()

        res_honest = analyzer.simulate_finite_scenario("Honest Production Block", block_size_n=1800)
        assert res_honest.verdict == ThreatCategory.LEGITIMATE
        assert res_honest.extractable_signature_length > 0

        res_starve = analyzer.simulate_finite_scenario("Starvation Small Block")
        assert res_starve.verdict == ThreatCategory.SUSPICIOUS
        assert res_starve.extractable_signature_length == 0

        res_attack = analyzer.simulate_finite_scenario("Adversary Disturbance", block_size_n=1800)
        assert res_attack.verdict == ThreatCategory.MALICIOUS
        assert res_attack.extractable_signature_length == 0
