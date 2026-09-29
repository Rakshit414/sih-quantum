# 🛡️ Q-SENTINEL: Quantum-Inspired Cyber Threat Detection Framework

> **Problem Statement SIH26141**: Quantum-Inspired Cyber Threat Detection for Teleportation-based Quantum Digital Signature (QDS) Protocols.  
> **Key Architectural Constraint**: Zero reliance on Artificial Intelligence / Machine Learning. Provable Information-Theoretic & Statistical Security.  
> **Testing Status**: 130/130 Automated Tests Passing (100% Green) | Master Release Certified.  
> **Hardware Footprint**: 100% Classical CPU Commodity Execution — No Cryogenic QPU Hardware Required.

---

## 📌 Executive Overview

Current public-key cryptosystems (RSA, DSA, ECDSA) will be rendered insecure by Shor’s algorithm on cryptographically relevant quantum computers. While **Quantum Digital Signatures (QDS)** offer information-theoretic security rooted in the fundamental laws of quantum physics (the No-Cloning theorem and Measurement Disturbance), their physical implementations remain exposed to cyber-attacks over noisy channels.

**Q-Sentinel** is an auditable, quantum-inspired threat detection watchtower designed specifically for teleportation-based QDS systems. It continuously monitors quantum measurement statistics and classical transmission tokens in real time, detecting **forgery, impersonation, replay, and channel manipulation** without black-box ML models.

---

## 🔬 System Architecture & Distributed Network

```
[Signer Node: Alice]                               [Adversarial Relay: Eve :8001]                     [Verifier Sink: Bob :8002]
┌───────────────────────────┐                      ┌──────────────────────────────┐                   ┌───────────────────────────┐
│ 1. Encode message to      │                      │ Real HTTP Channel Intercept  │                   │ 5. Receive 2 classical    │
│    Pauli Eigenstates      │                      │ • Active Forgery (~50% err)  │                   │    bits (m₁, m₂)          │
│    {|0⟩, |1⟩, |+⟩, |-⟩,   │                      │ • Signer Impersonation       │                   │ 6. Unitary Pauli Correct  │
│     |+i⟩, |-i⟩}           │                      │ • Stale Replay (>60s TTL)    │                   │    U = Z^{m₁} X^{m₂}      │
│ 2. Bell-State Measurement │                      │ • Clean Fiber Noise (p₀=2.8%)│                   │ 7. Projective Measurement │
│    (BSM) with EPR Pair    │──────────┬──────────►│ • Optical Taps / Trojan Laser│──────────┬───────►│    over Born-rule trials  │
│ 3. Dispatches (m₁, m₂)    │          │           └──────────────────────────────┘          │        └─────────────┬─────────────┘
│    + Quantum Token Stream │          │                                                     │                      │
└───────────────────────────┘          │           ┌──────────────────────────────┐          │                      ▼
                                       └──────────►│  14 Physical Hardware        │◄─────────┘        ┌───────────────────────────┐
                                                   │  Watchtowers                 │                   │ 8. Sequential Q-STAT      │
                                                   │  (CHSH S>2, APD current,     │                   │    • Page CUSUM (h=8.5)   │
                                                   │   Decoy PNS, Raman WDM)      │                   │    • Wald SPRT Likelihood │
                                                   └──────────────────────────────┘                   │    • Sub-second stopping  │
                                                                                                      │    • Catch Forgery @ N=6  │
                                                                                                      │    • SHA3-256 Audit Chain │
                                                                                                      └───────────────────────────┘
```

---

## 📐 Mathematical Foundations

### 1. Quantum Teleportation Protocol
For an unknown signature state $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$ and shared Bell state $|\Phi^+\rangle_{23} = \frac{1}{\sqrt{2}}(|00\rangle+|11\rangle)$:
The composite 3-qubit state expands as:
$$|\Psi_{123}\rangle = \frac{1}{2}\sum_{m_1, m_2 \in \{0, 1\}} |m_1 m_2\rangle_{12} \otimes (X^{m_2} Z^{m_1}|\psi\rangle)_3$$
Alice measures qubits 1 and 2 in the Bell basis, yielding classical bits $(m_1, m_2)$. Bob applies the Pauli unitary correction:
$$U_{\text{corr}} = Z^{m_1} X^{m_2}$$
recovering $|\psi\rangle$ with exact fidelity $F = 1.0$.

