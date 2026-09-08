# 📘 Q-SENTINEL Masterclass | Lesson 20: Post-Quantum Classical Hybrid Verification (Q-HYBRID)

> **File in Focus:** [`security/hybrid.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/hybrid.py)  
> **Pipeline Position:** Step 20 of the entire Q-Sentinel architecture (Cryptographic Defense-in-Depth Layer — Phase 29)  
> **Target Audience:** Fresher needing to understand defense-in-depth security, why pure quantum or pure classical systems have single points of failure, how HMAC-SHA3-512 pairs with Quantum Digital Signatures, and how timing side-channels are eliminated.

---

## 🧭 1. What Is This File and Why Does It Exist?

In military and enterprise cybersecurity, there is a golden rule:
> **Never rely on a single defensive mechanism, no matter how advanced it sounds.**

If a security system relies **only on classical cryptography** (like RSA or ECC):
* A scalable quantum computer running Shor’s algorithm will calculate the private key and forge signatures with zero trace.
* Even post-quantum algorithms (like Kyber or Dilithium) rely on mathematical computational hardness assumptions (lattice problems). If a mathematician discovers a polynomial-time classical algorithm to solve the Shortest Vector Problem (SVP), classical security collapses overnight.

If a security system relies **only on pure quantum signatures**:
* What happens if a backhoe accidentally cuts the quantum fiber line, or severe thermal noise temporarily raises the quantum bit error rate (QBER)? The entire organization suffers a total Denial-of-Service (DoS).
* What if an adversary intercepts the classical message payload in transit (e.g. changing `"Transfer $100"` to `"Transfer $10,000,000"`), but forwards valid quantum states that were generated for a different payload?

### The Solution: Dual-Layer Defense-in-Depth (Q-HYBRID)
[`security/hybrid.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/hybrid.py) implements a **hybrid verification engine** conforming to the National Quantum Mission (NQM) and NIST hybrid transition guidelines:
* **Layer 1 (Classical Integrity):** NIST FIPS 202 **HMAC-SHA3-512**. Provides classical cryptographic payload integrity and authentication using the Keccak cryptographic sponge construction.
* **Layer 2 (Quantum Unconditional Security):** **Teleportation-based Quantum Digital Signatures (QDS)** verified via the statistical **Q-STAT** engine.

To forge or alter a transaction in Q-Sentinel, an attacker must break **both** the computational collision resistance of SHA3-512 **and** the laws of quantum mechanics (No-Cloning and Heisenberg Uncertainty) simultaneously!

---

## 💡 2. Plain English Real-World Analogies

### Analogy 1: The High-Security Diplomatic Courier Pouch
Imagine you are sending a top-secret treaty between two nations:
* **Layer 1 (The Classical Wax Seal & HMAC):** You place the treaty inside an armored metal briefcase locked with a 128-digit cryptographic combination (HMAC-SHA3-512). If an attacker opens the briefcase or replaces the paper document, the lock fails to open, or the wax seal shatters into dust.
* **Layer 2 (The Quantum Escort & QDS):** Inside the briefcase is a living, exotic carrier bird (the quantum signature token). The bird's feathers are in a delicate quantum state that dissolves if anyone attempts to clone or photograph it. When the recipient receives the briefcase, they check the bird's quantum plumage.

**Why Both Are Necessary:**
1. If an attacker tampers with the paper treaty inside the briefcase (changing the text), **Layer 1 instantly catches it** before anyone even touches the bird.
2. If an attacker uses a supercomputer to guess the lock combination, but cannot synthesize the quantum bird, **Layer 2 instantly catches the forgery**.
3. A successful transaction requires **both locks to open in harmony**.

### Analogy 2: Two-Factor Authentication (Something You Know + Something You Are)
Think of everyday modern multi-factor authentication (MFA):
* You enter your master password (Classical knowledge).
* You scan your physical fingerprint on a biometric sensor (Physical reality).
In Q-Sentinel:
* **HMAC-SHA3-512** is the cryptographic mathematical proof ("something you know").
* **QDS Quantum Tokens** are the physical quantum state projections ("something that physically exists and cannot be duplicated").

