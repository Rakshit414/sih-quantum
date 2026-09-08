# 🛡️ Q-SENTINEL: Quantum-Inspired Cyber Threat Detection Framework

> **Problem Statement SIH26141**: Quantum-Inspired Cyber Threat Detection for Teleportation-based Quantum Digital Signature (QDS) Protocols.  
> **Key Architectural Constraint**: Zero reliance on Artificial Intelligence / Machine Learning. Provable Information-Theoretic & Statistical Security.

---

## 📌 Executive Overview

Current public-key cryptosystems (RSA, DSA, ECDSA) will be rendered insecure by Shor’s algorithm on cryptographically relevant quantum computers. While **Quantum Digital Signatures (QDS)** offer information-theoretic security rooted in the fundamental laws of quantum physics (the No-Cloning theorem and Measurement Disturbance), their physical implementations remain exposed to cyber-attacks over noisy channels.

**Q-Sentinel** is an auditable, quantum-inspired threat detection watchtower designed specifically for teleportation-based QDS systems. It continuously monitors quantum measurement statistics and classical transmission tokens in real time, detecting **forgery, impersonation, replay, and channel manipulation** without black-box ML models.

---

## 🔬 System Architecture

```
[Signer: Alice]                              [Simulated Quantum Channel]                           [Verifier: Bob]
┌───────────────────────────┐                ┌──────────────────────────┐                ┌───────────────────────────┐
│ 1. Encode message to      │                │ 2. Shared Bell Pair      │                │ 5. Receive 2 classical    │
│    Pauli Eigenstates      │                │    |Φ⁺⟩ = (|00⟩+|11⟩)/√2 │                │    bits (b₁, b₂)          │
│    {|0⟩, |1⟩, |+⟩, |-⟩}   │                └────────────┬─────────────┘                │ 6. Apply Pauli Correction │
│ 3. Bell-State Measurement │                             │                              │    U = Z^{b₁} X^{b₂}      │
│    (BSM) on Qubit + Pair  │                             ▼                              │ 7. Projective Measurement │
│ 4. Transmit 2 classical   │───────────────►[ Classical Channel (b₁, b₂) ]─────────────►│    over N Born-rule trials│
│    correction bits        │                             │                              └─────────────┬─────────────┘
└───────────────────────────┘                             ▼                                            │
                                              [ Adversarial Surface ]                                  ▼
                                              • Forgery (fake state)                     ┌───────────────────────────┐
                                              • Impersonation (wrong ID)                 │ 8. Q-STAT Engine          │
                                              • Replay (stale token)                     │    Exact Binomial Test    │
                                              • Channel Noise (bit/phase flip)           │    Z-Score & Confidence   │
                                                                                         │    LEGITIMATE /           │
                                                                                         │    SUSPICIOUS / MALICIOUS │
                                                                                         └───────────────────────────┘
```

---

## 📐 Mathematical Foundations

### 1. Quantum Teleportation Protocol
For an unknown signature state $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$ and shared Bell state $|\Phi^+\rangle_{23} = \frac{1}{\sqrt{2}}(|00\rangle+|11\rangle)$:
The composite 3-qubit state expands as:
$$|\Psi_{123}\rangle = \frac{1}{2}\sum_{b_1, b_2 \in \{0, 1\}} |b_1 b_2\rangle_{12} \otimes (X^{b_2} Z^{b_1}|\psi\rangle)_3$$
Alice measures qubits 1 and 2 in the Bell basis, yielding classical bits $(b_1, b_2)$. Bob applies the Pauli unitary correction:
$$U_{\text{corr}} = Z^{b_1} X^{b_2}$$
recovering $|\psi\rangle$ with exact fidelity $F = 1.0$.

### 2. Born-Rule Projective Measurement
Bob measures the received state against Alice's expected Pauli eigenbasis using projection operators $P_{\text{correct}} = |\psi_{\text{exp}}\rangle\langle\psi_{\text{exp}}|$ and $P_{\text{err}} = I - P_{\text{correct}}$.
- Honest state: $P_{\text{match}} = 1 - p_0$ (where $p_0$ is ambient channel decoherence).
- Forgery / Impersonation: Adversary guessing in a mutually unbiased basis experiences projective collapse with error rate:
  $$P(\text{err}) \approx 50\%$$

### 3. Q-STAT Statistical Decision Engine
Given $n_1$ error counts out of $N$ projective measurement trials:
1. **Empirical Error Rate**: $\hat{e} = \frac{n_1}{N}$
2. **Exact Binomial Hypothesis Test**:
   $$p\text{-value} = \sum_{k=n_1}^N \binom{N}{k} p_0^k (1 - p_0)^{N-k}$$
3. **Standardized Anomaly Score ($z$-Score)**:
   $$\sigma_0 = \sqrt{\frac{p_0(1 - p_0)}{N}}, \quad z = \frac{\hat{e} - p_0}{\sigma_0}$$
