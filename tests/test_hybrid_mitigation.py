"""
Unit Tests for Phase 29: Automated Mitigation & Post-Quantum Hybrid Verification
"""

import pytest
from security.signature import QDSKeyManager
from security.detector import QStatDetector, ThreatCategory
from security.mitigation import ThreatMitigationOrchestrator, IncidentReport
from security.hybrid import HybridSignatureVerifier, HybridVerificationResult
from security.attacks import AttackScenario, ThreatOrchestrator


class TestHybridAndMitigation:

    def setup_method(self):
        self.detector = QStatDetector(baseline_noise_p0=0.03)
        self.mitigator = ThreatMitigationOrchestrator()
        self.hybrid_verifier = HybridSignatureVerifier(detector=self.detector)
        self.alice_seed = "alice_master_soc_seed_2026"
        self.alice_mgr = QDSKeyManager(signer_id="Alice", private_seed=self.alice_seed)

    def test_mitigation_on_malicious_threat(self):
        """When a malicious threat occurs, orchestrator should revoke nonce, quarantine signer, and generate CEF log."""
        message = "Wire Transfer Approval"
        sig = self.alice_mgr.generate_signature(message, num_tokens=4)
        forged_sig, _ = ThreatOrchestrator.execute_scenario(AttackScenario.FORGERY, sig)
        
        assessment = self.detector.verify_signature_session(forged_sig, sig, trials_per_token=30)
        assert assessment.verdict == ThreatCategory.MALICIOUS

        report = self.mitigator.evaluate_and_mitigate(
            assessment=assessment,
            signature=forged_sig,
            message=message,
            auto_quarantine=True
        )

        assert report.verdict == ThreatCategory.MALICIOUS
        assert self.mitigator.is_quarantined("Alice")
        assert forged_sig.nonce in self.mitigator.revoked_nonces
        assert len(report.mitigation_actions) == 3
        assert "CEF:0|NationalQuantumMission|Q-Sentinel" in report.cef_log_entry

        # Test quarantine release
        self.mitigator.release_quarantine("Alice")
        assert not self.mitigator.is_quarantined("Alice")

    def test_hybrid_verification_honest_pass(self):
        """Honest transaction passes both classical SHA3-512 and quantum QDS."""
        message = "Payload Data Block #101"
        classical_digest = HybridSignatureVerifier.compute_classical_digest(message, self.alice_seed)
        sig = self.alice_mgr.generate_signature(message, num_tokens=6)

        res = self.hybrid_verifier.verify_hybrid_signature(
            message=message,
            claimed_classical_digest=classical_digest,
            received_quantum_signature=sig,
            expected_quantum_signature=sig,
            signer_seed=self.alice_seed,
            trials_per_token=50,
            ambient_noise=0.01
        )

        assert res.classical_hash_matched is True
        assert res.overall_verdict == ThreatCategory.LEGITIMATE
        assert "Dual-Layer Verified" in res.security_summary

    def test_hybrid_verification_classical_tampering_caught(self):
        """Altering classical message trips classical HMAC failure even before quantum layer."""
        message = "Payload Data Block #101"
        altered_message = "Payload Data Block #101 [TAMPERED]"
        classical_digest = HybridSignatureVerifier.compute_classical_digest(message, self.alice_seed)
        sig = self.alice_mgr.generate_signature(message, num_tokens=4)

        res = self.hybrid_verifier.verify_hybrid_signature(
            message=altered_message,
            claimed_classical_digest=classical_digest,
            received_quantum_signature=sig,
            expected_quantum_signature=sig,
            signer_seed=self.alice_seed,
            trials_per_token=30
        )

        assert res.classical_hash_matched is False
        assert res.overall_verdict == ThreatCategory.MALICIOUS
        assert "Classical Integrity Failure" in res.security_summary

    def test_hybrid_verification_quantum_forgery_caught(self):
        """Valid classical digest but forged quantum states is caught by quantum layer."""
        message = "Payload Data Block #101"
        classical_digest = HybridSignatureVerifier.compute_classical_digest(message, self.alice_seed)
        sig = self.alice_mgr.generate_signature(message, num_tokens=4)
        forged_sig, _ = ThreatOrchestrator.execute_scenario(AttackScenario.FORGERY, sig)

        res = self.hybrid_verifier.verify_hybrid_signature(
            message=message,
            claimed_classical_digest=classical_digest,
            received_quantum_signature=forged_sig,
            expected_quantum_signature=sig,
            signer_seed=self.alice_seed,
            trials_per_token=30
        )

        assert res.classical_hash_matched is True
        assert res.overall_verdict == ThreatCategory.MALICIOUS
        assert "Quantum Security Breach" in res.security_summary
