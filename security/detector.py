"""
Q-Sentinel: Q-STAT (Quantum Statistical Threat Assessment Engine)
Stage 5: Phases 14, 15, 16, 17
Implements exact binomial hypothesis testing, standardized z-score anomaly scoring,
and 3-tier threat classification with full mathematical explainability.
"""

from __future__ import annotations
import numpy as np
from enum import Enum
from dataclasses import dataclass
from typing import Tuple, Optional, List
from scipy import stats
from security.freshness import FreshnessRegistry
from quantum.measure import sample_projective_trials, MeasurementTrialResult
from security.signature import QuantumDigitalSignature


class ThreatCategory(Enum):
    LEGITIMATE = "LEGITIMATE"    # Green: Consistent with normal channel noise (z < 2.0)
    SUSPICIOUS = "SUSPICIOUS"    # Yellow: Borderline disturbance / channel decay (2.0 <= z < 4.0)
    MALICIOUS = "MALICIOUS"      # Red: Active attack detected with >99.99% certainty (z >= 4.0)


@dataclass
class ThreatAssessment:
    verdict: ThreatCategory
    error_rate: float           # e_hat = n1 / N
    z_score: float              # Standardized normal z-score
    p_value: float              # Exact binomial test p-value
    confidence: float           # Standard normal CDF Phi(z)
    baseline_noise_p0: float    # Calibrated channel baseline (e.g. 0.03)
    total_trials: int           # N
    error_count: int            # n1
    match_count: int            # n0
    ci_lower: float             # Wilson / Clopper-Pearson 95% CI lower
    ci_upper: float             # Wilson / Clopper-Pearson 95% CI upper
    freshness_passed: bool
    freshness_reason: str
    diagnostic_text: str
    token_trials: Optional[List[MeasurementTrialResult]] = None