### 2. Born-Rule Projective Measurement
Bob measures the received state against Alice's expected Pauli eigenbasis using projection operators $P_{\text{correct}} = |\psi_{\text{exp}}\rangle\langle\psi_{\text{exp}}|$ and $P_{\text{err}} = I - P_{\text{correct}}$.
- **Honest state**: $P_{\text{match}} = 1 - p_0$ (where $p_0 \approx 2.87\%$ is calibrated ambient channel decoherence).
- **Forgery / Impersonation**: Adversary guessing in a mutually unbiased basis experiences projective collapse with error rate:
  $$P(\text{err}) \approx 50\%$$

### 3. Sequential Q-STAT Decision Engine (Sub-Second Early Stopping)
1. **Wald's Sequential Probability Ratio Test (SPRT)**:
   $$\Lambda_n = \sum_{i=1}^n \log\frac{P(x_i \mid H_1)}{P(x_i \mid H_0)}$$
   - If $\Lambda_n \le B = -9.21$: Accept $H_0$ (**🟢 LEGITIMATE**, mint non-repudiation certificate).
   - If $\Lambda_n \ge A = +9.21$: Accept $H_1$ (**🔴 MALICIOUS**, abort link immediately at trial $N \approx 6$, saving **98.5%** of quantum bandwidth).
2. **Page's Cumulative Sum (CUSUM)**:
   $$S_n = \max(0, S_{n-1} + z_i - k)$$
   Instantly trips on intermittent micro-burst tampering if $S_n > h = 8.5$.
3. **Tamper-Evident SHA3-256 Audit Chain**:
   $$H_i = \text{SHA3-256}(H_{i-1} \parallel \text{Payload} \parallel \text{Timestamp} \parallel \text{Verdict})$$

---

## 🚀 Quick Start Guide (For Evaluators & Contributors)

### 1. Installation & Environment Setup
Clone the repository, switch to the production prototype branch, and install dependencies:

```bash
# 1. Clone the repository
git clone https://github.com/Rakshit414/sih-quantum.git
cd sih-quantum

# 2. Check out the prototype branch (or remain on main)
git checkout prototype-v2

# 3. Install Python requirements (Python 3.10+ / 3.14 supported)
python -m pip install -r requirements.txt
```

### 2. Run Automated Test Verification
Verify the complete 130-test suite across quantum foundations, physical watchtowers, sequential statistics, and AST boundaries:

```bash
python run_tests.py
```
> **Expected Result**: `130 passed in ~17s` (100% green pass rate).

---

### 3. Launching the Prototype

#### Option A: Quick-Start Standalone Mode (Single Terminal)
To immediately access the complete Streamlit SOC Cockpit with 16 functional tabs, interactive 3D Bloch spheres, Born-rule validations, and 1-Click Guided Attack Demos:

```bash
streamlit run app.py
```
*(Or use the cross-platform launcher: `python run_qsentinel.py`)*  
Open your browser at: **`http://localhost:8501`**.

---

#### Option B: Distributed Microservices Mode (Recommended for Full Evaluation)
To experience the true decoupled physical multi-node architecture (Alice Signer → Eve Channel Relay on Port 8001 → Bob Verifier Sink on Port 8002):

Open 3 terminal windows:

**Terminal 1 — Bob Verifier Sink (Port 8002)**:
```bash
python -m transport.bob_node
```
*(Starts the HTTP Verifier Sink daemon on port 8002 with Page CUSUM and Wald SPRT sequential processing)*

**Terminal 2 — Eve Channel Relay (Port 8001)**:
```bash
python -m transport.eve_channel
```
*(Starts the HTTP Adversarial Relay on port 8001 simulating fiber noise, state forgery, and impersonation)*

