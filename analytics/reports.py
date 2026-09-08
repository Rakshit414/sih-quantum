"""
Q-Sentinel: Formal Security Audit Certificate and Incident Report Generator
Produces exportable, tamper-evident cryptographic verification certificates (JSON and Plaintext)
for institutional audit trails and regulatory compliance.
"""

from __future__ import annotations
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional

from security.detector import ThreatAssessment, ThreatCategory
from security.signature import QuantumDigitalSignature
from security.multirecipient import MultiRecipientVerificationResult


class AuditReportGenerator:
    """
    Constructs formal audit certificates and incident response reports from Q-STAT evaluations.
    """

    @staticmethod
    def generate_verification_certificate_json(
        assessment: ThreatAssessment,
        signature: QuantumDigitalSignature,
        message: str,
        latency_ms: float = 0.0,
        multi_recipient: Optional[MultiRecipientVerificationResult] = None
    ) -> str:
        """
        Generates a structured JSON certificate containing complete statistical proofs and metadata.
        """
        cert_id = f"QDS-CERT-{uuid.uuid4().hex[:12].upper()}"
        now_utc = datetime.now(timezone.utc).isoformat()

        report_data = {
            "certificate_id": cert_id,
            "issuance_timestamp_utc": now_utc,
            "standard_specification": "SIH-26141 Q-SENTINEL PROTOCOL V2.0",
            "cryptographic_scheme": "Teleportation-Based Quantum Digital Signature (QDS)",
            "message_payload": {
                "content": message,
                "claimed_signer_identity": signature.signer_id,
                "token_count": len(signature.tokens),
                "nonce": signature.nonce,
                "message_timestamp": signature.timestamp
            },
            "quantum_transport_diagnostics": {
                "protocol": "3-Qubit Joint Bell-State Measurement (BSM)",
                "correction_gates_applied": "Pauli Unitary U = Z^{b1} X^{b2}",
                "baseline_noise_floor_p0": assessment.baseline_noise_p0,
                "measurement_trials_per_token": assessment.token_trials[0].num_trials if assessment.token_trials else 0,
                "total_projective_measurements": sum(t.num_trials for t in assessment.token_trials) if assessment.token_trials else 0
            },
            "statistical_evaluation_qstat": {
                "observed_error_rate": round(assessment.error_rate, 6),
                "exact_binomial_p_value": assessment.p_value,
                "standardized_z_score": round(assessment.z_score, 4),
                "statistical_confidence_pct": round(assessment.confidence * 100.0, 4),
                "confidence_interval_95": [round(assessment.ci_lower, 4), round(assessment.ci_upper, 4)],
                "freshness_validation": "PASSED" if assessment.freshness_passed else "FAILED_REPLAY",
                "verdict": assessment.verdict.value,
                "evaluation_latency_ms": round(latency_ms, 3)
            },
            "audit_decision": {
                "status": "APPROVED_AUTHENTIC" if assessment.verdict == ThreatCategory.LEGITIMATE else "REJECTED_THREAT_DETECTED",
                "diagnostic_proof": assessment.diagnostic_text
            }
        }

        if multi_recipient:
            report_data["multi_party_non_repudiation"] = {
                "cross_discrepancy_rate": round(multi_recipient.cross_discrepancy_rate, 4),
                "cross_z_score": round(multi_recipient.cross_z_score, 4),
                "non_repudiation_status": "VERIFIED_TRANSFERABLE" if multi_recipient.non_repudiation_passed else "REPUDIATION_ATTACK_DETECTED",
                "summary": multi_recipient.audit_summary
            }

        return json.dumps(report_data, indent=2)

    @staticmethod
    def generate_plain_text_certificate(
        assessment: ThreatAssessment,
        signature: QuantumDigitalSignature,
        message: str,
        latency_ms: float = 0.0
    ) -> str:
        """
        Renders a clean, official plain-text verification certificate.
        """
        cert_id = f"QDS-CERT-{uuid.uuid4().hex[:12].upper()}"
        now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        status_str = "AUTHENTIC AND ACCEPTED" if assessment.verdict == ThreatCategory.LEGITIMATE else f"REJECTED - {assessment.verdict.value}"

        lines = [
            "================================================================================",
            "                 Q-SENTINEL QUANTUM DIGITAL SIGNATURE AUDIT CERTIFICATE         ",
            "================================================================================",
            f"Certificate Reference : {cert_id}",
            f"Timestamp (UTC)       : {now_utc}",
            f"Protocol Standard     : Information-Theoretic Teleportation QDS (SIH-26141)",
            "--------------------------------------------------------------------------------",
            "TRANSACTION IDENTIFIERS:",
            f"Claimed Signer        : {signature.signer_id}",
            f"Message Payload       : {message}",
            f"Session Nonce         : {signature.nonce}",
            f"Number of Tokens      : {len(signature.tokens)} Pauli Eigenstates",
            "--------------------------------------------------------------------------------",
            "QUANTUM STATISTICAL TELEMETRY (Q-STAT):",
            f"Calibrated Noise Floor (p0) : {assessment.baseline_noise_p0 * 100.0:.2f}%",
            f"Observed Error Rate (e_hat) : {assessment.error_rate * 100.0:.2f}%",
            f"Standardized z-Score        : {assessment.z_score:+.4f} sigma",
            f"Exact Binomial p-Value      : {assessment.p_value:.6e}",
            f"Statistical Confidence      : {assessment.confidence * 100.0:.2f}%",
            f"Freshness Nonce Integrity   : {'VALID / UNUSED' if assessment.freshness_passed else 'REPLAY DETECTED'}",
            f"Verification Latency        : {latency_ms:.2f} ms",
            "--------------------------------------------------------------------------------",
            "FORMAL VERDICT & AUDIT DETERMINATION:",
            f"Assessment Classification   : {assessment.verdict.value}",
            f"Final Security Disposition  : {status_str}",
            f"Diagnostic Proof            : {assessment.diagnostic_text}",
            "================================================================================",
            "This certificate is issued under exact statistical binomial proof with zero ML.",
            "================================================================================"
        ]
        return "\n".join(lines)
