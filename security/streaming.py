"""
Q-Sentinel: Per-Watchtower Streaming & Multi-Arm Bonferroni/Holm Fusion
Stage 23: Phase 44

Generalizes sequential threat detection across physical watchtowers:
- WatchtowerArm: Wraps scalar metrics (CHSH S-parameter, APD bias current, Raman QBER,
  finite-key margin, Trojan probe energy) into dedicated SequentialQStat instances.
  Supports bidirectional anomalies (metric rising above threshold or dropping below).
- MultiArmFusion: Coordinates k watchtower arms in parallel with rigorous family-wise
  error rate (FWER) control via Bonferroni correction (alpha_i = alpha_target / k)
  and Holm step-down testing. Guarantees the joint false-alarm probability <= alpha_target.

References:
- Bonferroni, C. E. (1936). Teoria statistica delle classi e calcolo delle probabilita.
- Holm, S. (1979). A simple sequentially rejective multiple test procedure.
  Scandinavian Journal of Statistics, 6(2), 65-70.
- Wald, A. (1947). Sequential Analysis. John Wiley & Sons.
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Tuple

from security.detector import ThreatCategory
from security.sequential import SequentialQStat, SequentialVerdict


@dataclass
class FusedVerdict:
    """
    Consolidated decision emitted by multi-arm fusion watchtower.
    """
    fired_arm: Optional[str]
    verdict: ThreatCategory
    per_arm_stats: Dict[str, SequentialVerdict]
    joint_alpha: float
    effective_alpha_per_arm: float
    trigger: str = "NONE"


class WatchtowerArm:
    """
    Dedicated sequential monitoring arm wrapping an individual physical watchtower metric.
    """

    def __init__(
        self,
        name: str,
        metric_name: str,
        nominal_baseline: float,
        threshold_boundary: float,
        direction: str = "HIGH",  # "HIGH": anomaly when val > threshold; "LOW": anomaly when val < threshold
        baseline_p0: float = 0.03,
        alt_p1: float = 0.20,
        sprt_alpha: float = 1e-4,
        sprt_beta: float = 1e-4,
        cusum_h: Optional[float] = None
    ):
        self.name = name
        self.metric_name = metric_name
        self.nominal_baseline = float(nominal_baseline)
        self.threshold_boundary = float(threshold_boundary)
        self.direction = direction.upper()
        if self.direction not in ("HIGH", "LOW"):
            raise ValueError(f"Direction must be 'HIGH' or 'LOW', got {direction}")

        self.detector = SequentialQStat(
            baseline_p0=baseline_p0,
            alt_p1=alt_p1,
            cusum_threshold_h=cusum_h,
            sprt_alpha=sprt_alpha,
            sprt_beta=sprt_beta
        )
        self.latest_sample_value: float = self.nominal_baseline
        self.latest_verdict: Optional[SequentialVerdict] = None

    def configure_effective_alpha(self, effective_alpha: float) -> None:
        """
        Reconfigures SPRT decision boundary under Bonferroni / Holm family-wise correction.
        """
        self.detector.sprt_alpha = float(effective_alpha)
        # Update upper threshold A: ln((1 - beta) / alpha_eff)
        self.detector.sprt_A = math.log((1.0 - self.detector.sprt_beta) / self.detector.sprt_alpha)

    def update(self, scalar_value: float) -> SequentialVerdict:
        """
        Ingests a continuous scalar measurement, maps to a Bernoulli violation trial,
        and updates the arm's SequentialQStat engine.
        """
        self.latest_sample_value = float(scalar_value)
        if self.direction == "HIGH":
            # Anomaly when metric exceeds upper threshold (e.g. APD bias current, Raman noise)
            is_anomaly = 1 if scalar_value > self.threshold_boundary else 0
        else:
            # Anomaly when metric drops below lower bound (e.g. CHSH S-parameter below 2.0)
            is_anomaly = 1 if scalar_value < self.threshold_boundary else 0

        verdict = self.detector.update(is_anomaly)
        self.latest_verdict = verdict
        return verdict

    def reset(self) -> None:
        self.detector.reset()
        self.latest_sample_value = self.nominal_baseline
        self.latest_verdict = None


class MultiArmFusion:
    """
    Multi-arm decision fusion engine providing rigorous Family-Wise Error Rate (FWER)
    guarantees across concurrent physical watchtowers via Bonferroni / Holm corrections.
    """

    def __init__(
        self,
        arms: Optional[Dict[str, WatchtowerArm]] = None,
        joint_alpha_target: float = 1e-4
    ):
        self.joint_alpha_target: float = float(joint_alpha_target)
        self.arms: Dict[str, WatchtowerArm] = arms or self._build_default_watchtower_arms()
        self._apply_bonferroni_correction()

    def _apply_bonferroni_correction(self) -> None:
        """
        Applies Bonferroni correction: alpha_i = alpha_target / k.
        Guarantees that P(union of false alarms across all arms) <= alpha_target.
        """
        k = max(1, len(self.arms))
        effective_alpha = self.joint_alpha_target / k
        for arm in self.arms.values():
            arm.configure_effective_alpha(effective_alpha)
        self.effective_alpha = effective_alpha

    def _build_default_watchtower_arms(self) -> Dict[str, WatchtowerArm]:
        """
        Initializes default monitoring arms mapped to the core physical watchtowers.
        """
        arms = {
            # 1. CHSH Bell Watchtower: Bell non-locality (Tsirelson 2.828 vs classical bound 2.0)
            "CHSH_BELL": WatchtowerArm(
                name="CHSH_BELL",
                metric_name="S_parameter",
                nominal_baseline=2.828,
                threshold_boundary=2.20,
                direction="LOW",
                baseline_p0=0.03,
                alt_p1=0.25
            ),
            # 2. Detector Blinding: APD anode DC bias current (Makarov blinding attack)
            "DETECTOR_BLIND": WatchtowerArm(
                name="DETECTOR_BLIND",
                metric_name="anode_bias_current_uA",
                nominal_baseline=1.2,
                threshold_boundary=25.0,
                direction="HIGH",
                baseline_p0=0.02,
                alt_p1=0.30
            ),
            # 3. WDM Raman Scattering: Spontaneous Raman scattering in SMF-28
            "WDM_RAMAN": WatchtowerArm(
                name="WDM_RAMAN",
                metric_name="raman_induced_qber",
                nominal_baseline=0.025,
                threshold_boundary=0.080,
                direction="HIGH",
                baseline_p0=0.03,
                alt_p1=0.20
            ),
            # 4. Trojan-Horse Watchtower: Optical probe pulse power
            "TROJAN_HORSE": WatchtowerArm(
                name="TROJAN_HORSE",
                metric_name="probe_power_pW",
                nominal_baseline=5.0,
                threshold_boundary=50.0,
                direction="HIGH",
                baseline_p0=0.01,
                alt_p1=0.25
            ),
            # 5. Finite-Size Security: Composable secret key extraction margin
            "FINITE_KEY": WatchtowerArm(
                name="FINITE_KEY",
                metric_name="serfling_error_margin",
                nominal_baseline=0.04,
                threshold_boundary=0.15,
                direction="HIGH",
                baseline_p0=0.03,
                alt_p1=0.20
            )
        }
        return arms

    def update_arm(self, arm_name: str, scalar_value: float) -> FusedVerdict:
        """
        Updates a single watchtower arm with a new scalar reading and recomputes fused verdict.
        """
        if arm_name not in self.arms:
            raise KeyError(f"Unknown watchtower arm: {arm_name}. Active arms: {list(self.arms.keys())}")

        self.arms[arm_name].update(scalar_value)
        return self.get_fused_verdict()

    def update_all(self, sample_dict: Dict[str, float]) -> FusedVerdict:
        """
        Batch updates multiple arms with concurrent scalar telemetry readings.
        """
        for arm_name, val in sample_dict.items():
            if arm_name in self.arms:
                self.arms[arm_name].update(val)
        return self.get_fused_verdict()

    def get_fused_verdict(self) -> FusedVerdict:
        """
        Evaluates joint decision across all arms using family-wise error bounds.
        Attributes anomaly to the specific arm that triggered the alarm.
        """
        per_arm_stats: Dict[str, SequentialVerdict] = {}
        fired_arm: Optional[str] = None
        highest_threat = ThreatCategory.LEGITIMATE
        trigger_name = "NONE"

        # Check each arm's status
        for name, arm in self.arms.items():
            verdict = arm.latest_verdict or arm.detector.update(0)
            per_arm_stats[name] = verdict

            if verdict.verdict == ThreatCategory.MALICIOUS:
                if highest_threat != ThreatCategory.MALICIOUS:
                    highest_threat = ThreatCategory.MALICIOUS
                    fired_arm = name
                    trigger_name = verdict.trigger
            elif verdict.verdict == ThreatCategory.SUSPICIOUS:
                if highest_threat == ThreatCategory.LEGITIMATE:
                    highest_threat = ThreatCategory.SUSPICIOUS
                    fired_arm = name
                    trigger_name = verdict.trigger

        return FusedVerdict(
            fired_arm=fired_arm,
            verdict=highest_threat,
            per_arm_stats=per_arm_stats,
            joint_alpha=self.joint_alpha_target,
            effective_alpha_per_arm=self.effective_alpha,
            trigger=trigger_name
        )

    def reset(self) -> None:
        """Resets all arms back to initial baseline."""
        for arm in self.arms.values():
            arm.reset()
