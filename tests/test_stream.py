"""
Unit tests for Q-Sentinel Stage 8: Phase 26
Real-Time Network Threat Stream Engine & Traffic Generator
"""

import unittest
from analytics.stream import QuantumTrafficGenerator, StreamEvent
from security.detector import ThreatCategory
from security.attacks import AttackScenario


class TestNetworkTrafficStream(unittest.TestCase):

    def setUp(self):
        self.stream_gen = QuantumTrafficGenerator(base_signer_id="Alice", random_seed=42)

    def test_single_event_generation(self):
        event = self.stream_gen.generate_next_event(event_id=1, attack_probability=0.0, ambient_noise=0.01)
        self.assertEqual(event.event_id, 1)
        self.assertEqual(event.scenario, AttackScenario.LEGITIMATE)
        self.assertIn(event.assessment.verdict, [ThreatCategory.LEGITIMATE, ThreatCategory.SUSPICIOUS])
        self.assertNotEqual(event.assessment.verdict, ThreatCategory.MALICIOUS)
        self.assertLess(event.latency_ms, 15.0)

    def test_multi_event_stream_diversity(self):
        # Generate 20 events with 50% attack probability
        events = self.stream_gen.generate_stream(count=20, attack_probability=0.50, trials_per_token=30)
        self.assertEqual(len(events), 20)

        scenarios_observed = {e.scenario for e in events}
        # Should observe both legitimate and at least one attack scenario
        self.assertIn(AttackScenario.LEGITIMATE, scenarios_observed)
        self.assertTrue(len(scenarios_observed) > 1)

        # Ensure all events have valid mathematical assessments
        for e in events:
            self.assertIsNotNone(e.assessment.z_score)
            self.assertIsNotNone(e.assessment.p_value)
            self.assertGreater(e.assessment.total_trials, 0)
            if e.scenario in [AttackScenario.FORGERY, AttackScenario.IMPERSONATION]:
                self.assertEqual(e.assessment.verdict, ThreatCategory.MALICIOUS)


if __name__ == "__main__":
    unittest.main()