**Terminal 3 — Alice Signer & Streamlit SOC Dashboard**:
```bash
streamlit run app.py
```
*(Launches the Mission Control Dashboard at `http://localhost:8501`)*

> **Live Dashboard Integration**: Once all three terminals are running, the dashboard's **Live Microservices Monitor** will display green status badges (`EVE: ONLINE`, `BOB: ONLINE`). You can click the 1-click scenario toggles to inject attacks and watch Bob halt transmission trial-by-trial!

---

### 4. Additional Verification & Audit Tools

- **Run the Grand Unified Release Audit**:
  ```bash
  python run_audit.py
  ```
- **Run the Monte Carlo Performance Benchmark**:
  ```bash
  python benchmark.py --runs 50 --trials 50
  ```
- **Run Comparative Blind Red-Team Benchmark (V1 vs V2)**:
  ```bash
  python benchmark_v2.py
  ```

---

## 📊 Performance Benchmarks

Results across 500 Monte Carlo runs per scenario with $N = 400$ measurement trials ($p_0 = 2.87\%$):

| Metric | Measured Result | Benchmark Target | Status |
|---|---|---|---|
| **System Classification Accuracy** | **100.00%** | $\ge 98.00\%$ | ✅ PASS |
| **False Acceptance Rate (FAR)** | **0.00%** | $0.00\%$ | ✅ PASS |
| **False Rejection Rate (FRR)** | **0.00%** | $< 1.00\%$ | ✅ PASS |
| **Sequential Early Stopping (Forgery)** | **Trial 6** | $< 25\text{ trials}$ | ✅ PASS (98.5% bandwidth saved) |
| **Detection Latency** | **1.95 ms** | $< 15.0\text{ ms}$ | ✅ PASS |
| **Statistical Z-Separation ($\Delta z$)** | **+24.71 $\sigma$** | $> 10.0\text{ }\sigma$ | ✅ PASS |

### Attack Scenario Breakdown
- **Signature Forgery**: 100% caught ($z \approx +41.1\sigma$, Error $\approx 48.3\%$, SPRT stops at Trial 6).
- **Signer Impersonation**: 100% caught ($z \approx +26.9\sigma$, Error $\approx 32.6\%$, Mallory quarantined).
- **Replay Attack**: 100% intercepted by Freshness & Nonce Registry ($>60\text{s}$ TTL).
- **Channel Manipulation**: Smooth green $\to$ yellow $\to$ red progression via the physical disturbance slider.

---

## 📂 Repository Structure

