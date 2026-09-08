# 📘 Q-SENTINEL Masterclass | Lesson 31: The 14-Watchtower Automated Rehearsal Suite (rehearsal.py)

> **File in Focus:** [`rehearsal.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/rehearsal.py)  
> **Pipeline Position:** Step 31 of the entire Q-Sentinel architecture (Rehearsal & Jury Defense Tier — Phase 39)  
> **Target Audience:** Fresher needing to understand automated end-to-end rehearsal testing, how 14 physical and protocol watchtowers are verified in a single execution sweep, how Monte Carlo stress testing proves zero false negatives (0 FN), and how structured JSON rehearsal reports provide ironclad jury defense.

---

## 🧭 1. What Is This File and Why Does It Exist?

Imagine you are 15 minutes away from walking onto the stage at the Smart India Hackathon Grand Finale or presenting before a panel of Ministry of Defence and National Quantum Mission evaluators:
* The judges ask: *"Can you prove that every single one of your 14 defense modules is working right now, without errors, with zero false negatives, and with sub-millisecond latencies?"*
* If you try to manually run 14 different scripts from 14 terminal windows, you will stumble, lose time, and risk unexpected demo failures.

### The Live-Demo Nightmare vs. Automated Rehearsal
In aerospace engineering and mission-critical defense systems, engineers never rely on manual demonstrations.
They run an automated **System Readiness Sweep**:
[`rehearsal.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/rehearsal.py) is the **Monte Carlo Stress Rehearsal & Jury Defense Suite**. In **under 2.5 seconds**, it executes a synchronized sweep across **all 14 architectural watchtowers**, runs 100 randomized Monte Carlo stress iterations, verifies zero false negatives and zero false positives, and generates an auditable JSON report proving that the system is 100% operational.

---

## 💡 2. Plain English Real-World Analogies

