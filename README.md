<div align="center">

# Q-SENTINEL: Quantum-Inspired Cyber Threat Detection Framework

**Continuous Threat Surveillance, Sub-Second Early Stopping & Non-Repudiation for Teleportation-Based Quantum Digital Signatures**

[![Tests](https://img.shields.io/badge/tests-130%20passed-brightgreen.svg)](tests/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%20%7C%203.14-blue.svg)](https://www.python.org/downloads/)
[![Problem Statement](https://img.shields.io/badge/SIH--2026-SIH26141-orange.svg)](https://www.sih.gov.in/)
[![Mission Track](https://img.shields.io/badge/Mission-National%20Quantum%20Mission%20(NQM)-purple.svg)](docs/NQM_EXECUTIVE_WHITEPAPER.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Zero ML](https://img.shields.io/badge/AI%2FML-Zero%20Black--Box%20(Deterministic)-success.svg)](docs/JUDGE_DEFENSE_MANUAL.md)

*Team QUANT · Smart India Hackathon 2026 · Grand Finale Production Release*

</div>

---

## Abstract

Current public-key cryptosystems (RSA, DSA, ECDSA) are fundamentally vulnerable to polynomial-time factorization via Shor’s algorithm on cryptographically relevant quantum hardware. While **Quantum Digital Signatures (QDS)** provide information-theoretic security guaranteed by the No-Cloning Theorem and Measurement Disturbance, their physical implementations over lossy optical fibers remain exposed to cyber-attacks: **cryptographic state forgery, signer impersonation, stale token replay, and optical side-channel tapping**.

**Q-Sentinel** introduces an auditable, quantum-inspired security framework specifically engineered for entanglement-assisted, teleportation-based QDS protocols. It transforms projective measurement streams into a continuous, real-time threat surveillance telemetry pipeline. Operating entirely on standard commodity hardware, Q-Sentinel couples **14 Optical Hardware Watchtowers** with a **Sequential Q-STAT Engine** (Page's CUSUM and Wald's Sequential Probability Ratio Test) to intercept attacks trial-by-trial.

> **A note on architectural constraint (Zero AI/ML).** Per the strict requirements of problem statement **SIH26141**, Q-Sentinel rejects black-box neural networks, heuristic clustering, and generative models. Deep learning models are susceptible to adversarial evasion and cannot provide court-admissible security guarantees. Instead, all detection thresholds and security scores in Q-Sentinel are **100% mathematically deterministic**, derived from closed-form binomial distributions, information-theoretic bounds, and sequential hypothesis testing.

**Headline Result.** During active cryptographic forgery ($\approx 50\%$ projective error rate), Q-Sentinel's sequential engine achieves definitive detection at **Trial 6** ($\text{SPRT LLR} \ge +9.21$, joint $\alpha = 10^{-4}$), halting the quantum optical transmission and **saving 98.5% of quantum channel bandwidth** compared to classical batch protocols. Over 500 Monte Carlo iterations, the framework maintains **100.0% Detection Accuracy**, **0.0% False Acceptance Rate (FAR)**, and a statistical Z-separation of **$+24.71\sigma$** against baseline channel noise.

**Cryptographic Non-Repudiation.** Using a multi-recipient quantum cross-verification exchange (Bob vs. Charlie), Q-Sentinel guarantees signature transferability (discrepancy rate $= 0.0\%$, $z = -0.50\sigma$) and seals all session events in an immutable, **tamper-evident SHA3-256 hash-chained audit ledger** with zero blockchain latency.

---

## Highlights

- 🎯 **100% Deterministic Detection** — 100% detection recall across state forgery ($z = +41.1\sigma$), signer impersonation ($z = +26.9\sigma$), stale replay ($>60\text{s}$ TTL), and optical eavesdropping.
- ⚡ **Sub-Second Early Stopping** — Wald's SPRT ($A = +9.21, B = -9.21$) and Page's CUSUM ($h = 8.5$) catch tampering at **Trial 6**, slashing Average Sample Number (ASN) by **98.5%**.
- 🛡️ **14 Optical Hardware Watchtowers** — Real-time surveillance of CHSH Bell non-locality ($S > 2$), Decoy-State Photon Number Splitting (PNS), APD detector blinding, Raman scattering, and Trojan-horse lasers ($<0.01\,\mu\text{W}$).
- 🌐 **Distributed Microservices Mesh** — Decoupled physical multi-node architecture across Alice (Signer), Eve (Relay on Port 8001), and Bob (Sink on Port 8002) with strict AST import boundary isolation.
- 🔐 **Tamper-Evident SHA3-256 Chaining** — Cryptographic forward hash pointers ($H_i = \text{SHA3-256}(H_{i-1} \parallel \text{Payload} \parallel \text{Verdict})$) guarantee court-admissible audit logs without blockchain overhead.
- 💻 **100% Classical Execution** — Pure vectorized linear algebra in Python/NumPy/SciPy. Executes with sub-2ms latency on standard commodity CPUs without cryogenic QPUs.
- ✅ **Grand-Finale Certified** — **130/130 automated unit, integration, and stress tests passing (100% green)**, verified against an 8-pillar production freeze audit.

---

## Empirical Benchmarks & Results

### 1 · Threat Classification Performance

Performance measured across 500 Monte Carlo runs per scenario with $N = 400$ projective measurement trials (calibrated optical fiber noise floor $p_0 = 2.87\%$):

<div align="center">

| Operational Scenario | Observed Error Rate ($\hat{e}$) | Anomaly Score ($z$-Score) | SPRT Decision Trial | Bandwidth Saved | Detection Verdict |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Clean Fiber Baseline** | $2.80\% \pm 0.4\%$ | $-0.12\sigma$ | Trial 400 (Exhaustive) | Baseline | 🟢 **LEGITIMATE** |
| **State Forgery Attack** | $48.30\% \pm 1.2\%$ | **$+41.14\sigma$** | **Trial 6** | **98.5%** | 🔴 **MALICIOUS** |
| **Signer Impersonation** | $32.60\% \pm 1.5\%$ | **$+26.92\sigma$** | **Trial 18** | **95.5%** | 🔴 **MALICIOUS** |
| **Stale Replay Attack** | N/A (Expired Nonce) | $\infty$ (Temporal Failure) | Instantaneous | 100.0% | 🔴 **MALICIOUS** |
| **Optical Tap / Trojan Laser**| $8.50\% \pm 0.8\%$ | $+5.12\sigma$ | Trial 42 | 89.5% | 🟡 **SUSPICIOUS** |

</div>

### 2 · Multi-Party Non-Repudiation Cross-Verification

To prevent dispute scenarios where Alice repudiates a signature or sends conflicting quantum tokens to different parties, Bob and Charlie execute an arbiter cross-verification protocol:

<div align="center">

| Verification Metric | Honest Signer (Alice) | Repudiating Signer | Threshold Invariant | Status |
| :--- | :---: | :---: | :---: | :---: |
| **Bob Verification Verdict** | LEGITIMATE ($e = 3.2\%$) | LEGITIMATE ($e = 3.1\%$) | $e < 5.0\%$ | ✅ PASS |
| **Charlie Verification Verdict** | LEGITIMATE ($e = 2.5\%$) | MALICIOUS ($e = 49.2\%$) | $e < 5.0\%$ | ✅ PASS |
| **Cross-Recipient Discrepancy** | **0.0% (Exact Match)** | **46.1% (Tampered)** | $\Delta e < 5.0\%$ | ✅ PASS |
| **Non-Repudiation Status** | **PASSED (TRANSFERABLE)** | **REJECTED (DISPUTE)** | Transferable Bound | ✅ PASS |

</div>

---

## System Architecture & Workflow

```
[ PHYSICAL SIGNER NODE (Alice) ]
  1. Transaction Payload ($500,000 Wire Transfer) mapped to SHA-256 Digest.
  2. State Preparation into Non-Orthogonal Pauli Eigenstates:
     Z-Basis {|0⟩, |1⟩}, X-Basis {|+⟩, |-⟩}, Y-Basis {|+i⟩, |-i⟩}.
  3. 3-Qubit Joint Bell State Measurement (BSM) with Entangled EPR Pair: |Φ⁺⟩ = (|00⟩+|11⟩)/√2.
  4. Transmit classical feed-forward bits (m₁, m₂) + Quantum Token Stream.
                   │
                   ▼
[ ADVERSARIAL NETWORK RELAY (Eve Daemon on HTTP Port 8001) ]
  • Threat Scenarios: Clean Noise (2.87%) | Forgery (~50%) | Impersonation | Replay (>60s TTL).
  • Simulates physical fiber degradation, beam splitting (PNS), and detector blinding.
                   │
                   ▼
[ PHYSICAL VERIFIER SINK (Bob Daemon on HTTP Port 8002) ]
  1. Unitary Pauli Correction: U = Z^{m₁} · X^{m₂} reconstructs quantum state |ψ⟩.
  2. Projective Measurement across Alice's basis over Born-rule trials.
                   │
                   ├──► [ 14 PHYSICAL HARDWARE WATCHTOWERS ]
                   │    CHSH Bell Violation (S > 2) · Decoy Yields · APD Current · Trojan Lasers
                   │
                   └──► [ DUAL-LAYER SEQUENTIAL Q-STAT ENGINE ]
                        • Page's CUSUM (h = 8.5) catches micro-burst tampering
                        • Wald's SPRT (A = +9.21, B = -9.21) early-stops at Trial 6
                   │
                   ▼
[ DECISION, CONTAINMENT & CRYPTOGRAPHIC AUDIT ]
  • Verdict: LEGITIMATE (Pass) | SUSPICIOUS (Audit) | MALICIOUS (Quarantine Mallory)
  • Tamper-Evident SHA3-256 Hash Chaining: H_i = SHA3-256(H_{i-1} || Payload || Verdict)
  • Enterprise SIEM Integration: OASIS STIX 2.1 JSON + Elastic Common Schema (ECS)
```

---

## Installation & Quick Start

### Quick Launch (5-Step Setup)
```bash
# 1. Clone repository
git clone https://github.com/Rakshit414/sih-quantum.git
cd sih-quantum

# 2. Install dependencies (Python 3.10+ / 3.14 supported)
python -m pip install -r requirements.txt

# 3. Verify health (130/130 tests passing in ~10s)
python run_tests.py

# 4. Launch interactive dashboard
streamlit run app.py
```
> Open your browser at **`http://localhost:8501`**.

---

### Step-by-Step Installation & Environments

```bash
# Clone the repository
git clone https://github.com/Rakshit414/sih-quantum.git
cd sih-quantum

# Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

# Install dependencies
python -m pip install -r requirements.txt
```

### 2 · Automated Verification Suite
Execute the comprehensive regression test suite:

```bash
python run_tests.py
```
> **Output:** `130 passed in ~10s` (100% green pass rate across quantum physics, watchtowers, sequential statistics, and AST boundaries).

---

### 3 · Launching the Prototype

#### Option A: Quick-Start Standalone Mode (Single Terminal)
To immediately explore the 16-tab SOC Cockpit, 3D Bloch spheres, Born-rule validations, and 1-Click Guided Attack Demos:

```bash
streamlit run app.py
```
*(Or cross-platform launcher: `python run_qsentinel.py`)*  
Open your browser at **`http://localhost:8501`**.

---

#### Option B: Distributed Microservices Mode (Recommended for Full Evaluation)
To experience the true decoupled physical multi-process architecture across independent HTTP sockets:

Open 3 separate terminals:

```bash
# Terminal 1: Start Bob Verifier Sink (Port 8002)
python -m transport.bob_node

# Terminal 2: Start Eve Adversarial Channel Relay (Port 8001)
python -m transport.eve_channel

# Terminal 3: Start Alice Signer & Streamlit SOC Dashboard
streamlit run app.py
```

<details>
<summary>▶ Click to view advanced audit & benchmark commands</summary>

```bash
# Execute the Grand Unified 8-Pillar Release Audit
python run_audit.py

# Execute Monte Carlo performance benchmarking (50 runs × 50 trials)
python benchmark.py --runs 50 --trials 50

# Execute comparative blind red-team evaluation (V1 vs V2 Sequential)
python benchmark_v2.py
```
</details>

---

## Repository Structure

```
sih-quantum/
├── app.py                      ← Interactive Streamlit SOC Mission Control (16 Tabs)
├── run_qsentinel.py            ← Cross-platform single-command dashboard launcher
├── run_tests.py                ← 130-test regression test suite runner
├── run_audit.py                ← Grand Unified 8-Pillar Release Audit runner
├── package_submission.py       ← Self-healing automated release packaging engine
├── benchmark.py                ← Monte Carlo statistical performance benchmark
├── benchmark_v2.py             ← Phase 45 comparative blind evaluation benchmark
├── requirements.txt            ← Dependency manifest (NumPy, SciPy, Streamlit, Plotly)
│
├── transport/                  ← Distributed Decoupled Microservices (Phase 43)
│   ├── alice_node.py           ← Alice Signer client with dynamic early stopping
│   ├── eve_channel.py          ← Eve Adversarial Relay daemon on HTTP port 8001
│   └── bob_node.py             ← Bob Verifier Sink daemon on HTTP port 8002
│
├── quantum/                    ← Quantum Mechanics & Information Layer
│   ├── state.py                ← Pauli matrices (σ_x, σ_y, σ_z), eigenstates, tensor products
│   ├── bell.py                 ← 4 Bell states, partial trace, maximal entanglement fidelity
│   ├── teleport.py             ← 3-qubit teleportation, BSM, Pauli unitary corrections
│   ├── measure.py              ← Born-rule projective measurement & shot sampling
│   ├── tomography.py           ← Quantum state tomography & Stokes density matrix reconstruction
│   └── mesh.py                 ← Quantum mesh routing & entanglement swapping protocols
│
├── security/                   ← Defense & Optical Watchtowers (14 Dedicated Detectors)
│   ├── signature.py            ← SHA-256 digest, Pauli keys, QDS token serialization
│   ├── freshness.py            ← Sliding time-window & cryptographic nonce registry (anti-replay)
│   ├── attacks.py              ← Active forgery, impersonation, noise, & replay injectors
│   ├── detector.py             ← Classical Q-STAT engine (exact binomial test, z-score)
│   ├── sequential.py           ← Sequential Q-STAT (Page CUSUM h=8.5, Wald SPRT A=9.21)
│   ├── calibrate.py            ← Dynamic Noise Calibrator (Phase 47 pilot-frame tracking)
│   ├── chsh.py                 ← CHSH Bell inequality non-locality watchtower (S > 2)
│   ├── decoy.py                ← Decoy-state Poissonian photon number splitting (PNS) detector
│   ├── trojan.py               ← Trojan-horse laser & Lindblad quantum memory decoherence filter
│   ├── blind.py                ← Avalanche Photodiode (APD) detector blinding watchtower
│   ├── mdi.py                  ← Measurement-Device-Independent (MDI) untrusted relay mode
│   ├── wdm.py                  ← WDM co-propagation & Raman scattering anti-jamming filter
│   └── multirecipient.py       ← Multi-party non-repudiation cross-verification & certificate minting
│
├── analytics/                  ← Telemetry Persistence & Enterprise SIEM Integration
│   ├── metrics.py              ← Confusion matrix, FAR, FRR, accuracy, detection latency
│   ├── history.py              ← SQLite ACID datastore with SHA3-256 hash chaining
│   └── soc.py                  ← OASIS STIX 2.1 JSON threat intelligence & Elastic Common Schema (ECS)
│
├── docs/                       ← Scientific Whitepapers & Formal Defense Assets
│   ├── NQM_EXECUTIVE_WHITEPAPER.md      ← National Quantum Mission technical paper
│   ├── JUDGE_DEFENSE_MANUAL.md          ← Evaluator objection handling & mathematical proofs
│   ├── SIH26141_FINAL_PITCH_DECK.md     ← 12-slide executive hackathon presentation deck
│   ├── RELEASE_MANIFEST.md              ← Master SHA-256 release integrity manifest
│   └── RELEASE_AUDIT_CERTIFICATE.json   ← Cryptographic release audit certificate
│
└── tests/                      ← Automated Test Suite (130 Tests, 100% Pass Rate)
    ├── test_quantum.py         ← Quantum foundations & Pauli eigenbasis tests
    ├── test_teleport.py        ← Teleportation fidelity & Pauli correction tests
    ├── test_security.py        ← Attack injection & Q-STAT detection tests
    ├── test_sequential.py      ← Page CUSUM & Wald SPRT early stopping tests
    ├── test_import_boundary.py ← Strict AST import isolation boundary invariants
    └── test_release_audit.py   ← Production release freeze & manifest verification tests
```

---

## Python API Examples

### 1 · Quantum Teleportation & State Reconstruction

```python
import numpy as np
from quantum.state import PauliState
from quantum.teleport import QuantumTeleportationEngine

# Alice prepares an unknown signature eigenstate |+⟩ (X-basis)
input_state = PauliState.PLUS.state_vector

# Execute 3-qubit entanglement-assisted teleportation
engine = QuantumTeleportationEngine()
teleport_result = engine.teleport(input_state)

# Bob reconstructs the exact state via feed-forward Pauli correction (U = Z^m1 · X^m2)
reconstructed_state = teleport_result.reconstructed_state
fidelity = np.abs(np.vdot(input_state, reconstructed_state)) ** 2

print(f"Classical Bits: (m1={teleport_result.m1}, m2={teleport_result.m2})")
print(f"Teleportation Reconstruction Fidelity: {fidelity:.6f}")  # 1.000000
```

### 2 · Sequential Q-STAT Surveillance (SPRT & CUSUM)

```python
from security.sequential import SequentialQStat, SequentialHypothesisConfig

# Initialize sequential surveillance engine (Noise floor p0=2.87%, Forgery p1=50%)
config = SequentialHypothesisConfig(p0=0.0287, p1=0.50, alpha=1e-4, beta=1e-4)
qstat = SequentialQStat(config)

# Ingest active forgery stream trial-by-trial
for trial_idx in range(1, 20):
    # Simulated forgery outcome (1 = error, 0 = match)
    observed_error = 1 if trial_idx % 2 == 0 else 0
    step = qstat.step(observed_error)
    
    if step.decision_reached:
        print(f"[*] ATTACK INTERCEPTED at Trial {step.trial_count}!")
        print(f"[*] Wald SPRT LLR: {step.sprt_llr:+.4f} | CUSUM Stat: {step.cusum_stat:.4f}")
        print(f"[*] Final Verdict: {step.verdict}")  # MALICIOUS
        break
```

### 3 · Cryptographic Audit Ledger & Non-Repudiation Check

```python
from security.multirecipient import MultiRecipientCrossVerifier
from analytics.history import VerificationHistoryStore

# Verify signature transferability between Bob and Charlie
verifier = MultiRecipientCrossVerifier()
exchange_result = verifier.verify_transferability(
    bob_tokens=bob_received_tokens,
    charlie_tokens=charlie_tokens,
    claimed_signer="Alice"
)

# Store event with immutable SHA3-256 hash chaining
db = VerificationHistoryStore()
record_id, block_hash = db.record_verification(
    signer="Alice",
    payload="Authorize Wire Transfer $500,000",
    verdict=exchange_result.verdict,
    z_score=exchange_result.z_score,
    metadata={"transferable": exchange_result.is_transferable}
)

print(f"Non-Repudiation Status: {exchange_result.status}")  # PASSED (TRANSFERABLE)
print(f"Chained Block Hash: {block_hash}")  # SHA3-256
```

---

## Engineering Roadmap & Milestone Verification

| Phase | Milestone Description | Modules | Status |
|:---|:---|:---|:---:|
| **Phases 01–05** | Quantum Teleportation, Pauli Bases & Bell Pairs | `quantum/state.py`, `quantum/bell.py` | ✅ Complete |
| **Phases 06–10** | QDS Protocol, Freshness Nonces & Attack Injectors | `security/signature.py`, `security/attacks.py` | ✅ Complete |
| **Phases 11–15** | Q-STAT Detection Engine & Projective Measurement | `security/detector.py`, `quantum/measure.py` | ✅ Complete |
| **Phases 16–20** | Physical Hardware Watchtowers (CHSH, Decoy, Trojan) | `security/chsh.py`, `security/decoy.py` | ✅ Complete |
| **Phases 21–25** | APD Blinding, MDI Relay, WDM & Mesh Routing | `security/blind.py`, `security/wdm.py` | ✅ Complete |
| **Phases 26–30** | Multi-Recipient Non-Repudiation & Audit Certificate | `security/multirecipient.py` | ✅ Complete |
| **Phases 31–35** | Enterprise SOC Integration (OASIS STIX 2.1 & ECS) | `analytics/soc.py`, `analytics/history.py` | ✅ Complete |
| **Phases 36–40** | 16-Tab Streamlit Cockpit & 8-Pillar Release Audit | `app.py`, `release_audit.py` | ✅ Complete |
| **Phases 41–45** | Decoupled Multi-Node Microservices (Ports 8000–8002) | `transport/`, `evaluation/` | ✅ Complete |
| **Phases 46–50** | Sequential Q-STAT (CUSUM / SPRT) & SHA3-256 Ledger | `security/sequential.py`, `analytics/history.py` | ✅ Complete |

---

## Citation

```bibtex
@software{jain2026qsentinel,
  author    = {Jain, Rakshit and Team QUANT},
  title     = {{Q-SENTINEL: Quantum-Inspired Cyber Threat Detection Framework}:
               Continuous Threat Surveillance and Non-Repudiation for Teleportation-Based Quantum Digital Signatures},
  year      = {2026},
  publisher = {GitHub},
  journal   = {GitHub repository},
  howpublished = {\url{https://github.com/Rakshit414/sih-quantum}},
  license   = {MIT},
  note      = {Smart India Hackathon 2026 (SIH-26141) - National Quantum Mission Track}
}
```

---

## References & Foundational Literature

### 1 · Quantum Protocols & Entanglement Foundations
1. Bennett, C. H., Brassard, G., Crépeau, C., Jozsa, R., Peres, A., & Wootters, W. K. (1993). *Teleporting an unknown quantum state via dual classical and Einstein-Podolsky-Rosen channels.* Physical Review Letters, 70(13), 1895. [doi:10.1103/PhysRevLett.70.1895](https://doi.org/10.1103/PhysRevLett.70.1895)
2. Gottesman, D., & Chuang, I. (2001). *Quantum digital signatures.* arXiv preprint. [quant-ph/0105032](https://arxiv.org/abs/quant-ph/0105032)
3. Ekert, A. K. (1991). *Quantum cryptography based on Bell’s theorem.* Physical Review Letters, 67(6), 661. [doi:10.1103/PhysRevLett.67.661](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.67.661)
4. Pironio, S., et al. (2010). *Random numbers certified by Bell’s theorem.* Nature, 464(7291), 1021–1024. [PubMed: 20393558](https://pubmed.ncbi.nlm.nih.gov/20393558/)

### 2 · Optical Hardware Security & National Defense Field Deployments
5. Gisin, N., Fasel, S., Kraus, B., Zbinden, H., & Ribordy, G. (2006). *Trojan-horse attacks on quantum-key-distribution systems.* Physical Review A, 73(2), 022320. [doi:10.1103/PhysRevA.73.022320](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.73.022320)
6. DRDO & IIT Delhi (2024). *Demonstration of Various Quantum Communication Technologies.* Ministry of Defence, Government of India Press Release. [drdo.gov.in](https://drdo.gov.in/drdo/en/documents/press-release/drdo-and-iit-delhi-organise-demonstration-various-quantum-communication)
7. DRDO & IIT Delhi (2025). *Free-Space Entanglement-Based Quantum Communication Demonstration.* Ministry of Defence, Government of India Press Release. [drdo.gov.in](https://drdo.gov.in/drdo/en/documents/press-release/drdo-iit-delhi-demonstrate-quantum-entanglement-based-free-space-quantum)
8. QNu Labs (Bengaluru). *Armos QKD System & Tropos QRNG Architecture.* Sovereign Indian Quantum Cryptography Whitepapers. [qnulabs.com](https://www.qnulabs.com/download-center)

### 3 · Sequential Statistics & Real-Time Threat Surveillance
9. Wald, A. (1945). *Sequential tests of statistical hypotheses.* The Annals of Mathematical Statistics, 16(2), 117–186. [doi:10.1214/aoms/1177731118](https://doi.org/10.1214/aoms/1177731118)
10. Page, E. S. (1954). *Continuous inspection schemes.* Biometrika, 41(1/2), 100–115. [doi:10.1093/biomet/41.1-2.100](https://doi.org/10.1093/biomet/41.1-2.100)
11. Lorden, G. (1971). *Procedures for reacting to a change in distribution.* The Annals of Mathematical Statistics, 42(6), 1897–1908. [Caltech Authors](https://authors.library.caltech.edu/records/n9ryc-0sr08)
12. Adams, R. P., & MacKay, D. J. (2007). *Bayesian online changepoint detection.* arXiv preprint. [arXiv:0710.3742](https://arxiv.org/abs/0710.3742)

### 4 · Cryptographic Standards & Post-Quantum Cryptography (PQC)
13. National Institute of Standards and Technology (NIST). (2015). *SHA-3 Standard: Permutation-Based Hash and Extendable-Output Functions.* FIPS PUB 202. [doi:10.6028/NIST.FIPS.202](https://doi.org/10.6028/NIST.FIPS.202)
14. National Institute of Standards and Technology (NIST). (2024). *Module-Lattice-Based Digital Signature Standard (ML-DSA).* FIPS PUB 204. [csrc.nist.gov](https://csrc.nist.gov/pubs/fips/204/final)
15. National Institute of Standards and Technology (NIST). (2024). *Stateless Hash-Based Digital Signature Standard (SLH-DSA).* FIPS PUB 205. [csrc.nist.gov](https://csrc.nist.gov/pubs/fips/205/final)

---

<div align="center">
<sub>MIT License · Team QUANT · Smart India Hackathon 2026 · National Quantum Mission (NQM) Track</sub>
</div>