---

## 📐 3. The Cryptographic & Mathematical Foundations

```
                                Message Payload (M)
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 │                                               │
                 ▼                                               ▼
     ┌───────────────────────┐                       ┌───────────────────────┐
     │   Classical Layer 1   │                       │    Quantum Layer 2    │
     │   HMAC-SHA3-512       │                       │    QDS Token States   │
     │   (NIST FIPS 202)     │                       │    (|ψ_0> ... |ψ_k>)  │
     └───────────┬───────────┘                       └───────────┬───────────┘
                 │                                               │
                 │ Digest Matching                               │ Q-STAT Binomial Engine
                 │ hmac.compare_digest()                         │ (z-score, p-value, CI)
                 ▼                                               ▼
     ┌───────────────────────┐                       ┌───────────────────────┐
     │ classical_matched:    │                       │ quantum_assessment:   │
     │ True / False          │                       │ LEGITIMATE / MALICIOUS│
     └───────────┬───────────┘                       └───────────┬───────────┘
                 │                                               │
                 └───────────────────────┬───────────────────────┘
                                         │
                                         ▼
                         ┌───────────────────────────────┐
                         │  Hybrid Decision Matrix       │
                         │  Overall Verdict:             │
                         │  - Both Pass  -> LEGITIMATE   │
                         │  - Hash Fail  -> MALICIOUS    │
                         │  - Q-STAT Fail-> MALICIOUS    │
                         │  - Q Noise    -> SUSPICIOUS   │
                         └───────────────────────────────┘
```

### Formula 1: Classical HMAC-SHA3-512 Construction
Unlike SHA-2 (which uses the Merkle-Damgård construction and is vulnerable to length-extension attacks without HMAC wrapping), SHA-3 is built on the **Keccak cryptographic sponge function**:
* It operates on an internal state permutation of width $b = 1600\text{ bits}$ with rate $r = 576\text{ bits}$ and capacity $c = 1024\text{ bits}$ (for SHA3-512).
* The Hash-based Message Authentication Code (HMAC) binds the message payload $M$ to the signer's private seed $K$:
  $$\text{HMAC}_{K}(M) = \text{SHA3-512}\Big((K \oplus \text{opad}) \mathbin{\Vert} \text{SHA3-512}\big((K \oplus \text{ipad}) \mathbin{\Vert} M\big)\Big)$$
  where:
  * $\text{ipad} = 0x3636\dots36$ (inner padding)
  * $\text{opad} = 0x5C5C\dots5C$ (outer padding)
  * $\mathbin{\Vert}$ denotes byte concatenation.
* **Output:** A 512-bit (64-byte, 128-hex-character) cryptographic digest guaranteeing:
  * Collision resistance: $2^{256}$ operations.
  * Preimage resistance: $2^{512}$ operations.
  * Second-preimage resistance: $2^{512}$ operations.

