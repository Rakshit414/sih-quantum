# Q-SENTINEL: Quantum-Inspired Cyber Threat Detection Framework for Teleportation-Based QDS

## 1. Executive Summary & Problem Formulation

### 1.1 The Critical Threat Landscape
Modern public-key cryptography (RSA, DSA, ECDSA) relies on mathematical hardness assumptions—specifically integer factorization and the discrete logarithm problem. Shor’s algorithm running on a cryptographically relevant quantum computer (CRQC) solves these in polynomial time, rendering current digital signature infrastructures obsolete and vulnerable to "harvest now, decrypt/forge later" strategies.

### 1.2 The Quantum Digital Signature (QDS) Paradigm
Quantum Digital Signatures (QDS) provide **information-theoretic security** rooted in the fundamental laws of quantum physics:
1. **The No-Cloning Theorem**: An arbitrary unknown quantum state cannot be copied perfectly.
2. **Measurement Disturbance**: Measuring an unknown quantum state irreversibly alters it unless the measurement basis matches the state's eigenbasis.

In a **teleportation-based QDS protocol**, the signer does not physically transmit quantum signature states across long-distance, lossy fiber. Instead:
- Signer and verifier share maximally entangled **Bell pairs** $\left|\Phi^+\right\rangle$.
- The signer executes a joint Bell-State Measurement (BSM) on the signature qubit and their half of the Bell pair.
- The signer transmits 2 classical bits over an authenticated classical channel.
- The verifier applies the appropriate **Pauli correction operator** ($I, X, Z, Y$) to recover the signature state.

### 1.3 The Core Problem Addressed by Q-Sentinel
While QDS protocols are theoretically secure, physical implementations are noisy and vulnerable to cyber attacks targeting the quantum and classical transport channels:
- **Forgery**: An attacker creates an unauthorized signature state.
- **Impersonation**: An attacker submits a signature claiming to be another identity using altered or mismatched keys.
- **Replay Attacks**: An adversary retransmits valid classical correction tokens or session transcripts from a previous verification.
- **Channel Manipulation / Eavesdropping / Noise Injection**: An adversary disturbs the quantum entanglement or introduces bit/phase errors.

**The Constraint & Innovation**:
Standard intrusion detection systems rely on AI/ML models. However, AI/ML models are **black boxes**, non-deterministic, computationally heavy, and vulnerable to adversarial machine learning evasion.
**Q-Sentinel** solves this by establishing an **auditable, explainable, quantum-inspired threat detection watchtower** using **Pauli eigenstates, projective measurements, and exact binomial hypothesis testing**. Every alert is backed by an auditable mathematical proof.

---

## 2. Mathematical Foundations

```
                            [Quantum State Space: H₂]
                                       │
            ┌──────────────────────────┼──────────────────────────┐
            ▼                          ▼                          ▼
     Pauli-Z Basis              Pauli-X Basis              Pauli-Y Basis
   |0⟩ = [1, 0]ᵀ              |+⟩ = [1/√2, 1/√2]ᵀ        |i+⟩ = [1/√2, i/√2]ᵀ
   |1⟩ = [0, 1]ᵀ              |-⟩ = [1/√2, -1/√2]ᵀ       |i-⟩ = [1/√2, -i/√2]ᵀ
```

### 2.1 State Vector Mechanics & Born Rule
A single qubit state $\left|\psi\right\rangle \in \mathcal{H}_2$ is parameterized as:
$$\left|\psi\right\rangle = \alpha\left|0\right\rangle + \beta\left|1\right\rangle, \quad \alpha, \beta \in \mathbb{C}, \quad |\alpha|^2 + |\beta|^2 = 1$$

A projective measurement in an orthonormal basis $\mathcal{B} = \{\left|\phi_0\right\rangle, \left|\phi_1\right\rangle\}$ is represented by projection operators $P_0 = \left|\phi_0\right\rangle\left\langle\phi_0\right|$ and $P_1 = \left|\phi_1\right\rangle\left\langle\phi_1\right|$. By the Born rule, the probability of measuring outcome $i \in \{0, 1\}$ is:
$$P(i) = \text{Tr}(P_i \rho) = \left|\left\langle\phi_i | \psi\right\rangle\right|^2$$

### 2.2 Pauli Operators & Eigenstates
The standard Pauli operators act as transformation gates:
$$\sigma_0 = I = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}, \quad \sigma_1 = X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \quad \sigma_2 = Y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}, \quad \sigma_3 = Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$$

### 2.3 Entanglement & The Four Bell States
Maximally entangled two-qubit Bell states in $\mathcal{H}_4 = \mathcal{H}_2 \otimes \mathcal{H}_2$:
$$\left|\Phi^{\pm}\right\rangle = \frac{1}{\sqrt{2}}\left(\left|00\right\rangle \pm \left|11\right\rangle\right), \quad \left|\Psi^{\pm}\right\rangle = \frac{1}{\sqrt{2}}\left(\left|01\right\rangle \pm \left|10\right\rangle\right)$$

