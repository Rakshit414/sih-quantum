"""
Q-Sentinel: Blind Red-Team Adversarial Evaluation Harness
Stage 24: Phase 45

Implements an automated, rigorous adversarial evaluation grid:
Grid Dimensions:
1. AttackScenario: LEGITIMATE, FORGERY, IMPERSONATION, REPLAY, CHANNEL_NOISE
2. Severity (error-rate delta above p0): [0.02, 0.05, 0.10, 0.20, 0.35, 0.50]
3. Duty Cycle (fraction of session under active attack): [1.0, 0.50, 0.25, 0.15, 0.05]

Computes:
- Empirical ROC curve (sweeping decision threshold, evaluating True Positive Rate vs False Positive Rate)
- Detection delay distribution (trials required until decision / alarm)
- Average Sample Number (ASN) savings compared to fixed-sample batch tests
- Exports metrics to evaluation/results/grid_metrics.csv
"""

from __future__ import annotations
import os
import csv
import time
import math
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Tuple, Optional
import numpy as np

from security.attacks import AttackScenario
from security.detector import ThreatCategory
from security.sequential import SequentialQStat, SequentialVerdict
from security.streaming import MultiArmFusion


@dataclass
class GridCellResult:
    """Evaluation metrics for a specific (scenario, severity, duty_cycle) parameter cell."""
    scenario: str
    severity: float
    duty_cycle: float
    n_sessions: int
    true_positive_rate: float
    false_alarm_rate: float
    mean_detection_delay_trials: float
    median_detection_delay_trials: float
    asn_reduction_pct: float
    mean_posterior_error: float


@dataclass
class ROCPoint:
    """Individual empirical ROC coordinate."""
    threshold: float
    fpr: float
    tpr: float


