"""
Q-Sentinel: Quantum State Tomography (QST) Engine
Stage 9: Phase 28
Reconstructs the full 2x2 density matrix from Pauli expectation values (Stokes parameters),
and computes state fidelity, purity, Von Neumann entropy, and Bloch sphere coordinates.
Distinguishes environmental decoherence (mixed state) from active eavesdropping (projective collapse).
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Optional, Dict
import numpy as np

from quantum.state import (
    QubitState,
    PauliBasis,
    PAULI_I,
    PAULI_X,
    PAULI_Y,
    PAULI_Z,
    get_pauli_eigenstate
)


@dataclass
class TomographyResult:
    """
    Encapsulates reconstructed density matrix and quantum information metrics.
    """
    density_matrix: np.ndarray
    stokes_parameters: Tuple[float, float, float]  # (S1, S2, S3)
    bloch_vector_length: float
    fidelity: float
    purity: float
    von_neumann_entropy: float
    is_pure: bool
    diagnostic: str


class QuantumStateTomography:
    """
    Executes single-qubit quantum state tomography via Pauli basis projections.
    """

    @staticmethod
    def sample_pauli_expectation(state: QubitState, pauli_matrix: np.ndarray, num_trials: int = 200) -> float:
        """
        Estimates the expectation value <sigma> = <psi|sigma|psi> via simulated projective sampling.
        """
        # Theoretical expectation value
        theo_val = float(np.real(np.vdot(state.vector, pauli_matrix @ state.vector)))
        
        # Probabilities for eigenvalues +1 and -1:
        # <sigma> = P(+) - P(-)  and  P(+) + P(-) = 1
        # => P(+) = (1 + <sigma>) / 2, P(-) = (1 - <sigma>) / 2
        p_plus = float(np.clip((1.0 + theo_val) / 2.0, 0.0, 1.0))
        p_minus = 1.0 - p_plus

        # Sample num_trials
        outcomes = np.random.choice([1.0, -1.0], size=num_trials, p=[p_plus, p_minus])
        empirical_expectation = float(np.mean(outcomes))
        return empirical_expectation

    @classmethod
    def reconstruct_state(
        cls,
        target_state: QubitState,
        expected_state: Optional[QubitState] = None,
        num_trials_per_basis: int = 200
    ) -> TomographyResult:
        """
        Reconstructs the 2x2 density matrix rho from projective measurements along X, Y, and Z bases.
        rho = 0.5 * (I + S1*X + S2*Y + S3*Z)
        """
        # 1. Sample Stokes parameters along Pauli X, Y, Z
        s1 = cls.sample_pauli_expectation(target_state, PAULI_X, num_trials=num_trials_per_basis)
        s2 = cls.sample_pauli_expectation(target_state, PAULI_Y, num_trials=num_trials_per_basis)
        s3 = cls.sample_pauli_expectation(target_state, PAULI_Z, num_trials=num_trials_per_basis)

        bloch_len = float(np.sqrt(s1**2 + s2**2 + s3**2))
        
        # Physical boundary: Bloch vector length r <= 1.0
        # If sampling noise pushes r > 1.0, normalize to surface of Bloch sphere
        if bloch_len > 1.0:
            scale = 1.0 / bloch_len
            s1_phys = s1 * scale
            s2_phys = s2 * scale
            s3_phys = s3 * scale
            bloch_len = 1.0
        else:
            s1_phys, s2_phys, s3_phys = s1, s2, s3

        # 2. Synthesize density matrix rho
        rho = 0.5 * (PAULI_I + s1_phys * PAULI_X + s2_phys * PAULI_Y + s3_phys * PAULI_Z)

        # Enforce exact Hermiticity and unit trace
        rho = 0.5 * (rho + rho.conj().T)
        rho = rho / np.trace(rho).real

        # 3. Compute Purity: gamma = Tr(rho^2) in [0.5, 1.0]
        rho_sq = rho @ rho
        purity = float(np.real(np.trace(rho_sq)))
        purity = float(np.clip(purity, 0.5, 1.0))
        is_pure = purity >= 0.95

        # 4. Compute Von Neumann Entropy: S(rho) = -sum(lambda_i * log2(lambda_i))
        eigenvals = np.linalg.eigvalsh(rho)
        eigenvals = np.clip(eigenvals, 1e-12, 1.0)
        eigenvals = eigenvals / np.sum(eigenvals)
        entropy = float(-np.sum(eigenvals * np.log2(eigenvals)))
        entropy = max(0.0, entropy)

        # 5. Compute Quantum State Fidelity F(rho_exp, rho_rec)
        ref_state = expected_state or target_state
        # For pure reference state: F = <psi_ref| rho |psi_ref>
        fidelity = float(np.real(np.vdot(ref_state.vector, rho @ ref_state.vector)))
        fidelity = float(np.clip(fidelity, 0.0, 1.0))

        # 6. Generate Diagnostic Text
        if fidelity > 0.92 and purity > 0.90:
            diagnostic = f"High-fidelity pure state recovered (F={fidelity*100:.1f}%, Purity={purity*100:.1f}%). No channel decoherence."
        elif purity < 0.75:
            diagnostic = f"Mixed state detected (Purity={purity*100:.1f}%, Entropy={entropy:.3f} bits). Characteristic of depolarizing channel noise."
        else:
            diagnostic = f"Pure state mismatch (Fidelity={fidelity*100:.1f}%). Characteristic of active basis collapse or signature forgery."

        return TomographyResult(
            density_matrix=rho,
            stokes_parameters=(round(s1_phys, 4), round(s2_phys, 4), round(s3_phys, 4)),
            bloch_vector_length=round(bloch_len, 4),
            fidelity=round(fidelity, 4),
            purity=round(purity, 4),
            von_neumann_entropy=round(entropy, 4),
            is_pure=is_pure,
            diagnostic=diagnostic
        )