### 2.4 Quantum Teleportation Protocol
For an unknown state $\left|\psi\right\rangle = \alpha\left|0\right\rangle + \beta\left|1\right\rangle$ and shared Bell pair $\left|\Phi^+\right\rangle_{23}$:
The composite 3-qubit state is:
$$\left|\Psi_{123}\right\rangle = \frac{1}{2} \left[ \left|\Phi^+\right\rangle_{12} (\alpha\left|0\right\rangle + \beta\left|1\right\rangle)_3 + \left|\Phi^-\right\rangle_{12} (\alpha\left|0\right\rangle - \beta\left|1\right\rangle)_3 + \left|\Psi^+\right\rangle_{12} (\beta\left|0\right\rangle + \alpha\left|1\right\rangle)_3 + \left|\Psi^-\right\rangle_{12} (-\beta\left|0\right\rangle + \alpha\left|1\right\rangle)_3 \right]$$

Depending on the Bell-measurement outcome $(b_1, b_2) \in \{00, 01, 10, 11\}$ on qubits 1 and 2, the receiver applies the Pauli unitary correction $U = Z^{b_2} X^{b_1}$ to recover $\left|\psi\right\rangle_3 \equiv \left|\psi\right\rangle$.

### 2.5 Statistical Hypothesis Testing (Q-STAT Engine)
For $N$ verification trials with expected outcome $s_{exp}$ and baseline quantum channel error rate $p_0$ (decoherence floor, e.g., $p_0 = 0.03$):
Let $n_1 = \sum_{j=1}^N \mathbb{I}(outcome_j \ne s_{exp})$ be the count of invalid outcomes.
1. **Empirical Error Rate**:
   $$\hat{e} = \frac{n_1}{N}$$
2. **Exact Binomial p-value**:
   $$p\text{-value} = P(K \ge n_1 \mid K \sim \text{Binomial}(N, p_0)) = \sum_{k=n_1}^N \binom{N}{k} p_0^k (1 - p_0)^{N-k}$$
3. **Standardized Anomaly Score ($z$-Score)**:
   $$\sigma_0 = \sqrt{\frac{p_0(1 - p_0)}{N}}, \quad z = \frac{\hat{e} - p_0}{\sigma_0}$$
4. **Calibrated Three-Tier Threat Classification**:
   - $z < 2.0$ ($p\text{-value} \ge 0.0228$): **LEGITIMATE** (Consistent with expected environmental noise, 95% confidence).
   - $2.0 \le z < 4.0$ ($0.00003 \le p\text{-value} < 0.0228$): **SUSPICIOUS** (Channel disturbance or low-intensity tampering, requires elevated scrutiny).
   - $z \ge 4.0$ ($p\text{-value} < 0.00003$): **MALICIOUS** (Active attack detected: forgery, impersonation, or aggressive channel tampering with $>99.99\%$ certainty).

---

## 3. High-Level System Architecture

```
                                  ┌────────────────────────────────────────────────────────┐
                                  │                  CLIENT / OPERATOR                     │
                                  │   (Streamlit Dashboard / CLI / Automated Test Suite)   │
                                  └───────────┬────────────────────────────────┬───────────┘
                                              │ Parameters / Scenarios         │ Telemetry
                                              ▼                                ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       Q-SENTINEL CORE ENGINE                                           │
│                                                                                                        │
│   ┌────────────────────────────────┐         ┌─────────────────────────────────────────────────────┐   │
│   │     CRYPTOGRAPHIC SUITE        │         │              SIMULATED QUANTUM DOMAIN               │   │
│   │ ┌────────────────────────────┐ │         │ ┌──────────────────────┐   ┌──────────────────────┐ │   │
│   │ │ Key & Signature Generator  │ │ Qubits  │ │ Bell State Generator │   │ Teleportation Engine │ │   │
│   │ │ (Pauli Eigenstate Encoding)│─┼────────►│ │ |Φ⁺⟩ Entangled Pairs │──►│ (BSM + 2-bit feed)   │ │   │
│   │ └────────────────────────────┘ │         │ └──────────────────────┘   └──────────┬───────────┘ │   │
│   │ ┌────────────────────────────┐ │         └───────────────────────────────────────┼─────────────┘   │
│   │ │ Freshness & Nonce Registry │ │                                                 │                 │
│   │ │ (Replay Attack Defense)    │ │                                                 ▼                 │
│   │ └────────────────────────────┘ │         ┌─────────────────────────────────────────────────────┐   │
│   └────────────────────────────────┘         │            ADVERSARIAL ATTACK INJECTOR              │   │
│                                              │  • Forgery (random eigenstate injection)            │   │
│                                              │  • Impersonation (mismatched identity key)          │   │
│                                              │  • Replay (stale classical token / reused session)  │   │
│                                              │  • Channel Noise (bit-flip, phase-flip, depolarize) │   │
│                                              └───────────────────────┬─────────────────────────────┘   │
│                                                                      │ Disturbed States                │
│                                                                      ▼                                 │
│   ┌────────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                           PROJECTIVE MEASUREMENT & TELEMETRY SAMPLER                           │   │
│   │                            (N repeated Born-rule projective trials)                            │   │
│   └───────────────────────────────────┬────────────────────────────────────────────────────────────┘   │
│                                       │ Raw Outcome Counts (n₀, n₁)                                    │
│                                       ▼                                                                │
│   ┌────────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                        Q-STAT ENGINE (STATISTICAL THREAT EVALUATOR)                            │   │
│   │  • Exact Binomial Test (`binomtest`)   • Standardized Z-Score Calculation                      │   │
│   │  • Confidence Interval Estimation      • Decision Rule Classification                          │   │
│   └───────────────────────────────────┬────────────────────────────────────────────────────────────┘   │
│                                       │                                                                │
│                                       ▼                                                                │
│                     [VERDICT: LEGITIMATE / SUSPICIOUS / MALICIOUS]                                     │
│                     [Metrics: e_hat, z-score, p-value, confidence, latency]                           │
└───────────────────────────────────────┬────────────────────────────────────────────────────────────────┘
                                        ▼
                  ┌───────────────────────────────────────────┐
                  │ AUDIT PERSISTENCE & ANALYTICS DATASTORE   │
                  │  • SQLite / JSON Run Telemetry History    │
                  │  • ROC & Confusion Matrix Benchmarking    │
                  └───────────────────────────────────────────┘
```