### Formula 2: Constant-Time Digest Verification
A common vulnerability in naive cryptographic implementations is using standard string equality:
```python
# VULNERABLE TO TIMING ATTACKS:
if claimed_digest == expected_digest:  # Returns False on first mismatching character!
```
An attacker measuring nanosecond-level response times can discover the digest character-by-character by observing how long the comparison takes.
[`security/hybrid.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/hybrid.py) strictly uses **constant-time byte comparison**:
$$\text{compare\_digest}(a, b) = \left( \sum_{i=0}^{\text{len}-1} (a_i \oplus b_i) \right) == 0$$
Execution time is strictly invariant to where or whether a mismatch occurs, eliminating timing side-channels.

### Formula 3: Quantum Layer Verification (Q-STAT)
The quantum signature $\Sigma_{\text{QDS}}$ is verified using the statistical engine from Lesson 10:
$$\hat{e} = \frac{n_{\text{error}}}{N},\quad z = \frac{\hat{e} - p_0}{\sqrt{\frac{p_0(1-p_0)}{N}}}$$
$$\text{Quantum Verdict} = \begin{cases} 
\text{LEGITIMATE} & \text{if } z < 2.0 \\ 
\text{SUSPICIOUS} & \text{if } 2.0 \le z < 4.0 \\ 
\text{MALICIOUS} & \text{if } z \ge 4.0 
\end{cases}$$

### Formula 4: The Hybrid Decision Truth Table
The combined security engine evaluates the Cartesian product of both security layers:

| Classical Match ($C$) | Quantum Verdict ($Q$) | Overall Hybrid Verdict | Confidence | Security Summary |
| :---: | :---: | :---: | :---: | :--- |
| ❌ **False** | *Any* | **`MALICIOUS`** | $1.0$ | *Classical Integrity Failure: HMAC mismatch* |
| ✅ **True** | **`MALICIOUS`** | **`MALICIOUS`** | $Q.\text{conf}$ | *Quantum Security Breach: Classical valid, QDS forged* |
| ✅ **True** | **`SUSPICIOUS`** | **`SUSPICIOUS`** | $Q.\text{conf}$ | *Classical Valid. Elevated channel noise / disturbance* |
| ✅ **True** | **`LEGITIMATE`** | **`LEGITIMATE`** | $Q.\text{conf}$ | *Dual-Layer Verified: Both classical & quantum pass* |

---

## 🔬 4. Architectural Breakdown of `security/hybrid.py`

Let's examine how the Python implementation executes this dual verification.

### Class 1: `HybridVerificationResult` (Lines 20–33)
The audit result dataclass:
* `message: str`: The transaction payload.
* `signer_id: str`: The identity of the claimed signer (e.g. `"Alice"`).
* `classical_hash_matched: bool`: `True` if HMAC-SHA3-512 matched identically.
* `classical_digest: str`: Truncated hex digest (e.g. `"a3b9f10c82d4e7...` for clean dashboard display).
* `quantum_assessment: ThreatAssessment`: The full Q-STAT statistical diagnostic report.
* `overall_verdict: ThreatCategory`: The final hybrid verdict.
* `hybrid_confidence: float`: Numerical confidence ($0.0$ to $1.0$).
* `security_summary: str`: SIEM and audit text.

### Class 2: `HybridSignatureVerifier` (Lines 35–109)
The hybrid engine.

#### Method 1: `compute_classical_digest()` (Lines 43–50)
```python
@staticmethod
def compute_classical_digest(message: str, signer_seed: str) -> str:
    key_bytes = signer_seed.encode("utf-8")
    msg_bytes = message.encode("utf-8")
    return hmac.new(key_bytes, msg_bytes, hashlib.sha3_512).hexdigest()
```
* Binds the signer's private seed to the payload using Python's built-in, OpenSSL-backed `hashlib.sha3_512`.
* Computes an HMAC digest in a single, high-performance call.

#### Method 2: `verify_hybrid_signature()` (Lines 52–109)
Executes the two-step evaluation and synthesizes the hybrid verdict:

```python
# 1. Classical Layer Evaluation
expected_digest = self.compute_classical_digest(message, signer_seed)
classical_matched = hmac.compare_digest(claimed_classical_digest, expected_digest)

# 2. Quantum Layer Evaluation
quantum_assessment = self.detector.verify_signature_session(
    received_signature=received_quantum_signature,
    expected_signature=expected_quantum_signature,
    trials_per_token=trials_per_token,
    ambient_noise=ambient_noise
)

# 3. Hybrid Decision Logic
if not classical_matched:
    overall_verdict = ThreatCategory.MALICIOUS
    hybrid_confidence = 1.0
    summary = "Classical Integrity Failure: HMAC-SHA3-512 message digest mismatch. Message payload tampered."
elif quantum_assessment.verdict == ThreatCategory.MALICIOUS:
    overall_verdict = ThreatCategory.MALICIOUS
    hybrid_confidence = quantum_assessment.confidence
    summary = f"Quantum Security Breach: Classical hash valid, but Q-STAT rejected quantum states ({quantum_assessment.diagnostic_text})."
elif quantum_assessment.verdict == ThreatCategory.SUSPICIOUS:
    overall_verdict = ThreatCategory.SUSPICIOUS
    hybrid_confidence = quantum_assessment.confidence
    summary = "Classical Hash Valid. Quantum channel exhibits elevated noise / suspicious disturbance."
else:
    overall_verdict = ThreatCategory.LEGITIMATE
    hybrid_confidence = quantum_assessment.confidence
    summary = "Dual-Layer Verified: Both classical HMAC-SHA3-512 and quantum teleportation states verified authentic."
```

---

## ⚡ 5. Step-by-Step Code Execution Walkthrough

Let's trace three tests from [`tests/test_hybrid_mitigation.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/tests/test_hybrid_mitigation.py):

### Test 1: Honest Dual-Layer Verification (`test_hybrid_verification_honest_pass`)
* **Message:** `"Payload Data Block #101"`
* **Signer Seed:** `"alice_master_soc_seed_2026"`
* **Flow:**
  1. `compute_classical_digest` calculates HMAC-SHA3-512 over `"Payload Data Block #101"`.
  2. Alice generates 6 quantum tokens.
  3. `verify_hybrid_signature` is called:
     - `hmac.compare_digest()` returns `True` (`classical_matched = True`).
     - `QStatDetector` verifies 6 tokens across 50 trials (300 shots) at $1\%$ noise. Error rate is $\approx 1.0\% \ll 3.0\%$ baseline. $z$-score is negative ($\approx -2.0$). Verdict: `LEGITIMATE`.
  4. Hybrid decision engine evaluates:
     - `classical_matched == True`
     - `quantum_assessment.verdict == LEGITIMATE`
     - **Overall Verdict:** `ThreatCategory.LEGITIMATE`.
     - **Summary:** `"Dual-Layer Verified: Both classical HMAC-SHA3-512 and quantum teleportation states verified authentic."`

---

### Test 2: Classical Message Tampering (`test_hybrid_verification_classical_tampering_caught`)
* **Original Message:** `"Payload Data Block #101"`
* **Attacker Alteration:** `"Payload Data Block #101 [TAMPERED]"`
* **Quantum Tokens:** Left intact (or replayed).
* **Flow:**
  1. Recipient receives the altered payload and Alice's original digest.
  2. `compute_classical_digest` calculates HMAC-SHA3-512 over the altered message.
  3. Due to the avalanche effect of SHA-3, changing even one character flips over $50\%$ of the 512 bits in the hash!
  4. `hmac.compare_digest()` returns `False` (`classical_matched = False`).
  5. The hybrid engine immediately flags:
     - **Overall Verdict:** `ThreatCategory.MALICIOUS`.
     - **Confidence:** `1.0` ($100\%$).
     - **Summary:** `"Classical Integrity Failure: HMAC-SHA3-512 message digest mismatch. Message payload tampered."`
     - The altered payload is rejected instantly without needing to rely solely on the quantum layer!

---

### Test 3: Quantum Forgery with Valid Classical Digest (`test_hybrid_verification_quantum_forgery_caught`)
* **Message:** `"Payload Data Block #101"` (Untampered)
* **Classical Digest:** Valid HMAC computed by Alice.
* **Quantum Tokens:** Attacker intercepted Alice's quantum transmission and replaced them with forged random eigenstates (`AttackScenario.FORGERY`).
* **Flow:**
  1. `hmac.compare_digest()` returns `True` (`classical_matched = True`).
  2. `QStatDetector` measures the received quantum tokens against Alice's public basis.
  3. Measuring forged eigenstates in the conjugate basis causes a Born-rule $50\%$ error rate ($\hat{e} \approx 50.0\%$).
  4. Q-STAT calculates $z \approx +48.5 \ge 4.0$. Quantum Verdict: `ThreatCategory.MALICIOUS`.
  5. The hybrid engine evaluates:
     - `classical_matched == True`
     - `quantum_assessment.verdict == MALICIOUS`
     - **Overall Verdict:** `ThreatCategory.MALICIOUS`.
     - **Summary:** `"Quantum Security Breach: Classical hash valid, but Q-STAT rejected quantum states (Statistical Anomaly z=48.50)..."`
     - Even though the classical hash passed, the quantum defense-in-depth caught the forgery!

---

## ⚔️ 6. Hackathon Judge Defense & Viva Voce Q&A

### Q1: "If Quantum Digital Signatures offer information-theoretic security, why do you need classical HMAC-SHA3-512 at all?"
**Defense:**  
> *"Information-theoretic security guarantees that an attacker with infinite computing power cannot forge quantum states. However, in an engineering deployment, systems must be resilient against real-world operational realities:  
> 1. **Message Binding & High-Bandwidth Data:** A quantum signature token consists of fragile qubits. You cannot teleport a 50 GB database backup or a 10 MB legal PDF directly through a quantum channel. The classical layer hashes the large payload into a fixed 512-bit digest, and the quantum tokens sign that binding.  
> 2. **Defense-in-Depth:** If a physical fiber disruption or optical jamming attack elevates channel noise, the classical HMAC maintains cryptographic integrity while the quantum channel recalibrates.  
> 3. **Regulatory Compliance:** National Quantum Mission (NQM) and NIST guidelines mandate hybrid transitional architectures so organizations maintain certified classical compliance (FIPS 202) while integrating quantum security."*

### Q2: "Why did you choose SHA3-512 instead of SHA-256?"
**Defense:**  
> *"Two reasons:  
> 1. **Post-Quantum Security Margin:** Grover’s quantum search algorithm achieves a quadratic speedup on brute-force pre-image attacks. A 256-bit hash provides only 128 bits of post-quantum collision security. A 512-bit hash like SHA3-512 provides a full 256 bits of security even against a massive quantum computer running Grover’s algorithm!  
> 2. **Sponge Construction Immunity:** SHA-2 uses the Merkle-Damgård construction, which is susceptible to length-extension attacks if not carefully padded. SHA-3 is built on the Keccak sponge permutation ($b=1600$), which is structurally immune to length extension by design."*

### Q3: "What is a timing side-channel attack, and how is it prevented in `security/hybrid.py`?"
**Defense:**  
> *"If you compare two strings using Python's standard `==` operator, the CPU compares characters sequentially and returns `False` immediately upon the first non-matching byte. An attacker can precisely measure the verification latency: if the check takes 12 nanoseconds instead of 10 nanoseconds, they know the first byte was correct. By iterating over bytes, they can reconstruct the entire secret digest.  
> In [`security/hybrid.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/hybrid.py#L69), we use `hmac.compare_digest()`, which executes a constant-time XOR comparison across all bytes regardless of where differences occur, completely eliminating timing leakage."*

### Q4: "What happens if the classical hash passes, but the quantum channel exhibits elevated noise ($2.0 \le z < 4.0$)?"
**Defense:**  
> *"The hybrid engine classifies the overall verdict as `ThreatCategory.SUSPICIOUS`. The system does not immediately execute the high-value transaction, but it also does not permanently lock the user out.  
> Instead, it flags the transaction for automated baseline recalibration ([`security/calibrate.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/calibrate.py)) or requests a secondary multi-recipient verification exchange before clearing the payment."*

### Q5: "How does Q-HYBRID protect against a Man-in-the-Middle (MitM) who intercepts the classical network?"
**Defense:**  
> *"If a MitM intercepts the classical network and alters the message payload or replaces the classical hash, `hmac.compare_digest` fails immediately because the attacker does not possess Alice's private key seed.  
> If the MitM attempts to replay a previously captured classical hash and quantum signature, the Freshness Registry ([`security/freshness.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/freshness.py)) rejects the duplicate nonce.  
> If the MitM tries to forge the quantum states, the Born-rule $50\%$ error collapse trips the Q-STAT detector. The hybrid architecture covers all threat vectors."*

---

## 🔗 7. The Next Step in the Pipeline

With [`security/hybrid.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/hybrid.py), we have armed Q-Sentinel with a two-tier defense that bridges NIST classical cryptographic standards and quantum physics.

When a breach is detected by any of our watchtowers, what happens next? The system cannot just sit idle.
👉 **Lesson 21:** [`security/mitigation.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/mitigation.py)  
*(Automated Incident Response & Threat Mitigation: Dynamic signer quarantine, nonce revocation, Bell buffer purging, and generating Common Event Format [CEF] logs for enterprise SIEM integration).*
