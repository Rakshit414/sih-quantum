"""
Test Suite for Stage 23 (Phase 44): Per-Watchtower Streaming & Multi-Arm Bonferroni/Holm Fusion

Verifies:
1. Bonferroni mathematical scaling: alpha_i = alpha_target / k for k arms.
2. Single-arm anomaly attribution: FusedVerdict.fired_arm correctly identifies which arm alarmed.
3. Bidirectional anomaly detection: low-threshold breach (CHSH S < 2.0) and high-threshold breach (Blinding current > 25 uA).
4. Joint false-alarm protection across all concurrent arms under nominal background.
"""

import pytest
import numpy as np

from security.detector import ThreatCategory
from security.streaming import WatchtowerArm, MultiArmFusion, FusedVerdict


class TestStreamingMultiArmFusion:
    """Rigorous verification of family-wise error rate control and multi-arm attribution."""

    def test_bonferroni_correction_scaling(self):
        """
        Directly validates Bonferroni mathematical invariant:
        For joint_alpha_target = 1e-4 and k = 5 arms,
        effective_alpha_per_arm must be exactly 1e-4 / 5 = 2e-5.
        """
        fusion = MultiArmFusion(joint_alpha_target=1e-4)
        k = len(fusion.arms)
        assert k == 5, f"Expected default 5 arms, found {k}"

        expected_effective_alpha = 1e-4 / 5.0
        assert fusion.effective_alpha == pytest.approx(expected_effective_alpha, rel=1e-6)

        # Confirm every individual arm's internal detector has updated threshold
        for name, arm in fusion.arms.items():
            assert arm.detector.sprt_alpha == pytest.approx(expected_effective_alpha, rel=1e-6)

    def test_chsh_arm_low_threshold_anomaly_attribution(self):
        """
        Tests that when CHSH S-parameter collapses toward classical bound (e.g. S = 1.4 < 2.0),
        MultiArmFusion flags MALICIOUS and explicitly attributes fired_arm == 'CHSH_BELL'.
        """
        fusion = MultiArmFusion(joint_alpha_target=1e-4)

        # Ingest 25 degraded CHSH measurements (S = 1.4, severe entanglement loss)
        verdict = None
        for _ in range(25):
            verdict = fusion.update_arm("CHSH_BELL", 1.40)
            if verdict.verdict == ThreatCategory.MALICIOUS:
                break

        assert verdict is not None
        assert verdict.verdict == ThreatCategory.MALICIOUS
        assert verdict.fired_arm == "CHSH_BELL"
        assert verdict.per_arm_stats["CHSH_BELL"].trigger in ("CUSUM", "SPRT")

    def test_blinding_arm_high_threshold_anomaly_attribution(self):
        """
        Tests that when detector bias current surges (e.g. 80 uA > 25 uA Makarov blinding),
        MultiArmFusion flags MALICIOUS and attributes fired_arm == 'DETECTOR_BLIND'.
        """
        fusion = MultiArmFusion(joint_alpha_target=1e-4)

        verdict = None
        for _ in range(25):
            verdict = fusion.update_arm("DETECTOR_BLIND", 85.0)  # 85 uA >> 25 uA threshold
            if verdict.verdict == ThreatCategory.MALICIOUS:
                break

        assert verdict is not None
        assert verdict.verdict == ThreatCategory.MALICIOUS
        assert verdict.fired_arm == "DETECTOR_BLIND"

    def test_joint_nominal_stability_zero_false_alarms(self):
        """
        Under nominal physical conditions across all 5 arms concurrently,
        MultiArmFusion must maintain LEGITIMATE status across >= 200 trials.
        """
        np.random.seed(42)
        fusion = MultiArmFusion(joint_alpha_target=1e-4)

        nominal_stream = {
            "CHSH_BELL": 2.80,         # Healthy Bell non-locality
            "DETECTOR_BLIND": 1.25,     # Normal 1.25 uA bias current
            "WDM_RAMAN": 0.026,         # Normal 2.6% Raman QBER
            "TROJAN_HORSE": 6.0,        # Safe 6 pW background noise
            "FINITE_KEY": 0.045         # Safe Serfling margin
        }

        for _ in range(200):
            # Inject minor Gaussian noise within nominal operating envelopes
            sample = {
                "CHSH_BELL": nominal_stream["CHSH_BELL"] + np.random.normal(0, 0.02),
                "DETECTOR_BLIND": nominal_stream["DETECTOR_BLIND"] + np.random.normal(0, 0.2),
                "WDM_RAMAN": nominal_stream["WDM_RAMAN"] + np.random.normal(0, 0.002),
                "TROJAN_HORSE": nominal_stream["TROJAN_HORSE"] + np.random.normal(0, 1.0),
                "FINITE_KEY": nominal_stream["FINITE_KEY"] + np.random.normal(0, 0.005)
            }
            fused = fusion.update_all(sample)
            assert fused.verdict != ThreatCategory.MALICIOUS, (
                f"Joint false alarm triggered on arm {fused.fired_arm}"
            )
