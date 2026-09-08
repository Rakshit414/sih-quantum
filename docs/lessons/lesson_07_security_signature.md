# 📘 Q-SENTINEL Masterclass | Lesson 07: Quantum Digital Signature (QDS) Engine

> **File in Focus:** [`security/signature.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/signature.py)  
> **Pipeline Position:** Step 7 of the entire Q-Sentinel architecture (First file in the Cryptography & Security Layer)  
> **Target Audience:** Fresher transitioning from pure physics into cybersecurity and cryptographic protocols.

---

## 🧭 1. What Is This File and Why Does It Exist?

In the first 6 lessons, we built a virtual quantum physics laboratory: qubits, Pauli matrices, Bell entanglement, teleportation, projective measurements, tomography, and multi-hop repeater meshes.

Now, we put this physics to work for cybersecurity!

In classical computer security, when you sign a PDF or authorize a cryptocurrency transaction, your computer uses algorithms like **RSA** or **ECDSA** (Elliptic Curve Digital Signature Algorithm). These algorithms rely on mathematical puzzles (like factoring huge prime numbers) that are difficult for today's laptops.
However, **Shor's Algorithm** running on a future quantum computer will solve those mathematical puzzles in seconds, rendering every RSA and ECDSA signature instantly forgeable!

**Quantum Digital Signatures (QDS)** replace mathematical puzzles with the fundamental laws of quantum physics. 
Instead of signing a document with a mathematical string of numbers, Alice signs the document with a chain of **individual quantum particles (qubits)** prepared in secret Pauli eigenstates. 
Because of the **No-Cloning Theorem**, no adversary can copy or forge Alice's signature without leaving physical traces of disturbance.

[`security/signature.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/signature.py) is the **signer's pen**. It takes any arbitrary classical text message (e.g., *"Transfer $500,000 to Account #10492"*), hashes it using SHA-256, translates the hash into an array of quantum Pauli eigenstates using Alice's private key, and teleports the signature qubits to Bob!

---

## 💡 2. Plain English Real-World Analogies

### Analogy 1: The King's Royal Wax Seal with Living DNA
* In medieval times, a King verified a royal decree by pressing his personal signet ring into melted red wax. A clever forger could carve a duplicate ring and stamp fake wax seals.
* In classical computing (RSA), a signature is just a string of digital numbers. If a quantum computer finds the private key, it can stamp infinite fake seals.
* In a **Quantum Digital Signature (QDS)**, the King presses his ring into wax, but also infuses the wax with a unique chain of living, delicate microscopic organisms (quantum particles in superposition).
* If a forger tries to inspect, measure, or clone the organisms, **the organisms die and change color** (wave function collapse). When the recipient receives the seal, they immediately see that the organisms have collapsed into errors, exposing the forgery!

### Analogy 2: Why We Don't Send 1,000,000 Qubits
Imagine you want to sign a 500-page legal contract. 
* Do you need to convert all 500 pages of text into millions of quantum particles? No! Sending millions of qubits would be slow and expensive.
* Instead, Alice passes the 500 pages through a standard cryptographic hash function (**SHA-256**). 
* SHA-256 shrinks the entire 500-page document into a compact, 256-bit digital fingerprint (64 hexadecimal characters).
* If anyone changes even a single comma in the 500-page document, the SHA-256 fingerprint changes completely (the avalanche effect).
* Alice only needs to sign this compact fingerprint using her quantum tokens!

---

## 📐 3. The Architecture of a Quantum Digital Signature

The signature generation process follows a clean 4-step pipeline:

```
[Classical Message] 
       │
       ▼
[SHA-256 Cryptographic Digest] (256 bits)
       │
       ▼ + [Alice's Private Key Seed]
[Deterministic Bit & Basis Derivation]
       │
       ▼
[Array of Pauli Eigenstates] {|s_1⟩, |s_2⟩, ..., |s_m⟩}
       │
       ▼
[Quantum Teleportation Distribution to Bob]
```

