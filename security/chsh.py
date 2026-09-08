"""
Q-Sentinel: Device-Independent Entanglement Verification via CHSH Bell Inequality
Stage 13: Phase 34 (Q-CHSH)

Evaluates the Clauser-Horne-Shimony-Holt (CHSH) Bell inequality parameter S:
    S = E(A0, B0) + E(A0, B1) + E(A1, B0) - E(A1, B1)

Tests whether the distributed quantum entanglement underlying QDS teleportation
satisfies quantum non-locality (Tsirelson bound S <= 2*sqrt(2) ~ 2.828) or has collapsed
into classical local hidden variable (LHV) separable states (S <= 2.0).
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple, Optional, List
import numpy as np

from security.detector import ThreatCategory
from quantum.state import PauliBasis, get_pauli_eigenstate
from quantum.bell import create_bell_state, BellStateType


@dataclass
class CHSHMeasurementSetting:
    """
    Measurement observable configuration for Alice and Bob.
    """
    alice_index: int     # 0 for A0 (Z), 1 for A1 (X)
    bob_index: int       # 0 for B0 ((Z+X)/sqrt(2)), 1 for B1 ((Z-X)/sqrt(2))
    alice_name: str
    bob_name: str
    trials: int
    count_pp: int        # Outcome (+1, +1)
    count_pm: int        # Outcome (+1, -1)
    count_mp: int        # Outcome (-1, +1)
    count_mm: int        # Outcome (-1, -1)
    correlation_e: float
    std_error: float


@dataclass
class CHSHVerificationResult:
    """
    Full cryptanalytic outcome of the CHSH Bell Inequality Watchtower.
    """
    chsh_s_parameter: float
    theoretical_quantum_max: float      # 2 * sqrt(2) ~ 2.8284
    classical_limit: float              # 2.0000
    standard_error_s: float
    bell_violation_z_score: float
    entanglement_certified: bool
    verdict: ThreatCategory
    attack_classification: str
    correlations: Dict[str, float]
    cryptanalytic_proof: str


class CHSHBellWatcher:
    """
    Device-Independent Quantum Entanglement Watchtower using CHSH Bell Inequalities.
    Guarantees that teleportation Bell pairs have not been substituted by classical
    intercept-resend or separable state spoofing attacks.
    """

    def __init__(self, trials_per_setting: int = 400):
        self.trials: int = max(50, trials_per_setting)
        self.classical_bound: float = 2.0000
        self.tsirelson_bound: float = float(2.0 * np.sqrt(2.0))

        # Define 2x2 Pauli operators
        self.z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
        self.x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)

        # Alice measurement observables: A0 = Z, A1 = X
        self.a0 = self.z
        self.a1 = self.x

        # Bob measurement observables: B0 = (Z + X)/sqrt(2), B1 = (Z - X)/sqrt(2)
        inv_sqrt2 = 1.0 / np.sqrt(2.0)
        self.b0 = inv_sqrt2 * (self.z + self.x)
        self.b1 = inv_sqrt2 * (self.z - self.x)

    def _get_projectors(self, observable: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Computes the projection operators P(+) and P(-) for an observable with eigenvalues +/- 1.
        P(+) = (I + Observable) / 2
        P(-) = (I - Observable) / 2
        """
        eye = np.eye(2, dtype=complex)
        p_plus = 0.5 * (eye + observable)
        p_minus = 0.5 * (eye - observable)
        return p_plus, p_minus

    def measure_correlation(
        self,
        density_matrix: np.ndarray,
        alice_op: np.ndarray,
        bob_op: np.ndarray,
        num_trials: int
    ) -> Tuple[float, float, int, int, int, int]:
        """
        Simulates Born-rule projective measurement of Alice and Bob observables
        over N stochastic trials and returns the correlation E and standard error.
        """
        pa_plus, pa_minus = self._get_projectors(alice_op)
        pb_plus, pb_minus = self._get_projectors(bob_op)

        # 4 joint projectors
        proj_pp = np.kron(pa_plus, pb_plus)
        proj_pm = np.kron(pa_plus, pb_minus)
        proj_mp = np.kron(pa_minus, pb_plus)
        proj_mm = np.kron(pa_minus, pb_minus)

        prob_pp = float(np.clip(np.trace(density_matrix @ proj_pp).real, 0.0, 1.0))
        prob_pm = float(np.clip(np.trace(density_matrix @ proj_pm).real, 0.0, 1.0))
        prob_mp = float(np.clip(np.trace(density_matrix @ proj_mp).real, 0.0, 1.0))
        prob_mm = float(np.clip(np.trace(density_matrix @ proj_mm).real, 0.0, 1.0))

        # Normalize probability vector
        probs = np.array([prob_pp, prob_pm, prob_mp, prob_mm])
        s_prob = np.sum(probs)
        if s_prob > 0:
            probs = probs / s_prob
        else:
            probs = np.array([0.25, 0.25, 0.25, 0.25])

        # Sample multinomial counts
        counts = np.random.multinomial(num_trials, probs)
        n_pp, n_pm, n_mp, n_mm = int(counts[0]), int(counts[1]), int(counts[2]), int(counts[3])

        # Empirical correlation E = (N_++ + N_-- - N_+- - N_-+) / N
        e_corr = (n_pp + n_mm - n_pm - n_mp) / float(num_trials)
        # Standard error: sqrt((1 - E^2) / N)
        std_err = float(np.sqrt(max(1e-8, 1.0 - e_corr**2) / float(num_trials)))

        return e_corr, std_err, n_pp, n_pm, n_mp, n_mm

    def evaluate_state(
        self,
        density_matrix: np.ndarray,
        state_label: str = "Candidate Pair",
        num_trials: Optional[int] = None
    ) -> CHSHVerificationResult:
        """
        Executes complete 4-setting CHSH Bell test on the supplied 2-qubit density matrix.
        """
        trials = self.trials if num_trials is None else max(50, num_trials)

        # 4 correlation settings
        settings = [
            (0, 0, "A0 (Z)", "B0 ((Z+X)/sqrt(2))", self.a0, self.b0),
            (0, 1, "A0 (Z)", "B1 ((Z-X)/sqrt(2))", self.a0, self.b1),
            (1, 0, "A1 (X)", "B0 ((Z+X)/sqrt(2))", self.a1, self.b0),
            (1, 1, "A1 (X)", "B1 ((Z-X)/sqrt(2))", self.a1, self.b1),
        ]

        e_vals: Dict[str, float] = {}
        var_sum = 0.0

        for a_idx, b_idx, a_name, b_name, a_op, b_op in settings:
            e_corr, s_err, _, _, _, _ = self.measure_correlation(density_matrix, a_op, b_op, trials)
            key = f"E(A{a_idx}, B{a_idx})" if a_idx == b_idx else f"E(A{a_idx}, B{b_idx})"
            e_vals[key] = round(e_corr, 4)
            var_sum += s_err**2

        # CHSH formula: S = E(A0, B0) + E(A0, B1) + E(A1, B0) - E(A1, B1)
        e00 = e_vals["E(A0, B0)"]
        e01 = e_vals["E(A0, B1)"]
        e10 = e_vals["E(A1, B0)"]
        e11 = e_vals["E(A1, B1)"]

        s_param = e00 + e01 + e10 - e11
        std_error_s = float(np.sqrt(var_sum))

        # Standardized violation score relative to classical bound S = 2.0
        # z_Bell = (S - 2.0) / std_error_s
        z_bell = (s_param - self.classical_bound) / max(1e-6, std_error_s)

        # Classification and verdict
        if s_param > 2.25 and z_bell >= 2.5:
            entangled = True
            verdict = ThreatCategory.LEGITIMATE
            classification = "CERTIFIED_QUANTUM_ENTANGLEMENT"
            proof = (
                f"LEGITIMATE: CHSH parameter S = {s_param:.4f} exceeds classical limit 2.0000 "
                f"by {z_bell:+.2f} sigma (Theoretical Tsirelson Bound: 2.8284). "
                f"Device-independent proof guarantees non-classical entanglement for teleportation."
            )
        elif s_param > 2.00:
            entangled = True
            verdict = ThreatCategory.SUSPICIOUS
            classification = "WEAK_OR_NOISY_ENTANGLEMENT"
            proof = (
                f"SUSPICIOUS: CHSH parameter S = {s_param:.4f} is near the classical boundary "
                f"(z = {z_bell:+.2f} sigma). High channel noise or partial entanglement degradation observed."
            )
        else:
            entangled = False
            verdict = ThreatCategory.MALICIOUS
            classification = "CLASSICAL_LHV_SPOOFING_ATTACK"
            proof = (
                f"MALICIOUS: Bell inequality satisfied (S = {s_param:.4f} <= 2.0000, z = {z_bell:+.2f} sigma). "
                f"Distributed state admits a local hidden variable (LHV) model. "
                f"Adversary intercepted and replaced entangled Bell pairs with classical separable states."
            )

        return CHSHVerificationResult(
            chsh_s_parameter=round(s_param, 4),
            theoretical_quantum_max=round(self.tsirelson_bound, 4),
            classical_limit=round(self.classical_bound, 4),
            standard_error_s=round(std_error_s, 4),
            bell_violation_z_score=round(z_bell, 2),
            entanglement_certified=entangled,
            verdict=verdict,
            attack_classification=classification,
            correlations=e_vals,
            cryptanalytic_proof=proof
        )

    def simulate_chsh_scenario(
        self,
        scenario: str = "Honest Maximally Entangled",
        depolarizing_noise: float = 0.05
    ) -> CHSHVerificationResult:
        """
        Simulates CHSH Bell tests across honest, degraded, and adversarial spoofing scenarios.
        """
        # Create standard Phi+ state
        phi_plus = create_bell_state(BellStateType.PHI_PLUS).vector.reshape(4, 1)
        rho_ideal = phi_plus @ phi_plus.conj().T

        if "Honest" in scenario:
            # Add minor ambient noise: (1-p)*rho + p*I/4
            p = float(np.clip(depolarizing_noise, 0.0, 0.20))
            rho = (1.0 - p) * rho_ideal + p * 0.25 * np.eye(4, dtype=complex)
            return self.evaluate_state(rho, state_label="Honest Bell Pair")
        elif "Spoofing" in scenario or "Classical" in scenario:
            # Local Hidden Variable / Separable state: 50% |00><00| + 50% |11><11|
            # Entanglement completely broken (S <= sqrt(2) ~ 1.414 <= 2.0)
            rho_sep = np.zeros((4, 4), dtype=complex)
            rho_sep[0, 0] = 0.50
            rho_sep[3, 3] = 0.50
            return self.evaluate_state(rho_sep, state_label="Classical Separable Spoof")
        elif "Intercept" in scenario or "Measurement" in scenario:
            # Adversary measures in Z basis: collapses to mixture of |00> and |11> with classical noise
            rho_meas = np.zeros((4, 4), dtype=complex)
            rho_meas[0, 0] = 0.45
            rho_meas[3, 3] = 0.45
            rho_meas[1, 1] = 0.05
            rho_meas[2, 2] = 0.05
            return self.evaluate_state(rho_meas, state_label="Intercept-Resend Collapse")
        else:
            # Heavy noise (e.g. 40% depolarizing noise)
            p = 0.40
            rho_noisy = (1.0 - p) * rho_ideal + p * 0.25 * np.eye(4, dtype=complex)
            return self.evaluate_state(rho_noisy, state_label="High Thermal Noise")
