"""
Q-Sentinel: Projective Measurement & Born Sampling Engine
Stage 3: Phase 8
Implements projective quantum measurement using projection operators and
Born-rule stochastic sampling across N verification trials.
"""

from __future__ import annotations
import numpy as np
from dataclasses import dataclass
from typing import Tuple, Optional
from quantum.state import QubitState, PauliBasis, get_pauli_eigenstate


@dataclass
class MeasurementTrialResult:
    expected_state: QubitState
    received_state: QubitState
    theoretical_match_prob: float
    theoretical_error_prob: float
    num_trials: int
    n_match: int      # n0: outcomes agreeing with expected eigenstate
    n_error: int      # n1: outcomes disagreeing with expected eigenstate
    observed_error_rate: float
    raw_samples: np.ndarray  # 0 for match, 1 for error


def projective_measurement_single(
    state: QubitState,
    basis: PauliBasis,
    random_seed: Optional[int] = None
) -> Tuple[int, float]:
    """
    Performs a single projective measurement on |state⟩ in the specified PauliBasis.
    Returns: (measured_bit, probability_of_that_bit)
    """
    state.assert_normalized()
    state_0 = get_pauli_eigenstate(basis, 0)
    state_1 = get_pauli_eigenstate(basis, 1)
    
    # Born rule probabilities: P(i) = |⟨state_i | state⟩|²
    p0 = state_0.fidelity(state)
    p1 = state_1.fidelity(state)
    
    # Clip and normalize
    probs = np.array([p0, p1])
    probs = np.clip(probs, 0.0, 1.0)
    probs /= np.sum(probs)
    
    rng = np.random.default_rng(random_seed)
    measured_bit = int(rng.choice([0, 1], p=probs))
    return measured_bit, float(probs[measured_bit])


def sample_projective_trials(
    received_state: QubitState,
    expected_state: QubitState,
    num_trials: int = 200,
    ambient_noise: float = 0.0,
    random_seed: Optional[int] = None
) -> MeasurementTrialResult:
    """
    Simulates N repeated projective verification measurements against an expected eigenstate.
    
    ambient_noise: Natural channel decoherence baseline (e.g., 0.03 for 3% optical QBER).
    
    Returns MeasurementTrialResult containing empirical outcome distributions.
    """
    received_state.assert_normalized()
    expected_state.assert_normalized()
    
    # Theoretical quantum overlap: F = |⟨expected | received⟩|²
    fidelity = expected_state.fidelity(received_state)
    
    # Incorporate baseline ambient channel noise:
    # Error probability: P_error = (1 - fidelity) + ambient_noise * fidelity
    p_error_theoretical = float(np.clip((1.0 - fidelity) + ambient_noise * fidelity, 0.0, 1.0))
    p_match_theoretical = 1.0 - p_error_theoretical
    
    rng = np.random.default_rng(random_seed)
    # Samples: 0 = match (valid), 1 = error (tampered/noise)
    samples = rng.choice(
        [0, 1],
        size=num_trials,
        p=[p_match_theoretical, p_error_theoretical]
    )
    
    n_error = int(np.sum(samples))
    n_match = num_trials - n_error
    e_hat = float(n_error / num_trials)
    
    return MeasurementTrialResult(
        expected_state=expected_state,
        received_state=received_state,
        theoretical_match_prob=p_match_theoretical,
        theoretical_error_prob=p_error_theoretical,
        num_trials=num_trials,
        n_match=n_match,
        n_error=n_error,
        observed_error_rate=e_hat,
        raw_samples=samples
    )