### The Secret Mapping: Why Knowing the Bit Value Is Not Enough
Suppose token $i$ has bit value `0`. What quantum state does Alice prepare?
- If Alice's private seed selects the **Z-basis**: state is $|0\rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$
- If Alice's private seed selects the **X-basis**: state is $|+\rangle = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ 1 \end{pmatrix}$
- If Alice's private seed selects the **Y-basis**: state is $|i+\rangle = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ j \end{pmatrix}$

Even if an eavesdropper (Eve) knows that the message bit is `0`, **Eve has no idea which of the 3 bases Alice used**!
If Eve guesses wrong, her measurement collapses the state and triggers an immediate 50% error rate on Bob's end.

---

## 🔍 4. Line-by-Line Technical Breakdown of `security/signature.py`

```
┌─────────────────────────────────────────────────────────────┐
│                    security/signature.py                    │
├─────────────────────────────────────────────────────────────┤
│  1. SignatureToken Dataclass                                │
│  2. QuantumDigitalSignature Dataclass                       │
│  3. QDSKeyManager Class                                     │
│     - __init__(signer_id, private_seed)                     │
│     - generate_signature(message, num_tokens)               │
│  4. TransmittedQDS Dataclass                                │
│  5. distribute_signature_via_teleportation() Engine         │
└─────────────────────────────────────────────────────────────┘
```

---

### Component A: The `SignatureToken` Dataclass ([Lines 20–25](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/signature.py#L20-L25))

