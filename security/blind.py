"""
Q-Sentinel: Quantum Detector Blinding & Spatial-Mode Side-Channel Watchtower
Stage 13: Phase 33 (Q-BLIND)

Protects Avalanche Photodiode (APD) and Superconducting Nanowire Single-Photon Detector (SNSPD)
measurement setups against detector blinding attacks (Makarov / Lydersen attack),
spatial-mode beam-shift attacks, and anomalous periodic faked-state triggering patterns.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple, Optional, List
import numpy as np

from security.detector import ThreatCategory


@dataclass
class DetectorTelemetry:
    """
    Physical sensor readings from single-photon detector channels (APD / SNSPD).
    """
    channel_id: str
    bias_current_ua: float              # DC anode / bias current in microamperes (nominally < 1.0 uA in Geiger mode)
    spatial_offset_x_um: float          # Beam spatial displacement X on quadrant sensor (micrometers)
    spatial_offset_y_um: float          # Beam spatial displacement Y on quadrant sensor (micrometers)
    inter_arrival_times_us: List[float] # List of photon detection inter-arrival times (microseconds)
    double_click_count: int             # Simultaneous dual-detector click events
    total_clicks: int                   # Total registered clicks


@dataclass
class BlindingDetectionResult:
    """
    Comprehensive diagnostic output of the Q-BLIND watchtower.
    """
    blinding_detected: bool
    bias_current_ua: float
    operating_mode: str
    spatial_displacement_um: float
    spatial_breach: bool
    inter_arrival_entropy: float
    dead_time_violation: bool
    double_click_ratio: float
    verdict: ThreatCategory
    attack_classification: str
    cryptanalytic_proof: str


class DetectorBlindingWatcher:
    """
    Monitors physical detector operational parameters to prevent side-channel
    takeovers, detector blinding, and spatial efficiency mismatch exploits.
    """

    def __init__(
        self,
        current_threshold_ua: float = 5.0,        # Max allowable DC current before linear mode transition
        max_spatial_displacement_um: float = 2.5, # Maximum allowable beam spatial drift
        min_entropy_nats: float = 1.0,            # Minimum Shannon entropy for Poissonian click intervals
        detector_dead_time_us: float = 1.0        # Physical APD hold-off / dead time
    ):
        self.current_threshold: float = float(current_threshold_ua)
        self.spatial_limit: float = float(max_spatial_displacement_um)
        self.min_entropy: float = float(min_entropy_nats)
        self.dead_time: float = float(detector_dead_time_us)

    @staticmethod
    def calculate_interarrival_entropy(intervals_us: List[float], bins: int = 15) -> float:
        """
        Computes the Shannon entropy of detection inter-arrival times.
        Legitimate Poisson arrivals yield high continuous entropy.
        Adversarial faked-state pulse trains collapse into a deterministic low-entropy spike.
        """
        if not intervals_us or len(intervals_us) < 10:
            return 3.0  # Nominal default for small batches

        arr = np.asarray(intervals_us, dtype=float)
        # Filter negative or zero values
        arr = arr[arr > 0]
        if len(arr) < 5:
            return 0.0

        hist, _ = np.histogram(arr, bins=bins, density=True)
        # Compute discrete probability distribution
        p = hist / np.sum(hist) if np.sum(hist) > 0 else np.zeros_like(hist)
        p = p[p > 1e-12]
        if len(p) <= 1:
            return 0.0

        entropy = -np.sum(p * np.log(p))
        return float(round(entropy, 4))

    def evaluate_detector_state(self, telemetry: DetectorTelemetry) -> BlindingDetectionResult:
        """
        Evaluates physical detector telemetry against hardware baselines.
        """
        # 1. Bias Current & Operating Mode Assessment
        bias_ua = telemetry.bias_current_ua
        current_breach = bias_ua >= self.current_threshold

        if current_breach:
            operating_mode = "Linear Mode (Blinded / Single-Photon Inactive)"
        else:
            operating_mode = "Geiger Mode (Single-Photon Sensitive)"

        # 2. Spatial Alignment Assessment via Quadrant Sensor
        dx = telemetry.spatial_offset_x_um
        dy = telemetry.spatial_offset_y_um
        radial_displacement = float(np.sqrt(dx**2 + dy**2))
        spatial_breach = radial_displacement > self.spatial_limit

        # 3. Inter-arrival Timing & Dead-Time Statistics
        entropy = self.calculate_interarrival_entropy(telemetry.inter_arrival_times_us)
        entropy_breach = entropy < self.min_entropy

        # Check for physically impossible clicks occurring inside dead-time window
        dead_time_violations = sum(1 for t in telemetry.inter_arrival_times_us if 0 < t < (self.dead_time * 0.90))
        dead_time_breach = dead_time_violations > 0

        # Double click ratio
        tot = max(1, telemetry.total_clicks)
        dc_ratio = float(telemetry.double_click_count / tot)

        # 4. Threat Classification & Diagnostic Reasoning
        blinding_flag = current_breach or spatial_breach or entropy_breach or dead_time_breach

        if current_breach:
            verdict = ThreatCategory.MALICIOUS
            classification = "DETECTOR_BLINDING_CW_ATTACK"
            proof = (
                f"MALICIOUS: Anode bias current I_bias = {bias_ua:.2f} uA exceeds linear-mode threshold "
                f"({self.current_threshold:.1f} uA). APD has transitioned into classical linear mode. "
                f"Adversary is applying continuous-wave (CW) blinding light to control detection clicks."
            )
        elif spatial_breach:
            verdict = ThreatCategory.MALICIOUS
            classification = "SPATIAL_MODE_BEAM_SHIFT_ATTACK"
            proof = (
                f"MALICIOUS: Spatial beam displacement r = {radial_displacement:.2f} um (dx={dx:+.1f} um, "
                f"dy={dy:+.1f} um) exceeds quadrant tolerance limit ({self.spatial_limit:.1f} um). "
                f"Adversary exploiting spatial detector efficiency mismatch to manipulate Bell-state outcomes."
            )
        elif dead_time_breach or entropy_breach:
            verdict = ThreatCategory.MALICIOUS
            classification = "FAKED_STATE_TIMING_ATTACK"
            proof = (
                f"MALICIOUS: Non-Poissonian arrival statistics detected. Click interval entropy H = {entropy:.2f} nats "
                f"below physical threshold ({self.min_entropy:.2f} nats) with {dead_time_violations} dead-time violations. "
                f"Adversary injecting rigid periodic faked-state pulse trains."
            )
        elif bias_ua > (self.current_threshold * 0.60):
            verdict = ThreatCategory.SUSPICIOUS
            classification = "ELEVATED_BIAS_CURRENT"
            proof = (
                f"SUSPICIOUS: Approaching linear mode threshold (I_bias = {bias_ua:.2f} uA, 60%+ of threshold). "
                f"Background optical power or ambient thermal fluctuation elevated."
            )
        else:
            verdict = ThreatCategory.LEGITIMATE
            classification = "NOMINAL_GEIGER_OPERATION"
            proof = (
                f"LEGITIMATE: Detector channel '{telemetry.channel_id}' operating normally in Geiger mode. "
                f"Bias current I_bias = {bias_ua:.3f} uA, spatial drift r = {radial_displacement:.2f} um, "
                f"and interval entropy H = {entropy:.2f} nats are within calibrated physical tolerances."
            )

        return BlindingDetectionResult(
            blinding_detected=blinding_flag,
            bias_current_ua=round(bias_ua, 3),
            operating_mode=operating_mode,
            spatial_displacement_um=round(radial_displacement, 3),
            spatial_breach=spatial_breach,
            inter_arrival_entropy=entropy,
            dead_time_violation=dead_time_breach,
            double_click_ratio=round(dc_ratio, 5),
            verdict=verdict,
            attack_classification=classification,
            cryptanalytic_proof=proof
        )

    def simulate_detector_scan(
        self,
        scenario: str = "Honest",
        num_clicks: int = 300
    ) -> BlindingDetectionResult:
        """
        Simulates realistic detector telemetry for testing and live dashboard demonstrations.
        """
        if "Blinding" in scenario or "CW" in scenario:
            # High CW bright light injection
            bias_ua = float(np.random.uniform(12.0, 25.0))
            dx = float(np.random.normal(0.0, 0.3))
            dy = float(np.random.normal(0.0, 0.3))
            # Blinding produces uniform or deterministic pulse triggers
            intervals = list(np.random.normal(5.0, 0.05, num_clicks))
            dc_count = int(num_clicks * 0.01)
        elif "Spatial" in scenario:
            # Spatial beam shift exploit
            bias_ua = float(np.random.uniform(0.3, 0.8))
            dx = float(np.random.uniform(3.5, 5.0))
            dy = float(np.random.uniform(2.0, 3.5))
            intervals = list(np.random.exponential(scale=15.0, size=num_clicks))
            dc_count = int(num_clicks * 0.005)
        elif "Faked" in scenario or "Timing" in scenario:
            # Rigid periodic faked-state pulse train
            bias_ua = float(np.random.uniform(1.2, 2.5))
            dx = float(np.random.normal(0.0, 0.3))
            dy = float(np.random.normal(0.0, 0.3))
            # Periodic pulses at exactly 2.0 us with tiny jitter + some < dead time
            intervals = list(np.random.normal(2.0, 0.01, num_clicks))
            intervals[0] = 0.4  # Dead-time violation (< 1.0 us)
            dc_count = int(num_clicks * 0.08)
        else:
            # Nominal Honest Geiger Operation
            bias_ua = float(np.random.uniform(0.15, 0.55))
            dx = float(np.random.normal(0.0, 0.4))
            dy = float(np.random.normal(0.0, 0.4))
            # True Poissonian exponential inter-arrival intervals
            intervals = list(np.random.exponential(scale=20.0, size=num_clicks))
            # Filter strictly above dead time
            intervals = [max(1.2, t) for t in intervals]
            dc_count = int(num_clicks * 0.002)

        telemetry = DetectorTelemetry(
            channel_id="APD_Channel_A0",
            bias_current_ua=bias_ua,
            spatial_offset_x_um=dx,
            spatial_offset_y_um=dy,
            inter_arrival_times_us=intervals,
            double_click_count=dc_count,
            total_clicks=num_clicks
        )

        return self.evaluate_detector_state(telemetry)