4. **Three-Tier Classification**:
   - $z < 2.0$: **🟢 LEGITIMATE** (Standard 2-$\sigma$ noise boundary, 95% confidence).
   - $2.0 \le z < 4.0$: **🟡 SUSPICIOUS** (Channel disturbance / minor tampering, requires audit).
   - $z \ge 4.0$: **🔴 MALICIOUS** (Active attack detected with $>99.99\%$ certainty).

---

## 🚀 Quick Start Guide

### 1. Installation
Clone the repository and install requirements:
```bash
git clone https://github.com/your-team/q-sentinel.git
cd sih
pip install -r requirements.txt
```

### 2. Launch the SOC Dashboard
Start the interactive Streamlit dashboard:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### 3. Run Automated Tests
Execute the 23 unit tests verifying state vectors, Bell states, teleportation fidelity, and attack models:
```bash
python -m pytest tests/
```

### 4. Run the Performance Benchmark
Execute the Monte Carlo benchmark runner:
```bash
python benchmark.py --runs 50 --trials 50
```

---

## 📊 Performance Benchmarks

Results across 500 Monte Carlo runs per scenario with $N = 400$ measurement trials ($p_0 = 3.0\%$):

| Metric | Measured Result | Benchmark Target | Status |
|---|---|---|---|
| **System Classification Accuracy** | **100.00%** | $\ge 98.00\%$ | ✅ PASS |
| **False Acceptance Rate (FAR)** | **0.00%** | $0.00\%$ | ✅ PASS |
| **False Rejection Rate (FRR)** | **0.00%** | $< 1.00\%$ | ✅ PASS |
| **Detection Latency** | **1.95 ms** | $< 15.0\text{ ms}$ | ✅ PASS |
| **Statistical Z-Separation ($\Delta z$)** | **+24.71 $\sigma$** | $> 10.0\text{ }\sigma$ | ✅ PASS |

### Attack Scenario Breakdown
- **Signature Forgery**: 100% caught ($z \approx +41.1\sigma$, Error $\approx 48.3\%$).
- **Signer Impersonation**: 100% caught ($z \approx +26.9\sigma$, Error $\approx 32.6\%$).
- **Replay Attack**: 100% intercepted by Freshness & Nonce Registry.
- **Channel Manipulation**: Seamless progression Green $\to$ Yellow $\to$ Red via the disturbance slider.

---

## 📂 Repository Structure

```
sih/
├── app.py                      # Interactive Streamlit SOC Dashboard
├── benchmark.py                # Formal CLI benchmark runner
├── requirements.txt            # Dependency manifest
├── SIH26141_QSentinel_Plan.md  # Original problem analysis & battle plan
├── docs/
│   └── JUDGE_DEFENSE_MANUAL.md # Presentation pitches, formulas, & judge Q&A
├── quantum/
│   ├── __init__.py
│   ├── state.py                # Qubit states, Pauli matrices, tensor products
│   ├── bell.py                 # Bell states, partial trace, maximal entanglement
│   ├── teleport.py             # 3-qubit teleportation, BSM, Pauli corrections
│   └── measure.py              # Born-rule projective measurement engine
├── security/
│   ├── __init__.py
│   ├── signature.py            # SHA-256 digest, Pauli keys, QDS tokens
│   ├── freshness.py            # Sliding time-window & nonce registry (anti-replay)
│   ├── attacks.py              # Forgery, impersonation, noise, replay injectors
│   └── detector.py             # Q-STAT engine (binomial test, z-score, thresholds)
├── analytics/
│   ├── __init__.py
│   ├── metrics.py              # FAR, FRR, accuracy, latency, confusion matrix
│   └── history.py              # SQLite audit persistence datastore
└── tests/
    ├── __init__.py
    ├── test_quantum.py         # Unit tests for quantum foundations
    ├── test_teleport.py        # Unit tests for Bell states & teleportation
    ├── test_security.py        # Unit tests for attacks & detection
    └── test_analytics.py       # Unit tests for history & benchmarks
```

---

## 🏆 Innovation & Key Differentiators

1. **Continuous Telemetry vs Static Verification**: Rather than treating signature verification as a single binary pass/fail check, Q-Sentinel converts quantum projective measurements into a continuous security telemetry stream.
2. **Explainable-by-Construction**: Strictly complies with the "No AI/ML" constraint. Every alert is mathematically auditable down to a single closed-form binomial equation.
3. **Attack-Specific Fingerprinting**: Differentiates between physical channel degradation (smooth $z$-score rise), active cryptographic forgery ($\approx 50\%$ basis collapse), and replay attacks (temporal metadata failure).
4. **Sub-2 Millisecond Verification**: Optimized vectorized linear algebra ensures real-time operational feasibility for high-throughput financial and defense applications.