### Analogy 1: The NASA Rocket "Wet Dress Rehearsal" (T-Minus 10 Seconds)
Before NASA launches astronauts on a lunar mission:
* They don't just ignite the main engines on launch day and hope everything works.
* Days prior, they conduct a **Wet Dress Rehearsal**: they load cryogenic liquid hydrogen fuel, pressurize the flight tanks, test every sensor valve, simulate launch abort scenarios, and count down to T-minus 10 seconds.
* [`rehearsal.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/rehearsal.py) is the Wet Dress Rehearsal for Q-Sentinel: it simulates real laser blinding, Trojan probes, rogue repeaters, and quantum forgeries in rapid succession, verifying that every defensive valve trips correctly.

### Analogy 2: The Fire Station Morning Shift Diagnostic Sweep
Every morning at 8:00 AM, firefighters conduct a full vehicle sweep:
* They test the ladder hydraulics, check the water pressure gauges, test the siren, inspect the oxygen masks, and verify the radio frequencies.
* Only when all 14 checklist items read **PASS** is the engine certified ready for emergency response.

---

## 📐 3. The 14-Watchtower Defense Architecture

```
                       QuantumRehearsalRunner.rehearse_all_watchtowers()
                                              │
         ┌────────────────────────────────────┼────────────────────────────────────┐
         ▼ (Quantum Transport)                ▼ (Cryptographic Core)               ▼ (Hardware Watchtowers)
┌──────────────────────────────┐     ┌──────────────────────────────┐     ┌──────────────────────────────┐
│ 1. Quantum Teleportation     │     │ 4. Multi-Party Non-Repudiat. │     │ 7. Decoy PNS Defense         │
│    (Born projective meas.)   │     │    (Bob-Charlie Arbiter)     │     │    (Hwang-Lo 3-intensity)    │
├──────────────────────────────┤     ├──────────────────────────────┤     ├──────────────────────────────┤
│ 2. Q-STAT Hypothesis Engine  │     │ 5. Dual-Layer Hybrid PQC     │     │ 8. Trojan-Horse Probe        │
│    (z >= 4.0, p < 1e-15)     │     │    (HMAC-SHA3-512 + QDS)     │     │    (4-sensor multispectral)  │
├──────────────────────────────┤     ├──────────────────────────────┤     ├──────────────────────────────┤
│ 3. Sliding Freshness Nonce   │     │ 6. Quantum Mesh Repeaters    │     │ 9. APD Detector Blinding     │
│    (60s replay prevention)   │     │    (Rogue node localization) │     │    (Makarov CW current trip) │
└──────────────────────────────┘     └──────────────────────────────┘     └──────────────┬───────────────┘
                                                                                         │
         ┌───────────────────────────────────────────────────────────────────────────────┘
         ▼ (Physics Bounds & Enterprise CTI)
┌──────────────────────────────┐     ┌──────────────────────────────┐     ┌──────────────────────────────┐
│ 10. Device-Indep. CHSH Bell  │     │ 12. MDI Untrusted Relay      │     │ 14. Enterprise SOC SIEM      │
│     (S <= 2.0 classical rej) │     │     (HOM interference dip)   │     │     (OASIS STIX 2.1 / ECS)   │
├──────────────────────────────┤     ├──────────────────────────────┤     └──────────────────────────────┘
│ 11. Finite-Size Composable   │     │ 13. WDM Co-Propagation      │
│     (Serfling Martingale xi) │     │     (SMF-28 Raman defense)   │
└──────────────────────────────┘     └──────────────────────────────┘
```

### The 14-Watchtower Inventory Matrix:
| ID | Watchtower Name | Target Threat / Attack Vector | Physical Invariant Tested | Pass Condition |
| :---: | :--- | :--- | :--- | :--- |
| **WT-01** | **Quantum Teleportation (QDS)** | Basis reconstruction loss | Bennett 1993 3-qubit BSM circuit | Fidelity $F \ge 0.99$ |
| **WT-02** | **Q-STAT Hypothesis Engine** | Quantum Pauli eigenstate forgery | Exact binomial distribution | $z \ge 4.0\sigma$, Verdict = `MALICIOUS` |
| **WT-03** | **Sliding-Window Freshness** | Classical session replay attack | Nonce deduplication & 60s window | Duplicate nonce rejected = `MALICIOUS` |
| **WT-04** | **Multi-Party Non-Repudiation** | Alice split-brain repudiation | Token symmetrization cross-check | Discrepancy caught, non-repudiation fails |
| **WT-05** | **Dual-Layer Hybrid (Q-HYBRID)** | Classical message payload tampering | NIST FIPS 202 HMAC-SHA3-512 | Constant-time digest mismatch caught |
| **WT-06** | **Quantum Mesh Repeater (Q-MESH)** | Man-in-the-middle rogue repeater | 4-qubit entanglement swapping | Rogue repeater isolated to `"Repeater-2"` |
| **WT-07** | **Decoy-State PNS (Q-DECOY)** | Photon Number Splitting attack | Hwang-Lo 3-intensity statistics | Yield violation caught: $Y_1 \le Y_1^{\text{bound}}$ |
| **WT-08** | **Trojan-Horse (Q-TROJAN)** | Optical probe injection on modulators | Lindblad decoherence & 4-sensor gate | Power threshold breached: $P \ge 0.01\,\mu\text{W}$ |
| **WT-09** | **Detector Blinding (Q-BLIND)** | Makarov CW laser APD blinding | Geiger-to-linear mode phase transition | DC bias current breached: $I_{\text{bias}} \ge 5.0\,\mu\text{A}$ |
| **WT-10** | **Device-Independent CHSH (Q-CHSH)** | Separable state spoofing | Tsirelson quantum bound ($2\sqrt{2}$) | Classical bound obeyed ($S \le 2.0$) $\implies$ `MALICIOUS` |
| **WT-11** | **Finite-Size Security (Q-FINITE)** | Statistical sampling fluctuations | Serfling Martingale large-deviation | Phase error upper bound $e_U$ calculated |
| **WT-12** | **MDI Untrusted Relay (Q-MDI)** | Compromised central BSM detector | Two-photon HOM interference dip | Symmetric error breached ($e_Z > 8\%$) |
| **WT-13** | **Quantum WDM Raman (Q-WDM)** | Classical DWDM cross-talk jamming | Effective length $L_{\text{eff}}$ & SpRS | High-power $+14\text{ dBm}$ pump collapses SNR |
| **WT-14** | **Enterprise SOC SIEM (Q-SOC)** | Threat intelligence siloing | OASIS STIX 2.1 & ECS 8.x format | STIX bundle generated & HTTP 200 delivered |

---

## 🔬 4. Architectural Breakdown of `rehearsal.py`

Let's examine how [`rehearsal.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/rehearsal.py) orchestrates this sweep.

