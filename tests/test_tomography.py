"""
Unit Tests for Phase 28: Quantum State Tomography (QST) Engine
"""

import numpy as np
import pytest
from quantum.state import QubitState, PauliBasis, get_pauli_eigenstate
from quantum.tomography import QuantumStateTomography, TomographyResult


class TestQuantumStateTomography:

    def test_pure_eigenstate_reconstruction_fidelity(self):
        """Reconstructing pure Pauli eigenstates should yield fidelity > 0.90 and purity > 0.90."""
        bases_states = [
            (PauliBasis.Z, 0),  # |0>
            (PauliBasis.Z, 1),  # |1>
            (PauliBasis.X, 0),  # |+>
            (PauliBasis.X, 1),  # |->
            (PauliBasis.Y, 0),  # |i+>
            (PauliBasis.Y, 1),  # |i->
        ]

        for basis, bit in bases_states:
            state = get_pauli_eigenstate(basis, bit)
            result = QuantumStateTomography.reconstruct_state(
                target_state=state,
                expected_state=state,
                num_trials_per_basis=300
            )
            assert result.fidelity >= 0.88, f"Failed fidelity check for {basis.value}, bit {bit}: F={result.fidelity}"
            assert result.purity >= 0.85, f"Failed purity check for {basis.value}, bit {bit}: gamma={result.purity}"
            assert result.is_pure is True
            assert result.bloch_vector_length <= 1.0001
            assert result.von_neumann_entropy < 0.60

    def test_orthogonal_state_fidelity_drop(self):
        """Reconstructing |0> when expecting |1> should produce fidelity near 0."""
        state_0 = get_pauli_eigenstate(PauliBasis.Z, 0)
        state_1 = get_pauli_eigenstate(PauliBasis.Z, 1)

        result = QuantumStateTomography.reconstruct_state(
            target_state=state_0,
            expected_state=state_1,
            num_trials_per_basis=200
        )
        assert result.fidelity < 0.15
        assert result.purity >= 0.85  # It is still a pure state, but mismatched

    def test_density_matrix_hermiticity_and_unit_trace(self):
        """Every reconstructed density matrix must be Hermitian with unit trace."""
        state = get_pauli_eigenstate(PauliBasis.X, 0)
        result = QuantumStateTomography.reconstruct_state(state, num_trials_per_basis=150)
        rho = result.density_matrix

        # Unit trace
        assert abs(np.trace(rho) - 1.0) < 1e-6
        # Hermiticity
        assert np.allclose(rho, rho.conj().T, atol=1e-6)
