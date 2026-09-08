"""
Q-Sentinel: Post-Quantum Classical Hybrid Verification Engine (Q-HYBRID)
Stage 10: Phase 29
Implements dual-layer defense-in-depth:
Layer 1: Classical Cryptographic Integrity (SHA3-512 with HMAC binding)
Layer 2: Teleportation-based Quantum Digital Signature (QDS) verified via Q-STAT
Ensures forward security and protects against classical key extraction or quantum transport outages.
"""

from __future__ import annotations
import hashlib
import hmac
from dataclasses import dataclass
from typing import Tuple, Optional

from security.signature import QuantumDigitalSignature, QDSKeyManager
from security.detector import QStatDetector, ThreatAssessment, ThreatCategory


@dataclass
class HybridVerificationResult:
    """
    Dual-layer verification outcome across classical and quantum dimensions.
    """
    message: str
    signer_id: str
    classical_hash_matched: bool
    classical_digest: str
    quantum_assessment: ThreatAssessment
    overall_verdict: ThreatCategory
    hybrid_confidence: float
    security_summary: str


class HybridSignatureVerifier:
    """
    Evaluates dual-layer hybrid signatures combining classical SHA3-512 digests and quantum states.
    """

    def __init__(self, detector: Optional[QStatDetector] = None):
        self.detector = detector or QStatDetector(baseline_noise_p0=0.03)

    @staticmethod
    def compute_classical_digest(message: str, signer_seed: str) -> str:
        """
        Computes an HMAC-SHA3-512 classical cryptographic digest of the message payload.
        """
        key_bytes = signer_seed.encode("utf-8")
        msg_bytes = message.encode("utf-8")
        return hmac.new(key_bytes, msg_bytes, hashlib.sha3_512).hexdigest()

    def verify_hybrid_signature(
        self,
        message: str,
        claimed_classical_digest: str,
        received_quantum_signature: QuantumDigitalSignature,
        expected_quantum_signature: QuantumDigitalSignature,
        signer_seed: str,
        trials_per_token: int = 50,
        ambient_noise: float = 0.03
    ) -> HybridVerificationResult:
        """
        Executes dual-layer verification:
        1. Verifies classical SHA3-512 HMAC digest integrity.
        2. Verifies quantum teleportation states via Q-STAT.
        """
        # 1. Classical Layer Evaluation
        expected_digest = self.compute_classical_digest(message, signer_seed)
        classical_matched = hmac.compare_digest(claimed_classical_digest, expected_digest)

        # 2. Quantum Layer Evaluation
        quantum_assessment = self.detector.verify_signature_session(
            received_signature=received_quantum_signature,
            expected_signature=expected_quantum_signature,
            trials_per_token=trials_per_token,
            ambient_noise=ambient_noise
        )

        # 3. Hybrid Decision Logic
        if not classical_matched:
            # Classical tampering detected (payload alteration or key mismatch)
            overall_verdict = ThreatCategory.MALICIOUS
            hybrid_confidence = 1.0
            summary = "Classical Integrity Failure: HMAC-SHA3-512 message digest mismatch. Message payload tampered."
        elif quantum_assessment.verdict == ThreatCategory.MALICIOUS:
            # Quantum signature state rejected (forgery, impersonation, or replay)
            overall_verdict = ThreatCategory.MALICIOUS
            hybrid_confidence = quantum_assessment.confidence
            summary = f"Quantum Security Breach: Classical hash valid, but Q-STAT rejected quantum states ({quantum_assessment.diagnostic_text})."
        elif quantum_assessment.verdict == ThreatCategory.SUSPICIOUS:
            overall_verdict = ThreatCategory.SUSPICIOUS
            hybrid_confidence = quantum_assessment.confidence
            summary = "Classical Hash Valid. Quantum channel exhibits elevated noise / suspicious disturbance."
        else:
            overall_verdict = ThreatCategory.LEGITIMATE
            hybrid_confidence = quantum_assessment.confidence
            summary = "Dual-Layer Verified: Both classical HMAC-SHA3-512 and quantum teleportation states verified authentic."

        return HybridVerificationResult(
            message=message,
            signer_id=received_quantum_signature.signer_id,
            classical_hash_matched=classical_matched,
            classical_digest=claimed_classical_digest[:16] + "...",
            quantum_assessment=quantum_assessment,
            overall_verdict=overall_verdict,
            hybrid_confidence=hybrid_confidence,
            security_summary=summary
        )