### Class 1: `WatchtowerTestResult` (Lines 49–57)
Captures the output of an individual test:
* `watchtower_name: str`: Human-readable watchtower title.
* `scenario: str`: Specific adversarial scenario executed.
* `verdict: str`: Outcome classification (`SUCCESS`, `MALICIOUS`, `DELIVERED`).
* `latency_ms: float`: Execution latency in milliseconds.
* `passed: bool`: Boolean asserting that the test satisfied its security invariant.
* `details: str`: Physical metrics (e.g. $z$-score, fidelity, bias current, STIX object count).

### Class 2: `RehearsalReport` (Lines 60–125)
The aggregate report container:
* Metrics: `total_rehearsals`, `watchtowers_verified`, `passed_tests`, `failed_tests`, `false_positives`, `false_negatives`, `detection_rate_pct`, `accuracy_pct`, `mean_latency_ms`, `max_latency_ms`.
* Helper properties: `watchtowers_passed`, `watchtowers_total`, `watchtower_pass_rate`, `avg_latency_ms`.
* `to_json()` method (Lines 95–124): Serializes the entire sweep into a structured, SIEM-ingestible JSON document.

### Class 3: `QuantumRehearsalRunner` (Lines 127–442)
The master execution controller:

#### 1. The Full Sweep: `rehearse_all_watchtowers()` (Lines 137–382)
Iterates through all 14 watchtowers sequentially, wrapping each in high-precision `time.perf_counter()` timers and testing exact physical assertions:
* WT-01: Asserts `tele_res.fidelity > 0.99`.
* WT-02: Asserts `assess.verdict == ThreatCategory.MALICIOUS`.
* WT-03: Asserts `not is_fresh` (replay blocked).
* WT-04: Asserts `not mp_res.non_repudiation_passed`.
* WT-05: Asserts `not h_res.classical_hash_matched`.
* WT-06: Asserts `mesh_res.rogue_node_identified == "Repeater-2"`.
* WT-07: Asserts `pns_res.pns_attack_detected == True`.
* WT-08: Asserts `tr_res.verdict == ThreatCategory.MALICIOUS`.
* WT-09: Asserts `bl_res.verdict == ThreatCategory.MALICIOUS`.
* WT-10: Asserts `chsh_res.verdict == ThreatCategory.MALICIOUS`.
* WT-11: Asserts `f_res.verdict == ThreatCategory.MALICIOUS`.
* WT-12: Asserts `mdi_res.verdict == ThreatCategory.MALICIOUS`.
* WT-13: Asserts `w_res.verdict == ThreatCategory.MALICIOUS`.
* WT-14: Asserts `siem_disp.dispatch_status == "DELIVERED (HTTP 200 OK)"`.

#### 2. The Stress Test: `run_monte_carlo_stress_test()` (Lines 384–442)
Runs an intensive batch test of $N$ iterations (default $100$ runs):
* Alternates between legitimate transmissions ($i\text{ even}$) and randomized attacks ($i\text{ odd}$, alternating between Forgery and Channel Noise).
* Tracks:
  - `false_negatives` (attacks misclassified as `LEGITIMATE`).
  - `false_positives` (honest sessions misclassified as `MALICIOUS`).
