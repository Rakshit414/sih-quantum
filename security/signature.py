"""
Q-Sentinel: Quantum Digital Signature (QDS) Engine
Stage 3: Phases 6 & 7
Implements message digest encoding, Pauli-eigenstate signature generation,
and signature distribution via the quantum teleportation channel.
"""

from __future__ import annotations
import hashlib
import secrets
import time
from dataclasses import dataclass, field
from typing import List, Tuple, Optional
import numpy as np
from quantum.state import QubitState, PauliBasis, get_pauli_eigenstate
from quantum.teleport import teleport_qubit, TeleportationResult


@dataclass
class SignatureToken:
    index: int
    bit_value: int
    basis: PauliBasis
    eigenstate: QubitState


@dataclass
class QuantumDigitalSignature:
    message: str
    message_digest: str
    signer_id: str
    tokens: List[SignatureToken]
    timestamp: float = field(default_factory=time.time)
    nonce: str = field(default_factory=lambda: secrets.token_hex(16))

    @property
    def token_count(self) -> int:
        return len(self.tokens)

    @property
    def eigenstates(self) -> List[QubitState]:
        return [t.eigenstate for t in self.tokens]


class QDSKeyManager:
    """
    Manages private and public key representations for teleportation-based QDS.
    Uses cryptographically generated deterministic sequences for Pauli basis mappings.
    """

    def __init__(self, signer_id: str, private_seed: Optional[str] = None):
        self.signer_id = signer_id
        self.private_seed = private_seed or secrets.token_hex(32)

    def generate_signature(self, message: str, num_tokens: int = 8) -> QuantumDigitalSignature:
        """
        Signs a classical message by:
        1. Computing SHA-256 digest of the message.
        2. Deriving a deterministic basis sequence from private_seed and digest.
        3. Preparing an array of Pauli eigenstates { |s_1⟩, ..., |s_m⟩ }.
        """
        digest = hashlib.sha256(message.encode("utf-8")).hexdigest()
        digest_bytes = bytes.fromhex(digest)
        seed_bytes = bytes.fromhex(hashlib.sha256(self.private_seed.encode("utf-8")).hexdigest())

        tokens: List[SignatureToken] = []
        bases = [PauliBasis.Z, PauliBasis.X, PauliBasis.Y]

        for i in range(num_tokens):
            # Deterministic bit and basis derivation
            bit_val = (digest_bytes[i % len(digest_bytes)] >> (i % 8)) & 1
            basis_idx = (seed_bytes[i % len(seed_bytes)] + i) % 3
            basis = bases[basis_idx]

            state = get_pauli_eigenstate(basis, bit_val)
            token = SignatureToken(
                index=i,
                bit_value=bit_val,
                basis=basis,
                eigenstate=state
            )
            tokens.append(token)

        return QuantumDigitalSignature(
            message=message,
            message_digest=digest,
            signer_id=self.signer_id,
            tokens=tokens
        )


@dataclass
class TransmittedQDS:
    original_signature: QuantumDigitalSignature
    teleportation_results: List[TeleportationResult]
    received_states: List[QubitState]
    average_teleportation_fidelity: float


def distribute_signature_via_teleportation(
    signature: QuantumDigitalSignature,
    random_seed: Optional[int] = None
) -> TransmittedQDS:
    """
    Teleports each qubit of the quantum digital signature from Signer to Verifier.
    """
    results: List[TeleportationResult] = []
    received_states: List[QubitState] = []
    
    for i, token in enumerate(signature.tokens):
        seed = (random_seed + i) if random_seed is not None else None
        res = teleport_qubit(token.eigenstate, random_seed=seed)
        results.append(res)
        received_states.append(res.recovered_state)
        
    avg_fidelity = float(np.mean([r.fidelity for r in results])) if results else 1.0
    
    return TransmittedQDS(
        original_signature=signature,
        teleportation_results=results,
        received_states=received_states,
        average_teleportation_fidelity=avg_fidelity
    )
