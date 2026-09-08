"""
Unit tests for Q-Sentinel Stage 6: Analytics, Metrics & Telemetry History
Phase 19 & 20
"""
import unittest
import os
import tempfile
import pandas as pd
from security.detector import ThreatAssessment, ThreatCategory
from analytics.history import TelemetryStore
from analytics.metrics import compute_benchmark


class TestAnalyticsAndHistory(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_qsentinel.db")
        self.store = TelemetryStore(db_path=self.db_path)

    def test_log_and_retrieve_verification(self):
        assessment = ThreatAssessment(
            verdict=ThreatCategory.LEGITIMATE,
            error_rate=0.03,
            z_score=0.45,
            p_value=0.52,
            confidence=0.67,
            baseline_noise_p0=0.03,
            total_trials=200,
            error_count=6,
            match_count=194,
            ci_lower=0.015,
            ci_upper=0.065,
            freshness_passed=True,
            freshness_reason="Fresh token",
            diagnostic_text="Clean verification"
        )
        run_id = self.store.log_verification(
            assessment=assessment,
            signer_id="Alice",
            scenario="Legitimate",
            message="Test message wire",
            latency_ms=1.85
        )
        self.assertGreater(run_id, 0)
        
        runs = self.store.get_recent_runs(limit=10)
        self.assertEqual(len(runs), 1)
        self.assertEqual(runs[0]["signer_id"], "Alice")
        self.assertEqual(runs[0]["verdict"], "LEGITIMATE")

        df = self.store.get_dataframe()
        self.assertFalse(df.empty)
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["Signer"], "Alice")

    def test_clear_history(self):
        self.test_log_and_retrieve_verification()
        self.store.clear_history()
        runs = self.store.get_recent_runs()
        self.assertEqual(len(runs), 0)

    def test_quick_benchmark_generation(self):
        # Run small 5-iteration benchmark
        rep = compute_benchmark(num_runs_per_scenario=5, trials_per_token=20, token_count=4)
        self.assertEqual(rep.total_runs, 25)
        self.assertGreaterEqual(rep.accuracy, 0.95)
        self.assertLessEqual(rep.false_acceptance_rate, 0.05)


if __name__ == "__main__":
    unittest.main()
