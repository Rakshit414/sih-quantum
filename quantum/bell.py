"""
Q-Sentinel: Bell State Entanglement Engine
Stage 2: Phase 4
Generates maximally entangled 2-qubit Bell states, verifies purity, and validates partial trace.
"""

from __future__ import annotations
import numpy as np
from enum import Enum
from quantum.state import QubitState, HADAMARD, CNOT, PAULI_X, PAULI_Z


class BellStateType(Enum):
    PHI_PLUS = "PHI_PLUS"    # |Φ⁺⟩ = (|00⟩ + |11⟩) / √2
    PHI_MINUS = "PHI_MINUS"  # |Φ⁻⟩ = (|00⟩ - |11⟩) / √2
    PSI_PLUS = "PSI_PLUS"    # |Ψ⁺⟩ = (|01⟩ + |10⟩) / √2
    PSI_MINUS = "PSI_MINUS"  # |Ψ⁻⟩ = (|01⟩ - |10⟩) / √2


def create_bell_state(bell_type: BellStateType = BellStateType.PHI_PLUS) -> QubitState:
    """
    Generates a canonical Bell state by preparing standard 2-qubit computational basis
    states and passing them through Hadamard and CNOT gates.
    """
    # Base state |00⟩
    vec_00 = np.array([[1.0], [0.0], [0.0], [0.0]], dtype=np.complex128)
    
    # H on qubit 1: H (x) I
    H_kron_I = np.kron(HADAMARD, np.eye(2, dtype=np.complex128))
    state_after_H = H_kron_I @ vec_00
    
    # CNOT with control=qubit 1, target=qubit 2 -> creates |Φ⁺⟩
    phi_plus_vec = CNOT @ state_after_H
    
    if bell_type == BellStateType.PHI_PLUS:
        return QubitState(phi_plus_vec, label="|Φ⁺⟩")
    elif bell_type == BellStateType.PHI_MINUS:
        # |Φ⁻⟩ = (Z (x) I) |Φ⁺⟩
        Z_kron_I = np.kron(PAULI_Z, np.eye(2, dtype=np.complex128))
        return QubitState(Z_kron_I @ phi_plus_vec, label="|Φ⁻⟩")
    elif bell_type == BellStateType.PSI_PLUS:
        # |Ψ⁺⟩ = (X (x) I) |Φ⁺⟩
        X_kron_I = np.kron(PAULI_X, np.eye(2, dtype=np.complex128))
        return QubitState(X_kron_I @ phi_plus_vec, label="|Ψ⁺⟩")
    elif bell_type == BellStateType.PSI_MINUS:
        # |Ψ⁻⟩ = (iY (x) I) |Φ⁺⟩ or (ZX (x) I) |Φ⁺⟩
        ZX = PAULI_Z @ PAULI_X
        ZX_kron_I = np.kron(ZX, np.eye(2, dtype=np.complex128))
        return QubitState(ZX_kron_I @ phi_plus_vec, label="|Ψ⁻⟩")
    else:
        raise ValueError(f"Unknown Bell state type: {bell_type}")


def partial_trace_b(rho_ab: np.ndarray) -> np.ndarray:
    """
    Computes the partial trace over subsystem B for a 2-qubit density matrix rho_AB (4x4).
    rho_A = Tr_B(rho_AB) = sum_j <j_B| rho_AB |j_B> (2x2).
    """
    if rho_ab.shape != (4, 4):
        raise ValueError(f"Expected 4x4 density matrix, got {rho_ab.shape}")
    
    # Basis vectors for subsystem B
    b0 = np.array([[1.0], [0.0]], dtype=np.complex128)
    b1 = np.array([[0.0], [1.0]], dtype=np.complex128)
    
    # Projector blocks (I (x) <0|) and (I (x) <1|)
    proj_0 = np.kron(np.eye(2, dtype=np.complex128), b0.T.conj())
    proj_1 = np.kron(np.eye(2, dtype=np.complex128), b1.T.conj())
    
    rho_a = (proj_0 @ rho_ab @ proj_0.T.conj()) + (proj_1 @ rho_ab @ proj_1.T.conj())
    return rho_a


def verify_maximal_entanglement(bell_state: QubitState, tol: float = 1e-6) -> bool:
    """
    Mathematically verifies maximal entanglement:
    1. Bipartite purity Tr(rho_AB^2) == 1 (pure state).
    2. Reduced subsystem A density matrix rho_A == 0.5 * I_2 (maximally mixed, entropy = 1).
    3. Reduced purity Tr(rho_A^2) == 0.5.
    """
    rho_ab = bell_state.to_density_matrix()
    total_purity = np.trace(rho_ab @ rho_ab).real
    if abs(total_purity - 1.0) > tol:
        return False
    
    rho_a = partial_trace_b(rho_ab)
    expected_rho_a = 0.5 * np.eye(2, dtype=np.complex128)
    if not np.allclose(rho_a, expected_rho_a, atol=tol):
        return False
        
    reduced_purity = np.trace(rho_a @ rho_a).real
    return abs(reduced_purity - 0.5) < tol
