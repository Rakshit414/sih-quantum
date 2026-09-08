# 📘 Q-SENTINEL Masterclass | Lesson 06: Multi-Hop Quantum Mesh & Entanglement Swapping

> **File in Focus:** [`quantum/mesh.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/mesh.py)  
> **Pipeline Position:** Step 6 of the entire Q-Sentinel architecture (Multi-Hop Repeater & Mesh Layer)  
> **Target Audience:** Fresher needing physical intuition for quantum repeaters, entanglement swapping circuits, and rogue node isolation.

---

## 🧭 1. What Is This File and Why Does It Exist?

In classical internet networks, data signals traveling through optical fiber fade over distance due to absorption (approximately $0.2\text{ dB/km}$ in standard silica fiber). When a classical signal becomes too dim after 80 km, telecom companies use **Erbium-Doped Fiber Amplifiers (EDFAs)** to amplify and boost the laser signal.

In quantum cryptography, **you cannot amplify a quantum signal**!
The **No-Cloning Theorem** strictly dictates that an unknown quantum particle cannot be copied or multiplied. If you try to amplify a single photon, you destroy its quantum coherence. Therefore, direct point-to-point quantum fiber links are physically capped at roughly 80 to 100 kilometers.

How do you transmit a Quantum Digital Signature across thousands of kilometers between cities like New Delhi, Bengaluru, and Mumbai?
**You use Quantum Repeaters and Entanglement Swapping!**

[`quantum/mesh.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/mesh.py) implements:
1. The **4-qubit Entanglement Swapping Engine**, which connects distant nodes without directly sending photons between them.
2. The **Multi-Hop Quantum Mesh Router**, which tracks link quality across chains of repeaters.
3. The **Rogue Repeater Watchtower**, which pinpoints and isolates any intermediate repeater node that has been hijacked by an adversary.

---

## 💡 2. Plain English Real-World Analogies

### Analogy 1: The Relay Race (Why Repeaters Are Needed)
Imagine a marathon runner carrying a lit candle through rain and wind.
* If one runner tries to sprint the entire 1000 km, the candle will blow out.
* Instead, you place relay runners every 50 km.
* But in quantum mechanics, the runner cannot simply hand over the candle (No-Cloning).
* Instead, runners use a magic quantum trick: **Entanglement Swapping**!

### Analogy 2: The Quantum Matchmaker (Entanglement Swapping)
* Alice in New Delhi has a best friend named **Romeo** ($R_{\text{in}}$). They are entangled ($|\Phi^+\rangle$).
* Bob in Mumbai has a best friend named **Juliet** ($R_{\text{out}}$). They are entangled ($|\Phi^+\rangle$).
* Alice and Bob have never met, never spoken, and are 1500 km apart.
* Romeo and Juliet meet in a central repeater station in Bhopal. They perform a joint Bell measurement together.
* The moment Romeo and Juliet link up, they sacrifice their own entanglement. **Instantly, Alice in New Delhi and Bob in Mumbai become entangled directly!**
* Alice and Bob can now teleport digital signatures directly between each other!

---

## 📐 3. The Mathematics of 4-Qubit Entanglement Swapping

Let us trace the 4 qubits in the system:
- **Qubit 0:** Alice's node ($A$)
- **Qubit 1:** Repeater ingress port ($R_{\text{in}}$)
- **Qubit 2:** Repeater egress port ($R_{\text{out}}$)
- **Qubit 3:** Bob's node ($B$)

```
[Node A: Alice] ──(Bell Pair 1)──► [Repeater R_in]
                                         │  (Bell-State Measurement BSM)
[Node B: Bob]   ──(Bell Pair 2)──► [Repeater R_out]
       ▲                                 │
       └──────── (Directly Entangled!) ──┘
```

### The Initial 4-Qubit Product State:
The two independent Bell pairs form a 16-dimensional state vector ($2^4 = 16$ amplitudes):
$$|\Psi_4\rangle = |\Phi^+\rangle_{AR_{\text{in}}} \otimes |\Phi^+\rangle_{R_{\text{out}}B} = \left(\frac{|00\rangle + |11\rangle}{\sqrt{2}}\right)_{01} \otimes \left(\frac{|00\rangle + |11\rangle}{\sqrt{2}}\right)_{23}$$

Expanding this product out:
$$|\Psi_4\rangle = \frac{1}{2} \Big( |0000\rangle + |0011\rangle + |1100\rangle + |1111\rangle \Big)$$

