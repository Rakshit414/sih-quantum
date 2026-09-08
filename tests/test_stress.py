"""
Unit tests for Q-Sentinel Stage 8: Phase 24
End-to-End Automated Test Suite & CI Stress Testing
Validates extreme boundary conditions, sample size asymptotics, message payload variations,
and clock skew edge cases in the freshness registry.
"""

import unittest
import numpy as np
import time
from quantum.state import QubitState, STATE_0, STATE_1, STATE_PLUS, STATE_MINUS
from security.signature import QDSKeyManager
from security.detector import QStatDetector, ThreatCategory
from security.freshness import FreshnessRegistry
from security.attacks import ThreatOrchestrator, AttackScenario


class TestStressAndBoundaries(unittest.TestCase):

    def setUp(self):
        self.detector = QStatDetector(baseline_noise_p0=0.03, z_suspicious_threshold=2.0, z_malicious_threshold=4.0)
        self.mgr = QDSKeyManager(signer_id="Alice", private_seed="stress_seed_alpha_2026")

    def test_extreme_payload_lengths(self):
        """Tests that empty, small, and massive (10,000 chars) messages generate valid deterministic signatures."""
        test_messages = [
            "",  # Empty string edge case
            "A",  # Single char
            "Standard wire transfer authorization #1001",
            "X" * 10000,  # 10,000 characters payload stress
            "Global Banking Network | Wire Transfer Token EUR-USD-GBP-JPY (Ref: 98234-X7)"  # Special Characters payload
        ]
        for msg in test_messages:
            sig = self.mgr.generate_signature(msg, num_tokens=8)
            self.assertEqual(sig.token_count, 8)
            self.assertTrue(len(sig.message_digest) == 64)  # SHA-256 hex length
            # Ensure all prepared eigenstates are strictly normalized
            for t in sig.tokens:
                t.eigenstate.assert_normalized()

    def test_noise_floor_boundary_zero_and_maximum(self):
        """Tests asymptotic mathematical boundaries: zero error count vs 100% error count."""
        now = time.time()
        
        # 1. Zero error boundary (n1 = 0, N = 500)
        res_zero = self.detector.evaluate(
            error_count=0,
            total_trials=500,
            signer_id="Alice",
            nonce="bound_zero_nonce",
            timestamp=now,
            current_time=now
        )
        self.assertEqual(res_zero.verdict, ThreatCategory.LEGITIMATE)
        self.assertEqual(res_zero.error_rate, 0.0)
        self.assertLess(res_zero.z_score, 0.0)  # Negative z-score (better than baseline noise)
        self.assertEqual(res_zero.p_value, 1.0)  # Maximum p-value under greater test

        # 2. Complete error boundary (n1 = 500, N = 500)
        res_max = self.detector.evaluate(
            error_count=500,
            total_trials=500,
            signer_id="Alice",
            nonce="bound_max_nonce",
            timestamp=now,
            current_time=now
        )
        self.assertEqual(res_max.verdict, ThreatCategory.MALICIOUS)
        self.assertEqual(res_max.error_rate, 1.0)
        self.assertGreater(res_max.z_score, 50.0)
        self.assertLess(res_max.p_value, 1e-15)

    def test_sample_size_asymptotics(self):
        """Tests that statistical engine behaves consistently from N=10 to N=10,000."""
        now = time.time()
        
        for N in [10, 50, 200, 1000, 10000]:
            # Simulate 50% error rate (forgery)
            n1 = int(0.50 * N)
            res = self.detector.evaluate(
                error_count=n1,
                total_trials=N,
                signer_id="Alice",
                nonce=f"asymptotic_nonce_{N}",
                timestamp=now,
                current_time=now
            )
            self.assertEqual(res.verdict, ThreatCategory.MALICIOUS)
            self.assertGreater(res.z_score, 4.0)

    def test_clock_skew_and_window_boundaries(self):
        """Tests strict mathematical boundaries of the sliding time window (60s)."""
        reg = FreshnessRegistry(max_time_window_seconds=60.0)
        now = 100000.0

        # Boundary 1: Exactly 59.9s old -> Must PASS
        is_fresh, _ = reg.verify_and_register("Alice", "nonce_59s", timestamp=now - 59.9, current_time=now)
        self.assertTrue(is_fresh)

        # Boundary 2: Exactly 60.1s old -> Must FAIL (Stale)
        is_fresh, reason = reg.verify_and_register("Alice", "nonce_60s", timestamp=now - 60.1, current_time=now)
        self.assertFalse(is_fresh)
        self.assertIn("Stale signature timestamp", reason)

        # Boundary 3: Future timestamp (+6.0s skew) -> Must FAIL
        is_fresh, reason = reg.verify_and_register("Alice", "nonce_future", timestamp=now + 6.0, current_time=now)
        self.assertFalse(is_fresh)
        self.assertIn("Future timestamp detected", reason)

    def test_rapid_verification_throughput(self):
        """Simulates 250 back-to-back signature verifications to verify numerical stability and zero drift."""
        sig = self.mgr.generate_signature("Rapid test wire #7701", num_tokens=8)
        latencies = []
        malicious_count = 0
        total_iterations = 200

        for i in range(total_iterations):
            t0 = time.perf_counter()
            sig.nonce = f"rapid_nonce_{i}_{time.time_ns()}"
            sig.timestamp = time.time()
            res = self.detector.verify_signature_session(
                received_signature=sig,
                expected_signature=sig,
                trials_per_token=50,
                ambient_noise=0.03
            )
            dt = (time.perf_counter() - t0) * 1000.0
            latencies.append(dt)
            if res.verdict == ThreatCategory.MALICIOUS:
                malicious_count += 1
            
        frr = malicious_count / total_iterations
        self.assertLessEqual(frr, 0.01, f"False rejection rate {frr:.2%} exceeds 1.00% benchmark target")
        mean_latency = np.mean(latencies)
        self.assertLess(mean_latency, 10.0, f"Mean latency {mean_latency:.2f}ms exceeds 10ms threshold")


if __name__ == "__main__":
    unittest.main()