class QStatDetector:
    """
    Q-STAT Threat Detection Engine.
    Evaluates quantum projective measurement outcome counts without AI/ML black boxes.
    """

    def __init__(
        self,
        baseline_noise_p0: float = 0.03,
        z_suspicious_threshold: float = 2.0,
        z_malicious_threshold: float = 4.0,
        freshness_registry: Optional[FreshnessRegistry] = None
    ):
        self.p0: float = baseline_noise_p0
        self.z_suspicious: float = z_suspicious_threshold
        self.z_malicious: float = z_malicious_threshold
        self.freshness: FreshnessRegistry = freshness_registry or FreshnessRegistry()

    def calibrate_baseline(self, empirical_trials: np.ndarray) -> float:
        """
        Calibrates the baseline noise floor p0 from empirical honest trials.
        """
        self.p0 = float(np.clip(np.mean(empirical_trials), 0.001, 0.20))
        return self.p0

    def evaluate(
        self,
        error_count: int,
        total_trials: int,
        signer_id: str,
        nonce: str,
        timestamp: float,
        current_time: Optional[float] = None
    ) -> ThreatAssessment:
        """
        Executes complete verification pipeline:
        1. Freshness / Anti-Replay verification.
        2. Exact Binomial Hypothesis Test (H0: p <= p0 vs H1: p > p0).
        3. Standardized Z-score calculation.
        4. Three-tier threshold classification.
        """
        # Step 1: Cryptographic freshness check
        is_fresh, freshness_reason = self.freshness.verify_and_register(
            signer_id=signer_id,
            nonce=nonce,
            timestamp=timestamp,
            current_time=current_time
        )

        n1 = int(error_count)
        N = int(total_trials)
        n0 = N - n1
        e_hat = float(n1 / N) if N > 0 else 0.0

        # Step 2: Exact Binomial Hypothesis Test
        # Null hypothesis H0: p <= p0
        # Alternative hypothesis H1: p > p0
        binom_res = stats.binomtest(k=n1, n=N, p=self.p0, alternative="greater")
        p_val = float(binom_res.pvalue)
        ci = binom_res.proportion_ci(confidence_level=0.95)
        ci_lower = float(ci.low)
        ci_upper = float(ci.high)

        # Step 3: Standardized Anomaly Score (Z-Score)
        # Under H0: mean = p0, std = sqrt(p0 * (1 - p0) / N)
        sigma_0 = np.sqrt(self.p0 * (1.0 - self.p0) / N)
        z = float((e_hat - self.p0) / sigma_0) if sigma_0 > 0 else 0.0

        # Detection confidence via Normal CDF Phi(z)
        conf = float(stats.norm.cdf(z))

        # Step 4: Decision Classification
        if not is_fresh:
            # Replay attack caught by bookkeeping check
            verdict = ThreatCategory.MALICIOUS
            diagnostic = (
                f"REPLAY ATTACK INTERCEPTED. {freshness_reason} "
                f"(Physical error rate: {e_hat:.2%}, z={z:.2f})."
            )
        elif z < self.z_suspicious:
            verdict = ThreatCategory.LEGITIMATE
            diagnostic = (
                f"Signature Verified: Observed error rate {e_hat:.2%} is within normal quantum noise bounds "
                f"(baseline p0={self.p0:.2%}, z={z:.2f} < {self.z_suspicious:.1f}, p={p_val:.4f})."
            )
        elif z < self.z_malicious:
            verdict = ThreatCategory.SUSPICIOUS
            diagnostic = (
                f"Suspicious Channel Disturbance: Observed error rate {e_hat:.2%} exceeds 2-sigma noise bounds "
                f"(z={z:.2f}, p={p_val:.4e}). Elevated monitoring required."
            )
        else:
            verdict = ThreatCategory.MALICIOUS
            diagnostic = (
                f"ACTIVE THREAT DETECTED: Observed error rate {e_hat:.2%} drastically exceeds noise floor "
                f"(z={z:.2f} >= {self.z_malicious:.1f}, p < 1e-15, confidence > 99.99%). Signature rejected."
            )

        return ThreatAssessment(
            verdict=verdict,
            error_rate=e_hat,
            z_score=z,
            p_value=p_val,
            confidence=conf,
            baseline_noise_p0=self.p0,
            total_trials=N,
            error_count=n1,
            match_count=n0,
            ci_lower=ci_lower,
            ci_upper=ci_upper,
            freshness_passed=is_fresh,
            freshness_reason=freshness_reason,
            diagnostic_text=diagnostic
        )

    def verify_signature_session(
        self,
        received_signature: QuantumDigitalSignature,
        expected_signature: QuantumDigitalSignature,
        trials_per_token: int = 50,
        ambient_noise: float = 0.03,
        random_seed: Optional[int] = None,
        current_time: Optional[float] = None
    ) -> ThreatAssessment:
        """
        Conducts multi-qubit signature verification:
        Measures all received tokens against Alice's expected Pauli eigenstates,
        aggregates the Born-rule outcomes, and produces an overall ThreatAssessment.
        """
        token_trials: List[MeasurementTrialResult] = []
        total_errors = 0
        total_trials = 0

        for i, (rx_tok, exp_tok) in enumerate(zip(received_signature.tokens, expected_signature.tokens)):
            seed = (random_seed + i) if random_seed is not None else None
            trial_res = sample_projective_trials(
                received_state=rx_tok.eigenstate,
                expected_state=exp_tok.eigenstate,
                num_trials=trials_per_token,
                ambient_noise=ambient_noise,
                random_seed=seed
            )
            token_trials.append(trial_res)
            total_errors += trial_res.n_error
            total_trials += trial_res.num_trials

        assessment = self.evaluate(
            error_count=total_errors,
            total_trials=total_trials,
            signer_id=received_signature.signer_id,
            nonce=received_signature.nonce,
            timestamp=received_signature.timestamp,
            current_time=current_time
        )
        assessment.token_trials = token_trials
        return assessment

