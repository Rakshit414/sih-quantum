"""
Q-Sentinel: Formal Cybersecurity Benchmark Runner
Stage 6: Phase 19
Runs Monte Carlo simulations and outputs academic and hackathon evaluation tables.
"""

import argparse
import sys
from analytics.metrics import compute_benchmark


def main():
    parser = argparse.ArgumentParser(description="Q-Sentinel Performance & Attack Resilience Benchmark")
    parser.add_argument("--runs", type=int, default=50, help="Number of Monte Carlo iterations per scenario (default: 50)")
    parser.add_argument("--trials", type=int, default=50, help="Projective measurement trials per qubit token (default: 50)")
    parser.add_argument("--tokens", type=int, default=8, help="Number of Pauli-eigenstate tokens per signature (default: 8)")
    parser.add_argument("--noise", type=float, default=0.03, help="Baseline ambient channel noise p0 (default: 0.03)")
    args = parser.parse_args()

    print("=" * 80)
    print(f"  Q-SENTINEL: QUANTUM DIGITAL SIGNATURE THREAT DETECTION BENCHMARK")
    print(f"  Configuration: {args.runs} runs/scenario | {args.tokens} tokens/sig | {args.trials} trials/token (N={args.tokens*args.trials})")
    print(f"  Ambient Noise Floor: p0 = {args.noise:.1%}")
    print("=" * 80)

    report = compute_benchmark(
        num_runs_per_scenario=args.runs,
        trials_per_token=args.trials,
        token_count=args.tokens,
        ambient_noise=args.noise
    )

    print("\n[+] OVERALL SECURITY PERFORMANCE METRICS")
    print("-" * 80)
    print(f"  * Total Executed Verifications   : {report.total_runs}")
    print(f"  * System Classification Accuracy : {report.accuracy * 100:.2f}%")
    print(f"  * False Acceptance Rate (FAR)    : {report.false_acceptance_rate * 100:.2f}%  (Target: 0.00%)")
    print(f"  * False Rejection Rate (FRR)     : {report.false_rejection_rate * 100:.2f}%  (Target: < 1.00%)")
    print(f"  * Mean Detection Latency         : {report.avg_latency_ms:.2f} ms")
    print(f"  * Mean Z-Score (Honest)          : {report.avg_z_legitimate:+.2f}")
    print(f"  * Mean Z-Score (Attacks)         : {report.avg_z_attacks:+.2f}")
    print(f"  * Statistical Z-Separation (Delta_z): {report.z_separation:+.2f} sigma  (Discernibility)")
    print("-" * 80)

    print("\n[+] SCENARIO-BY-SCENARIO BREAKDOWN")
    print("-" * 80)
    print(f"{'Scenario':<30} | {'Mean Error':<12} | {'Mean Z':<10} | {'Latency':<10} | {'Verdicts (L / S / M)'}")
    print("-" * 80)
    for sc_name, data in report.scenario_breakdowns.items():
        v = data["verdicts"]
        v_str = f"{v['LEGITIMATE']:>3} / {v['SUSPICIOUS']:>3} / {v['MALICIOUS']:>3}"
        print(f"{sc_name:<30} | {data['mean_error_rate']*100:>10.2f}% | {data['mean_z']:>+9.2f} | {data['mean_latency_ms']:>8.2f}ms | {v_str}")
    print("-" * 80)

    print("\n[+] CONFUSION MATRIX")
    print("-" * 80)
    print(f"{'Ground Truth':<15} | {'Classified LEGITIMATE':<22} | {'Classified SUSPICIOUS':<22} | {'Classified MALICIOUS'}")
    print("-" * 80)
    for gt, pred in report.confusion_matrix.items():
        print(f"{gt:<15} | {pred['LEGITIMATE']:<22} | {pred['SUSPICIOUS']:<22} | {pred['MALICIOUS']}")
    print("-" * 80)

    if report.false_acceptance_rate == 0.0 and report.accuracy >= 0.98:
        print("\n>>> BENCHMARK STATUS: PASS (Information-Theoretic Security Criteria Satisfied)")
    else:
        print("\n>>> BENCHMARK STATUS: WARNING (Elevated False Acceptance or Rejection)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
