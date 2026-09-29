# Q-SENTINEL: Technical Rationale & Evaluator Defense Manual
**Companion Specifications:** [`docs/THREAT_MODEL.md`](THREAT_MODEL.md) | [`docs/ARCHITECTURE.md`](ARCHITECTURE.md)  
**Standard Track:** Smart India Hackathon (SIH-26141) · National Quantum Mission (NQM)  

---

## 1. Executive Summaries

### 30-Second Elevator Pitch
> *"Quantum computers will break RSA and ECDSA using Shor's algorithm. Quantum Digital Signatures (QDS) protect us with the laws of physics, but they introduce a new challenge: quantum channels are noisy, fragile, and vulnerable to physical tampering. Current intrusion detection systems rely on AI/ML, which are non-deterministic black boxes. We built **Q-Sentinel**—a quantum-inspired statistical watchtower that monitors teleportation-based QDS systems in real time. Using Pauli eigenstates, projective measurements, exact binomial hypothesis testing, and sequential Wald SPRT, Q-Sentinel mathematically proves whether a signature is authentic or under attack with zero AI/ML."*

### 1-Minute Technical Overview
> *"Our project, Q-Sentinel, directly answers SIH26141. Teleportation-based QDS transmits quantum signature states using shared Bell pairs $|\Phi^+\rangle$ and two classical correction bits $(m_1, m_2)$ that specify a Pauli correction $U = Z^{m_1} X^{m_2}$.
> If an attacker tampers with the quantum state or classical bits, the verifier holds a corrupted state. In Q-Sentinel, we sample repeated Born-rule projective measurements across the signature's Pauli eigenstates. 
> Under the null hypothesis that errors are purely environmental noise ($p_0 \approx 3\%$), we run an exact binomial test and compute a standardized $z$-score. If $z \ge 4.0$, the signature is deterministically rejected with $>99.99\%$ statistical confidence. Simultaneously, our sequential SPRT engine early-stops active attacks at Trial 6, slashing quantum bandwidth consumption by 98.5% with sub-2 millisecond latency."*

---

## 2. Whiteboard Mathematics (Formulas to Draw on Demand)

### 1. Quantum Teleportation Composite State
Composite 3-qubit state before measurement:
$$|\Psi_{123}\rangle = \frac{1}{2} \left[ |00\rangle_{12} |\psi\rangle_3 + |01\rangle_{12} (X|\psi\rangle)_3 + |10\rangle_{12} (Z|\psi\rangle)_3 + |11\rangle_{12} (ZX|\psi\rangle)_3 \right]$$
- Alice measures qubits 1 and 2 in Bell basis $\to$ outcome $(m_1, m_2) \in \{00, 01, 10, 11\}$.
- Bob applies Pauli unitary correction $U = Z^{m_1} X^{m_2}$ on qubit 3 $\to$ recovered state $|\psi\rangle_3 \equiv |\psi\rangle$.

### 2. Born-Rule Projective Measurement & MUB Overlap
$$P(\text{match}) = |\langle \psi_{\text{expected}} | \psi_{\text{received}} \rangle|^2$$
For an attacker guessing a Pauli eigenstate in a mutually unbiased basis (e.g. state is in $Z$, attacker guesses $X$):
$$|\langle 0 | + \rangle|^2 = \left|\frac{1}{\sqrt{2}}\right|^2 = 0.50 \implies \hat{e} \approx 50\%$$

### 3. Exact Binomial Hypothesis Test (Q-STAT)
- Null Hypothesis $H_0: p \le p_0$ (Calibrated optical fiber noise floor $p_0 = 0.030$).
- Alternative Hypothesis $H_1: p > p_0$ (Active attack / tampering).
$$p\text{-value} = \sum_{k=n_1}^N \binom{N}{k} p_0^k (1 - p_0)^{N-k}$$

### 4. Standardized Anomaly Z-Score
For $N = 400$ total trials ($8 \text{ tokens} \times 50 \text{ trials/token}$):
$$\sigma_0 = \sqrt{\frac{p_0(1 - p_0)}{N}} = \sqrt{\frac{0.03 \times 0.97}{400}} \approx 0.008529, \quad z = \frac{\hat{e} - p_0}{\sigma_0}$$
- $z < 2.0$: **LEGITIMATE** ($\approx 95.4\%$ normal noise boundary).
- $2.0 \le z < 4.0$: **SUSPICIOUS** (Channel disturbance / secondary audit trigger).
- $z \ge 4.0$: **MALICIOUS** ($>99.997\%$ certainty of active attack).

---

## 3. Evaluator Defense & Technical Objection Rationale

#### Q1: "Why didn't you use Qiskit, Cirq, or real quantum hardware?"
**Answer**: "A 1-to-3 qubit teleportation protocol involves Hilbert spaces of dimension 2, 4, and 8. Using full quantum SDKs introduces heavy compilation overhead, API latency, and library version instability without adding any mathematical depth. Our custom NumPy engine implements the exact linear algebra—state vectors, Pauli matrices, Kronecker products, and Born rule projection. Furthermore, physical QPUs currently lack multi-session coherence times needed to test repeatable cyber-attack telemetry."

