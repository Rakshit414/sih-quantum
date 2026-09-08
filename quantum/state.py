"""
Q-Sentinel: Quantum State and Hilbert Space Engine
Stage 1: Mathematical Engine & Quantum State Representation
Phases 1, 2, 3: Qubit States, Pauli Operators, and Multi-Qubit Tensor Spaces
"""

from __future__ import annotations
import numpy as np
from enum import Enum
from typing import Tuple, List, Union


class PauliBasis(Enum):
    Z = "Z"  # Computational basis {|0>, |1>}
    X = "X"  # Hadamard basis {|+>, |->}
    Y = "Y"  # Circular basis {|i+>, |i->}


# Fundamental 2x2 Pauli Unitary Matrices
PAULI_I = np.array([[1.0, 0.0], [0.0, 1.0]], dtype=np.complex128)
PAULI_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128)
PAULI_Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=np.complex128)
PAULI_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=np.complex128)

# Canonical Single-Qubit Hadamard Gate
HADAMARD = np.array([[1.0, 1.0], [1.0, -1.0]], dtype=np.complex128) / np.sqrt(2.0)

# Canonical 2-Qubit Controlled-NOT (CNOT) Gate in standard basis {|00>, |01>, |10>, |11>}
CNOT = np.array([
    [1.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 1.0],
    [0.0, 0.0, 1.0, 0.0]
], dtype=np.complex128)


class QubitState:
    """
    Represents a pure quantum state vector in Hilbert space H_{2^n}.
    Enforces normalization and provides exact linear algebra transformations.
    """

    def __init__(self, vector: Union[np.ndarray, List[complex]], label: str = "custom"):
        vec = np.asarray(vector, dtype=np.complex128)
        if vec.ndim == 1:
            vec = vec.reshape(-1, 1)
        elif vec.ndim == 2 and vec.shape[1] != 1:
            if vec.shape[0] == 1:
                vec = vec.T
            else:
                raise ValueError(f"State vector must have shape (2^n, 1), got {vec.shape}")

        norm_sq = np.vdot(vec, vec).real
        if abs(norm_sq - 1.0) > 1e-6:
            if norm_sq > 1e-12:
                vec = vec / np.sqrt(norm_sq)
            else:
                raise ValueError("State vector norm cannot be zero.")

        self.vector: np.ndarray = vec
        self.dimension: int = vec.shape[0]
        self.n_qubits: int = int(np.log2(self.dimension))
        if 2 ** self.n_qubits != self.dimension:
            raise ValueError(f"State dimension {self.dimension} must be a power of 2.")
        self.label: str = label

    def assert_normalized(self, tol: float = 1e-6) -> None:
        """Asserts that |||psi>||^2 == 1.0 within numerical tolerance."""
        norm_sq = np.vdot(self.vector, self.vector).real
        assert abs(norm_sq - 1.0) < tol, f"State {self.label} is not normalized: norm_sq={norm_sq}"

    def inner_product(self, other: QubitState) -> complex:
        """Computes <self | other>."""
        if self.dimension != other.dimension:
            raise ValueError(f"Dimension mismatch: {self.dimension} vs {other.dimension}")
        return complex(np.vdot(self.vector, other.vector))

    def fidelity(self, other: QubitState) -> float:
        """
        Computes state fidelity F(|psi>, |phi>) = |<psi | phi>|^2.
        For identical pure states, F = 1.0; for orthogonal states, F = 0.0.
        """
        overlap = self.inner_product(other)
        return float(abs(overlap) ** 2)

    def apply_unitary(self, U: np.ndarray, new_label: str = "") -> QubitState:
        """Applies a unitary transformation: |psi'> = U |psi>."""
        if U.shape != (self.dimension, self.dimension):
            raise ValueError(f"Unitary shape {U.shape} does not match state dimension {self.dimension}")
        new_vec = U @ self.vector
        return QubitState(new_vec, label=new_label or f"U({self.label})")

    def tensor(self, other: QubitState, new_label: str = "") -> QubitState:
        """Computes composite tensor product state: |psi> (x) |phi>."""
        composite_vec = np.kron(self.vector, other.vector)
        lbl = new_label or f"({self.label} ⊗ {other.label})"
        return QubitState(composite_vec, label=lbl)

    def to_density_matrix(self) -> np.ndarray:
        """Computes pure density operator rho = |psi><psi|."""
        return self.vector @ self.vector.conj().T

    def __repr__(self) -> str:
        return f"QubitState(qubits={self.n_qubits}, label='{self.label}')"


# Computational Z-basis eigenstates: Z|0> = +|0>, Z|1> = -|1>
STATE_0 = QubitState(np.array([1.0, 0.0]), label="|0⟩")
STATE_1 = QubitState(np.array([0.0, 1.0]), label="|1⟩")

# Hadamard X-basis eigenstates: X|+> = +|+>, X|-> = -|->
STATE_PLUS = QubitState(np.array([1.0, 1.0]) / np.sqrt(2.0), label="|+⟩")
STATE_MINUS = QubitState(np.array([1.0, -1.0]) / np.sqrt(2.0), label="|−⟩")

# Circular Y-basis eigenstates: Y|i+> = +|i+>, Y|i-> = -|i->
STATE_I_PLUS = QubitState(np.array([1.0, 1.0j]) / np.sqrt(2.0), label="|i+⟩")
STATE_I_MINUS = QubitState(np.array([1.0, -1.0j]) / np.sqrt(2.0), label="|i−⟩")

# Canonical Registry of the Six Pauli Eigenstates used in QDS
PAULI_EIGENSTATES = {
    (PauliBasis.Z, 0): STATE_0,
    (PauliBasis.Z, 1): STATE_1,
    (PauliBasis.X, 0): STATE_PLUS,
    (PauliBasis.X, 1): STATE_MINUS,
    (PauliBasis.Y, 0): STATE_I_PLUS,
    (PauliBasis.Y, 1): STATE_I_MINUS,
}


def tensor_product(*states: QubitState) -> QubitState:
    """Computes the Kronecker product of an arbitrary list of quantum states."""
    if not states:
        raise ValueError("At least one state must be provided.")
    result = states[0]
    for s in states[1:]:
        result = result.tensor(s)
    return result


def get_pauli_eigenstate(basis: PauliBasis, bit_value: int) -> QubitState:
    """Retrieves canonical Pauli eigenstate for given basis and bit value."""
    key = (basis, bit_value)
    if key not in PAULI_EIGENSTATES:
        raise ValueError(f"Invalid basis/bit pair: {basis}, {bit_value}")
    return PAULI_EIGENSTATES[key]