---

## 4. The 25-Phase Implementation Blueprint

To ensure complete clarity for all six team members, the implementation is decomposed into 25 systematic phases categorized across 8 operational stages.

### Stage 1: Mathematical Engine & Quantum State Representation (Phases 1–3)

#### Phase 1: Hilbert Space & Single-Qubit State Simulator
- **Objective**: Establish foundational complex vector space $\mathcal{H}_2$ for single-qubit representation with strict mathematical invariants.
- **Implementation**:
  - Represent state $|\psi\rangle$ as a $2 \times 1$ complex NumPy array (`dtype=np.complex128`).
  - Implement computational basis states $|0\rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix}, |1\rangle = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$.
  - Implement validation function `assert_normalized()` enforcing $\left| |\alpha|^2 + |\beta|^2 - 1.0 \right| < 10^{-7}$.
  - Implement fidelity function $F(|\psi\rangle, |\phi\rangle) = |\langle \psi | \phi \rangle|^2$.
- **Why this matters**: Prevents numeric drift and unnormalized states that would corrupt probability amplitudes in downstream teleportation.
- **Verification**: Unit tests asserting inner product $\langle 0 | 1 \rangle = 0$, $\langle 0 | 0 \rangle = 1$, and normalization preservation under arbitrary unitaries.

#### Phase 2: Pauli Operators & Pauli Eigenstate Suite
- **Objective**: Implement unitary Pauli matrices ($\sigma_0, \sigma_1, \sigma_2, \sigma_3$) and construct the six fundamental Pauli eigenstates used for QDS keys.
- **Implementation**:
  - Construct operators: $I, X, Y, Z$ as $2 \times 2$ complex arrays.
  - Implement eigenvectors:
    - Z-basis: $|0\rangle, |1\rangle$
    - X-basis: $|+\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle), |-\rangle = \frac{1}{\sqrt{2}}(|0\rangle - |1\rangle)$
    - Y-basis: $|i+\rangle = \frac{1}{\sqrt{2}}(|0\rangle + i|1\rangle), |i-\rangle = \frac{1}{\sqrt{2}}(|0\rangle - i|1\rangle)$
  - Create an enumerated registry `PauliBasis` and `PauliEigenstate`.
- **Verification**: Confirm eigenvalue relations: $X|\pm\rangle = \pm |\pm\rangle$, $Y|i\pm\rangle = \pm |i\pm\rangle$, $Z|0/1\rangle = \pm |0/1\rangle$.

#### Phase 3: Tensor Products & Multi-Qubit State Space
- **Objective**: Implement composite state vector math across $\mathcal{H}_{2^n}$ using the Kronecker product ($\otimes$).
- **Implementation**:
  - Implement `tensor_product(*states)` using `np.kron` to build composite vectors of $2, 3, \dots, n$ qubits.
  - Implement composite gate generators (e.g., $H \otimes I$, $X \otimes Z$).
  - Implement multi-qubit inner products and norm validation for length $2^n$ vectors.
- **Verification**: Test that $|0\rangle \otimes |1\rangle = [0, 1, 0, 0]^T$ and that $(A \otimes B)(|\psi\rangle \otimes |\phi\rangle) = (A|\psi\rangle) \otimes (B|\phi\rangle)$.

---

### Stage 2: Quantum Entanglement & Teleportation Channel (Phases 4–5)