* Calls `rehearse_all_watchtowers()` and compiles the master `RehearsalReport`.

---

## ⚡ 5. Real Execution Trace & Output Analysis

When executed via `python rehearsal.py`, the terminal output displays:

```text
================================================================================
Q-SENTINEL: MONTE CARLO STRESS REHEARSAL & JURY DEFENSE SUITE (PHASE 39)
================================================================================
[*] Executing full watchtower sweep...

Execution Summary [2026-09-08 06:32:40 UTC]:
  Total Monte Carlo Sessions: 100
  Watchtowers Verified:       14/14
  Watchtower Sweep Pass Rate: 14/14 (100%)
  Malicious Detection Rate:   100.0% (0 False Negatives)
  False Positive Rate:        0/50 (0.0%)
  Average Session Latency:    2.33 ms
  Peak Maximum Latency:       3.35 ms
--------------------------------------------------------------------------------
Watchtower Diagnostic Results:
  [PASS] Quantum Teleportation (QDS)              | Latency:  0.33 ms | Fidelity=1.0000, Bell bits=(1, 1)
  [PASS] Q-STAT Hypothesis Engine                 | Latency:  2.16 ms | z=+60.09 sigma, Error=69.2%, p=2.32e-191
  [PASS] Sliding-Window Freshness                 | Latency:  0.00 ms | Replay detected: Nonce already processed
  [PASS] Multi-Party Non-Repudiation              | Latency:  4.49 ms | Transferability failure caught: discrepancy=50.0%
  [PASS] Dual-Layer Hybrid (Q-HYBRID)             | Latency:  2.20 ms | HMAC-SHA3-512 mismatch intercepted at classical layer
  [PASS] Quantum Mesh Repeater (Q-MESH)           | Latency:  0.20 ms | Isolated rogue node: Repeater-2
  [PASS] Decoy-State PNS Defense (Q-DECOY)        | Latency:  0.03 ms | Yield violation caught: Y1=0.0000e+00
  [PASS] Trojan-Horse Watchtower (Q-TROJAN)       | Latency:  0.10 ms | Power metering threshold breached: P=2.0 uW
  [PASS] Detector Blinding Watchtower (Q-BLIND)   | Latency:  0.17 ms | Geiger-to-linear transition: bias=16.8 uA
  [PASS] Device-Independent Bell Test (Q-CHSH)    | Latency:  0.41 ms | Classical bound obeyed (S=1.300 <= 2.0)
  [PASS] Finite-Size Composable Security (Q-FINITE) | Latency:  0.04 ms | Phase error upper bound: e_U=36.4%
  [PASS] MDI Untrusted Relay Watchtower (Q-MDI)   | Latency:  4.38 ms | Forbidden symmetric error breached: e_Z=14.9%
  [PASS] Quantum WDM Raman Defense (Q-WDM)        | Latency:  0.03 ms | Raman noise collapsed SNR to 0.00
  [PASS] Enterprise SOC Integration (Q-SOC)       | Latency:  0.17 ms | STIX objects=7, Severity=7/10
================================================================================
```

### Key Analytical Takeaways:
1. **100% Pass Rate:** All 14 watchtowers executed and passed their physical and cryptographic assertions.
2. **Zero False Negatives:** Detection rate is exactly $100.0\%$. Zero attacks bypassed the watchtower grid.
3. **Zero False Positives:** Zero false alarms in calibrated optical channels ($0/50 = 0.0\%$).
4. **Sub-3ms Total Latency:** The average session latency across all 100 runs was **$2.33\text{ ms}$**, with a peak latency of **$3.35\text{ ms}$**.

---

## ⚔️ 6. Hackathon Judge Defense & Viva Voce Q&A

