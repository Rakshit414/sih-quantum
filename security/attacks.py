"""
Q-Sentinel: Adversarial Threat Modeling & Attack Simulation Engine
Stage 4: Phases 9, 10, 12, 13
Simulates Forgery, Impersonation, Replay, and Quantum Channel Disturbance (Bit/Phase Flips).
"""

from __future__ import annotations
import numpy as np
import time
from enum import Enum
from typing import List, Tuple, Optional
from quantum.state import (
    QubitState,
    PauliBasis,
    PAULI_X,
    PAULI_Y,
    PAULI_Z,
    get_pauli_eigenstate,
)
from security.signature import (
    QuantumDigitalSignature,
    SignatureToken,
    QDSKeyManager,
)


class AttackScenario(Enum):
    LEGITIMATE = "Legitimate"
    FORGERY = "Signature Forgery"
    IMPERSONATION = "Signer Impersonation"
    REPLAY = "Replay Attack"
    CHANNEL_NOISE = "Channel Manipulation / Noise"


def apply_quantum_channel_noise(
    state: QubitState,
    noise_level: float,
    basis: Optional[PauliBasis] = None,
    bit_value: Optional[int] = None,
    rng: Optional[np.random.Generator] = None
) -> Tuple[QubitState, str]:
    """
    Applies quantum channel noise parameterized by error probability epsilon.
    When basis and bit_value are provided, channel errors flip the state towards
    the orthogonal subspace, causing measurement disturbances observable in that basis.
    """
    if noise_level <= 0.0:
        return state, "No noise applied"

    if rng is None:
        rng = np.random.default_rng()

    if rng.random() < noise_level:
        if basis is not None and bit_value is not None:
            flipped_state = get_pauli_eigenstate(basis, 1 - bit_value)
            return flipped_state, f"Channel Error ({basis.value}-basis flip)"
        else:
            err = rng.choice([PAULI_X, PAULI_Y, PAULI_Z])
            return QubitState(err @ state.vector, label=f"Noisy({state.label})"), "Pauli Channel Noise"

    return state, "Clean transmission"


def simulate_forgery_attack(
    original_signature: QuantumDigitalSignature,
    random_seed: Optional[int] = None
) -> Tuple[QuantumDigitalSignature, str]:
    """
    Threat Model 1: Signature Forgery.
    Adversary Eve fabricates a signature without possessing the private key seed.
    Eve guesses random eigenstates; measurement overlap drops to ~50%.
    """
    rng = np.random.default_rng(random_seed)
    bases = [PauliBasis.Z, PauliBasis.X, PauliBasis.Y]
    forged_tokens: List[SignatureToken] = []

    for token in original_signature.tokens:
        guessed_basis = rng.choice(bases)
        guessed_bit = int(rng.choice([0, 1]))
        guessed_state = get_pauli_eigenstate(guessed_basis, guessed_bit)
        
        forged_tokens.append(SignatureToken(
            index=token.index,
            bit_value=guessed_bit,
            basis=guessed_basis,
            eigenstate=guessed_state
        ))

    forged_sig = QuantumDigitalSignature(
        message=original_signature.message,
        message_digest=original_signature.message_digest,
        signer_id=original_signature.signer_id,
        tokens=forged_tokens,
        timestamp=original_signature.timestamp,
        nonce=original_signature.nonce
    )
    desc = "Adversary Eve forged signature tokens using random Pauli basis guesses."
    return forged_sig, desc


def simulate_impersonation_attack(
    original_signature: QuantumDigitalSignature,
    adversary_id: str = "Mallory",
    random_seed: Optional[int] = None
) -> Tuple[QuantumDigitalSignature, str]:
    """
    Threat Model 2: Signer Impersonation.
    Adversary Mallory signs the message with her own key seed, but attaches Alice's
    claimed Signer ID. The verifier uses Alice's registered bases, resulting in ~50% mismatch.
    """
    mallory_mgr = QDSKeyManager(signer_id=adversary_id, private_seed="mallory_unauthorized_seed_42")
    mallory_sig = mallory_mgr.generate_signature(
        message=original_signature.message,
        num_tokens=original_signature.token_count
    )

    # Impersonate Alice by spoofing signer_id
    impersonated_sig = QuantumDigitalSignature(
        message=original_signature.message,
        message_digest=original_signature.message_digest,
        signer_id=original_signature.signer_id,  # Claiming Alice!
        tokens=mallory_sig.tokens,
        timestamp=original_signature.timestamp,
        nonce=original_signature.nonce
    )
    desc = f"Adversary '{adversary_id}' signed message using unauthorized key, masquerading as '{original_signature.signer_id}'."
    return impersonated_sig, desc


