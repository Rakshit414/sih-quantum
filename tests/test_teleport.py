"""
Unit tests for Q-Sentinel Stage 2: Bell States and Teleportation Protocol
Phases 4 & 5
"""
import unittest
import numpy as np
from quantum.state import (
    STATE_0,
    STATE_1,
    STATE_PLUS,
    STATE_MINUS,
    STATE_I_PLUS,
    STATE_I_MINUS,
    QubitState,
)
from quantum.bell import create_bell_state, BellStateType, verify_maximal_entanglement, partial_trace_b
from quantum.teleport import teleport_qubit, get_pauli_correction_matrix


class TestTeleportation(unittest.TestCase):

    def test_all_four_bell_states_maximal_entanglement(self):
        for b_type in BellStateType:
            bell = create_bell_state(b_type)
            self.assertEqual(bell.dimension, 4)
            self.assertEqual(bell.n_qubits, 2)
            self.assertTrue(verify_maximal_entanglement(bell), f"Bell state {b_type} failed maximal entanglement check")

    def test_bell_state_reduced_density_matrix(self):
        phi_plus = create_bell_state(BellStateType.PHI_PLUS)
        rho_ab = phi_plus.to_density_matrix()
        rho_a = partial_trace_b(rho_ab)
        # For maximally entangled state, rho_A must be 0.5 * I_2
        expected_rho_a = np.array([[0.5, 0.0], [0.0, 0.5]], dtype=np.complex128)
        np.testing.assert_allclose(rho_a, expected_rho_a, atol=1e-7)

    def test_teleportation_fidelity_all_six_pauli_eigenstates(self):
        test_states = [STATE_0, STATE_1, STATE_PLUS, STATE_MINUS, STATE_I_PLUS, STATE_I_MINUS]
        for state in test_states:
            # Test all 4 possible Bell measurement outcomes
            for forced_bits in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                result = teleport_qubit(state, forced_bits=forced_bits)
                self.assertTrue(result.success, f"Teleportation failed for {state.label} with bits {forced_bits}")
                self.assertAlmostEqual(result.fidelity, 1.0, places=5)

    def test_teleportation_arbitrary_superposition_state(self):
        # Arbitrary normalized superposition: cos(pi/6)|0> + e^{i*pi/4}sin(pi/6)|1>
        theta = np.pi / 6.0
        phi = np.pi / 4.0
        alpha = np.cos(theta)
        beta = np.exp(1.0j * phi) * np.sin(theta)
        custom_state = QubitState(np.array([alpha, beta]), label="|custom⟩")
        
        # Test 10 random teleportation runs
        for i in range(10):
            res = teleport_qubit(custom_state, random_seed=i)
            self.assertTrue(res.success)
            self.assertAlmostEqual(res.fidelity, 1.0, places=5)

    def test_pauli_correction_matrices(self):
        U00, name00 = get_pauli_correction_matrix(0, 0)
        self.assertEqual(name00, "I")
        U01, name01 = get_pauli_correction_matrix(0, 1)
        self.assertEqual(name01, "X")
        U10, name10 = get_pauli_correction_matrix(1, 0)
        self.assertEqual(name10, "Z")
        U11, name11 = get_pauli_correction_matrix(1, 1)
        self.assertEqual(name11, "ZX")


if __name__ == "__main__":
    unittest.main()