```
sih-quantum/
├── app.py                      # Interactive Streamlit SOC Dashboard (16 Tabs)
├── run_qsentinel.py            # Cross-platform dashboard launcher
├── run_tests.py                # 130-test regression test suite runner
├── run_audit.py                # Grand Unified 8-Pillar Release Audit
├── benchmark.py                # Monte Carlo statistical benchmark
├── benchmark_v2.py             # Phase 45 comparative blind evaluation benchmark
├── requirements.txt            # Dependency manifest (Python 3.10+ / 3.14)
│
├── transport/                  # Decoupled Distributed Microservices (Phase 43)
│   ├── alice_node.py           # Alice Signer client with dynamic early stopping
│   ├── eve_channel.py          # Eve Relay daemon on HTTP port 8001
│   └── bob_node.py             # Bob Verifier daemon on HTTP port 8002
│
├── quantum/                    # Quantum Foundations Layer
│   ├── state.py                # Qubit states, Pauli matrices, tensor products
│   ├── bell.py                 # Bell states, partial trace, maximal entanglement
│   ├── teleport.py             # 3-qubit teleportation, BSM, Pauli corrections
│   ├── measure.py              # Born-rule projective measurement engine
│   ├── tomography.py           # Quantum state tomography & Stokes vectors
│   └── mesh.py                 # Quantum mesh routing & entanglement swapping
│
├── security/                   # Defense & Watchtower Layer (14 Optical Watchtowers)
│   ├── signature.py            # SHA-256 digest, Pauli keys, QDS tokens
│   ├── freshness.py            # Sliding time-window & nonce registry (anti-replay)
│   ├── attacks.py              # Forgery, impersonation, noise, replay injectors
│   ├── detector.py             # Classical Q-STAT engine (binomial test, z-score)
│   ├── sequential.py           # Sequential Q-STAT (CUSUM h=8.5, Wald SPRT A=9.21)
│   ├── calibrate.py            # Dynamic Noise Calibrator (Phase 47)
│   ├── chsh.py                 # CHSH Bell inequality non-locality watchtower
│   ├── decoy.py                # Decoy-state PNS watchtower
│   ├── trojan.py               # Trojan-horse laser & Lindblad memory detector
│   ├── blind.py                # APD detector blinding watchtower
│   ├── mdi.py                  # Measurement-Device-Independent (MDI) relay
│   ├── wdm.py                  # WDM co-propagation & Raman scattering filter
│   └── multirecipient.py       # Non-repudiation cross-verification & certificates
│
├── analytics/                  # Persistence & Enterprise SIEM Integration
│   ├── metrics.py              # Statistical confusion matrix, FAR, FRR
│   ├── history.py              # SQLite ACID-compliant persistence & SHA3-256 chain
│   └── soc.py                  # OASIS STIX 2.1 JSON & Elastic Common Schema (ECS)
│
├── docs/                       # Executive Presentation & Defense Assets
│   ├── presentation_deck_v2.html # 16:9 Widescreen visual slide deck
│   ├── SLIDE_WORKFLOW_AND_TECH_STACK.md # Copy-paste prompt & slide breakdown
│   ├── VIDEO_DEMO_SCRIPT_SIH26141.md    # Full government-ready video demo script
│   ├── JUDGE_DEFENSE_MANUAL.md          # Defense manual, Q&A, and math proofs
│   └── NQM_EXECUTIVE_WHITEPAPER.md      # National Quantum Mission formal whitepaper
│
└── tests/                      # 130 Automated Tests (100% Pass Rate)
    ├── test_quantum.py         # Quantum state & Pauli tests
    ├── test_teleport.py        # Bell teleportation fidelity tests
    ├── test_security.py        # Attack injection & detection tests
    ├── test_sequential.py      # CUSUM & SPRT early-stopping tests
    ├── test_import_boundary.py # AST import isolation boundary invariants
    └── test_release_audit.py   # Master release freeze & manifest tests
```

---

## 🏆 Presentation & Evaluation Resources

- 📽️ **Interactive Visual Presentation Slides (16:9)**: Open [`docs/presentation_deck_v2.html`](docs/presentation_deck_v2.html) in any web browser.
- 📋 **AI Presentation Prompt Guide (ChatGPT / Claude / Gamma)**: Review [`docs/SLIDE_WORKFLOW_AND_TECH_STACK.md`](docs/SLIDE_WORKFLOW_AND_TECH_STACK.md).
- 🎬 **Video Walkthrough Demonstration Script**: Review [`docs/VIDEO_DEMO_SCRIPT_SIH26141.md`](docs/VIDEO_DEMO_SCRIPT_SIH26141.md).
- 🛡️ **Judge Defense & Q&A Manual**: Review [`docs/JUDGE_DEFENSE_MANUAL.md`](docs/JUDGE_DEFENSE_MANUAL.md).

---

## 🏛️ Innovation & Key Differentiators

1. **Sub-Second Early Stopping**: Page's CUSUM and Wald's SPRT cut transmission in **6 trials** during an attack, saving **98.5% of quantum optical bandwidth**.
2. **Explainable-by-Construction (Zero AI/ML)**: Strictly complies with the "No AI/ML" constraint. Every alert is mathematically auditable down to a deterministic statistical equation.
3. **Decoupled Microservice Architecture**: Physical separation of Alice, Eve (:8001), and Bob (:8002) over independent HTTP sockets with strict AST import isolation.
4. **Tamper-Evident SHA3-256 Audit Chaining**: Zero blockchain overhead while cryptographically preventing log modification or repudiation disputes.
5. **100% Classical Execution**: Zero cryogenic QPU hardware needed—runs with sub-2ms latency on standard commodity CPUs.
