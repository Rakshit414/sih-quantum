<div align="center">

# Q-SENTINEL: Quantum-Inspired Cyber Threat Detection Framework

**Continuous Threat Surveillance, Sub-Second Early Stopping & Non-Repudiation for Teleportation-Based Quantum Digital Signatures**

[![CI](https://github.com/Rakshit414/sih-quantum/actions/workflows/ci.yml/badge.svg)](https://github.com/Rakshit414/sih-quantum/actions/workflows/ci.yml)
[![Tests](https://img.shields.io/badge/tests-130%20passed-brightgreen.svg)](tests/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%20%7C%203.14-blue.svg)](https://www.python.org/downloads/)
[![Problem Statement](https://img.shields.io/badge/SIH--2026-SIH26141-orange.svg)](https://www.sih.gov.in/)
[![Mission Track](https://img.shields.io/badge/Mission-National%20Quantum%20Mission%20(NQM)-purple.svg)](docs/NQM_EXECUTIVE_WHITEPAPER.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Zero ML](https://img.shields.io/badge/AI%2FML-Zero%20Black--Box%20(Deterministic)-success.svg)](docs/ARCHITECTURE.md)

*Team QUANT · Smart India Hackathon 2026 · Grand Finale Production Release*

</div>

---

## Abstract

Current public-key cryptosystems (RSA, DSA, ECDSA) are fundamentally vulnerable to polynomial-time factorization via Shor’s algorithm on cryptographically relevant quantum hardware. While **Quantum Digital Signatures (QDS)** provide theoretical security guaranteed by the No-Cloning Theorem and Measurement Disturbance, their physical implementations over lossy optical fibers remain exposed to cyber-attacks: **cryptographic state forgery, signer impersonation, stale token replay, and optical side-channel tapping**.

**Q-Sentinel** introduces an auditable, quantum-inspired security framework specifically engineered for entanglement-assisted, teleportation-based QDS protocols. It transforms projective measurement streams into a continuous, real-time threat surveillance telemetry pipeline. Operating entirely on standard commodity hardware, Q-Sentinel couples **14 Optical Hardware Watchtowers** with a **Sequential Q-STAT Engine** (Page's CUSUM and Wald's Sequential Probability Ratio Test) to intercept attacks trial-by-trial.

> **A note on architectural constraint (Zero AI/ML).** Per the strict requirements of problem statement **SIH26141**, Q-Sentinel rejects black-box neural networks, heuristic clustering, and generative models. Deep learning models are susceptible to adversarial evasion and cannot provide court-admissible security guarantees. Instead, all detection thresholds and security scores in Q-Sentinel are **100% mathematically deterministic**, derived from closed-form binomial distributions, information-theoretic bounds, and sequential hypothesis testing.

**Headline Result.** During active cryptographic forgery ($\approx 50\%$ projective error rate), Q-Sentinel's sequential engine achieves definitive detection at **Trial 6** ($\text{SPRT LLR} \ge +9.21$, joint $\alpha = 10^{-4}$), halting the quantum optical transmission and **saving 98.5% of quantum channel bandwidth** compared to classical batch protocols. Over Monte Carlo benchmarking, the framework demonstrates **0.00% False Acceptance Rate (FAR)** ($0/2000$, 95% Wilson CI: $[0.00\%, 0.19\%]$), **0.00% Hard False Rejection Rate (FRR)** ($0/500$, 95% Wilson CI: $[0.00\%, 0.74\%]$), and a statistical Z-separation of **$+33.26\sigma$** against baseline channel noise.

**Cryptographic Non-Repudiation.** Using a multi-recipient quantum cross-verification exchange (Bob vs. Charlie), Q-Sentinel guarantees signature transferability (discrepancy rate $= 0.0\%$, $z = -0.50\sigma$) and seals all session events in an immutable, **tamper-evident SHA3-256 hash-chained audit ledger** with zero blockchain latency.

---

## Highlights

- 🎯 **100% Deterministic Detection** — Mathematically closed-form detection across state forgery ($z = +57.56\sigma$), signer impersonation ($z = +35.08\sigma$), stale replay ($>60\text{s}$ TTL), and optical eavesdropping.
- ⚡ **Sub-Second Early Stopping** — Wald's SPRT ($A = +9.21, B = -9.21$) and Page's CUSUM ($h = 8.5$) catch tampering at **Trial 6**, slashing Average Sample Number (ASN) by **98.5%**.
- 🛡️ **14 Optical Hardware Watchtowers** — Real-time surveillance of CHSH Bell non-locality ($S > 2$), Decoy-State Photon Number Splitting (PNS), APD detector blinding, Raman scattering, and Trojan-horse lasers ($<0.01\,\mu\text{W}$).
- 🌐 **Distributed Microservices Mesh** — Decoupled physical multi-node architecture across Alice (Signer), Eve (Relay on Port 8001), and Bob (Sink on Port 8002) with strict AST import boundary isolation.
- 🔐 **Tamper-Evident SHA3-256 Chaining** — Cryptographic forward hash pointers ($H_i = \text{SHA3-256}(H_{i-1} \parallel \text{Payload} \parallel \text{Verdict})$) guarantee court-admissible audit logs without blockchain overhead.
- 💻 **100% Classical Execution** — Pure vectorized linear algebra in Python/NumPy/SciPy. Executes with sub-2ms latency on standard commodity CPUs without cryogenic QPUs.
- ✅ **Grand-Finale Certified** — **130/130 automated unit, integration, and stress tests passing (100% green)**, verified against an 8-pillar production freeze audit.

---

## Empirical Benchmarks & Statistical Performance

### 1 · Threat Classification Performance

Performance measured across 500 Monte Carlo runs per scenario with $N = 400$ projective measurement trials ($8 \text{ tokens} \times 50 \text{ trials/token}$) under calibrated optical fiber noise floor $p_0 = 3.00\%$:

$$\sigma_0 = \sqrt{\frac{p_0(1 - p_0)}{N}} = \sqrt{\frac{0.03 \times 0.97}{400}} \approx 0.008529, \quad z = \frac{\hat{e} - p_0}{\sigma_0}$$

<div align="center">

| Operational Scenario | Observed Error Rate ($\hat{e}$) | Anomaly Score ($z$-Score) | SPRT Decision Trial | Bandwidth Saved | Detection Verdict |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Clean Fiber Baseline** | $2.85\% \pm 0.4\%$ | $-0.18\sigma$ | Trial 400 (Exhaustive) | Baseline | 🟢 **LEGITIMATE** |
| **State Forgery Attack** | $52.09\% \pm 1.2\%$ | **$+57.56\sigma$** | **Trial 6** | **98.5%** | 🔴 **MALICIOUS** |
| **Signer Impersonation** | $32.92\% \pm 1.5\%$ | **$+35.08\sigma$** | **Trial 18** | **95.5%** | 🔴 **MALICIOUS** |
| **Stale Replay Attack** | N/A (Expired Nonce) | $\infty$ (Temporal Failure) | Instantaneous | 100.0% | 🔴 **MALICIOUS** |
| **Channel Noise / Jamming** | $37.02\% \pm 1.8\%$ | **$+39.89\sigma$** | **Trial 14** | **96.5%** | 🔴 **MALICIOUS** |
| **Optical Tap / Trojan Laser**| $8.50\% \pm 0.8\%$ | $+6.45\sigma$ | Trial 42 | 89.5% | 🟡 **SUSPICIOUS** |

</div>

#### Statistical Error Rates & 95% Wilson Confidence Intervals:
- **False Acceptance Rate (FAR)**: **0.00%** ($0/2000$, Wilson 95% CI: $[0.00\%, 0.19\%]$). Attack states ($e \ge 32.9\%$) produce $z \ge +35\sigma$, rendering false acceptance mathematically negligible ($p < 10^{-200}$).
- **Hard False Rejection Rate (FRR to MALICIOUS)**: **0.00%** ($0/500$, Wilson 95% CI: $[0.00\%, 0.74\%]$). Requires $z \ge 4.0$, which under $H_0$ occurs with theoretical probability $P(Z \ge 4.0) \approx 3.17 \times 10^{-5}$.
- **Honest Warning Rate (SUSPICIOUS)**: **~2.28%** nominal theoretical $\alpha$ for $2.0 \le z < 4.0$ (observed $\approx 1$ in 50 runs), which triggers a non-disruptive pilot-frame recalibration rather than hard transaction abort.

---

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
  • Threat Scenarios: Clean Noise (3.0%) | Forgery (~50%) | Impersonation | Replay (>60s TTL).
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

Detailed architectural diagrams and state flow: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).  
Formal adversary models and security bounds: [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md).  

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

### Docker Containerization

Run Q-Sentinel in an isolated, non-root Linux container:

```bash
# Build Docker image
docker build -t qsentinel:latest .

# Run container (headless web dashboard on port 8501)
docker run -p 8501:8501 qsentinel:latest

# Or launch multi-container stack via Docker Compose
docker compose up
```

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
*(Or cross-platform launcher: `python run_qsentinel.py`, Windows script: `scripts/run_qsentinel.bat`, Linux script: `scripts/run_qsentinel.sh`)*  
Open your browser at **`http://localhost:8501`**.

---

#### Option B: Distributed Microservices Mode (Decoupled Multi-Process)
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

# Execute Monte Carlo performance benchmarking (50 runs × 50 trials, reproducible seed)
python benchmark.py --runs 50 --trials 50 --seed 42

# Execute full 500-iteration publication benchmark
python benchmark.py --runs 500 --seed 42

# Execute comparative blind red-team evaluation (V1 vs V2 Sequential)
python benchmark_v2.py
```
</details>

---

## Limitations & Operational Scope

1. **Optical Fiber Attenuation & Range**: In unamplified standard single-mode optical fiber ($\approx 0.2\,\text{dB/km}$ attenuation at 1550 nm), single-photon quantum communication is physically distance-bounded ($\approx 100\text{--}150\,\text{km}$) without trusted intermediate nodes or quantum repeaters.
2. **Classical Channel Availability**: Q-Sentinel assumes the classical communication channel provides availability; complete denial-of-service (such as physical fiber cuts) halts transactions securely (fail-closed) without compromising unforgeability.
3. **Finite Block Length Effects**: Asymptotic security bounds require finite-size statistical corrections for short signature lengths, modeled via Serfling's inequality in `security/finite.py`.
4. **Simulation Scope**: This codebase provides a high-fidelity numerical state-vector and density-matrix quantum physics engine executing on classical CPUs. Direct physical fiber deployments require hardware DAC/ADC drivers and single-photon avalanche photodiode (SPAD) instruments.

---

## Repository Structure

```
sih-quantum/
├── .github/workflows/ci.yml    ← Multi-Python (3.10-3.12) GitHub Actions CI workflow
├── app.py                      ← Interactive Streamlit SOC Mission Control (16 Tabs)
├── run_qsentinel.py            ← Cross-platform single-command dashboard launcher
├── run_tests.py                ← 130-test regression test suite runner
├── run_audit.py                ← Grand Unified 8-Pillar Release Audit runner
├── package_submission.py       ← Self-healing automated release packaging engine
├── benchmark.py                ← Monte Carlo statistical performance benchmark
├── benchmark_v2.py             ← Phase 45 comparative blind evaluation benchmark
├── requirements.txt            ← Dependency manifest (NumPy, SciPy, Streamlit, Plotly)
├── Dockerfile                  ← Production multi-stage Docker container specification
├── docker-compose.yml          ← Orchestrated container stack configuration
├── LICENSE                     ← Open source MIT License
│
├── scripts/                    ← One-click execution wrappers
│   ├── run_qsentinel.bat       ← Windows one-click dashboard launcher
│   ├── run_tests.bat           ← Windows automated test suite runner
│   ├── run_audit.bat           ← Windows master release audit runner
│   └── run_qsentinel.sh        ← Linux / macOS shell execution launcher
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
│   ├── calibrate.py            ← Dynamic Noise Calibrator (pilot-frame tracking)
│   ├── chsh.py                 ← CHSH Bell inequality non-locality watchtower (S > 2)
│   ├── decoy.py                ← Decoy-state Poissonian photon number splitting (PNS) detector
│   ├── trojan.py               ← Trojan-horse laser & Lindblad quantum memory decoherence filter
│   ├── blind.py                ← Avalanche Photodiode (APD) detector blinding watchtower
│   ├── mdi.py                  ← Measurement-Device-Independent (MDI) untrusted relay mode
│   ├── wdm.py                  ← WDM co-propagation & Raman scattering anti-jamming filter
│   └── multirecipient.py       ← Multi-party non-repudiation cross-verification & certificate minting
│
├── analytics/                  ← Telemetry Persistence & Enterprise SIEM Integration
│   ├── metrics.py              ← Confusion matrix, FAR, FRR, Wilson CI, accuracy, latency
│   ├── history.py              ← SQLite ACID datastore with SHA3-256 hash chaining
│   └── soc.py                  ← OASIS STIX 2.1 JSON threat intelligence & Elastic Common Schema (ECS)
│
├── docs/                       ← Scientific Whitepapers & Formal Defense Assets
│   ├── THREAT_MODEL.md                  ← Formal adversary capabilities & attack bounds
│   ├── ARCHITECTURE.md                  ← 4-tier architectural specification & formulas
│   ├── JUDGE_DEFENSE_MANUAL.md          ← Evaluator defense rationale & math whiteboard guide
│   ├── NQM_EXECUTIVE_WHITEPAPER.md      ← National Quantum Mission technical paper
│   ├── SIH26141_FINAL_PITCH_DECK.md     ← 12-slide executive hackathon presentation deck
│   ├── RELEASE_MANIFEST.md              ← Master SHA-256 release integrity manifest
│   └── RELEASE_AUDIT_CERTIFICATE.json   ← Cryptographic release audit certificate
│
└── tests/                      ← Automated Test Suite (130 Tests, 100% Pass Rate)
    ├── test_quantum.py         ← Quantum foundations & Pauli eigenbasis tests
    ├── test_teleport.py        ← Teleportation fidelity & Pauli correction tests
    ├── test_security.py        ← Attack injection & Q-STAT detection tests
    ├── test_sequential.py      ← Page CUSUM & Wald SPRT early stopping tests
    ├── test_deployment.py      ← Launchers, Docker, and packaging verification tests
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

# Initialize sequential surveillance engine (Noise floor p0=3.0%, Forgery p1=50%)
config = SequentialHypothesisConfig(p0=0.03, p1=0.50, alpha=1e-4, beta=1e-4)
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
from analytics.history import TelemetryStore

# Verify signature transferability between Bob and Charlie
verifier = MultiRecipientCrossVerifier()
exchange_result = verifier.verify_transferability(
    bob_tokens=bob_received_tokens,
    charlie_tokens=charlie_tokens,
    claimed_signer="Alice"
)

# Store event with immutable SHA3-256 hash chaining
db = TelemetryStore()
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

Machine-readable metadata: [`CITATION.cff`](CITATION.cff).

---

## References & Foundational Literature

### 1 · Quantum Protocols & Signature Foundations
1. **Gottesman, D., & Chuang, I. (2001).** *Quantum Digital Signatures.* arXiv preprint. [arXiv:quant-ph/0105032](https://arxiv.org/abs/quant-ph/0105032)  
   *(Foundational protocol for quantum public keys, Pauli eigenstate verification, and information-theoretic unforgeability; implemented in `security/signature.py`).*
2. **Bennett, C. H., Brassard, G., Crépeau, C., Jozsa, R., Peres, A., & Wootters, W. K. (1993).** *Teleporting an unknown quantum state via dual classical and Einstein-Podolsky-Rosen channels.* Physical Review Letters, 70(13), 1895. [Semantic Scholar Free PDF](https://www.semanticscholar.org/paper/Teleporting-an-unknown-quantum-state-via-dual-and-Bennett-Brassard/e0f06f52e5058fc94c34a2c2626e2e9c1db16a03) | [doi:10.1103/PhysRevLett.70.1895](https://doi.org/10.1103/PhysRevLett.70.1895)  
   *(Foundational 3-qubit teleportation, Bell-state measurement, and Pauli corrections $U = Z^{m_1} X^{m_2}$; implemented in `quantum/teleport.py`).*
3. **Ekert, A. K. (1991).** *Quantum cryptography based on Bell’s theorem.* Physical Review Letters, 67(6), 661. [Semantic Scholar Free PDF](https://www.semanticscholar.org/paper/Quantum-cryptography-based-on-Bell's-theorem.-Ekert/7f08d6d539556a38618e792c90c749b5c306d860) | [doi:10.1103/PhysRevLett.67.661](https://doi.org/10.1103/PhysRevLett.67.661)  
   *(Entanglement-based security, EPR Bell pairs $|\Phi^+\rangle$, and CHSH non-locality verification; implemented in `quantum/bell.py` and `security/chsh.py`).*

### 2 · Optical Hardware Security & Physical Watchtowers
4. **Gisin, N., Fasel, S., Kraus, B., Zbinden, H., & Ribordy, G. (2006).** *Trojan-horse attacks on quantum-key-distribution systems.* Physical Review A, 73(2), 022320. [Semantic Scholar Free PDF](https://www.semanticscholar.org/paper/Trojan-horse-attacks-on-quantum-key-distribution-Gisin-Fasel/748880628e9d3e8e390c50d32ca4a3ff0d6bb6c4) | [doi:10.1103/PhysRevA.73.022320](https://doi.org/10.1103/PhysRevA.73.022320)  
   *(Multi-spectral optical filtering, back-reflection power thresholds $<0.01\,\mu\text{W}$, and Trojan-horse laser countermeasures; implemented in `security/trojan.py`).*
5. **Lydersen, L., Wiechers, C., Wittmann, C., Elser, D., Skaar, J., & Makarov, V. (2010).** *Hacking commercial quantum cryptography systems by tailored bright illumination.* Nature Photonics, 4, 686–689. [arXiv:1008.4593](https://arxiv.org/abs/1008.4593)  
   *(Avalanche Photodiode / APD detector blinding and Geiger-mode saturation watchtower; implemented in `security/blind.py`).*
6. **Lo, H.-K., Ma, X., & Chen, K. (2005).** *Decoy state quantum key distribution.* Physical Review Letters, 94(23), 230501. [arXiv:quant-ph/0411047](https://arxiv.org/abs/quant-ph/0411047)  
   *(Multi-intensity decoy pulse statistics against photon number splitting / PNS attacks; implemented in `security/decoy.py`).*
7. **Lo, H.-K., Curty, M., & Qi, B. (2012).** *Measurement-device-independent quantum key distribution.* Physical Review Letters, 108(13), 130503. [arXiv:1109.1473](https://arxiv.org/abs/1109.1473)  
   *(Measurement-Device-Independent / MDI untrusted relay architecture eliminating detector side-channels; implemented in `security/mdi.py`).*

### 3 · Sequential Statistics & Real-Time Threat Surveillance
8. **Wald, A. (1945).** *Sequential tests of statistical hypotheses.* The Annals of Mathematical Statistics, 16(2), 117–186. [Project Euclid Open Access](https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-16/issue-2/Sequential-Tests-of-Statistical-Hypotheses/10.1214/aoms/1177731118.full) | [doi:10.1214/aoms/1177731118](https://doi.org/10.1214/aoms/1177731118)  
   *(Wald's Sequential Probability Ratio Test / SPRT enabling sub-second early stopping at Trial 6 with 98.5% channel bandwidth savings; implemented in `security/sequential.py`).*
9. **Page, E. S. (1954).** *Continuous inspection schemes.* Biometrika, 41(1/2), 100–115. [Semantic Scholar Free Summary](https://www.semanticscholar.org/paper/Continuous-Inspection-Schemes-Page/33fcb7496695b281f62bca6ad457c15433297a76) | [doi:10.1093/biomet/41.1-2.100](https://doi.org/10.1093/biomet/41.1-2.100)  
   *(Cumulative Sum / CUSUM control chart with $h=8.5, k=0.18$ for catching micro-burst and intermittent tampering; implemented in `security/sequential.py`).*

### 4 · Cryptographic Integrity Standards & National Deployments
10. **National Institute of Standards and Technology (NIST). (2015).** *SHA-3 Standard: Permutation-Based Hash and Extendable-Output Functions.* FIPS PUB 202. [NIST CSRC Open Access](https://csrc.nist.gov/pubs/fips/202/final) | [doi:10.6028/NIST.FIPS.202](https://doi.org/10.6028/NIST.FIPS.202)  
    *(Federal standard for immutable SHA3-256 hash-chaining audit ledgers and HMAC-SHA3-512 anti-replay tokens; implemented in `analytics/history.py` and `security/freshness.py`).*
11. **Defence Research and Development Organisation (DRDO) & IIT Delhi (2024 & 2025).** *Demonstrations of Sovereign Quantum Communication Technologies & Free-Space Entanglement.* Ministry of Defence, Government of India. [DRDO Press Release (2024)](https://drdo.gov.in/drdo/en/documents/press-release/drdo-and-iit-delhi-organise-demonstration-various-quantum-communication) | [DRDO Press Release (2025)](https://drdo.gov.in/drdo/en/documents/press-release/drdo-iit-delhi-demonstrate-quantum-entanglement-based-free-space-quantum)  
    *(Indian sovereign defense field deployments aligning with Problem Statement SIH-26141 under the National Quantum Mission).*
12. **QNu Labs (Bengaluru).** *Armos QKD System & Tropos QRNG Architecture.* Sovereign Indian Quantum Cryptography Deployments. [QNu Labs Official Portal](https://www.qnulabs.com/)  
    *(Commercial Indian hardware integration reference for physical single-photon detectors and quantum entropy sources).*

---

<div align="center">
<sub>MIT License · Team QUANT · Smart India Hackathon 2026 · National Quantum Mission (NQM) Track</sub>
</div>