def simulate_replay_attack(
    original_signature: QuantumDigitalSignature,
    simulated_delay_seconds: float = 120.0
) -> Tuple[QuantumDigitalSignature, str]:
    """
    Threat Model 3: Replay Attack.
    Adversary intercepts a previously valid signature token and attempts to retransmit
    it at a later time with identical nonces and stale timestamps.
    """
    replayed_sig = QuantumDigitalSignature(
        message=original_signature.message,
        message_digest=original_signature.message_digest,
        signer_id=original_signature.signer_id,
        tokens=original_signature.tokens,
        timestamp=original_signature.timestamp - simulated_delay_seconds,  # Stale timestamp
        nonce=original_signature.nonce  # Reused duplicate nonce
    )
    desc = f"Adversary intercepted and retransmitted previous session (stale by {simulated_delay_seconds:.0f}s, reused nonce '{original_signature.nonce[:8]}...')."
    return replayed_sig, desc


class ThreatOrchestrator:
    """
    Unified simulation dispatcher for all 5 security scenarios.
    """

    @staticmethod
    def execute_scenario(
        scenario: AttackScenario,
        original_signature: QuantumDigitalSignature,
        channel_noise_level: float = 0.0,
        random_seed: Optional[int] = None
    ) -> Tuple[QuantumDigitalSignature, str]:
        """
        Applies selected attack scenario to the signature.
        """
        if scenario == AttackScenario.LEGITIMATE:
            return original_signature, "Honest transmission under standard channel conditions."
        elif scenario == AttackScenario.FORGERY:
            return simulate_forgery_attack(original_signature, random_seed=random_seed)
        elif scenario == AttackScenario.IMPERSONATION:
            return simulate_impersonation_attack(original_signature, random_seed=random_seed)
        elif scenario == AttackScenario.REPLAY:
            return simulate_replay_attack(original_signature)
        elif scenario == AttackScenario.CHANNEL_NOISE:
            rng = np.random.default_rng(random_seed)
            noisy_tokens: List[SignatureToken] = []
            applied_perturbations = []
            for t in original_signature.tokens:
                disturbed_state, perturb_desc = apply_quantum_channel_noise(
                    t.eigenstate, channel_noise_level, basis=t.basis, bit_value=t.bit_value, rng=rng
                )
                noisy_tokens.append(SignatureToken(
                    index=t.index,
                    bit_value=t.bit_value,
                    basis=t.basis,
                    eigenstate=disturbed_state
                ))
                if perturb_desc != "Clean transmission":
                    applied_perturbations.append(f"Qubit {t.index}: {perturb_desc}")

            # If noise level > 0 and no qubit was perturbed by chance, perturb at least one
            if not applied_perturbations and channel_noise_level > 0.0 and noisy_tokens:
                idx = int(rng.integers(0, len(noisy_tokens)))
                t = noisy_tokens[idx]
                flipped_state = get_pauli_eigenstate(t.basis, 1 - t.bit_value)
                noisy_tokens[idx] = SignatureToken(
                    index=t.index,
                    bit_value=t.bit_value,
                    basis=t.basis,
                    eigenstate=flipped_state
                )
                applied_perturbations.append(f"Qubit {idx}: Bit-Flip ({t.basis.value})")

            noisy_sig = QuantumDigitalSignature(
                message=original_signature.message,
                message_digest=original_signature.message_digest,
                signer_id=original_signature.signer_id,
                tokens=noisy_tokens,
                timestamp=original_signature.timestamp,
                nonce=original_signature.nonce
            )
            summary = f"Channel manipulation with error rate ε = {channel_noise_level*100:.1f}%. "
            summary += f"({len(applied_perturbations)} qubits disturbed: {', '.join(applied_perturbations[:3])}...)" if applied_perturbations else "(No bits perturbed this run)"
            return noisy_sig, summary
        else:
            raise ValueError(f"Unknown attack scenario: {scenario}")