class RedTeamEvaluationHarness:
    """
    Parametric adversarial stress evaluation harness testing sequential detection performance.
    """

    def __init__(
        self,
        baseline_p0: float = 0.03,
        alt_p1: float = 0.20,
        session_length: int = 100,
        results_dir: str = "evaluation/results"
    ):
        self.baseline_p0 = float(baseline_p0)
        self.alt_p1 = float(alt_p1)
        self.session_length = int(session_length)
        self.results_dir = results_dir
        os.makedirs(self.results_dir, exist_ok=True)

        self.severities = [0.02, 0.05, 0.10, 0.20, 0.35, 0.50]
        self.duty_cycles = [1.0, 0.50, 0.25, 0.15, 0.05]
        self.scenarios = [
            AttackScenario.LEGITIMATE,
            AttackScenario.FORGERY,
            AttackScenario.IMPERSONATION,
            AttackScenario.REPLAY,
            AttackScenario.CHANNEL_NOISE
        ]

    def generate_synthetic_session(
        self,
        scenario: AttackScenario,
        severity: float,
        duty_cycle: float
    ) -> Tuple[List[int], bool]:
        """
        Generates a sequence of Bernoulli trials for an individual session.
        Returns:
            trial_outcomes: List of {0, 1} outcomes.
            is_attack: True if session contains adversarial tampering, False if honest.
        """
        is_attack = (scenario != AttackScenario.LEGITIMATE)
        trials = np.zeros(self.session_length, dtype=int)

        # Baseline noise floor across whole session
        trials[:] = np.random.choice([0, 1], size=self.session_length, p=[1 - self.baseline_p0, self.baseline_p0])

        if is_attack:
            attack_len = max(1, int(round(self.session_length * duty_cycle)))
            # Compute attack error rate
            if scenario in (AttackScenario.FORGERY, AttackScenario.IMPERSONATION):
                p_attack = min(0.99, max(0.01, 0.50))
            elif scenario == AttackScenario.CHANNEL_NOISE:
                p_attack = min(0.99, max(0.01, self.baseline_p0 + severity))
            elif scenario == AttackScenario.REPLAY:
                # Replay has baseline physical errors plus stale timestamp
                p_attack = min(0.99, max(0.01, self.baseline_p0 + 0.10))
            else:
                p_attack = min(0.99, max(0.01, self.baseline_p0 + severity))

            # Pick random contiguous attack window
            max_start = max(0, self.session_length - attack_len)
            start_idx = np.random.randint(0, max_start + 1) if max_start > 0 else 0
            attack_slice = slice(start_idx, start_idx + attack_len)
            trials[attack_slice] = np.random.choice([0, 1], size=attack_len, p=[1 - p_attack, p_attack])

        return trials.tolist(), is_attack

    def evaluate_cell(
        self,
        scenario: AttackScenario,
        severity: float,
        duty_cycle: float,
        n_sessions: int = 25
    ) -> GridCellResult:
        """
        Evaluates detector performance for a single grid parameter configuration.
        """
        delays: List[int] = []
        alarms: List[bool] = []
        is_attack = (scenario != AttackScenario.LEGITIMATE)

        for _ in range(n_sessions):
            trials, _ = self.generate_synthetic_session(scenario, severity, duty_cycle)
            detector = SequentialQStat(baseline_p0=self.baseline_p0, alt_p1=self.alt_p1)
            
            alarm_triggered = False
            delay = self.session_length

            for idx, trial in enumerate(trials, start=1):
                verdict = detector.update(trial)
                if verdict.verdict == ThreatCategory.MALICIOUS:
                    alarm_triggered = True
                    delay = idx
                    break

            alarms.append(alarm_triggered)
            delays.append(delay)

        if is_attack:
            tpr = float(np.mean(alarms))
            far = 0.0
        else:
            tpr = 0.0
            far = float(np.mean(alarms))

        mean_delay = float(np.mean(delays))
        median_delay = float(np.median(delays))
        asn_reduction = float(max(0.0, (1.0 - (mean_delay / self.session_length)) * 100.0))

        return GridCellResult(
            scenario=scenario.value,
            severity=severity,
            duty_cycle=duty_cycle,
            n_sessions=n_sessions,
            true_positive_rate=round(tpr, 4),
            false_alarm_rate=round(far, 4),
            mean_detection_delay_trials=round(mean_delay, 2),
            median_detection_delay_trials=round(median_delay, 2),
            asn_reduction_pct=round(asn_reduction, 2),
            mean_posterior_error=round(self.baseline_p0 + (severity if is_attack else 0.0), 4)
        )

    def run_full_grid(self, n_sessions_per_cell: int = 15) -> List[GridCellResult]:
        """
        Executes full adversarial grid sweep and exports results to CSV.
        """
        results: List[GridCellResult] = []

        # 1. Legitimate baseline cell
        legit_res = self.evaluate_cell(AttackScenario.LEGITIMATE, severity=0.0, duty_cycle=1.0, n_sessions=n_sessions_per_cell*2)
        results.append(legit_res)

        # 2. Attack scenario sweeps
        attack_scenarios = [s for s in self.scenarios if s != AttackScenario.LEGITIMATE]
        for sc in attack_scenarios:
            for sev in self.severities:
                for dc in self.duty_cycles:
                    cell_res = self.evaluate_cell(sc, severity=sev, duty_cycle=dc, n_sessions=n_sessions_per_cell)
                    results.append(cell_res)

        self.export_results_csv(results)
        return results

    def compute_roc_curve(self, n_evals: int = 200) -> List[ROCPoint]:
        """
        Computes empirical ROC curve points by sweeping CUSUM threshold h from 2.0 to 18.0.
        """
        thresholds = np.linspace(2.0, 18.0, 15)
        roc_points: List[ROCPoint] = []

        # Pre-generate 100 legitimate and 100 attack sessions
        legit_sessions = [self.generate_synthetic_session(AttackScenario.LEGITIMATE, 0.0, 1.0)[0] for _ in range(n_evals // 2)]
        attack_sessions = [self.generate_synthetic_session(AttackScenario.CHANNEL_NOISE, 0.15, 0.25)[0] for _ in range(n_evals // 2)]

        for h in thresholds:
            # Measure FPR under H0
            false_alarms = 0
            for trials in legit_sessions:
                det = SequentialQStat(baseline_p0=self.baseline_p0, alt_p1=self.alt_p1, cusum_threshold_h=h)
                for t in trials:
                    if det.update(t).cusum_stat >= h:
                        false_alarms += 1
                        break
            fpr = false_alarms / len(legit_sessions)

            # Measure TPR under H1
            true_positives = 0
            for trials in attack_sessions:
                det = SequentialQStat(baseline_p0=self.baseline_p0, alt_p1=self.alt_p1, cusum_threshold_h=h)
                for t in trials:
                    if det.update(t).cusum_stat >= h:
                        true_positives += 1
                        break
            tpr = true_positives / len(attack_sessions)

            roc_points.append(ROCPoint(threshold=round(float(h), 2), fpr=round(fpr, 4), tpr=round(tpr, 4)))

        # Export ROC CSV
        roc_path = os.path.join(self.results_dir, "roc_curve.csv")
        with open(roc_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["threshold", "fpr", "tpr"])
            writer.writeheader()
            for p in roc_points:
                writer.writerow(asdict(p))

        return roc_points

    def export_results_csv(self, results: List[GridCellResult], filename: str = "grid_metrics.csv") -> str:
        """
        Exports evaluation results to disk in CSV format.
        """
        filepath = os.path.join(self.results_dir, filename)
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            if results:
                writer = csv.DictWriter(f, fieldnames=list(asdict(results[0]).keys()))
                writer.writeheader()
                for r in results:
                    writer.writerow(asdict(r))
        return filepath
