"""
Q-Sentinel: Security Performance Metrics & Benchmarking Suite
Calculates False Acceptance Rate (FAR), False Rejection Rate (FRR),
Accuracy, Detection Latency, Z-Score Separation, and Wilson 95% Confidence Intervals.
"""

from __future__ import annotations
import numpy as np
import time
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple, Optional
from security.detector import ThreatCategory, ThreatAssessment, QStatDetector
from security.signature import QDSKeyManager, QuantumDigitalSignature
from security.attacks import AttackScenario, ThreatOrchestrator


def wilson_score_interval(successes: int, trials: int, confidence: float = 0.95) -> Tuple[float, float]:
    """
    Computes the Wilson score continuity-corrected confidence interval for a binomial proportion.
    Particularly robust for proportions near 0 or 1 where normal approximations fail.
    """
    if trials <= 0:
        return (0.0, 0.0)
    z = 1.95996  # 95% two-sided normal quantile
    p = successes / trials
    denom = 1.0 + (z**2) / trials
    centre = (p + (z**2) / (2.0 * trials)) / denom
    margin = (z / denom) * np.sqrt((p * (1.0 - p) / trials) + ((z**2) / (4.0 * trials**2)))
    lower = max(0.0, centre - margin)
    upper = min(1.0, centre + margin)
    return (float(lower), float(upper))


@dataclass
class BenchmarkReport:
    total_runs: int
    accuracy: float
    false_acceptance_rate: float            # FAR: attacks misclassified as LEGITIMATE
    false_rejection_rate: float             # FRR: honest runs misclassified as MALICIOUS
    avg_latency_ms: float
    z_separation: float                     # avg_z(attacks) - avg_z(legitimate)
    avg_z_legitimate: float
    avg_z_attacks: float
    confusion_matrix: Dict[str, Dict[str, int]]
    scenario_breakdowns: Dict[str, Dict[str, Any]]
    far_ci: Tuple[float, float] = (0.0, 0.0)
    frr_ci: Tuple[float, float] = (0.0, 0.0)
    suspicious_rate_honest: float = 0.0
    suspicious_rate_ci: Tuple[float, float] = (0.0, 0.0)


