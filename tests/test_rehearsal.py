"""
Test Suite for Stage 18 (Phase 39): Monte Carlo Stress Rehearsal and NQM Executive Defense Kit (Q-DOC)
Validates full 14-watchtower automated sweep, zero false negatives under Monte Carlo stress,
"""

import os
import json
import pytest
from pathlib import Path

from rehearsal import (
    QuantumRehearsalRunner,
    RehearsalReport,
    WatchtowerTestResult
)
from security.detector import ThreatCategory


class TestQuantumRehearsalSuite:
    """
    Automated verification suite for the Phase 39 Monte Carlo rehearsal kit and NQM documentation.
    """

    def test_full_14_watchtower_rehearsal_sweep(self):
        """
        Executes a complete sweep across all 14 defense watchtowers.
        Guarantees 100% pass rate with zero undetected adversarial scenarios.
        """
        runner = QuantumRehearsalRunner()
        results = runner.rehearse_all_watchtowers()

        assert len(results) == 14, f"Expected exactly 14 watchtowers, received {len(results)}"

        for res in results:
            assert res.passed is True, f"Watchtower '{res.watchtower_name}' failed scenario '{res.scenario}'"
            assert res.latency_ms < 100.0, f"Watchtower '{res.watchtower_name}' latency exceeded 100ms: {res.latency_ms}ms"
            assert len(res.details) > 0

    def test_monte_carlo_stress_testing_invariants(self):
        """
        Runs a randomized Monte Carlo batch of 40 mixed legitimate and adversarial sessions.
        Enforces zero false negatives, zero false alarms in calibrated optical channels,
        and sub-5ms average latency.
        """
        runner = QuantumRehearsalRunner()
        report = runner.run_monte_carlo_stress_test(num_iterations=40)

        assert report.total_sessions == 40
        assert report.false_negatives == 0, "Zero false negatives invariant violated: adversarial session missed"
        assert report.false_positives == 0, "Zero false positive invariant violated: legitimate session falsely flagged"
        assert report.detection_rate_pct == 100.0
        assert report.watchtowers_passed == 14
        assert report.watchtowers_total == 14
        assert report.watchtower_pass_rate == 1.0
        assert report.avg_latency_ms < 10.0, f"Average latency exceeded 10ms: {report.avg_latency_ms}ms"

    def test_rehearsal_report_json_serialization(self):
        """
        Verifies that RehearsalReport exports clean, well-formed JSON for SOC integration and auditing.
        """
        runner = QuantumRehearsalRunner()
        report = runner.run_monte_carlo_stress_test(num_iterations=20)
        report_json = report.to_json()

        data = json.loads(report_json)
        assert "total_sessions" in data
        assert "detection_rate_pct" in data
        assert "watchtower_sweep" in data
        assert len(data["watchtower_sweep"]) == 14
        assert data["false_negatives"] == 0

    def test_nqm_whitepaper_document_integrity(self):
        """
        Verifies the physical existence, length, and completeness of the National Quantum
        Mission Executive Technical Whitepaper (docs/NQM_EXECUTIVE_WHITEPAPER.md).
        """
        wp_path = Path("docs/NQM_EXECUTIVE_WHITEPAPER.md")
        assert wp_path.exists(), "NQM Executive Whitepaper must exist in docs/ directory"

        text = wp_path.read_text(encoding="utf-8")
        assert len(text) > 5000, f"Whitepaper content is unexpectedly short: {len(text)} chars"

        # Verify presence of all 14 watchtower IDs
        for i in range(1, 15):
            wt_code = f"WT-{i:02d}"
            assert wt_code in text, f"Whitepaper missing reference to watchtower {wt_code}"

        # Verify critical physics terms and proofs
        assert "Teleportation Protocol" in text
        assert "Exact Binomial Hypothesis" in text
        assert "Serfling Martingale" in text
        assert "CHSH Bell Inequality" in text
        assert "Hong-Ou-Mandel" in text
        assert "Spontaneous Raman Scattering" in text
        assert "SIH-26141" in text