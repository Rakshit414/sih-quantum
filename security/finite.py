"""
Q-Sentinel: Finite-Size Security Analysis & Serfling Bound Watchtower
Stage 14: Phase 35 (Q-FINITE)

Evaluates composable finite-key security (epsilon-security <= 10^-10) for QDS sessions
using Serfling's Martingale large-deviation inequality for sampling without replacement
and Leftover Hash Lemma / Smooth Min-Entropy calculus:
    xi(N, n, eps_PE) = sqrt((N - n + 1) * ln(1/eps_PE) / (2 * n * N))
    e_U = e_sample + xi(N, n, eps_PE)
    ell <= (N - n) * (1 - h2(e_U)) - leak_EC - 2*log2(1/eps_PA) - 2*log2(1/eps_cor)
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple, Optional
import numpy as np

from security.detector import ThreatCategory


@dataclass
class FiniteKeyParameters:
    """
    Structural parameters of a finite-size quantum digital signature exchange.
    """
    total_qubits_N: int             # Total transmitted quantum signature tokens (e.g. 1000 - 4000)
    sample_qubits_n: int            # Qubits consumed for parameter estimation (e.g. 200 - 1000)
    observed_sample_errors: int     # Physical errors measured in sample
    error_correction_efficiency: float = 1.16  # Practical Shannon error-correction overhead f_EC
    target_epsilon_pe: float = 1e-10           # Parameter estimation failure probability
    target_epsilon_sec: float = 1e-10          # Target composable security parameter


@dataclass
class FiniteSecurityResult:
    """
    Cryptanalytic outcome of the finite-key composable security evaluation.
    """
    total_block_size_N: int
    sample_size_n: int
    raw_sample_error_rate: float
    serfling_deviation_xi: float
    upper_bound_phase_error: float
    extractable_signature_length: int
    distillation_rate: float
    error_correction_leakage: int
    composable_epsilon: float
    is_composably_secure: bool
    verdict: ThreatCategory
    attack_classification: str
    cryptanalytic_proof: str


class FiniteSizeSecurityAnalyzer:
    """
    Evaluates whether a finite-block quantum signature transmission satisfies
    information-theoretic composable epsilon-security under finite-sample fluctuations.
    """

    def __init__(
        self,
        f_ec: float = 1.16,
        target_epsilon_sec: float = 1e-10,
        max_tolerable_error: float = 0.180  # Finite-size QDS threshold (18%)
    ):
        self.f_ec: float = float(f_ec)
        self.eps_sec: float = float(target_epsilon_sec)
        self.e_threshold: float = float(max_tolerable_error)

    @staticmethod
    def binary_entropy(p: float) -> float:
        """
        Computes the binary Shannon entropy h2(p) = -p*log2(p) - (1-p)*log2(1-p).
        """
        val = float(np.clip(p, 1e-12, 0.50))
        return -val * np.log2(val) - (1.0 - val) * np.log2(1.0 - val)

    def compute_serfling_deviation(
        self,
        total_N: int,
        sample_n: int,
        eps_pe: float = 1e-10
    ) -> float:
        """
        Computes Serfling's finite-sampling deviation cutoff xi:
        xi(N, n, eps) = sqrt( (N - n + 1) * ln(1/eps) / (2 * n * N) )
        """
        if sample_n <= 0 or total_N <= sample_n:
            return 1.0

        numerator = float(total_N - sample_n + 1) * np.log(1.0 / max(1e-15, eps_pe))
        denominator = 2.0 * float(sample_n) * float(total_N)
        xi = np.sqrt(max(0.0, numerator / denominator))
        return float(round(xi, 5))

    def evaluate_session_security(
        self,
        params: FiniteKeyParameters
    ) -> FiniteSecurityResult:
        """
        Performs rigorous finite-size composable security analysis on the session parameters.
        """
        total_N = params.total_qubits_N
        sample_n = params.sample_qubits_n

        if sample_n <= 0 or total_N <= sample_n:
            return FiniteSecurityResult(
                total_block_size_N=total_N,
                sample_size_n=sample_n,
                raw_sample_error_rate=1.0,
                serfling_deviation_xi=1.0,
                upper_bound_phase_error=1.0,
                extractable_signature_length=0,
                distillation_rate=0.0,
                error_correction_leakage=0,
                composable_epsilon=1.0,
                is_composably_secure=False,
                verdict=ThreatCategory.MALICIOUS,
                attack_classification="INVALID_SAMPLE_PARTITION",
                cryptanalytic_proof="MALICIOUS: Invalid parameter estimation partition. Sample size must be strictly less than total block size."
            )

        # 1. Observed sample error rate
        e_sample = float(params.observed_sample_errors / sample_n)

        # 2. Serfling large-deviation bound for sampling without replacement
        xi = self.compute_serfling_deviation(total_N, sample_n, params.target_epsilon_pe)

        # 3. Finite-key upper bound on phase error rate
        e_upper = float(min(0.50, e_sample + xi))

        # 4. Remaining qubits available for signature key distillation: m = N - n
        m = total_N - sample_n

        # 5. Error correction classical leakage: leak_EC = f_EC * m * h2(e_sample)
        h2_e = self.binary_entropy(e_sample)
        leak_ec = int(np.ceil(self.f_ec * m * h2_e))

        # 6. Finite-key Leftover Hash Lemma privacy amplification penalty:
        # Penalty = 2 * log2(1 / (2 * eps_PA)) + 2 * log2(1 / eps_cor)
        # Using eps_PA = eps_cor = eps_sec / 4
        sub_eps = max(1e-15, params.target_epsilon_sec / 4.0)
        privacy_penalty = int(np.ceil(2.0 * np.log2(1.0 / (2.0 * sub_eps)) + 2.0 * np.log2(1.0 / sub_eps)))

        # 7. Extractable secure signature length ell
        # ell = floor( m * (1 - h2(e_upper)) - leak_EC - privacy_penalty )
        h2_upper = self.binary_entropy(e_upper)
        asymptotic_bound = m * (1.0 - h2_upper)
        ell = int(np.floor(asymptotic_bound - leak_ec - privacy_penalty))

        distill_rate = float(max(0.0, ell / float(total_N)))

        # 8. Threat Category & Classification
        if ell > 0 and e_upper < self.e_threshold:
            is_secure = True
            verdict = ThreatCategory.LEGITIMATE
            classification = "COMPOSABLY_SECURE_FINITE_SESSION"
            proof = (
                f"LEGITIMATE: Composable finite-key security certified (epsilon = {params.target_epsilon_sec:.1e}). "
                f"Extractable signature length ell = {ell} tokens from block N = {total_N} (rate = {distill_rate*100:.1f}%). "
                f"Serfling fluctuation delta = {xi:.4f}, bound phase error e_U = {e_upper*100:.2f}% < {self.e_threshold*100:.1f}% threshold."
            )
        elif e_sample >= 0.08:
            # Active attack or heavy disturbance causing security collapse
            is_secure = False
            verdict = ThreatCategory.MALICIOUS
            classification = "FINITE_SIZE_SECURITY_COLLAPSE"
            proof = (
                f"MALICIOUS: Finite-size security failure. Measured sample error ({e_sample*100:.2f}%) "
                f"exceeds safe physical bounds (bound phase error e_U = {e_upper*100:.2f}% > {self.e_threshold*100:.1f}%). "
                f"Adversary induced excessive channel disturbance or eavesdropping on finite block N = {total_N}."
            )
        else:
            # Physical error is low (e_sample < 8%), but finite block size is too small (or xi too large) to extract key!
            is_secure = False
            verdict = ThreatCategory.SUSPICIOUS
            classification = "FINITE_BLOCK_SIZE_STARVATION"
            proof = (
                f"SUSPICIOUS: Finite-size block starvation. Observed sample error ({e_sample*100:.2f}%) is low, "
                f"but Serfling statistical fluctuation penalty (delta = {xi:.4f}) exhausts the extractable length "
                f"(ell = {ell} <= 0). Session block size N = {total_N} must be increased."
            )

        return FiniteSecurityResult(
            total_block_size_N=total_N,
            sample_size_n=sample_n,
            raw_sample_error_rate=round(e_sample, 5),
            serfling_deviation_xi=round(xi, 5),
            upper_bound_phase_error=round(e_upper, 5),
            extractable_signature_length=max(0, ell),
            distillation_rate=round(distill_rate, 4),
            error_correction_leakage=leak_ec,
            composable_epsilon=params.target_epsilon_sec,
            is_composably_secure=is_secure,
            verdict=verdict,
            attack_classification=classification,
            cryptanalytic_proof=proof
        )

    def simulate_finite_scenario(
        self,
        scenario: str = "Honest Production Block",
        block_size_n: int = 1600
    ) -> FiniteSecurityResult:
        """
        Simulates finite-size QDS parameter estimation across realistic operational scenarios.
        """
        n_total = max(200, block_size_n)
        sample_n = n_total // 3  # Standard 1/3 sampling ratio

        if "Honest" in scenario:
            # Baseline physical error ~ 2.5%
            errs = int(sample_n * np.random.uniform(0.020, 0.035))
            params = FiniteKeyParameters(
                total_qubits_N=n_total,
                sample_qubits_n=sample_n,
                observed_sample_errors=errs,
                error_correction_efficiency=self.f_ec,
                target_epsilon_sec=self.eps_sec
            )
        elif "Starvation" in scenario or "Small" in scenario:
            # Block size too small (e.g. N = 250, sample = 75)
            small_N = 250
            small_n = 75
            errs = int(small_n * 0.025)
            params = FiniteKeyParameters(
                total_qubits_N=small_N,
                sample_qubits_n=small_n,
                observed_sample_errors=errs,
                error_correction_efficiency=self.f_ec,
                target_epsilon_sec=self.eps_sec
            )
        elif "Adversary" in scenario or "Disturbance" in scenario or "Attack" in scenario:
            # Adversary induces 14% QBER
            errs = int(sample_n * 0.14)
            params = FiniteKeyParameters(
                total_qubits_N=n_total,
                sample_qubits_n=sample_n,
                observed_sample_errors=errs,
                error_correction_efficiency=self.f_ec,
                target_epsilon_sec=self.eps_sec
            )
        else:
            # Marginal near-threshold case (8% error)
            errs = int(sample_n * 0.08)
            params = FiniteKeyParameters(
                total_qubits_N=n_total,
                sample_qubits_n=sample_n,
                observed_sample_errors=errs,
                error_correction_efficiency=self.f_ec,
                target_epsilon_sec=self.eps_sec
            )

        return self.evaluate_session_security(params)