def compute_benchmark(
    num_runs_per_scenario: int = 100,
    trials_per_token: int = 50,
    token_count: int = 8,
    ambient_noise: float = 0.03,
    random_seed: Optional[int] = None
) -> BenchmarkReport:
    """
    Executes an end-to-end Monte Carlo security benchmark across all attack scenarios.
    """
    if random_seed is not None:
        np.random.seed(random_seed)

    alice_mgr = QDSKeyManager(signer_id="Alice", private_seed="bench_seed_alice_999")
    base_message = "Transfer Authorization #44120"
    legit_sig = alice_mgr.generate_signature(base_message, num_tokens=token_count)
    
    scenarios = [
        AttackScenario.LEGITIMATE,
        AttackScenario.FORGERY,
        AttackScenario.IMPERSONATION,
        AttackScenario.REPLAY,
        AttackScenario.CHANNEL_NOISE,
    ]
    
    detector = QStatDetector(baseline_noise_p0=ambient_noise)
    
    # Tracking
    latencies: List[float] = []
    z_legit_list: List[float] = []
    z_attack_list: List[float] = []
    
    # Confusion: ground_truth -> {LEGITIMATE: count, SUSPICIOUS: count, MALICIOUS: count}
    confusion: Dict[str, Dict[str, int]] = {
        "HONEST": {"LEGITIMATE": 0, "SUSPICIOUS": 0, "MALICIOUS": 0},
        "ATTACK": {"LEGITIMATE": 0, "SUSPICIOUS": 0, "MALICIOUS": 0},
    }
    
    scenario_breakdowns: Dict[str, Dict[str, Any]] = {}
    
    seed_offset = (random_seed * 1000) if random_seed is not None else 0

    for sc in scenarios:
        sc_name = sc.value
        sc_z_scores = []
        sc_errors = []
        sc_latencies = []
        sc_verdicts = {"LEGITIMATE": 0, "SUSPICIOUS": 0, "MALICIOUS": 0}
        
        for r in range(num_runs_per_scenario):
            noise_val = 0.35 if sc == AttackScenario.CHANNEL_NOISE else 0.0
            
            # Generate or perturb signature
            pert_sig, desc = ThreatOrchestrator.execute_scenario(
                scenario=sc,
                original_signature=legit_sig,
                channel_noise_level=noise_val,
                random_seed=10000 + seed_offset + r
            )
            
            # If not a replay scenario, ensure fresh nonce so we isolate the statistical test
            if sc != AttackScenario.REPLAY:
                pert_sig.nonce = f"bench_nonce_{sc_name}_{seed_offset}_{r}"
                pert_sig.timestamp = time.time()
            else:
                # Replay must use stale/duplicate nonce
                pert_sig.nonce = "stale_duplicate_nonce_001"
                pert_sig.timestamp = time.time() - 150.0  # stale
                
            # Time verification latency
            t0 = time.perf_counter()
            assessment = detector.verify_signature_session(
                received_signature=pert_sig,
                expected_signature=legit_sig,
                trials_per_token=trials_per_token,
                ambient_noise=ambient_noise,
                random_seed=20000 + seed_offset + r
            )
            dt_ms = (time.perf_counter() - t0) * 1000.0
            
            latencies.append(dt_ms)
            sc_latencies.append(dt_ms)
            sc_z_scores.append(assessment.z_score)
            sc_errors.append(assessment.error_rate)
            sc_verdicts[assessment.verdict.value] += 1
            
            is_honest_ground_truth = (sc == AttackScenario.LEGITIMATE)
            gt_key = "HONEST" if is_honest_ground_truth else "ATTACK"
            confusion[gt_key][assessment.verdict.value] += 1
            
            if is_honest_ground_truth:
                z_legit_list.append(assessment.z_score)
            else:
                z_attack_list.append(assessment.z_score)
                
        scenario_breakdowns[sc_name] = {
            "mean_z": float(np.mean(sc_z_scores)),
            "mean_error_rate": float(np.mean(sc_errors)),
            "mean_latency_ms": float(np.mean(sc_latencies)),
            "verdicts": sc_verdicts
        }
        
    total_honest = num_runs_per_scenario
    total_attacks = num_runs_per_scenario * 4  # 4 attack scenarios
    total_runs = total_honest + total_attacks
    
    # Metrics
    # FAR: Attack accepted as LEGITIMATE
    attack_accepted_count = confusion["ATTACK"]["LEGITIMATE"]
    far = (attack_accepted_count / total_attacks) if total_attacks > 0 else 0.0
    far_ci = wilson_score_interval(attack_accepted_count, total_attacks)

    # FRR: Honest classified as MALICIOUS (Hard Rejection)
    honest_malicious_count = confusion["HONEST"]["MALICIOUS"]
    frr = (honest_malicious_count / total_honest) if total_honest > 0 else 0.0
    frr_ci = wilson_score_interval(honest_malicious_count, total_honest)

    # Honest classified as SUSPICIOUS (Channel Warning / Audit Trigger)
    honest_suspicious_count = confusion["HONEST"]["SUSPICIOUS"]
    suspicious_rate = (honest_suspicious_count / total_honest) if total_honest > 0 else 0.0
    suspicious_ci = wilson_score_interval(honest_suspicious_count, total_honest)

    # Overall Accuracy: (Honest classified as LEGITIMATE + Attacks classified as MALICIOUS or SUSPICIOUS) / total
    correct_honest = confusion["HONEST"]["LEGITIMATE"]
    correct_attacks = confusion["ATTACK"]["MALICIOUS"] + confusion["ATTACK"]["SUSPICIOUS"]
    accuracy = (correct_honest + correct_attacks) / total_runs
    
    avg_z_legit = float(np.mean(z_legit_list)) if z_legit_list else 0.0
    avg_z_att = float(np.mean(z_attack_list)) if z_attack_list else 0.0
    z_sep = avg_z_att - avg_z_legit
    avg_lat = float(np.mean(latencies)) if latencies else 0.0
    
    return BenchmarkReport(
        total_runs=total_runs,
        accuracy=accuracy,
        false_acceptance_rate=far,
        false_rejection_rate=frr,
        avg_latency_ms=avg_lat,
        z_separation=z_sep,
        avg_z_legitimate=avg_z_legit,
        avg_z_attacks=avg_z_att,
        confusion_matrix=confusion,
        scenario_breakdowns=scenario_breakdowns,
        far_ci=far_ci,
        frr_ci=frr_ci,
        suspicious_rate_honest=suspicious_rate,
        suspicious_rate_ci=suspicious_ci
    )
