"""
Test Suite for Stage 24 (Phase 45): Blind Red-Team Evaluation Harness & Boundary Verification

Verifies:
1. RedTeamEvaluationHarness synthetic session generation across all attack scenarios.
2. Grid evaluation and ASN metric calculations.
3. Empirical ROC curve generation and CSV export.
4. Boundary discipline: security/ packages never import from evaluation/.
"""

import os
import ast
from pathlib import Path
import pytest

from security.attacks import AttackScenario
from evaluation.harness import RedTeamEvaluationHarness, GridCellResult, ROCPoint


class TestRedTeamEvaluationHarness:
    """Verifies adversarial grid execution and boundary discipline."""

    def test_one_way_boundary_discipline(self):
        """
        Validates that security/sequential.py and security/streaming.py
        contain ZERO imports of evaluation/ packages.
        """
        workspace_root = Path(__file__).resolve().parent.parent
        sequential_path = workspace_root / "security" / "sequential.py"
        streaming_path = workspace_root / "security" / "streaming.py"

        for file_path in (sequential_path, streaming_path):
            assert file_path.exists(), f"File {file_path} missing"
            tree = ast.parse(file_path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        assert not alias.name.startswith("evaluation"), (
                            f"Illegal import {alias.name} found in {file_path}"
                        )
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        assert not node.module.startswith("evaluation"), (
                            f"Illegal import from {node.module} in {file_path}"
                        )

    def test_synthetic_session_generation_scenarios(self):
        """Verifies session generator for legitimate and attack scenarios."""
        harness = RedTeamEvaluationHarness(session_length=50)

        # Legitimate session
        trials_legit, is_attack_legit = harness.generate_synthetic_session(
            AttackScenario.LEGITIMATE, severity=0.0, duty_cycle=1.0
        )
        assert len(trials_legit) == 50
        assert not is_attack_legit

        # Forgery session (duty_cycle = 0.50)
        trials_forge, is_attack_forge = harness.generate_synthetic_session(
            AttackScenario.FORGERY, severity=0.50, duty_cycle=0.50
        )
        assert len(trials_forge) == 50
        assert is_attack_forge
        # In a 50% duty-cycle forgery session, there must be error trials
        assert sum(trials_forge) > sum(trials_legit)

    def test_grid_evaluation_and_asn_savings(self):
        """Tests that evaluate_cell computes ASN reduction and detection rate."""
        harness = RedTeamEvaluationHarness(session_length=100)

        result = harness.evaluate_cell(
            scenario=AttackScenario.FORGERY,
            severity=0.50,
            duty_cycle=1.0,
            n_sessions=10
        )
        assert isinstance(result, GridCellResult)
        assert result.true_positive_rate == 1.0
        assert result.mean_detection_delay_trials < 30.0
        assert result.asn_reduction_pct > 70.0

    def test_roc_curve_generation_and_csv_export(self, tmp_path):
        """Tests empirical ROC curve calculation and CSV persistence."""
        results_dir = str(tmp_path / "results")
        harness = RedTeamEvaluationHarness(session_length=40, results_dir=results_dir)

        roc_points = harness.compute_roc_curve(n_evals=20)
        assert len(roc_points) > 0
        assert all(isinstance(p, ROCPoint) for p in roc_points)

        # Assert CSV created
        csv_file = os.path.join(results_dir, "roc_curve.csv")
        assert os.path.exists(csv_file)
        assert os.path.getsize(csv_file) > 50