#### Q2: "Why is AI/ML excluded? Wouldn't an autoencoder detect anomalies better?"
**Answer**: "First, the problem statement explicitly forbids AI/ML. Second, in mission-critical cryptography, AI/ML models are **black boxes** that cannot provide deterministic information-theoretic guarantees. An ML detector can be evaded through adversarial perturbations or fail due to distribution shifts. In Q-Sentinel, every decision is an exact mathematical hypothesis test backed by an auditable $p$-value and $z$-score."

#### Q3: "How do you distinguish physical channel noise from a cyber attack?"
**Answer**: "By continuously calibrating against the baseline noise floor $p_0$ via `DynamicNoiseCalibrator` from pilot reference frames. Natural thermal and birefringence decoherence causes low-rate independent errors ($z < 2.0$). An active cyber attack (forgery or impersonation) forces projective collapse into orthogonal or unbiased subspaces, causing error rates of ~50% ($z > 35.0$). Borderline channel manipulation falls cleanly into our **SUSPICIOUS** tier ($2.0 \le z < 4.0$), alerting operators before catastrophic failure."

#### Q4: "How does Q-Sentinel catch replay attacks if the quantum states were originally valid?"
**Answer**: "By recognizing the physics of quantum mechanics: qubits cannot be cloned (No-Cloning Theorem) and cannot be stored indefinitely without decoherence. Therefore, an attacker replaying a signature retransmits the classical teleportation bits and session metadata. Q-Sentinel incorporates a **Cryptographic Freshness & Nonce Registry** using sliding UTC time windows and monotonic nonce tracking. Replayed sessions are intercepted deterministically as a bookkeeping violation."

#### Q5: "Isn't 100% accuracy with 0.00% False Rejection Rate statistically implausible?"
**Answer**: "We report metrics with statistical precision:
- **False Acceptance Rate (FAR)**: $0.00\%$ ($0/2000$, Wilson 95% CI: $[0.00\%, 0.19\%]$). Attack states ($e \approx 33\%\text{--}50\%$) produce $z \ge +35\sigma$, making accidental acceptance into LEGITIMATE ($z < 2.0$) astronomically impossible ($p < 10^{-200}$).
- **Hard False Rejection Rate (FRR to MALICIOUS)**: $0.00\%$ ($0/500$, Wilson 95% CI: $[0.00\%, 0.74\%]$). To be rejected as MALICIOUS, an honest signature must breach $z \ge 4.0$, which occurs with theoretical probability $P(Z \ge 4.0) \approx 3.17 \times 10^{-5}$.
- **Elevated Warning Rate (SUSPICIOUS)**: Honest sessions occasionally enter SUSPICIOUS ($2.0 \le z < 4.0$) with theoretical nominal rate $\alpha \approx 2.28\%$ (empirically 1 in 50 runs). This triggers a secondary pilot-frame calibration rather than hard rejection."

#### Q6: "What happens if an adaptive attacker tampers with only 1 token out of 8 to stay under the radar?"
**Answer**: "This is fully analyzed in [`docs/THREAT_MODEL.md`](THREAT_MODEL.md) Section 4.2. First, each token is evaluated individually, and Page's CUSUM detects localized error bursts ($h=8.5$). Second, because message payloads are hashed with SHA-256 before token mapping, altering even 1 bit of the signed transaction scrambles the entire token sequence by the Avalanche Effect. An attacker cannot forge a meaningful message by flipping a single token."

---

## 4. Live Demonstration Script (Under 2 Minutes)

1. **Step 1 — Normal Run**:
   - Select *1. Legitimate Verification*. Click *Execute Teleportation & Verification*.
   - Point out: Green verdict banner 🟢, $z \approx 0.21$, error rate $\approx 3.1\%$, teleportation pipeline shows exact state recovery $|+⟩ \to |+⟩$.
2. **Step 2 — Forgery Attack**:
   - Select *2. Signature Forgery*. Click *Execute*.
   - Point out: Instant Red alert 🔴, error rate jumps to $\approx 50\%$, $z$-score jumps to $+54.1\sigma$, $p < 1e-15$. Show measurement distribution chart where invalid outcomes dominate.
3. **Step 3 — Replay Attack**:
   - Select *4. Replay Attack*. Click *Execute*.
   - Point out: Red alert 🔴 with diagnostic: *"REPLAY ATTACK INTERCEPTED. Stale timestamp / duplicate nonce"*. Explain why freshness registry is used for replay.
4. **Step 4 — Channel Noise Slider**:
   - Select *5. Quantum Channel Manipulation*.
   - Set $\epsilon = 0.10 \to$ Watch status flip to Yellow 🟡 (**SUSPICIOUS**).
   - Set $\epsilon = 0.35 \to$ Watch status flip to Red 🔴 (**MALICIOUS**).
5. **Step 5 — Telemetry History**:
   - Scroll down to the *Anomaly Score Trend* chart showing the real-time $z$-score history with horizontal threshold lines.