### Q1: "Why do you have 14 watchtowers? Isn't that over-engineering?"
**Defense:**  
> *"In quantum cryptography, every physical hardware component has an associated vulnerability vector that can compromise security if left unmonitored:  
> * **Laser Sources:** Vulnerable to Photon Number Splitting $\to$ Solved by **Q-DECOY** (WT-07).  
> * **Phase Modulators:** Vulnerable to Trojan probe back-reflections $\to$ Solved by **Q-TROJAN** (WT-08).  
> * **Single-Photon Detectors:** Vulnerable to continuous-wave laser blinding $\to$ Solved by **Q-BLIND** (WT-09).  
> * **Untrusted Relays:** Vulnerable to fake coincidence announcements $\to$ Solved by **Q-MDI** (WT-12).  
> * **Commercial Fiber:** Vulnerable to Raman scattering noise $\to$ Solved by **Q-WDM** (WT-13).  
> * **Finite Keys:** Vulnerable to finite-sample fluctuations $\to$ Solved by **Q-FINITE** (WT-11).  
> Having 14 watchtowers is not over-engineering; it is the comprehensive coverage required to achieve commercial defense-grade quantum cybersecurity."*

### Q2: "How does `rehearsal.py` prevent stochastic test flaking?"
**Defense:**  
> *"Quantum simulations rely on random multinomial and Poisson sampling. If trial counts are too low, normal statistical variance can occasionally cause a test assertion to fluctuate across a decision boundary.  
> In [`rehearsal.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/rehearsal.py), we carefully sized sample counts ($N=1,200$ for MDI, $N=3,000$ for Decoy, $N=300$ for CHSH) such that the physical separation between honest and attack states is greater than $4.5\sigma$. This reduces the theoretical probability of a false assertion to less than $10^{-6}$, guaranteeing rock-solid repeatability across thousands of automated CI/CD runs."*

### Q3: "What is the difference between `rehearsal.py` and `benchmark.py`?"
**Defense:**  
> *"They serve complementary roles in our evaluation hierarchy:  
> * [`benchmark.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/benchmark.py) (Phase 19) focuses on **statistical metrics**: evaluating FAR, FRR, $z$-score separations ($\Delta z$), and confusion matrices for signature verification.  
> * [`rehearsal.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/rehearsal.py) (Phase 39) focuses on **comprehensive architectural sweeps**: verifying all 14 physical watchtowers, hardware side-channels, and CTI bundlers in an end-to-end integration test."*

### Q4: "How does `rehearsal.py` integrate with the Streamlit Web Dashboard?"
**Defense:**  
> *"In [`app.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/app.py), Tab 15 (NQM Defense Whitepaper & Rehearsal Kit) imports `QuantumRehearsalRunner`.  
> Operators can click 'Execute 14-Watchtower Rehearsal Sweep' directly from the web browser. The dashboard runs `rehearse_all_watchtowers()`, displays a green checklist of all 14 passing watchtowers with live latencies, and allows operators to download the complete JSON rehearsal certificate."*

### Q5: "How does `test_nqm_whitepaper_document_integrity` ensure compliance?"
**Defense:**  
> *"In `tests/test_rehearsal.py` (Lines 72–95), automated tests inspect the text of `docs/NQM_EXECUTIVE_WHITEPAPER.md`.  
> It verifies that all 14 watchtower codes (`WT-01` through `WT-14`) and mathematical proofs (Serfling Martingale, CHSH Tsirelson Bound, Hong-Ou-Mandel Visibility, Spontaneous Raman Scattering) exist in the documentation. This ensures that our code and technical whitepaper remain 100% synchronized."*

---

## 🔗 7. The Next Step in the Pipeline

With [`rehearsal.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/rehearsal.py), we have verified that all 14 watchtowers pass with 100% accuracy and zero false negatives.

Now, how do we perform the **ultimate release audit** across all 8 architectural pillars and seal the entire codebase with a SHA-256 cryptographic checksum?
👉 **Lesson 32:** [`release_audit.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/release_audit.py)  
*(The Grand Unified Release Auditor: `GrandUnifiedReleaseAuditor`, verifying all 8 architectural pillars, confirming 97 passing unit tests, and computing the cryptographic SHA-256 Release Seal).*
