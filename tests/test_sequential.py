"""
Test Suite for Stage 21 (Phase 42): Sequential Threat Detection Engine (SequentialQStat)

Verifies:
1. Legitimate session stability: zero false alarms across >= 500 trials under baseline noise p0=0.03.
2. Forgery attack detection: rapid low-double-digit trial catch rate under ~48% error.
3. Sub-threshold / intermittent attack detection: empirical recall measurement under ~15% duty-cycle attack.
4. Mathematical properties: Beta-Binomial credible interval, CUSUM accumulation, and Wald SPRT decision rules.
"""

import pytest
import numpy as np
from security.detector import ThreatCategory
from security.sequential import (
    SequentialQStat,
    SequentialVerdict,
    SequentialSessionReport,
    evaluate_sequential_session
)


class TestSequentialQStat:
    """Unit tests for SequentialQStat mathematical correctness and operational invariants."""

    def test_legitimate_session_no_false_alarm(self):
        """
        Under calibrated baseline noise p0=0.03, the detector must NOT trigger
        a false alarm across >= 500 sequential trials at default thresholds.
        """
        np.random.seed(42)
        detector = SequentialQStat(baseline_p0=0.03, alt_p1=0.20)
        
        # Simulate 500 honest trials with Bernoulli(p=0.03)
        trials = np.random.choice([0, 1], size=500, p=[0.97, 0.03])
        
        for idx, trial in enumerate(trials, start=1):
            verdict = detector.update(int(trial))
            # CUSUM and SPRT must not trigger MALICIOUS false alarm
            assert verdict.verdict != ThreatCategory.MALICIOUS, (
                f"False alarm triggered at trial {idx}: trigger={verdict.trigger}, "
                f"cusum={verdict.cusum_stat}, sprt_llr={verdict.sprt_llr}"
            )

    def test_forgery_attack_low_double_digit_detection(self):
        """
        Under forgery attack (~48% error rate), SequentialQStat must detect MALICIOUS
        within a low-double-digit number of trials (strictly < 25 trials).
        """
        np.random.seed(1337)
        detector = SequentialQStat(baseline_p0=0.03, alt_p1=0.20)
        
        # Simulate forgery trials with Bernoulli(p=0.48)
        trials = np.random.choice([0, 1], size=100, p=[0.52, 0.48])
        
        detection_trial = None
        for idx, trial in enumerate(trials, start=1):
            verdict = detector.update(int(trial))
            if verdict.verdict == ThreatCategory.MALICIOUS:
                detection_trial = idx
                break

        assert detection_trial is not None, "Forgery attack failed to be detected within 100 trials"
        assert detection_trial < 25, f"Detection took {detection_trial} trials, expected < 25 trials"
        assert verdict.trigger in ("CUSUM", "SPRT")

    def test_subthreshold_intermittent_attack_recall(self):
        """
        Evaluates sub-threshold / intermittent attack scenario:
        Attack is active for only ~15% of session trials (e.g. 30 out of 200 trials),
        introducing localized tampering. Measures and asserts empirical recall >= 85%.
        """
        np.random.seed(2026)
        n_sessions = 100
        session_length = 200
        detected_count = 0

        for _ in range(n_sessions):
            detector = SequentialQStat(baseline_p0=0.03, alt_p1=0.20)
            
            # Baseline noise for 85% of trials, attack (p=0.45) for 15% of trials
            session_trials = np.zeros(session_length, dtype=int)
            # 85% legitimate background
            background_indices = np.arange(session_length)
            # 15% attack window (30 contiguous trials or random burst)
            attack_start = np.random.randint(20, session_length - 40)
            attack_range = slice(attack_start, attack_start + 30)
            
            # Populate background with p0=0.03
            session_trials[:] = np.random.choice([0, 1], size=session_length, p=[0.97, 0.03])
            # Inject burst attack with p=0.45
            session_trials[attack_range] = np.random.choice([0, 1], size=30, p=[0.55, 0.45])

            detected = False
            for t in session_trials:
                v = detector.update(int(t))
                if v.verdict == ThreatCategory.MALICIOUS:
                    detected = True
                    break
            if detected:
                detected_count += 1

        empirical_recall = detected_count / n_sessions
        # Report the exact empirical recall measured
        print(f"\n[MEASURED] Sub-threshold 15% duty-cycle empirical recall: {empirical_recall*100:.1f}%")
        assert empirical_recall >= 0.85, (
            f"Expected empirical recall >= 85%, measured {empirical_recall*100:.1f}%"
        )

    def test_beta_binomial_posterior_and_reset(self):
        """Verifies Bayesian posterior updating and detector reset functionality."""
        detector = SequentialQStat(baseline_p0=0.03, alt_p1=0.20, prior_concentration=20.0)
        assert detector.alpha == pytest.approx(0.6, abs=1e-3)
        assert detector.beta == pytest.approx(19.4, abs=1e-3)

        # Ingest 10 error-free trials
        for _ in range(10):
            detector.update(0)

        assert detector.n_trials == 10
        assert detector.error_count == 0
        assert detector.alpha == pytest.approx(0.6, abs=1e-3)
        assert detector.beta == pytest.approx(29.4, abs=1e-3)
        
        # Reset restores initial state
        detector.reset()
        assert detector.n_trials == 0
        assert detector.cusum_stat == 0.0
        assert detector.sprt_llr == 0.0

    def test_sequential_session_wrapper(self):
        """Verifies evaluate_sequential_session integration wrapper."""
        trials = [0]*30 + [1]*15 + [0]*10
        report = evaluate_sequential_session(
            trial_outcomes=trials,
            baseline_p0=0.03,
            alt_p1=0.20,
            early_stop_on_decision=True
        )
        assert report.total_trials == len(trials)
        assert report.early_stopped is True
        assert report.trials_to_decision < len(trials)
        assert report.confirmatory_assessment is not None
        assert "Sequential Verdict" in report.diagnostic_summary
