"""
Unit tests for Q-Sentinel Stage 1: Quantum Foundations & State Representation
Phases 1, 2, 3
"""
import unittest
import numpy as np
from quantum.state import (
    QubitState,
    PauliBasis,
    PAULI_X,
    PAULI_Y,
    PAULI_Z,
    STATE_0,
    STATE_1,
    STATE_PLUS,
    STATE_MINUS,
    STATE_I_PLUS,
    STATE_I_MINUS,
    get_pauli_eigenstate,
    tensor_product,
)


class TestQuantumState(unittest.TestCase):

    def test_normalization_and_dimensions(self):
        # 1-qubit normalization
        q = QubitState([3.0, 4.0])
        self.assertEqual(q.dimension, 2)
        self.assertEqual(q.n_qubits, 1)
        q.assert_normalized()
        np.testing.assert_allclose(np.vdot(q.vector, q.vector).real, 1.0, atol=1e-7)

    def test_pauli_z_eigenstates(self):
        # Z|0> = |0>, Z|1> = -|1>
        z0 = STATE_0.apply_unitary(PAULI_Z)
        self.assertAlmostEqual(z0.fidelity(STATE_0), 1.0)
        z1 = STATE_1.apply_unitary(PAULI_Z)
        self.assertAlmostEqual(z1.fidelity(STATE_1), 1.0)
        self.assertAlmostEqual(STATE_0.fidelity(STATE_1), 0.0)

    def test_pauli_x_eigenstates(self):
        # X|+> = |+>, X|-> = -|->
        x_plus = STATE_PLUS.apply_unitary(PAULI_X)
        self.assertAlmostEqual(x_plus.fidelity(STATE_PLUS), 1.0)
        x_minus = STATE_MINUS.apply_unitary(PAULI_X)
        self.assertAlmostEqual(x_minus.fidelity(STATE_MINUS), 1.0)
        self.assertAlmostEqual(STATE_PLUS.fidelity(STATE_MINUS), 0.0)

    def test_pauli_y_eigenstates(self):
        # Y|i+> = |i+>, Y|i-> = -|i->
        y_plus = STATE_I_PLUS.apply_unitary(PAULI_Y)
        self.assertAlmostEqual(y_plus.fidelity(STATE_I_PLUS), 1.0)
        y_minus = STATE_I_MINUS.apply_unitary(PAULI_Y)
        self.assertAlmostEqual(y_minus.fidelity(STATE_I_MINUS), 1.0)
        self.assertAlmostEqual(STATE_I_PLUS.fidelity(STATE_I_MINUS), 0.0)

    def test_mutually_unbiased_bases_overlaps(self):
        # Overlap between Z eigenstates and X eigenstates is exactly 0.5 (1/sqrt(2) squared)
        self.assertAlmostEqual(STATE_0.fidelity(STATE_PLUS), 0.5)
        self.assertAlmostEqual(STATE_0.fidelity(STATE_MINUS), 0.5)
        self.assertAlmostEqual(STATE_1.fidelity(STATE_PLUS), 0.5)
        self.assertAlmostEqual(STATE_1.fidelity(STATE_MINUS), 0.5)
        # Overlap with Y basis is also 0.5
        self.assertAlmostEqual(STATE_0.fidelity(STATE_I_PLUS), 0.5)
        self.assertAlmostEqual(STATE_PLUS.fidelity(STATE_I_PLUS), 0.5)

    def test_tensor_product(self):
        # |0> (x) |1> should be [0, 1, 0, 0]^T
        q01 = tensor_product(STATE_0, STATE_1)
        self.assertEqual(q01.dimension, 4)
        self.assertEqual(q01.n_qubits, 2)
        expected = np.array([[0.0], [1.0], [0.0], [0.0]], dtype=np.complex128)
        np.testing.assert_allclose(q01.vector, expected, atol=1e-7)

    def test_eigenstate_registry_retrieval(self):
        s = get_pauli_eigenstate(PauliBasis.X, 0)
        self.assertAlmostEqual(s.fidelity(STATE_PLUS), 1.0)
        s = get_pauli_eigenstate(PauliBasis.Z, 1)
        self.assertAlmostEqual(s.fidelity(STATE_1), 1.0)


if __name__ == "__main__":
    unittest.main()