```python
@dataclass
class SignatureToken:
    index: int
    bit_value: int
    basis: PauliBasis
    eigenstate: QubitState
```
Represents an individual quantum token:
- `index`: The sequential position of this token in the signature ($0, 1, 2, \dots, m-1$).
- `bit_value`: The classical bit (0 or 1) derived from the message hash.
- `basis`: The [`PauliBasis`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/state.py#L13) ($Z, X$, or $Y$) determined by Alice's private seed.
- `eigenstate`: The physical [`QubitState`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/state.py#L37) particle generated for transmission.

---

### Component B: The `QuantumDigitalSignature` Envelope ([Lines 28–44](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/signature.py#L28-L44))

```python
@dataclass
class QuantumDigitalSignature:
    message: str
    message_digest: str
    signer_id: str
    tokens: List[SignatureToken]
    timestamp: float = field(default_factory=time.time)
    nonce: str = field(default_factory=lambda: secrets.token_hex(16))
```
This is the complete cryptographic envelope:
1. `message`: The classical payload string.
2. `message_digest`: The SHA-256 hexadecimal hash string.
3. `signer_id`: The identity of the signer (e.g., `"Alice"`).
4. `tokens`: The list of quantum signature tokens.
5. `timestamp`: High-precision POSIX timestamp marking the exact second the signature was minted.
6. `nonce`: A 32-character cryptographically secure random hexadecimal string (`secrets.token_hex(16)`). **This nonce is used in Lesson 08 to defeat replay attacks!**

---

### Component C: The `QDSKeyManager` Engine ([Lines 46–90](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/signature.py#L46-L90))

```python
class QDSKeyManager:
    def __init__(self, signer_id: str, private_seed: Optional[str] = None):
        self.signer_id = signer_id
        self.private_seed = private_seed or secrets.token_hex(32)
```
Initializes the signer's identity and private cryptographic seed. If no seed is provided, it generates a 256-bit cryptographically secure seed (`secrets.token_hex(32)`).

#### Signature Generation Logic:
```python
def generate_signature(self, message: str, num_tokens: int = 8) -> QuantumDigitalSignature:
    # 1. Compute SHA-256 digest of classical message
    digest = hashlib.sha256(message.encode("utf-8")).hexdigest()
    digest_bytes = bytes.fromhex(digest)
    seed_bytes = bytes.fromhex(hashlib.sha256(self.private_seed.encode("utf-8")).hexdigest())

    tokens: List[SignatureToken] = []
    bases = [PauliBasis.Z, PauliBasis.X, PauliBasis.Y]

    for i in range(num_tokens):
        # 2. Extract deterministic bit from message digest
        bit_val = (digest_bytes[i % len(digest_bytes)] >> (i % 8)) & 1
        
        # 3. Derive deterministic basis from private seed
        basis_idx = (seed_bytes[i % len(seed_bytes)] + i) % 3
        basis = bases[basis_idx]

        # 4. Fetch the canonical physical quantum eigenstate
        state = get_pauli_eigenstate(basis, bit_val)
        tokens.append(SignatureToken(index=i, bit_value=bit_val, basis=basis, eigenstate=state))

    return QuantumDigitalSignature(...)
```

#### How the deterministic derivation works:
- **`bit_val` extraction:** Picks the $i$-th byte of the SHA-256 digest, bit-shifts by `(i % 8)`, and bitwise-ANDs with `1`. This extracts one bit directly from the message payload.
- **`basis` derivation:** Takes the $i$-th byte of the private key seed, adds index $i$, and takes modulo 3 (`% 3`). This produces an index `0, 1, or 2` mapping to $Z, X$, or $Y$.
- **Result:** The quantum state is mathematically bound to both the **content of the message** and the **private key of Alice**.

---

### Component D: Teleportation Distribution ([Lines 93–124](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/signature.py#L93-L124))

```python
def distribute_signature_via_teleportation(
    signature: QuantumDigitalSignature,
    random_seed: Optional[int] = None
) -> TransmittedQDS:
    results: List[TeleportationResult] = []
    received_states: List[QubitState] = []
    
    for i, token in enumerate(signature.tokens):
        res = teleport_qubit(token.eigenstate, random_seed=seed)
        results.append(res)
        received_states.append(res.recovered_state)
        
    avg_fidelity = float(np.mean([r.fidelity for r in results])) if results else 1.0
    return TransmittedQDS(
        original_signature=signature,
        teleportation_results=results,
        received_states=received_states,
        average_teleportation_fidelity=avg_fidelity
    )
```
- Alice does not send raw photons through open space.
- She loops through each token in the signature and teleports it qubit-by-qubit using [`teleport_qubit`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/teleport.py#L45).
- Bob reconstructs every state in his lab, ready for verification!

---

## 🔗 5. How This File Connects to the Next File in the Pipeline

Notice that every [`QuantumDigitalSignature`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/signature.py#L28) includes:
- A `timestamp` (the exact time it was created)
- A `nonce` (a unique 32-character random string)

In Step 8, **[`security/freshness.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/freshness.py)**:
- We build the **Anti-Replay Registry**.
- Bob uses the nonce and timestamp to guarantee that an adversary cannot record a genuine signature from last week and replay it today to authorize an unauthorized wire transfer!

---

## 🎓 6. Professor's Viva / Hackathon Defense Guide

> **Judge:** *"Why is a Quantum Digital Signature (QDS) superior to classical RSA or ECDSA signatures?"*  
> **Your Answer:** *"Classical digital signatures rely on computational hardness assumptions (e.g., factoring large integers or computing discrete logarithms). In 1994, Peter Shor proved that a cryptographically relevant quantum computer can break these problems in polynomial time using Shor's algorithm.  
> In contrast, Quantum Digital Signatures offer **Information-Theoretic Security**. The signature consists of physical quantum eigenstates. Under the No-Cloning theorem and the uncertainty principle, an adversary cannot copy or measure these states without creating physical collapse errors ($\approx 50\%$). Even an adversary with infinite computing power cannot break a QDS signature without violating the fundamental laws of quantum physics."*

> **Judge:** *"How does your system prevent an attacker from modifying the classical message without touching the qubits?"*  
> **Your Answer:** *"Because the quantum tokens are derived directly from the SHA-256 digest of the classical message payload: `bit_val = (digest_bytes[i] >> (i % 8)) & 1`. If an attacker tampers with even a single bit of the classical message text, the SHA-256 digest completely changes. When the verifier checks the received quantum tokens against the expected digest, the bit values will disagree, causing projective measurement collapse and triggering a malicious alert."*

---
*(End of Lesson 07. Whenever you are ready, reply with **"next"** to proceed to **Lesson 08: security/freshness.py**!)*