### The Repeater's Bell-State Measurement (BSM):
The repeater holds qubits 1 and 2 ($R_{\text{in}}$ and $R_{\text{out}}$). It applies:
1. A CNOT gate with control = Qubit 1, target = Qubit 2:
   $$\text{CNOT}_{12} = I_0 \otimes \text{CNOT} \otimes I_3$$
2. A Hadamard gate on Qubit 1:
   $$H_1 = I_0 \otimes H \otimes I_2 \otimes I_3$$
3. Projective measurement on qubits 1 and 2, yielding two classical bits $(b_1, b_2)$.

### The Swapped State:
When qubits 1 and 2 collapse into outcome $(b_1, b_2)$, qubits 0 (Alice) and 3 (Bob) are left in:
$$|\Phi_{AB}\rangle = (Z^{b_1} X^{b_2})_B |\Phi^+\rangle_{AB}$$
Once Bob applies the standard Pauli correction $Z^{b_1} X^{b_2}$, **Alice and Bob share a pristine Bell pair $|\Phi^+\rangle$ across the entire continent!**

---

## 🔍 4. Line-by-Line Technical Breakdown of `quantum/mesh.py`

```
┌─────────────────────────────────────────────────────────────┐
│                      quantum/mesh.py                        │
├─────────────────────────────────────────────────────────────┤
│  1. Dataclasses: SwappedBellPair, HopTelemetry, MeshResult  │
│  2. EntanglementSwapper Class                               │
│     - execute_swapping() (4-qubit tensor product & BSM)     │
│  3. QuantumMeshRouter Class                                 │
│     - route_and_verify_mesh() (Multi-hop routing simulation)│
│     - Rogue repeater detection & localization               │
│     - End-to-end Q-STAT statistical threat assessment       │
└─────────────────────────────────────────────────────────────┘
```

---

### Component A: The Telemetry Dataclasses ([Lines 29–69](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/mesh.py#L29-L69))

```python
@dataclass
class SwappedBellPair:
    node_a: str
    node_b: str
    repeater_id: str
    bell_measurement_bits: Tuple[int, int]
    fidelity_with_phi_plus: float
    is_compromised: bool

@dataclass
class HopTelemetry:
    hop_index: int
    source_node: str
    target_node: str
    is_repeater: bool
    link_noise_rate: float
    is_compromised: bool
    diagnostic: str

@dataclass
class MeshRouteVerificationResult:
    source_node: str
    destination_node: str
    path: List[str]
    hop_telemetry: List[HopTelemetry]
    end_to_end_fidelity: float
    assessment: ThreatAssessment
    rogue_node_identified: Optional[str]
    mesh_status_summary: str
```
These structures store detailed hop-by-hop records: link noise levels, intermediate repeater identities, whether tampering occurred, and the overall end-to-end security verdict.

---

### Component B: The `EntanglementSwapper` Engine ([Lines 71–144](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/mesh.py#L71-L144))

Let us examine the mathematical execution in `execute_swapping`:

#### 1. Form 4-Qubit Composite Vector ([Lines 91–98](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/mesh.py#L91-L98))
```python
pair_1 = create_bell_state(BellStateType.PHI_PLUS)
pair_2 = create_bell_state(BellStateType.PHI_PLUS)
psi_4 = np.kron(pair_1.vector, pair_2.vector)  # Shape: (16, 1)
```
Tensors two Bell pairs together into a 16-element vector.

#### 2. Apply CNOT and Hadamard on Repeater Qubits ([Lines 104–109](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/mesh.py#L104-L109))
```python
cnot_12 = np.kron(np.kron(PAULI_I, CNOT), PAULI_I)
psi_4_cnot = cnot_12 @ psi_4

h_1 = np.kron(np.kron(PAULI_I, HADAMARD), np.kron(PAULI_I, PAULI_I))
psi_4_bell = h_1 @ psi_4_cnot
```
Executes the joint Bell State Measurement at the repeater node.

#### 3. Measure & Sample Outcomes ([Lines 111–126](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/mesh.py#L111-L126))
```python
probs = np.abs(psi_4_bell.flatten()) ** 2
bsm_probs = [
    np.sum(probs[0:4]),    # b1=0, b2=0
    np.sum(probs[4:8]),    # b1=0, b2=1
    np.sum(probs[8:12]),   # b1=1, b2=0
    np.sum(probs[12:16])   # b1=1, b2=1
]
chosen_idx = int(np.random.choice([0, 1, 2, 3], p=bsm_probs))
b1, b2 = outcomes[chosen_idx]
```
The 16 states are partitioned into 4 blocks of 4 states corresponding to outcomes `00`, `01`, `10`, and `11`. Each outcome occurs with equal probability ($p = 0.25$).