#### Phase 4: Bell State Generation & Entanglement Verification
- **Objective**: Generate the four maximally entangled 2-qubit Bell states that serve as the physical entanglement resource for teleportation.
- **Implementation**:
  - Construct canonical Hadamard gate $H = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$ and CNOT gate $CNOT = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{pmatrix}$.
  - Synthesize $|\Phi^+\rangle = CNOT(H \otimes I)|00\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$.
  - Synthesize $|\Phi^-\rangle, |\Psi^+\rangle, |\Psi^-\rangle$ via local Pauli pre-rotations.
  - Compute density matrix $\rho = |\Phi^+\rangle\langle\Phi^+|$ and confirm purity $\text{Tr}(\rho^2) = 1$.
- **Verification**: Demonstrate maximal entanglement by computing partial trace $\rho_A = \text{Tr}_B(\rho) = \frac{1}{2}I_2$ (maximally mixed reduced state, Von Neumann entropy = 1).

#### Phase 5: Quantum Teleportation Protocol Pipeline
- **Objective**: Implement the complete, deterministic 3-qubit quantum teleportation protocol.
- **Implementation**:
  - Input: arbitrary secret state $|\psi\rangle$ (Signer) and pre-shared Bell pair $|\Phi^+\rangle_{23}$.
  - System state: $|\Psi_{123}\rangle = |\psi\rangle_1 \otimes |\Phi^+\rangle_{23}$.
  - Signer applies $CNOT_{12}$ followed by $H_1$.
  - Projective measurement on qubits 1 and 2 yields classical bits $b_1, b_2 \in \{0, 1\}$.
  - State of qubit 3 collapses to: $X^{b_1} Z^{b_2} |\psi\rangle$.
  - Classical transmission: $(b_1, b_2)$ transmitted to Verifier.
  - Pauli correction: Verifier executes $U_{corr} = Z^{b_2} X^{b_1}$ on qubit 3.
- **Verification**: Calculate state fidelity $F(|\psi\rangle_{original}, |\psi\rangle_{teleported}) = 1.000000$ across all 6 Pauli eigenstates.

---

### Stage 3: QDS Protocol & Projective Verification Engine (Phases 6–8)

#### Phase 6: QDS Key Generation & Message-to-Eigenstate Encoding
- **Objective**: Construct the cryptographic mapping between digital messages, private keys, and quantum signature states.
- **Implementation**:
  - Private key: sequence of bit-values $k \in \{0, 1\}$ paired with basis choices $b \in \{X, Y, Z\}$ generated via cryptographically secure pseudo-random seed (`secrets` module).
  - Public verification metadata: basis specifications and authorized signer public ID.
  - Message digest: Compute SHA-256 of the classical message; use digest bits to select corresponding signature token states.
  - Signature payload: Sequence of prepared Pauli eigenstates $\{|s_1\rangle, |s_2\rangle, \dots, |s_m\rangle\}$.
- **Verification**: Deterministic state preparation check: verify that message hash bit `0` under basis `X` consistently yields $|+\rangle$.

#### Phase 7: Teleportation-Driven Signature Distribution
- **Objective**: Route the generated signature states from Signer (Alice) to Verifier (Bob) exclusively through the simulated quantum teleportation channel.
- **Implementation**:
  - For each signature qubit:
    1. Spawn a dedicated Bell pair $|\Phi^+\rangle$.
    2. Teleport the signature qubit through the Stage 2 pipeline.
    3. Package the verification packet: classical message, claimed signer ID, teleported quantum state vector, and session metadata.
- **Verification**: Ensure multi-qubit signature sequences arrive intact with zero bit/phase error under an undisturbed channel.

#### Phase 8: Projective Measurement Verification & Born Sampling Engine
- **Objective**: Implement the Verifier’s physical measurement module using basis projection operators and Born-rule stochastic sampling.
- **Implementation**:
  - Given expected eigenstate $|s_{exp}\rangle$ and basis $B \in \{X, Y, Z\}$:
    - Construct projection operator $P_{correct} = |s_{exp}\rangle\langle s_{exp}|$ and $P_{incorrect} = I - P_{correct}$.
    - Compute theoretical success probability $P_{pass} = \langle \psi_{received} | P_{correct} | \psi_{received} \rangle$.
    - Simulate $N$ repeated trials (e.g., $N = 200$) using `np.random.choice([0, 1], size=N, p=[P_fail, P_pass])`.
  - Aggregate outcome counts: $n_0$ (expected matches) and $n_1$ (erroneous outcomes).
- **Verification**: Validate that an honest state yields $n_1 \approx 0$ (or within calibrated noise bounds), while an orthogonal state yields $n_1 = N$.

---

### Stage 4: Adversarial Attack Simulation Engine (Phases 9–13)

