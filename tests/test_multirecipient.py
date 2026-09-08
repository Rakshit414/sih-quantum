"""
Unit Tests for Phase 27: Multi-Party Non-Repudiation Cross-Verification & Formal Audit Reporting
"""

import json
import pytest
from security.signature import QDSKeyManager
from security.detector import QStatDetector, ThreatCategory
from security.multirecipient import MultiRecipientCoordinator
from analytics.reports import AuditReportGenerator


class TestMultiRecipientAndReports:

    def setup_method(self):
        import numpy as np
        np.random.seed(42)
        self.detector = QStatDetector(baseline_noise_p0=0.03)
        self.coordinator = MultiRecipientCoordinator(detector=self.detector)
        self.alice_mgr = QDSKeyManager(signer_id="Alice", private_seed="alice_test_seed_12345")

    def test_honest_multi_recipient_verification(self):
        """Honest signature sent to Bob and Charlie should pass non-repudiation with 0 discrepancy."""
        message = "Transfer Approval #5544"
        result = self.coordinator.verify_multi_recipient_session(
            message=message,
            signer_manager=self.alice_mgr,
            simulate_repudiation=False,
            trials_per_token=40,
            ambient_noise=0.02
        )
        assert result.non_repudiation_passed is True
        assert result.verdict == ThreatCategory.LEGITIMATE
        assert result.cross_discrepancy_rate <= 0.125
        assert "Non-Repudiation Verified" in result.audit_summary

    def test_repudiation_attack_detected(self):
        """If Alice sends forged/conflicting tokens to Charlie, cross-verification should detect it."""
        message = "Transfer Approval #5544"
        result = self.coordinator.verify_multi_recipient_session(
            message=message,
            signer_manager=self.alice_mgr,
            simulate_repudiation=True,
            trials_per_token=40,
            ambient_noise=0.02
        )
        assert result.non_repudiation_passed is False
        assert result.verdict == ThreatCategory.MALICIOUS
        assert "Repudiation Attack Detected" in result.audit_summary

    def test_formal_audit_certificate_generation(self):
        """Verifies JSON and Plaintext audit certificate schemas."""
        message = "Execute Command #99"
        sig = self.alice_mgr.generate_signature(message, num_tokens=4)
        assessment = self.detector.verify_signature_session(
            received_signature=sig,
            expected_signature=sig,
            trials_per_token=30,
            ambient_noise=0.02
        )
        
        # Test JSON Certificate
        json_cert = AuditReportGenerator.generate_verification_certificate_json(
            assessment=assessment,
            signature=sig,
            message=message,
            latency_ms=1.45
        )
        parsed = json.loads(json_cert)
        assert "certificate_id" in parsed
        assert parsed["standard_specification"] == "SIH-26141 Q-SENTINEL PROTOCOL V2.0"
        assert parsed["statistical_evaluation_qstat"]["verdict"] == "LEGITIMATE"
        assert parsed["audit_decision"]["status"] == "APPROVED_AUTHENTIC"

        # Test Plaintext Certificate
        text_cert = AuditReportGenerator.generate_plain_text_certificate(
            assessment=assessment,
            signature=sig,
            message=message,
            latency_ms=1.45
        )
        assert "Q-SENTINEL QUANTUM DIGITAL SIGNATURE AUDIT CERTIFICATE" in text_cert
        assert "Standardized z-Score" in text_cert
        assert "AUTHENTIC AND ACCEPTED" in text_cert
