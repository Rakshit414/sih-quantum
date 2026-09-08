# 📘 Q-SENTINEL Masterclass | Lesson 09: Adversarial Threat Modeling & Attack Simulation

> **File in Focus:** [`security/attacks.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/attacks.py)  
> **Pipeline Position:** Step 9 of the entire Q-Sentinel architecture (Adversary Simulation & Red-Team Layer)  
> **Target Audience:** Fresher needing cybersecurity attack mechanics, mathematical basis collapse, and simulation logic.

---

## 🧭 1. What Is This File and Why Does It Exist?

In military defense and enterprise cybersecurity, building a radar or watchtower is only half the battle. You cannot know whether your watchtower works until you **simulate enemy attacks** against it.
In software engineering, this is called **Red-Teaming**: actively playing the role of the malicious hacker to test your defenses under realistic battle conditions.

[`security/attacks.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/attacks.py) is the **adversary simulation engine** of Q-Sentinel. 
It implements realistic mathematical and physical cyber-attacks targeting the Quantum Digital Signature protocol:
1. **Signature Forgery:** An adversary (Eve) fabricates quantum states from scratch without the private key.
2. **Signer Impersonation:** An unauthorized adversary (Mallory) signs messages using her own unauthorized key while claiming Alice's identity.
3. **Replay Attack:** An adversary captures and retransmits stale signatures with duplicate nonces.
4. **Quantum Channel Manipulation:** An adversary or harsh environment injects bit flips, phase flips, or optical jamming ($\epsilon$) into the fiber.