#### Phase 9: Threat Model 1 — Signature Forgery Attack
- **Objective**: Simulate an active adversary (Eve) attempting to fabricate a valid digital signature without possession of the private key seed.
- **Implementation**:
  - Eve does not know the exact Pauli eigenstate sequence $\{|s_i\rangle\}$.
  - Eve generates either random pure states $|\psi_{forge}\rangle = \cos(\theta)|0\rangle + e^{i\phi}\sin(\theta)|1\rangle$ or random guesses from $\{|0\rangle, |1\rangle, |+\rangle, |-\rangle, |i+\rangle, |i-\rangle\}$.
  - Calculate theoretical overlap: when Eve guesses a random Pauli state, expected overlap with true state is $|\langle s_{true} | s_{forge} \rangle|^2 = \frac{1}{2}$ (for non-matching bases) or $0$ (for opposite eigenstates).
  - Overall expected error rate: $\hat{e} \approx 50\%$.
- **Verification**: Run 500 trials of forgery attack; verify empirical error rate $\hat{e} \in [0.45, 0.55]$.

#### Phase 10: Threat Model 2 — Signer Impersonation Attack
- **Objective**: Simulate an attacker asserting Alice's identity while utilizing unauthorized or illegitimate key material.
- **Implementation**:
  - Adversary uses a legitimate signature format but derived from Mallory's private key seed.
  - Verifier measures the received quantum states against Alice’s registered public verification basis.
  - Mismatch between Mallory's states and Alice's registered bases induces high-rate projective collapse into the incorrect subspace ($\hat{e} \approx 50\%$).
  - Attach identity tag mismatch telemetry.
- **Verification**: Confirm detection engine differentiates legitimate Alice signature from Mallory's impersonated signature.

#### Phase 11: Threat Model 3 — Replay Attack & Cryptographic Freshness Engine
- **Objective**: Implement and detect replay attacks where an adversary intercepts and retransmits legitimate classical teleportation correction bits and past verification sessions.
- **Implementation**:
  - Understand the distinct nature of Replay: In quantum mechanics, quantum states cannot be stored indefinitely without decoherence, and classical replay uses stale tokens.
  - Implement a **Session Freshness & Nonce Registry**:
    - Each teleportation session is cryptographically bound to a unique monotonic sequence number, high-resolution UTC timestamp, and single-use cryptographic nonce: $\text{Token} = \text{HMAC}(K_{auth}, Nonce \parallel Timestamp \parallel b_1 b_2)$.
    - Verifier maintains a sliding freshness window and replay cache.
    - If a previously used session token is detected, it is immediately flagged as a REPLAY ATTACK before or during statistical evaluation.
- **Verification**: Submit an identical valid verification packet twice; assert that run 1 passes as LEGITIMATE and run 2 is intercepted and classified as REPLAY.

#### Phase 12: Threat Model 4 — Quantum Channel Manipulation & Environmental Noise
- **Objective**: Implement controllable quantum noise models simulating environmental decoherence, eavesdropping (intercept-resend), and quantum channel tampering.
- **Implementation**:
  - Parameterize a disturbance parameter $\epsilon \in [0.0, 1.0]$.
  - Implement noise channels:
    1. **Bit-Flip Channel**: $|\psi\rangle \to \sqrt{1 - \epsilon}|\psi\rangle + \sqrt{\epsilon} X |\psi\rangle$.
    2. **Phase-Flip Channel**: $|\psi\rangle \to \sqrt{1 - \epsilon}|\psi\rangle + \sqrt{\epsilon} Z |\psi\rangle$.
    3. **Depolarizing Channel**: $\rho \to (1 - \epsilon)\rho + \frac{\epsilon}{2} I$.
  - Intercept-Resend: Adversary measures in random basis $M \in \{X, Z\}$ and forwards collapsed state.
- **Verification**: Sweep $\epsilon$ from $0.0$ to $0.40$ in steps of $0.05$; verify empirical error rate $\hat{e}$ increases linearly with $\epsilon$.

#### Phase 13: Unified Threat Simulation Orchestrator
- **Objective**: Provide a clean, unified API for injecting any attack scenario on demand during verification runs.
- **Implementation**:
  - Create class `ThreatOrchestrator` supporting scenarios: `SCENARIO_LEGITIMATE`, `SCENARIO_FORGERY`, `SCENARIO_IMPERSONATION`, `SCENARIO_REPLAY`, `SCENARIO_CHANNEL_NOISE`.
  - Expose parameter configuration: noise level $\epsilon$, number of trials $N$, targeted qubits.
  - Return clean `SimulationContext` encapsulating all intermediate quantum states, classical bit streams, and applied disturbances for full audit visibility.
- **Verification**: Execute automated test matrix cycling through all 5 scenarios and confirming appropriate state corruption.

---

### Stage 5: Quantum-Inspired Statistical Detection Framework (Q-STAT) (Phases 14–17)

