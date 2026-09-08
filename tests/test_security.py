"""
Unit tests for Q-Sentinel Stages 3, 4, 5:
Security, Attacks, Freshness, and Q-STAT Detection Engine
"""
import unittest
import numpy as np
import time
from security.signature import QDSKeyManager, distribute_signature_via_teleportation
from security.freshness import FreshnessRegistry
from security.attacks import AttackScenario, ThreatOrchestrator
from security.detector import QStatDetector, ThreatCategory
from quantum.measure import sample_projective_trials


class TestSecurityAndDetection(unittest.TestCase):

    def setUp(self):
        self.alice_mgr = QDSKeyManager(signer_id="Alice", private_seed="alice_super_secret_seed_2026")
        self.message = "Authorize Bank Wire #98234 - Amount: $500,000"
        self.sig = self.alice_mgr.generate_signature(self.message, num_tokens=8)
        self.detector = QStatDetector(baseline_noise_p0=0.03, z_suspicious_threshold=2.0, z_malicious_threshold=4.0)

    def test_signature_generation_determinism(self):
        # Same key and message should generate identical states
        sig2 = self.alice_mgr.generate_signature(self.message, num_tokens=8)
        self.assertEqual(self.sig.token_count, sig2.token_count)
        self.assertEqual(self.sig.message_digest, sig2.message_digest)
        for t1, t2 in zip(self.sig.tokens, sig2.tokens):
            self.assertEqual(t1.basis, t2.basis)
            self.assertEqual(t1.bit_value, t2.bit_value)
            self.assertAlmostEqual(t1.eigenstate.fidelity(t2.eigenstate), 1.0)

    def test_teleportation_distribution_fidelity(self):
        transmitted = distribute_signature_via_teleportation(self.sig, random_seed=42)
        self.assertEqual(len(transmitted.received_states), 8)
        self.assertAlmostEqual(transmitted.average_teleportation_fidelity, 1.0, places=4)

    def test_legitimate_scenario_passes_qstat(self):
        # Sample 200 trials with nominal ambient noise 3%
        token0 = self.sig.tokens[0]
        trial = sample_projective_trials(
            received_state=token0.eigenstate,
            expected_state=token0.eigenstate,
            num_trials=200,
            ambient_noise=0.03,
            random_seed=123
        )
        verdict = self.detector.evaluate(
            error_count=trial.n_error,
            total_trials=trial.num_trials,
            signer_id=self.sig.signer_id,
            nonce=self.sig.nonce,
            timestamp=self.sig.timestamp
        )
        self.assertEqual(verdict.verdict, ThreatCategory.LEGITIMATE)
        self.assertLess(verdict.z_score, 2.0)
        self.assertTrue(verdict.freshness_passed)

    def test_forgery_attack_detected_as_malicious(self):
        forged_sig, desc = ThreatOrchestrator.execute_scenario(
            scenario=AttackScenario.FORGERY,
            original_signature=self.sig,
            random_seed=42
        )
        forged_sig.nonce = "new_unique_forgery_nonce_1"
        verdict = self.detector.verify_signature_session(
            received_signature=forged_sig,
            expected_signature=self.sig,
            trials_per_token=50,
            ambient_noise=0.03,
            random_seed=42
        )
        self.assertEqual(verdict.verdict, ThreatCategory.MALICIOUS)
        self.assertGreater(verdict.error_rate, 0.35)
        self.assertGreater(verdict.z_score, 4.0)
        self.assertLess(verdict.p_value, 1e-6)

    def test_impersonation_attack_detected(self):
        impersonated_sig, desc = ThreatOrchestrator.execute_scenario(
            scenario=AttackScenario.IMPERSONATION,
            original_signature=self.sig,
            random_seed=77
        )
        impersonated_sig.nonce = "impersonation_unique_nonce_2"
        verdict = self.detector.verify_signature_session(
            received_signature=impersonated_sig,
            expected_signature=self.sig,
            trials_per_token=50,
            ambient_noise=0.03,
            random_seed=77
        )
        self.assertEqual(verdict.verdict, ThreatCategory.MALICIOUS)
        self.assertGreater(verdict.error_rate, 0.35)
        self.assertGreater(verdict.z_score, 4.0)

    def test_replay_attack_freshness_check(self):
        freshness = FreshnessRegistry(max_time_window_seconds=60.0)
        det = QStatDetector(freshness_registry=freshness)

        # 1st run: fresh
        res1 = det.evaluate(
            error_count=6,
            total_trials=200,
            signer_id="Alice",
            nonce="replay_test_nonce_abc",
            timestamp=self.sig.timestamp
        )
        self.assertTrue(res1.freshness_passed)
        self.assertEqual(res1.verdict, ThreatCategory.LEGITIMATE)

        # 2nd run: identical nonce (replay attack)
        res2 = det.evaluate(
            error_count=6,
            total_trials=200,
            signer_id="Alice",
            nonce="replay_test_nonce_abc",
            timestamp=self.sig.timestamp
        )
        self.assertFalse(res2.freshness_passed)
        self.assertEqual(res2.verdict, ThreatCategory.MALICIOUS)
        self.assertIn("Replay attack detected", res2.diagnostic_text)

    def test_stale_timestamp_rejected(self):
        freshness = FreshnessRegistry(max_time_window_seconds=60.0)
        det = QStatDetector(freshness_registry=freshness)
        # Signature is 120 seconds old
        stale_time = self.sig.timestamp - 120.0
        res = det.evaluate(
            error_count=6,
            total_trials=200,
            signer_id="Alice",
            nonce="stale_nonce_xyz",
            timestamp=stale_time,
            current_time=self.sig.timestamp
        )
        self.assertFalse(res.freshness_passed)
        self.assertEqual(res.verdict, ThreatCategory.MALICIOUS)
        self.assertIn("Stale signature timestamp", res.diagnostic_text)

    def test_channel_noise_transitions_green_to_yellow_to_red(self):
        now = time.time()
        # 1. Very low noise: 3% -> LEGITIMATE
        v_low = self.detector.evaluate(error_count=6, total_trials=200, signer_id="A", nonce="noise_n1", timestamp=now, current_time=now)
        self.assertEqual(v_low.verdict, ThreatCategory.LEGITIMATE)

        # 2. Moderate disturbance: error count 15 / 200 = 7.5% -> SUSPICIOUS (z ~ 3.73)
        v_med = self.detector.evaluate(error_count=15, total_trials=200, signer_id="A", nonce="noise_n2", timestamp=now, current_time=now)
        self.assertEqual(v_med.verdict, ThreatCategory.SUSPICIOUS)
        self.assertTrue(2.0 <= v_med.z_score < 4.0)

        # 3. Severe channel tampering: error count 40 / 200 = 20% -> MALICIOUS (z ~ 14.1)
        v_high = self.detector.evaluate(error_count=40, total_trials=200, signer_id="A", nonce="noise_n3", timestamp=now, current_time=now)
        self.assertEqual(v_high.verdict, ThreatCategory.MALICIOUS)
        self.assertGreater(v_high.z_score, 4.0)


if __name__ == "__main__":
    unittest.main()
