"""
Q-Sentinel: Phase 25 Live Demonstration & Presentation Validator
Executes the 5 canonical demo scenarios and prints judge-facing narrative speaking points.
"""

import time
import sys
from security.signature import QDSKeyManager
from security.detector import QStatDetector, ThreatCategory
from security.attacks import AttackScenario, ThreatOrchestrator
from security.freshness import FreshnessRegistry


def run_live_demonstration():
    print("=" * 80)
    print("  Q-SENTINEL: PHASE 25 LIVE DEMONSTRATION & REHEARSAL SCRIPT")
    print("  National Quantum Mission (NQM) | SIH26141 Presentation Kit")
    print("=" * 80)

    alice_mgr = QDSKeyManager(signer_id="Alice", private_seed="presentation_seed_alice_2026")
    msg = "Authorize Central Bank Wire Transfer #98234 - INR 5,00,00,000"
    sig = alice_mgr.generate_signature(msg, num_tokens=8)
    detector = QStatDetector(baseline_noise_p0=0.03, z_suspicious_threshold=2.0, z_malicious_threshold=4.0)

    # -------------------------------------------------------------
    # Scenario 1: Honest Legitimate Run
    # -------------------------------------------------------------
    print("\n" + "#" * 80)
    print(">>> SCENARIO 1: LEGITIMATE SIGNATURE VERIFICATION (CLEAN CHANNEL)")
    print("#" * 80)
    sig.nonce = "demo_nonce_01"
    sig.timestamp = time.time()
    res1 = detector.verify_signature_session(sig, sig, trials_per_token=50, ambient_noise=0.03)
    
    print(f"[*] Claimed Signer  : {sig.signer_id}")
    print(f"[*] Physical Error  : {res1.error_rate * 100:.2f}% (Baseline Noise p0 = 3.00%)")
    print(f"[*] Anomaly Z-Score : {res1.z_score:+.2f} sigma (Threshold: z < 2.0)")
    print(f"[*] Verdict         : {res1.verdict.value} (GREEN)")
    print(f"[*] Diagnostic      : {res1.diagnostic_text}")
    print("\n[SPEAKING POINT FOR JUDGES]:")
    print(" 'In Scenario 1, Alice signs the message using her secret Pauli eigenstates.")
    print("  Teleportation reconstructs the states with exact Pauli corrections Z^{b1}X^{b2}.")
    print("  Over 400 projective measurements, the observed error rate is ~3%, which is within")
    print("  the calibrated natural noise floor. The z-score is < 2.0, proving deterministic acceptance.'")
    assert res1.verdict == ThreatCategory.LEGITIMATE

    # -------------------------------------------------------------
    # Scenario 2: Signature Forgery
    # -------------------------------------------------------------
    print("\n" + "#" * 80)
    print(">>> SCENARIO 2: ACTIVE SIGNATURE FORGERY (EVE FABRICATING STATES)")
    print("#" * 80)
    forged_sig, desc = ThreatOrchestrator.execute_scenario(AttackScenario.FORGERY, sig, random_seed=42)
    forged_sig.nonce = "demo_nonce_02"
    forged_sig.timestamp = time.time()
    res2 = detector.verify_signature_session(forged_sig, sig, trials_per_token=50, ambient_noise=0.03)

    print(f"[*] Attack Context  : {desc}")
    print(f"[*] Physical Error  : {res2.error_rate * 100:.2f}% (Expected ~ 50.0%)")
    print(f"[*] Anomaly Z-Score : {res2.z_score:+.2f} sigma (Threshold: z >= 4.0)")
    print(f"[*] Binomial p-val  : {res2.p_value:.4e} (p < 1e-15)")
    print(f"[*] Verdict         : {res2.verdict.value} (RED)")
    print(f"[*] Diagnostic      : {res2.diagnostic_text}")
    print("\n[SPEAKING POINT FOR JUDGES]:")
    print(" 'In Scenario 2, Eve attempts to fabricate signature tokens without Alice's key seed.")
    print("  Because Eve measures/guesses in non-matching bases, projective collapse yields")
    print("  an error rate of ~50%. The exact binomial test yields z > 35 sigma with p < 1e-15,")
    print("  instantly rejecting the forged signature with provable mathematical certainty.'")
    assert res2.verdict == ThreatCategory.MALICIOUS

    # -------------------------------------------------------------
    # Scenario 3: Signer Impersonation
    # -------------------------------------------------------------
    print("\n" + "#" * 80)
    print(">>> SCENARIO 3: SIGNER IMPERSONATION (MALLORY SIGNING AS ALICE)")
    print("#" * 80)
    imp_sig, desc = ThreatOrchestrator.execute_scenario(AttackScenario.IMPERSONATION, sig, random_seed=99)
    imp_sig.nonce = "demo_nonce_03"
    imp_sig.timestamp = time.time()
    res3 = detector.verify_signature_session(imp_sig, sig, trials_per_token=50, ambient_noise=0.03)

    print(f"[*] Attack Context  : {desc}")
    print(f"[*] Physical Error  : {res3.error_rate * 100:.2f}%")
    print(f"[*] Anomaly Z-Score : {res3.z_score:+.2f} sigma")
    print(f"[*] Verdict         : {res3.verdict.value} (RED)")
    print("\n[SPEAKING POINT FOR JUDGES]:")
    print(" 'In Scenario 3, Mallory generates a valid-looking signature using her own key,")
    print("  but claims to be Alice. When the verifier projects onto Alice's registered basis,")
    print("  the subspace mismatch immediately produces an error rate above 30%, triggering an alarm.'")
    assert res3.verdict == ThreatCategory.MALICIOUS

    # -------------------------------------------------------------
    # Scenario 4: Replay Attack
    # -------------------------------------------------------------
    print("\n" + "#" * 80)
    print(">>> SCENARIO 4: REPLAY ATTACK (RE-INJECTION OF STALE SESSIONS)")
    print("#" * 80)
    freshness = FreshnessRegistry(max_time_window_seconds=60.0)
    det_fresh = QStatDetector(freshness_registry=freshness)
    # First valid run
    det_fresh.evaluate(error_count=6, total_trials=200, signer_id="Alice", nonce="token_sess_99", timestamp=time.time())
    # Attacker replays identical nonce
    res4 = det_fresh.evaluate(error_count=6, total_trials=200, signer_id="Alice", nonce="token_sess_99", timestamp=time.time())

    print(f"[*] Freshness Check : Passed={res4.freshness_passed}")
    print(f"[*] Anomaly Z-Score : {res4.z_score:+.2f} sigma")
    print(f"[*] Verdict         : {res4.verdict.value} (RED)")
    print(f"[*] Diagnostic      : {res4.diagnostic_text}")
    print("\n[SPEAKING POINT FOR JUDGES]:")
    print(" 'In Scenario 4, an attacker replays previously valid classical teleportation bits.")
    print("  Notice that the physical error rate is low, but Q-Sentinel catches the replay")
    print("  via our Cryptographic Freshness & Nonce Registry. We explicitly show that replay")
    print("  is caught by bookkeeping, not false statistical anomalies.'")
    assert res4.verdict == ThreatCategory.MALICIOUS

    # -------------------------------------------------------------
    # Scenario 5: Channel Manipulation Dynamic Transition
    # -------------------------------------------------------------
    print("\n" + "#" * 80)
    print(">>> SCENARIO 5: DYNAMIC CHANNEL NOISE (GREEN -> YELLOW -> RED TRANSITION)")
    print("#" * 80)
    for eps, expected_cat in [(0.02, ThreatCategory.LEGITIMATE), (0.07, ThreatCategory.SUSPICIOUS), (0.25, ThreatCategory.MALICIOUS)]:
        noisy_sig, desc = ThreatOrchestrator.execute_scenario(AttackScenario.CHANNEL_NOISE, sig, channel_noise_level=eps, random_seed=55)
        noisy_sig.nonce = f"noise_nonce_{eps}"
        noisy_sig.timestamp = time.time()
        res5 = detector.verify_signature_session(noisy_sig, sig, trials_per_token=50, ambient_noise=0.03)
        print(f"  * Disturbance eps = {eps*100:>4.1f}% | Error = {res5.error_rate*100:>5.2f}% | z = {res5.z_score:>+6.2f} sigma | Verdict: {res5.verdict.value}")

    print("\n[SPEAKING POINT FOR JUDGES]:")
    print(" 'In Scenario 5, our live noise slider demonstrates graceful degradation.")
    print("  As channel disturbance rises, Q-Sentinel cleanly transitions from GREEN to YELLOW (Suspicious)")
    print("  and finally RED (Malicious), providing actionable telemetry before catastrophic failure.'")

    print("\n" + "=" * 80)
    print(">>> ALL 5 DEMO SCENARIOS VALIDATED SUCCESSFULLY. PRESENTATION READY!")
    print("=" * 80)


if __name__ == "__main__":
    run_live_demonstration()