#### Phase 14: Quantum Noise Floor Calibration & Empirical Baseline
- **Objective**: Mathematically calibrate the baseline channel error probability $p_0$ to prevent false alarms due to natural quantum decoherence.
- **Implementation**:
  - In real-world quantum fiber / satellite links, thermal fluctuations and birefringence induce optical error rate (QBER) typically around $1\% - 3\%$.
  - Model baseline noise floor $p_0 = 0.03$ ($3\%$).
  - Allow user/environment calibration routine: execute 1000 honest trials to compute empirical baseline $\bar{p}_0$ and variance.
- **Verification**: Verify that with honest transmission under baseline noise, false alarms do not exceed theoretical statistical bounds ($\le 5\%$).

#### Phase 15: Exact Binomial Hypothesis Testing
- **Objective**: Implement the primary statistical engine using exact binomial testing without relying on uncalibrated heuristics or black-box ML.
- **Implementation**:
  - Null Hypothesis $H_0: p \le p_0$ (The signature is legitimate; observed errors are caused purely by benign channel noise).
  - Alternative Hypothesis $H_1: p > p_0$ (The signature is under attack / forged / tampered).
  - Given $n_1$ erroneous outcomes out of $N$ trials:
  - Compute one-tailed p-value using `scipy.stats.binomtest(k=n1, n=N, p=p0, alternative='greater').pvalue`.
  - Compute Wilson score confidence intervals for the true error rate $\hat{e}$.
- **Verification**: Test edge cases: $n_1 = 0 \implies p = 1.0$; $n_1 = N \implies p \approx 0.0$.

#### Phase 16: Standardized Anomaly Score & Z-Score Normal Approximation
- **Objective**: Derive a smooth, standardized continuous anomaly metric ($z$-score) for real-time dashboard telemetry and alerting.
- **Implementation**:
  - Compute standard error under null hypothesis: $\sigma_0 = \sqrt{\frac{p_0(1 - p_0)}{N}}$.
  - Compute standardized $z$-score:
    $$z = \frac{\hat{e} - p_0}{\sigma_0}$$
  - Calculate detection confidence metric via standard normal cumulative distribution function:
    $$\text{Confidence} = \Phi(z) = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^z e^{-t^2/2} dt = \frac{1}{2}\left[1 + \text{erf}\left(\frac{z}{\sqrt{2}}\right)\right]$$
  - Handled by `scipy.stats.norm.cdf(z)`.
- **Verification**: Verify that for $N = 200, p_0 = 0.03$, an observed error rate of $\hat{e} = 0.03 \implies z = 0.0, \text{Confidence} = 50\%$; $\hat{e} = 0.50 \implies z = 38.9, \text{Confidence} > 99.999\%$.

#### Phase 17: Three-Tier Threat Classification & Threshold Rigor
- **Objective**: Map continuous $z$-scores to clear, defensible operational threat levels with rigorous mathematical justification.
- **Implementation**:
  - Category Definition:
    - **LEGITIMATE** ($z < 2.0$): Standard 2-sigma boundary ($\approx 95.4\%$ of normal variation). Signature accepted deterministically.
    - **SUSPICIOUS** ($2.0 \le z < 4.0$): Between 2-sigma and 4-sigma ($p \in [0.00003, 0.045]$). Indicates channel degradation, minor tampering, or high noise. Flagged for audit.
    - **MALICIOUS** ($z \ge 4.0$): Exceeds 4-sigma ($p < 0.00003$, $>99.997\%$ certainty of attack). Signature deterministically rejected; threat alert dispatched.
  - Produce human-readable, auditable diagnostic string:
    `"Observed error rate 48.50% vs expected 3.00% (z=37.68, p < 1e-15). Active attack detected with >99.99% confidence."`
- **Verification**: Assert that every verdict contains the exact mathematical justification, error rate, $z$-score, and threshold boundary.

---

### Stage 6: Modular Software Architecture & Data Contracts (Phases 18–20)

#### Phase 18: Package Modularization & Object-Oriented Domain Models
- **Objective**: Structure the codebase cleanly into production-grade Python packages with strong typing and zero circular dependencies.
- **Implementation**:
  - Directory Layout:
    ```
    sih/
    ├── quantum/
    │   ├── __init__.py
    │   ├── state.py           # Qubit state vectors, Pauli matrices, normalization
    │   ├── bell.py            # Bell state generation, partial trace, fidelity
    │   ├── teleport.py        # 3-qubit teleportation, BSM, Pauli corrections
    │   └── measure.py         # Born-rule projective measurement engine
    ├── security/
    │   ├── __init__.py
    │   ├── signature.py       # Message digest, Pauli key preparation, QDS token
    │   ├── freshness.py       # Nonce registry, timestamp verification, replay guard
    │   ├── attacks.py         # Forgery, impersonation, noise, replay simulators
    │   └── detector.py        # Q-STAT engine (binomial test, z-score, thresholds)
    ├── analytics/
    │   ├── __init__.py
    │   ├── metrics.py         # FAR, FRR, accuracy, confusion matrix, latency
    │   └── history.py         # Telemetry persistence (JSON/SQLite datastore)
    ├── dashboard/
    │   ├── __init__.py
    │   ├── visualizer.py      # Quantum circuit & teleportation schematic
    │   └── charts.py          # Plotly gauge, outcome histograms, ROC curves
    ├── tests/
    │   ├── test_quantum.py    # Unit tests for quantum mechanics
    │   ├── test_teleport.py   # Unit tests for teleportation pipeline
    │   ├── test_security.py   # Unit tests for attacks & detection
    │   └── test_stats.py       # Unit tests for statistical formulas
    ├── app.py                 # Streamlit interactive application entrypoint
    ├── benchmark.py           # CLI benchmark runner for quantitative performance
    ├── requirements.txt
    └── README.md
    ```
  - Define dataclasses: `QubitState`, `BellPair`, `TeleportationResult`, `SignatureToken`, `VerificationResult`.
