"""
Q-Sentinel: Quantum Teleportation Protocol Pipeline
Stage 2: Phase 5
Implements deterministic and stochastic 3-qubit teleportation using shared Bell pairs,
Bell-state projective measurement, classical bit transmission, and Pauli corrections.
"""

from __future__ import annotations
import numpy as np
from dataclasses import dataclass
from typing import Tuple, Optional
from quantum.state import QubitState, HADAMARD, CNOT, PAULI_I, PAULI_X, PAULI_Z
from quantum.bell import create_bell_state, BellStateType


@dataclass
class TeleportationResult:
    original_state: QubitState
    bell_measurement_bits: Tuple[int, int]  # (b1, b2)
    pre_correction_state: QubitState
    applied_correction: str
    recovered_state: QubitState
    fidelity: float
    success: bool


def get_pauli_correction_matrix(b1: int, b2: int) -> Tuple[np.ndarray, str]:
    """
    Determines the exact Pauli unitary required to restore the teleported qubit:
    U_corr = Z^{b1} @ X^{b2}.
    """
    if (b1, b2) == (0, 0):
        return PAULI_I, "I"
    elif (b1, b2) == (0, 1):
        return PAULI_X, "X"
    elif (b1, b2) == (1, 0):
        return PAULI_Z, "Z"
    elif (b1, b2) == (1, 1):
        # Z @ X = -i Y
        return PAULI_Z @ PAULI_X, "ZX"
    else:
        raise ValueError(f"Invalid Bell measurement bits: ({b1}, {b2})")


def teleport_qubit(
    input_state: QubitState,
    bell_pair: Optional[QubitState] = None,
    forced_bits: Optional[Tuple[int, int]] = None,
    random_seed: Optional[int] = None
) -> TeleportationResult:
    """
    Executes the standard 3-qubit quantum teleportation protocol.
    
    Qubit 1: Alice's secret signature state |psi⟩ = alpha|0⟩ + beta|1⟩
    Qubit 2: Alice's half of entangled pair |Φ⁺⟩
    Qubit 3: Bob's half of entangled pair |Φ⁺⟩
    
    Returns TeleportationResult with state telemetry and verified fidelity.
    """
    input_state.assert_normalized()
    if bell_pair is None:
        bell_pair = create_bell_state(BellStateType.PHI_PLUS)
    
    # 1. Composite 3-qubit state |Psi_123⟩ = |psi⟩_1 ⊗ |Φ⁺⟩_23 (8x1 vector)
    composite_state = input_state.tensor(bell_pair)
    vec = composite_state.vector  # (8, 1)
    
    # 2. Alice applies CNOT on qubits 1 and 2 (leaves qubit 3 untouched)
    # Gate: CNOT_12 (x) I_3 (8x8 unitary)
    cnot_12_kron_I = np.kron(CNOT, np.eye(2, dtype=np.complex128))
    vec = cnot_12_kron_I @ vec
    
    # 3. Alice applies Hadamard on qubit 1: H_1 (x) I_2 (x) I_3 (8x8 unitary)
    H_kron_I_kron_I = np.kron(np.kron(HADAMARD, np.eye(2, dtype=np.complex128)), np.eye(2, dtype=np.complex128))
    vec = H_kron_I_kron_I @ vec
    
    # 4. Projective Bell measurement on qubits 1 & 2
    # The 4 outcomes (00, 01, 10, 11) correspond to 2-qubit basis slices in vec
    # vec is 8 elements: index = b1 * 4 + b2 * 2 + q3
    # Outcome probabilities by Born rule:
    p_00 = np.vdot(vec[0:2], vec[0:2]).real
    p_01 = np.vdot(vec[2:4], vec[2:4]).real
    p_10 = np.vdot(vec[4:6], vec[4:6]).real
    p_11 = np.vdot(vec[6:8], vec[6:8]).real
    probs = np.array([p_00, p_01, p_10, p_11])
    probs = np.clip(probs, 0.0, 1.0)
    probs /= np.sum(probs)  # normalize numerical precision
    
    if forced_bits is not None:
        b1, b2 = forced_bits
    else:
        rng = np.random.default_rng(random_seed)
        outcome_idx = rng.choice(4, p=probs)
        bit_map = [(0, 0), (0, 1), (1, 0), (1, 1)]
        b1, b2 = bit_map[outcome_idx]
    
    # 5. Extract collapsed state of qubit 3 (Bob's qubit)
    start_idx = (b1 * 2 + b2) * 2
    bob_raw_vec = vec[start_idx : start_idx + 2]
    norm_sq = np.vdot(bob_raw_vec, bob_raw_vec).real
    if norm_sq > 1e-12:
        bob_raw_vec = bob_raw_vec / np.sqrt(norm_sq)
    pre_correction = QubitState(bob_raw_vec, label=f"Collapsed_({b1}{b2})")
    
    # 6. Bob receives (b1, b2) via classical channel and applies Pauli correction U_corr = Z^{b1} X^{b2}
    U_corr, corr_label = get_pauli_correction_matrix(b1, b2)
    bob_recovered_vec = U_corr @ pre_correction.vector
    recovered_state = QubitState(bob_recovered_vec, label=f"Teleported({input_state.label})")
    
    # 7. Compute fidelity F = |⟨psi | recovered⟩|²
    fidelity = input_state.fidelity(recovered_state)
    
    return TeleportationResult(
        original_state=input_state,
        bell_measurement_bits=(b1, b2),
        pre_correction_state=pre_correction,
        applied_correction=corr_label,
        recovered_state=recovered_state,
        fidelity=fidelity,
        success=bool(abs(fidelity - 1.0) < 1e-5)
    )
