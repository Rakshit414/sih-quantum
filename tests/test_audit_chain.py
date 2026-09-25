"""
Unit tests for Q-Sentinel Phase 48: Hash-Chained Audit Log
Verifies tamper-evident cryptographic chaining (SHA3-256) in TelemetryStore.
"""

import unittest
import os
import tempfile
import sqlite3
from analytics.history import TelemetryStore, canonical_json
from security.detector import ThreatAssessment, ThreatCategory


class TestAuditChain(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_audit.db")
        self.store = TelemetryStore(db_path=self.db_path)

    def test_empty_chain(self):
        is_valid, broken_id, reason = self.store.verify_chain()
        self.assertTrue(is_valid)
        self.assertIsNone(broken_id)
        self.assertIn("empty", reason.lower())

    def test_sequential_append_and_verify(self):
        entry_hashes = []
        for i in range(10):
            record = {
                "event_index": i,
                "node": f"Node_{i % 3}",
                "metric_val": i * 1.5,
                "status": "OK" if i % 2 == 0 else "FLAGGED"
            }
            h = self.store.append_chained(record)
            self.assertEqual(len(h), 64)
            entry_hashes.append(h)

        chain = self.store.get_audit_chain(limit=20)
        self.assertEqual(len(chain), 10)

        # Check genesis link
        self.assertEqual(chain[-1]["prev_hash"], "0" * 64)

        # Verify chain integrity
        is_valid, broken_id, reason = self.store.verify_chain()
        self.assertTrue(is_valid)
        self.assertIsNone(broken_id)
        self.assertEqual(reason, "Chain intact")

    def test_tamper_payload_detection(self):
        for i in range(1, 11):
            self.store.append_chained({"seq": i, "data": f"record_{i}"})

        # Directly tamper with payload in row 5
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE audit_chain SET payload_json = ? WHERE id = 5",
                ('{"data":"maliciously_altered_record_5","seq":5}',)
            )
            conn.commit()

        is_valid, broken_id, reason = self.store.verify_chain()
        self.assertFalse(is_valid)
        self.assertEqual(broken_id, 5)
        self.assertIn("Hash mismatch at id 5", reason)

    def test_row_deletion_detection(self):
        for i in range(1, 11):
            self.store.append_chained({"seq": i, "data": f"record_{i}"})

        # Directly delete row 5
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM audit_chain WHERE id = 5")
            conn.commit()

        is_valid, broken_id, reason = self.store.verify_chain()
        self.assertFalse(is_valid)
        self.assertEqual(broken_id, 6)
        self.assertIn("Broken link at id 6", reason)

    def test_tamper_prev_hash_detection(self):
        for i in range(1, 6):
            self.store.append_chained({"seq": i, "data": f"entry_{i}"})

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE audit_chain SET prev_hash = ? WHERE id = 3", ("f" * 64,))
            conn.commit()

        is_valid, broken_id, reason = self.store.verify_chain()
        self.assertFalse(is_valid)
        self.assertEqual(broken_id, 3)
        self.assertIn("Broken link at id 3", reason)

    def test_log_verification_automatic_chaining(self):
        assessment = ThreatAssessment(
            verdict=ThreatCategory.LEGITIMATE,
            error_rate=0.02,
            z_score=0.1,
            p_value=0.6,
            confidence=0.9,
            baseline_noise_p0=0.03,
            total_trials=100,
            error_count=2,
            match_count=98,
            ci_lower=0.005,
            ci_upper=0.05,
            freshness_passed=True,
            freshness_reason="Fresh",
            diagnostic_text="Valid session"
        )
        self.store.log_verification(
            assessment=assessment,
            signer_id="Alice",
            scenario="Legitimate",
            message="Secure transaction 1",
            latency_ms=1.2
        )
        self.store.log_verification(
            assessment=assessment,
            signer_id="Bob",
            scenario="IntermittentAttack",
            message="Secure transaction 2",
            latency_ms=2.1
        )

        chain = self.store.get_audit_chain()
        self.assertEqual(len(chain), 2)
        is_valid, broken_id, _ = self.store.verify_chain()
        self.assertTrue(is_valid)
        self.assertIsNone(broken_id)

    def test_clear_history_clears_audit_chain(self):
        self.store.append_chained({"test": "data"})
        self.assertEqual(len(self.store.get_audit_chain()), 1)
        self.store.clear_history()
        self.assertEqual(len(self.store.get_audit_chain()), 0)
        is_valid, _, _ = self.store.verify_chain()
        self.assertTrue(is_valid)

    def test_canonical_json_determinism(self):
        obj1 = {"b": 1, "a": 2, "nested": {"z": 9, "y": 8}}
        obj2 = {"nested": {"y": 8, "z": 9}, "a": 2, "b": 1}
        self.assertEqual(canonical_json(obj1), canonical_json(obj2))


if __name__ == "__main__":
    unittest.main()
