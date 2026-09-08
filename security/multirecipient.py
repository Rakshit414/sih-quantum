"""
Q-Sentinel: Multi-Party Non-Repudiation Cross-Verification Protocol
Implements quantum signature transferability and cross-recipient consistency checks
to prevent repudiation and dispute attacks (Alice denying her signature to Charlie).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional
import numpy as np

from quantum.state import QubitState, PauliBasis, get_pauli_eigenstate
from security.signature import QuantumDigitalSignature, SignatureToken, QDSKeyManager
from security.detector import QStatDetector, ThreatAssessment, ThreatCategory
from security.attacks import AttackScenario, ThreatOrchestrator


@dataclass
class MultiRecipientVerificationResult:
    """
    Encapsulates results from a multi-party QDS verification exchange
    between Alice (Signer), Bob (Primary Recipient), and Charlie (Secondary Recipient / Arbiter).
    """
    message: str
    signer_id: str
    bob_assessment: ThreatAssessment
    charlie_assessment: ThreatAssessment
    cross_discrepancy_rate: float
    cross_z_score: float
    non_repudiation_passed: bool
    verdict: ThreatCategory
    audit_summary: str


class MultiRecipientCoordinator:
    """
    Orchestrates multi-party QDS distribution and dispute-prevention cross-checks.
    """

    def __init__(self, detector: Optional[QStatDetector] = None):
        self.detector = detector or QStatDetector(baseline_noise_p0=0.03)

    def verify_multi_recipient_session(
        self,
        message: str,
        signer_manager: QDSKeyManager,
        simulate_repudiation: bool = False,
        trials_per_token: int = 50,
        ambient_noise: float = 0.03
    ) -> MultiRecipientVerificationResult:
        """
        Executes signature generation and dual-recipient teleportation to Bob and Charlie.
        If simulate_repudiation is True, Alice maliciously sends conflicting quantum states
        to Charlie to attempt subsequent repudiation before an arbiter.
        """
        # 1. Alice generates legitimate signature intended for Bob
        sig_bob = signer_manager.generate_signature(message, num_tokens=8)

        # 2. Alice generates signature for Charlie
        if simulate_repudiation:
            # Alice deliberately tampers with Charlie's tokens (e.g. inverted bases or forged tokens)
            sig_charlie, _ = ThreatOrchestrator.execute_scenario(
                scenario=AttackScenario.FORGERY,
                original_signature=sig_bob
            )
        else:
            # Honest distribution: identical valid quantum signature states
            sig_charlie = signer_manager.generate_signature(message, num_tokens=8)

        # 3. Bob measures and evaluates his signature
        bob_assessment = self.detector.verify_signature_session(
            received_signature=sig_bob,
            expected_signature=sig_bob,
            trials_per_token=trials_per_token,
            ambient_noise=ambient_noise
        )

        # 4. Charlie measures and evaluates his signature
        charlie_assessment = self.detector.verify_signature_session(
            received_signature=sig_charlie,
            expected_signature=sig_bob,  # Compared against Alice's public record
            trials_per_token=trials_per_token,
            ambient_noise=ambient_noise
        )

        # 5. Cross-Verification Check between Bob and Charlie (Token Symmetrization)
        # Compare empirical agreement across measurement trials
        n_tokens = len(bob_assessment.token_trials)
        discrepancies = 0
        total_comparisons = n_tokens

        for i in range(n_tokens):
            bob_trial = bob_assessment.token_trials[i]
            charlie_trial = charlie_assessment.token_trials[i]
            
            # Check if Bob and Charlie observe statistically divergent error distributions
            bob_err_rate = bob_trial.n_error / bob_trial.num_trials
            charlie_err_rate = charlie_trial.n_error / charlie_trial.num_trials
            
            if abs(bob_err_rate - charlie_err_rate) > 0.20:
                discrepancies += 1

        cross_discrepancy_rate = discrepancies / max(1, total_comparisons)
        
        # Standardized cross z-score
        std_cross = np.sqrt(0.03 * 0.97 / max(1, total_comparisons))
        cross_z = (cross_discrepancy_rate - 0.03) / std_cross if std_cross > 0 else 0.0

        # Non-repudiation condition: Both verifiers agree and cross discrepancy is negligible
        both_legit = (
            bob_assessment.verdict == ThreatCategory.LEGITIMATE and
            charlie_assessment.verdict == ThreatCategory.LEGITIMATE
        )
        non_repudiation_passed = both_legit and (cross_discrepancy_rate <= 0.125)

        if not non_repudiation_passed:
            verdict = ThreatCategory.MALICIOUS
            if simulate_repudiation:
                summary = "Repudiation Attack Detected: Alice submitted conflicting quantum signature states to Bob and Charlie."
            else:
                summary = f"Multi-party verification failed. Bob verdict: {bob_assessment.verdict.value}, Charlie verdict: {charlie_assessment.verdict.value}."
        else:
            verdict = ThreatCategory.LEGITIMATE
            summary = "Non-Repudiation Verified: Bob and Charlie exhibit statistical state consistency under information-theoretic bounds."

        return MultiRecipientVerificationResult(
            message=message,
            signer_id=signer_manager.signer_id,
            bob_assessment=bob_assessment,
            charlie_assessment=charlie_assessment,
            cross_discrepancy_rate=cross_discrepancy_rate,
            cross_z_score=float(cross_z),
            non_repudiation_passed=non_repudiation_passed,
            verdict=verdict,
            audit_summary=summary
        )