- **Verification**: Python `import` tree loads without warnings or circular dependencies.

#### Phase 19: Security Performance Benchmark & Quantitative Metrics Suite
- **Objective**: Implement formal cybersecurity evaluation metrics to quantitatively validate the detection framework.
- **Implementation**:
  - Build `benchmark.py` executing Monte Carlo simulations across 1000 runs per attack vector.
  - Compute:
    1. **Verification Accuracy**: $\frac{TP + TN}{TP + TN + FP + FN}$.
    2. **False Acceptance Rate (FAR)**: $\frac{FP}{FP + TN}$ (Forged signatures mistakenly marked LEGITIMATE). Target: $0.00\%$.
    3. **False Rejection Rate (FRR)**: $\frac{FN}{TP + FN}$ (Honest signatures mistakenly marked MALICIOUS). Target: $< 1.00\%$.
    4. **Detection Latency**: Execution time from measurement sampling to verdict generation (Target: $< 10$ milliseconds).
    5. **Z-Score Separation**: $\Delta z = \bar{z}_{\text{attack}} - \bar{z}_{\text{legitimate}}$ (Demonstrates statistical discernibility).
- **Verification**: Execute benchmark; output tabular performance summary proving $\text{FAR} = 0.0\%$ and $\Delta z > 20$.

#### Phase 20: Audit Logging & Telemetry Persistence Datastore
- **Objective**: Ensure all verification decisions, quantum measurement parameters, and attack detections are stored in an auditable database.
- **Implementation**:
  - Implement SQLite/JSON logger in `analytics/history.py`.
  - Log schema: `run_id`, `timestamp`, `message`, `signer_id`, `scenario`, `trials_N`, `error_rate`, `z_score`, `p_value`, `verdict`, `latency_ms`, `diagnostic_text`.
  - Provide exportable JSON/CSV format for security incident response reports.
- **Verification**: Run 10 consecutive verifications; verify database records match displayed dashboard metrics identically.

---

### Stage 7: Interactive Dashboard & Visualizations (Phases 21–23)

#### Phase 21: Streamlit Dashboard Skeleton & 3-Panel Ergonomics
- **Objective**: Develop an intuitive, high-impact operator interface for real-time threat monitoring and scenario execution.
- **Implementation**:
  - **Left Panel (Control & Configuration)**:
    - Message input string.
    - Signer identity selector (Alice, Bob, Mallory).
    - Scenario selector: Normal, Forgery, Impersonation, Replay, Channel Noise.
    - Channel Noise slider $\epsilon \in [0.0, 0.50]$ (interactive).
    - Trial count slider $N \in [50, 1000]$.
    - "Execute Teleportation & Verification" trigger button.
  - **Center Panel (Quantum Pipeline & Distributions)**:
    - Quantum teleportation state tracker (Alice state $\to$ Bell pair $\to$ BSM bits $\to$ Pauli correction $\to$ Bob state).
    - Measurement outcome distribution bar chart (expected vs observed).
  - **Right Panel (Security Decision & Anomaly Telemetry)**:
    - Real-time threat status badge (🟢 LEGITIMATE / 🟡 SUSPICIOUS / 🔴 MALICIOUS).
    - Live Anomaly Score Gauge.
    - Statistical metrics card ($\hat{e}, z\text{-score}, p\text{-value}$, confidence).
    - Auditable explanation banner.
- **Verification**: Launch `streamlit run app.py`; verify responsive layout and error-free rendering.

#### Phase 22: Plotly Quantum Visualizer & Outcome Histograms
- **Objective**: Build interactive graphics showing theoretical quantum probability distributions alongside empirical measurement outcomes.
- **Implementation**:
  - Build Plotly horizontal/vertical bar charts comparing:
    - Theoretical Born probability: $P(|0\rangle), P(|1\rangle)$ or $P(|+\rangle), P(|-\rangle)$.
    - Empirical measurement frequencies across $N$ trials.
  - Visually highlight anomalies: when forgery occurs, show empirical bars diverging drastically from expected quantum eigenstates.
- **Verification**: Inspect generated plots; verify tooltips, color coding (green for expected, red for error), and dynamic resizing.