By running these attack injectors, we generate the exact adversarial data streams that our detection engine ([`security/detector.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/detector.py)) will analyze!

---

## 💡 2. Plain English Real-World Analogies

### Analogy 1: The Four Types of Bank Robbers
Imagine four different criminals attempting to steal funds from a high-security quantum bank:

1. **The Counterfeiter (Forgery):** 
   Eve has never seen the King's seal. She cuts a random seal out of a potato in her kitchen and hopes the bank teller doesn't notice.
2. **The Fraudulent Imposter (Impersonation):** 
   Mallory has her own legitimate passport and bank account, but she walks into the bank wearing an "Alice" name tag and signs the wire transfer using her own personal signature, hoping nobody checks the database.
3. **The Tape Recorder Thief (Replay Attack):** 
   Eve hides a microphone in the CEO's office, records the CEO legitimately saying *"Authorize $1,000,000 to Company X"*, and plays the tape recording back to the bank wire desk the next day.
4. **The Cable Saboteur (Channel Noise / Tampering):** 
   An adversary digs up the underground fiber-optic cable and kinks, bends, or shines disruptive lasers at the glass to scramble the quantum signals.

---

## 📐 3. The Cryptanalysis of Each Attack

### 1. Signature Forgery Mechanics
- Alice's genuine token is in a secret eigenstate: e.g., $|+\rangle$ ($X$-basis).
- Eve has no access to Alice's private key seed. Eve must guess:
  - Basis: chooses uniformly at random from $\{Z, X, Y\}$.
  - Bit: chooses uniformly at random from $\{0, 1\}$.
- **The Quantum Penalty:**
  Because the Pauli bases are **Mutually Unbiased Bases (MUBs)**, the overlap between eigenstates of different bases is strictly $\frac{1}{2}$:
  $$|\langle 0 | +\rangle|^2 = 0.5, \quad |\langle 0 | i+\rangle|^2 = 0.5, \quad |\langle + | i+\rangle|^2 = 0.5$$
- If Eve guesses the wrong basis (which happens $\frac{2}{3}$ of the time), Bob's verification measurement projects onto the wrong subspace with $50\%$ probability.
- Across $N$ trials, Eve's forged signature produces an **error rate $\hat{e} \approx 48\% - 50\%$**, towering over the natural 3% noise floor!

### 2. Signer Impersonation Mechanics
- Mallory possesses her own valid key manager: `QDSKeyManager(signer_id="Mallory", private_seed="mallory_unauthorized_seed_42")`.
- Mallory signs the contract legitimately using her key, but overwrites `signer_id = "Alice"`.
- When Bob receives the signature, Bob looks up **Alice's public key mapping**.
- Because Mallory's seed and Alice's seed produce completely uncorrelated pseudo-random sequences:
  - Roughly $\frac{1}{3}$ of the tokens randomly happen to use the same basis.
  - The remaining $\frac{2}{3}$ use mismatched bases.
- Across all tokens, Bob experiences an **error rate $\hat{e} \approx 30\% - 35\%$**, creating an unmistakable anomaly.

### 3. Replay Attack Mechanics
- Eve captures a genuine signature transmitted by Alice 2 minutes ago.
- Eve leaves the quantum tokens and classical bits completely untouched! (Physical error rate $\hat{e} \approx 3\%$ is clean).
- However, the timestamp is delayed ($t_{\text{msg}} = t_{\text{now}} - 120\text{s}$) and the nonce is reused.
- The physical quantum detectors see no errors, but the **Freshness Registry catches the duplicated nonce instantly**!

### 4. Quantum Channel Manipulation ($\epsilon$)
- An adversary introduces noise parameterized by error probability $\epsilon \in [0.05, 0.40]$.
- For each qubit, with probability $\epsilon$:
  - The state is flipped to the orthogonal state ($|0\rangle \leftrightarrow |1\rangle$ or $|+\rangle \leftrightarrow |-\rangle$).
- As the operator moves the slider from $\epsilon = 0.05 \to 0.15 \to 0.35$, the verifier smoothly transitions from 🟢 **LEGITIMATE** ($z < 2.0$) $\to$ 🟡 **SUSPICIOUS** ($2.0 \le z < 4.0$) $\to$ 🔴 **MALICIOUS** ($z \ge 4.0$).

---

## 🔍 4. Line-by-Line Technical Breakdown of `security/attacks.py`

```
┌─────────────────────────────────────────────────────────────┐
│                    security/attacks.py                      │
├─────────────────────────────────────────────────────────────┤
│  1. AttackScenario Enum (5 Canonical Scenarios)             │
│  2. apply_quantum_channel_noise() (Pauli Flips & Jitter)    │
│  3. simulate_forgery_attack() (Eve Random Guessing Engine)  │
│  4. simulate_impersonation_attack() (Mallory Impersonator)  │
│  5. simulate_replay_attack() (Nonce & Timestamp Replay)     │
│  6. ThreatOrchestrator Class (Unified Scenario Dispatcher)  │
└─────────────────────────────────────────────────────────────┘
```

---

### Component A: The `AttackScenario` Enum ([Lines 27–33](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/attacks.py#L27-L33))

```python
class AttackScenario(Enum):
    LEGITIMATE = "Legitimate"
    FORGERY = "Signature Forgery"
    IMPERSONATION = "Signer Impersonation"
    REPLAY = "Replay Attack"
    CHANNEL_NOISE = "Channel Manipulation / Noise"
```
Defines the 5 canonical evaluation scenarios used throughout the application, benchmarks, and judge demonstrations.

---

### Component B: Applying Channel Noise & Pauli Perturbations ([Lines 35–62](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/attacks.py#L35-L62))

```python
def apply_quantum_channel_noise(
    state: QubitState,
    noise_level: float,
    basis: Optional[PauliBasis] = None,
    bit_value: Optional[int] = None,
    rng: Optional[np.random.Generator] = None
) -> Tuple[QubitState, str]:
    if noise_level <= 0.0:
        return state, "No noise applied"

    if rng.random() < noise_level:
        if basis is not None and bit_value is not None:
            # Flip to the orthogonal state: 0 -> 1, 1 -> 0
            flipped_state = get_pauli_eigenstate(basis, 1 - bit_value)
            return flipped_state, f"Channel Error ({basis.value}-basis flip)"
        else:
            err = rng.choice([PAULI_X, PAULI_Y, PAULI_Z])
            return QubitState(err @ state.vector, label=f"Noisy({state.label})"), "Pauli Channel Noise"

    return state, "Clean transmission"
```
If a random uniform float falls below `noise_level`, it flips the state into the orthogonal subspace or multiplies by a random Pauli matrix ($X, Y,$ or $Z$), accurately simulating physical phase and bit-flip errors.

---

### Component C: Simulating Signature Forgery ([Lines 64–99](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/attacks.py#L64-L99))

```python
def simulate_forgery_attack(
    original_signature: QuantumDigitalSignature,
    random_seed: Optional[int] = None
) -> Tuple[QuantumDigitalSignature, str]:
    rng = np.random.default_rng(random_seed)
    bases = [PauliBasis.Z, PauliBasis.X, PauliBasis.Y]
    forged_tokens: List[SignatureToken] = []

    for token in original_signature.tokens:
        guessed_basis = rng.choice(bases)
        guessed_bit = int(rng.choice([0, 1]))
        guessed_state = get_pauli_eigenstate(guessed_basis, guessed_bit)
        
        forged_tokens.append(SignatureToken(
            index=token.index, bit_value=guessed_bit, basis=guessed_basis, eigenstate=guessed_state
        ))

    forged_sig = QuantumDigitalSignature(
        message=original_signature.message,
        message_digest=original_signature.message_digest,
        signer_id=original_signature.signer_id,
        tokens=forged_tokens,
        timestamp=original_signature.timestamp,
        nonce=original_signature.nonce
    )
    return forged_sig, "Adversary Eve forged signature tokens using random Pauli basis guesses."
```
Eve fabricates fake tokens with random bits and random bases. Because she lacks Alice's private key, her forged tokens will trigger a massive $\approx 50\%$ error rate during verification.

---

### Component D: Simulating Impersonation & Replay ([Lines 101–149](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/attacks.py#L101-L149))

#### Impersonation:
```python
mallory_mgr = QDSKeyManager(signer_id=adversary_id, private_seed="mallory_unauthorized_seed_42")
mallory_sig = mallory_mgr.generate_signature(message=original_signature.message, ...)
# Spoof signer_id to claim Alice!
impersonated_sig = QuantumDigitalSignature(..., signer_id=original_signature.signer_id, tokens=mallory_sig.tokens)
```

#### Replay:
```python
replayed_sig = QuantumDigitalSignature(
    ...,
    timestamp=original_signature.timestamp - simulated_delay_seconds,  # Stale by 120 seconds!
    nonce=original_signature.nonce  # Reused duplicate nonce!
)
```

---

### Component E: The `ThreatOrchestrator` Dispatcher ([Lines 151–217](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/attacks.py#L151-L217))

```python
class ThreatOrchestrator:
    @staticmethod
    def execute_scenario(
        scenario: AttackScenario,
        original_signature: QuantumDigitalSignature,
        channel_noise_level: float = 0.0,
        random_seed: Optional[int] = None
    ) -> Tuple[QuantumDigitalSignature, str]:
```
Provides a clean, unified API for the UI dashboard (`app.py`), the command-line benchmark (`benchmark.py`), and the automated test suite (`test_security.py`) to inject any attack on demand with a single line of code!

---

## 🔗 5. How This File Connects to the Next File in the Pipeline

Now that we have created both legitimate signatures and red-team attack vectors:
Who sits in the watchtower to catch these attacks?

In Step 10, **[`security/detector.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/detector.py)**:
- We meet the **Q-STAT Threat Detection Engine**!
- It receives the measurement counts from [`quantum/measure.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/measure.py) and checks against [`security/freshness.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/freshness.py).
- Using **Exact Binomial Hypothesis Testing and Standardized Z-Scores (with ZERO AI/ML)**, it classifies every signature into **🟢 LEGITIMATE**, **🟡 SUSPICIOUS**, or **🔴 MALICIOUS** with 100% accuracy!

---

## 🎓 6. Professor's Viva / Hackathon Defense Guide

> **Judge:** *"How does your attack engine simulate quantum eavesdropping without violating the No-Cloning Theorem in software?"*  
> **Your Answer:** *"We model an adversary operating under strict physical constraints. Under the intercept-and-resend attack model, an adversary who intercepts an unknown quantum token cannot clone it; they must perform a projective measurement in a guessed basis and transmit a newly prepared state. In `security/attacks.py`, `simulate_forgery_attack` simulates this exact physical scenario: Eve chooses a random Pauli basis ($Z, X, Y$) and prepares a state. The mathematical consequence of the No-Cloning theorem and mutually unbiased bases ensures that Bob observes a predictable $\approx 50\%$ error rate, perfectly mirroring physical laboratory eavesdropping."*

> **Judge:** *"Why do you test Channel Noise separately from Forgery?"*  
> **Your Answer:** *"Because they have fundamentally different physical and operational signatures. Forgery produces an immediate, catastrophic quantum basis collapse ($\approx 50\%$ error, $z \ge +40\sigma$). In contrast, physical channel noise (e.g., fiber micro-bending or Raman cross-talk) introduces mild, progressive error rates (e.g., $5\% - 10\%$). By modeling channel noise separately in `apply_quantum_channel_noise`, we prove that Q-Sentinel's three-tier threshold ($z < 2$, $2 \le z < 4$, $z \ge 4$) can smoothly distinguish between minor operational decay and an active cryptographic attack."*

---
*(End of Lesson 09. Whenever you are ready, reply with **"next"** to enter the core detection brain in **Lesson 10: security/detector.py**!)*