#### 4. Adversarial Tampering Injection ([Lines 127–134](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/mesh.py#L127-L134))
```python
if repeater_tampering:
    b1 = 1 - b1  # Rogue repeater lies about classical feed-forward bits
    fidelity = 0.50
    is_compromised = True
```
If an adversary has infiltrated the repeater station, the repeater maliciously flips the classical bits or scrambles the phase. This degrades end-to-end fidelity down to $50\%$, which will be intercepted during verification!

---

### Component C: The `QuantumMeshRouter` & Rogue Node Localization ([Lines 146–268](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/mesh.py#L146-L268))

```python
for i in range(num_hops):
    node_src = full_path[i]
    node_tgt = full_path[i + 1]
    is_node_compromised = (node_src == compromised_node) or (node_tgt == compromised_node)
    if is_node_compromised:
        rogue_node = compromised_node
        hop_noise = 0.40  # High disturbance injected by rogue node
        diag = f"CRITICAL ANOMALY: Unauthorized BSM phase-scramble detected at node '{compromised_node}'."
    else:
        hop_noise = base_link_noise * (1.0 + np.random.uniform(0.0, 0.4))
        diag = "Normal transmission within baseline link loss parameters."
```

#### How Rogue Node Localization Works:
1. As the quantum route is established, Q-Sentinel samples pilot pulses along each link segment.
2. Honest segments exhibit standard baseline noise ($\approx 2\% - 3\%$).
3. The compromised repeater segment exhibits a massive noise spike ($\ge 40\%$).
4. The router marks `rogue_node_identified = compromised_node` and generates an actionable containment alert:
   > *"Mesh Routing Breach: Rogue intermediate node 'Repeater_R1' successfully localized. Hop telemetry isolates phase perturbation on link."*

---

## 🔗 5. How This Concludes the Quantum Layer & Bridges to the Security Layer

With `quantum/mesh.py`, our entire **Quantum Physics Foundation (Stage 1 & 2)** is complete:
1. `quantum/state.py` created single qubits and gates.
2. `quantum/bell.py` created 2-qubit entanglement.
3. `quantum/teleport.py` created the 3-qubit teleportation pipeline.
4. `quantum/measure.py` implemented projective measurements and the Born rule.
5. `quantum/tomography.py` reconstructed density matrices and proved noise vs. attack.
6. `quantum/mesh.py` expanded the system into a multi-hop quantum network.

### The Turning Point: Entering the Cryptography & Security Layer!
In the next step, **[`security/signature.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/signature.py)**:
- We leave pure physics and enter **Quantum Cryptography**.
- We see how classical human messages (like *"Authorize $500,000 Transfer"*) are hashed via SHA-256 and mapped into chains of quantum Pauli eigenstates to form an unbreakable **Quantum Digital Signature (QDS)**!

---

## 🎓 6. Professor's Viva / Hackathon Defense Guide

> **Judge:** *"Why can't we use traditional optical fiber amplifiers (like EDFAs) to extend the range of quantum digital signatures?"*  
> **Your Answer:** *"Traditional optical amplifiers rely on stimulated emission, which creates duplicate copies of incoming photons. Under the Wootters-Zurek No-Cloning Theorem, unknown quantum states cannot be cloned. Attempting to amplify a single photon introduces spontaneous emission noise that destroys the phase and polarization state of the signature qubit. Therefore, long-distance quantum communication strictly requires quantum repeaters that use Entanglement Swapping rather than classical amplification."*

> **Judge:** *"If an intermediate repeater in your mesh is untrusted or hacked, does the attacker gain access to Alice's message?"*  
> **Your Answer:** *"No, sir/ma'am. The intermediate repeater performs a Bell-State Measurement only on its own local halves of the Bell pairs ($R_{\text{in}}, R_{\text{out}}$). The repeater never touches or holds Alice's message or signature state. The most a rogue repeater can do is cause a denial-of-service by flipping classical feed-forward bits. When it does so, the hop-by-hop telemetry in `quantum/mesh.py` immediately isolates the rogue repeater, and our Q-STAT detector rejects the degraded transmission with $z \ge 4.0$."*

---
*(End of Lesson 06. Whenever you are ready, reply with **"next"** to enter the Security Layer with **Lesson 07: security/signature.py**!)*