#### Phase 23: Dynamic Threat Score Gauge & Temporal Attack Stream
- **Objective**: Deliver high-end security monitoring visual components indicating threat levels and historical stability.
- **Implementation**:
  - Plotly Gauge Chart for $z$-score:
    - Green zone: $0 \le z < 2$.
    - Yellow zone: $2 \le z < 4$.
    - Red zone: $4 \le z \le 20+$.
    - Needle dynamically animated to current run's $z$-score.
  - Running line chart displaying $z$-scores across past 20 verification events, highlighting anomaly spikes.
- **Verification**: Switch scenarios from Legitimate $\to$ Channel Noise $\to$ Forgery; observe gauge needle transitioning smoothly from green to red.

---

### Stage 8: Integration, Stress Testing & Presentation Readiness (Phases 24–25)

#### Phase 24: End-to-End Automated Test Suite & CI Stress Testing
- **Objective**: Ensure absolute software reliability, boundary testing, and regression protection before presentation.
- **Implementation**:
  - Comprehensive `pytest` test suite:
    - Quantum gates: Unitary preservation, trace preservation.
    - Teleportation fidelity: 100% exact state recovery.
    - Noise models: Monotonic error rate scaling with noise parameter $\epsilon$.
    - Attack detection: Zero false negatives across 200 simulated attack runs.
    - Statistical edge cases: $n_1 = 0, n_1 = N$, small $N$, large $N$.
- **Verification**: Run `python -m pytest tests/` with 100% passing tests and $>90\%$ code coverage.

#### Phase 25: Live Demonstration Scenarios, Presentation Pitch Kit & Judge Defense Manual
- **Objective**: Prepare the 6-person team to present, demonstrate, and defend the project with complete confidence.
- **Implementation**:
  - Scripted 5-scenario demo run:
    1. **Scenario 1 (Normal)**: Legitimate payment approval $\to$ Green status, $z \approx 0.8$, accepted.
    2. **Scenario 2 (Forgery)**: Fabricated token $\to$ Red status, $z \approx 18.5$, immediate rejection.
    3. **Scenario 3 (Impersonation)**: Mallory signing as Alice $\to$ Red status, identity mismatch detected.
    4. **Scenario 4 (Replay)**: Stale session re-injected $\to$ Red status, caught by Freshness Nonce Registry.
    5. **Scenario 5 (Channel Noise)**: Drag noise slider $0\% \to 15\% \to 30\% \to$ Watch gauge transition Green $\to$ Yellow $\to$ Red live!
  - Prepare 30-second, 1-minute, and 3-minute pitches.
  - Compile the Judge Q&A Defense Manual covering why ML was avoided, why teleportation is used, how thresholds are derived, and real-world scalability.
- **Verification**: Team dry-run of live demo completed in under 3 minutes with zero errors.

---

## 5. Team Operational Matrix (Roles for the 6 Teammates)

| Member | Primary Focus Area | Assigned Phases | Key Deliverables |
|---|---|---|---|
| **Member 1 (Quantum Lead)** | Quantum Foundations & Teleportation | Phases 1, 2, 3, 4, 5 | `quantum/state.py`, `quantum/bell.py`, `quantum/teleport.py` |
| **Member 2 (Crypto Lead)** | QDS Keys & Measurement Mechanics | Phases 6, 7, 8 | `security/signature.py`, `quantum/measure.py` |
| **Member 3 (Adversarial Lead)** | Attack Modeling & Injection Engine | Phases 9, 10, 11, 12, 13 | `security/attacks.py`, `security/freshness.py` |
| **Member 4 (Detection Lead)** | Q-STAT Statistical Decision Engine | Phases 14, 15, 16, 17 | `security/detector.py` |
| **Member 5 (Frontend / UX Lead)** | Streamlit Dashboard & Plotly Visuals | Phases 21, 22, 23 | `app.py`, `dashboard/charts.py`, `dashboard/visualizer.py` |
| **Member 6 (QA & Benchmarks Lead)**| Testing, Metrics, History & Pitch Kit | Phases 18, 19, 20, 24, 25 | `tests/`, `benchmark.py`, `analytics/`, Judge Defense Kit |

*As the 7th member (AI Lead Architect), I will implement all modules, write clean documented code, create test cases, and explain each component in detail.*

---

## 6. Verification Plan

### Automated Testing
- Execute `pytest tests/` covering single-qubit unitaries, Bell state fidelity, teleportation protocol correctness, and statistical hypothesis tests.
- Execute `python benchmark.py --runs 500` to verify:
  - Accuracy: $> 99.5\%$
  - False Acceptance Rate (FAR): $0.00\%$
  - False Rejection Rate (FRR): $< 1.00\%$
  - Latency: $< 15\text{ ms}$ per verification.

### Live Demonstration Verification
- Launch Streamlit UI via `streamlit run app.py`.
- Step through the 5 canonical demo scenarios and verify real-time gauge animation, state diagram tracking, and alert generation.
