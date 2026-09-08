# 📘 Q-SENTINEL Masterclass | Lesson 03: The Quantum Teleportation Protocol

> **File in Focus:** [`quantum/teleport.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/teleport.py)  
> **Pipeline Position:** Step 3 of the entire Q-Sentinel architecture (Teleportation Pipeline)  
> **Target Audience:** Fresher needing physical intuition, step-by-step mathematical expansion, code logic, and hackathon defense readiness.

---

## 🧭 1. What Is This File and Why Does It Exist?

In classical networking, if Alice wants to send a file to Bob, she makes a copy of the bytes and transmits them through a cable. 
In quantum cryptography, the **No-Cloning Theorem** forbids making a copy of an unknown quantum particle. Furthermore, if Alice tries to physically shoot a single fragile photon through hundreds of kilometers of glass fiber, it will almost certainly be lost or absorbed along the way.

**Quantum Teleportation** is the groundbreaking protocol (invented by Bennett, Brassard, Crépeau, Jozsa, Peres, and Wootters in 1993) that solves this problem.
It allows Alice to transfer an unknown quantum state $|\psi\rangle$ to Bob **without physically sending the particle itself**!

[`quantum/teleport.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/teleport.py) implements the complete 3-qubit teleportation pipeline. It takes an input qubit (Alice's signature token), entangles it with a shared Bell pair, performs a joint Bell-state measurement, transmits 2 classical bits, and applies the exact Pauli correction on Bob's end to reconstruct the state with **100% fidelity ($F = 1.0$)**.

---

## 💡 2. Plain English Real-World Analogies

### Analogy 1: The Quantum Fax Machine
Imagine you have a one-of-a-kind ancient parchment with delicate golden ink:
* You cannot make a photocopy (No-Cloning Theorem).
* You feed the parchment into a special scanner. The scanning process burns the original parchment to ash (measurement destruction).
* The scanner outputs two tiny pieces of paper with two numbers: e.g., `(1, 0)`.
* You call Bob on a normal telephone and tell him: *"Apply operation 1, 0."*
* Bob takes a blank piece of paper that was previously entangled with your scanner, turns a magical knob according to your two numbers, and **the exact ancient golden ink reappears on his paper!**
* The physical paper did not fly through the sky; only the **quantum information** was teleported!

### Analogy 2: The Two-Bit Padlock
Alice has a secret treasure (the qubit). She locks it in a box with a special 4-way combination lock:
* The combination can only be one of four values: `(0, 0)`, `(0, 1)`, `(1, 0)`, or `(1, 1)`.
* By measuring her qubits, she determines which of the 4 combinations the lock snapped into.
* She texts those 2 bits to Bob over normal WhatsApp or public radio.
* If an eavesdropper (Eve) intercepts those 2 bits, **they are completely useless to her**! They look like random coin tosses.
* Only Bob, who holds the other half of the entangled Bell pair, can use those 2 bits to unlock the state.

---

## 📐 3. The 3-Qubit Mathematical Expansion

To understand the code, let us look at the 3 qubits involved:
1. **Qubit 1:** Alice's unknown signature state: $|\psi\rangle_1 = \alpha|0\rangle + \beta|1\rangle$ (where $|\alpha|^2 + |\beta|^2 = 1$).
2. **Qubit 2:** Alice's half of the shared Bell pair: $|\Phi^+\rangle_{23} = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$.
3. **Qubit 3:** Bob's half of the shared Bell pair.

### The Combined 3-Qubit System ($8 \times 1$ Vector):
The joint state of all three qubits begins as:
$$|\Psi_{123}\rangle = |\psi\rangle_1 \otimes |\Phi^+\rangle_{23} = (\alpha|0\rangle + \beta|1\rangle) \otimes \frac{|00\rangle + |11\rangle}{\sqrt{2}}$$

Multiplying this out into the 8-dimensional basis yields:
$$|\Psi_{123}\rangle = \frac{1}{\sqrt{2}} \Big( \alpha|000\rangle + \alpha|011\rangle + \beta|100\rangle + \beta|111\rangle \Big)$$

### The Circuit Operations:
1. **Alice applies CNOT on Qubit 1 (control) and Qubit 2 (target):**
   - If Qubit 1 is `0`, Qubit 2 remains unchanged.
   - If Qubit 1 is `1`, Qubit 2 flips ($0 \leftrightarrow 1$).
   $$|\Psi'\rangle = \frac{1}{\sqrt{2}} \Big( \alpha|000\rangle + \alpha|011\rangle + \beta|110\rangle + \beta|101\rangle \Big)$$

2. **Alice applies a Hadamard Gate to Qubit 1:**
   - $|0\rangle \to \frac{|0\rangle + |1\rangle}{\sqrt{2}}$ and $|1\rangle \to \frac{|0\rangle - |1\rangle}{\sqrt{2}}$.

### The Miraculous Rearrangement:
When you regroup the mathematical terms by Alice's first two qubits, something astonishing happens:
$$|\Psi''\rangle = \frac{1}{2} \Bigg[ |00\rangle_{12} \underbrace{(\alpha|0\rangle + \beta|1\rangle)_3}_{\text{exact } |\psi\rangle} + |01\rangle_{12} \underbrace{(\alpha|1\rangle + \beta|0\rangle)_3}_{X|\psi\rangle} + |10\rangle_{12} \underbrace{(\alpha|0\rangle - \beta|1\rangle)_3}_{Z|\psi\rangle} + |11\rangle_{12} \underbrace{(\alpha|1\rangle - \beta|0\rangle)_3}_{ZX|\psi\rangle} \Bigg]$$

Look closely at Bob's Qubit 3:
- If Alice measures **`00`**, Bob's qubit is already **$|\psi\rangle$**! (Correction: Identity $I$).
- If Alice measures **`01`**, Bob's qubit is **$X|\psi\rangle$**! (Correction: apply $X$ to flip it back).
- If Alice measures **`10`**, Bob's qubit is **$Z|\psi\rangle$**! (Correction: apply $Z$ to fix the phase).
- If Alice measures **`11`**, Bob's qubit is **$ZX|\psi\rangle$**! (Correction: apply $ZX$ to fix both).

---

## 🔍 4. Line-by-Line Technical Breakdown of `quantum/teleport.py`

```
┌─────────────────────────────────────────────────────────────┐
│                    quantum/teleport.py                      │
├─────────────────────────────────────────────────────────────┤
│  1. TeleportationResult Dataclass                           │
│  2. get_pauli_correction_matrix(b1, b2)                     │
│  3. teleport_qubit() Step-by-Step Execution                 │
│     - Step A: 8-dimensional composite state                │
│     - Step B: CNOT_12 Gate                                  │
│     - Step C: Hadamard_1 Gate                               │
│     - Step D: Born-Rule Bell Measurement (b1, b2)           │
│     - Step E: Extract & Normalize Bob's Qubit 3             │
│     - Step F: Apply Pauli Correction U = Z^{b1} X^{b2}      │
│     - Step G: Compute Fidelity F = |⟨psi|recovered⟩|²       │
└─────────────────────────────────────────────────────────────┘
```

---

### Component A: The `TeleportationResult` Dataclass ([Lines 16–25](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/teleport.py#L16-L25))

```python
@dataclass
class TeleportationResult:
    original_state: QubitState
    bell_measurement_bits: Tuple[int, int]  # (b1, b2)
    pre_correction_state: QubitState
    applied_correction: str
    recovered_state: QubitState
    fidelity: float
    success: bool
```
This dataclass acts as the flight telemetry recorder. It stores the input state, the 2 classical bits generated, the state of Bob's qubit before correction, the correction gate applied, the final recovered state, and the mathematical fidelity.

---

### Component B: Pauli Correction Lookup ([Lines 27–43](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/teleport.py#L27-L43))

```python
def get_pauli_correction_matrix(b1: int, b2: int) -> Tuple[np.ndarray, str]:
    """
    Determines exact Pauli unitary: U_corr = Z^{b1} @ X^{b2}.
    """
    if (b1, b2) == (0, 0):
        return PAULI_I, "I"
    elif (b1, b2) == (0, 1):
        return PAULI_X, "X"
    elif (b1, b2) == (1, 0):
        return PAULI_Z, "Z"
    elif (b1, b2) == (1, 1):
        return PAULI_Z @ PAULI_X, "ZX"
```
This implements the universal unitary correction rule:
$$U_{\text{corr}} = Z^{b_1} X^{b_2}$$
- If $b_1 = 0, b_2 = 0 \implies Z^0 X^0 = I$
- If $b_1 = 0, b_2 = 1 \implies Z^0 X^1 = X$
- If $b_1 = 1, b_2 = 0 \implies Z^1 X^0 = Z$
- If $b_1 = 1, b_2 = 1 \implies Z^1 X^1 = ZX$

---

### Component C: The `teleport_qubit` Execution Engine ([Lines 45–122](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/teleport.py#L45-L122))

Let us trace the execution flow inside `teleport_qubit`:

#### 1. Form the 8-Dimensional Composite Vector ([Lines 64–67](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/teleport.py#L64-L67))
```python
composite_state = input_state.tensor(bell_pair)
vec = composite_state.vector  # Shape: (8, 1)
```
Takes Alice's 2-element vector and tensor-products it with the 4-element Bell pair, creating an 8-element state vector representing the entire universe of the 3 qubits.

#### 2. Apply CNOT on Qubits 1 and 2 ([Lines 68–71](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/teleport.py#L68-L71))
```python
cnot_12_kron_I = np.kron(CNOT, np.eye(2, dtype=np.complex128))
vec = cnot_12_kron_I @ vec
```
Constructs the $8 \times 8$ unitary matrix $\text{CNOT}_{12} \otimes I_3$ and applies it to `vec`. Notice that Qubit 3 (Bob's qubit) is multiplied by identity $I_2$, meaning Bob's particle is physically untouched in his lab.

#### 3. Apply Hadamard on Qubit 1 ([Lines 73–75](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/teleport.py#L73-L75))
```python
H_kron_I_kron_I = np.kron(np.kron(HADAMARD, np.eye(2, dtype=np.complex128)), np.eye(2, dtype=np.complex128))
vec = H_kron_I_kron_I @ vec
```
Constructs the $8 \times 8$ unitary matrix $H_1 \otimes I_2 \otimes I_3$ and rotates Qubit 1 into the diagonal basis.

#### 4. Projective Measurement by Born Rule ([Lines 77–96](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/teleport.py#L77-L96))
```python
p_00 = np.vdot(vec[0:2], vec[0:2]).real
p_01 = np.vdot(vec[2:4], vec[2:4]).real
p_10 = np.vdot(vec[4:6], vec[4:6]).real
p_11 = np.vdot(vec[6:8], vec[6:8]).real
probs = np.array([p_00, p_01, p_10, p_11])
...
outcome_idx = rng.choice(4, p=probs)
b1, b2 = bit_map[outcome_idx]
```
- In quantum mechanics, Alice's measurement collapses the wave function.
- Each of the 4 outcomes (`00`, `01`, `10`, `11`) corresponds to a 2-element slice of the 8-element vector.
- The Born rule states that the probability of outcome $k$ is the sum of the squared amplitudes of that slice. In an ideal teleportation channel, each outcome occurs with an equal probability of **exactly $25\%$ ($p = 0.25$)**!
- A random choice is made according to these physical probabilities, producing Alice's classical measurement bits $(b_1, b_2)$.

#### 5. Extract Bob's Collapsed Qubit & Apply Correction ([Lines 98–109](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/teleport.py#L98-L109))
```python
start_idx = (b1 * 2 + b2) * 2
bob_raw_vec = vec[start_idx : start_idx + 2]
bob_raw_vec = bob_raw_vec / np.sqrt(np.vdot(bob_raw_vec, bob_raw_vec).real)
pre_correction = QubitState(bob_raw_vec, label=f"Collapsed_({b1}{b2})")

U_corr, corr_label = get_pauli_correction_matrix(b1, b2)
bob_recovered_vec = U_corr @ pre_correction.vector
recovered_state = QubitState(bob_recovered_vec, label=f"Teleported({input_state.label})")
```
- Bob extracts his slice of the collapsed wave function (`pre_correction`).
- He applies $U_{\text{corr}} = Z^{b_1} X^{b_2}$.
- `recovered_state` is now physically identical to Alice's original state!

#### 6. Verify Fidelity ([Lines 110–121](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/teleport.py#L110-L121))
```python
fidelity = input_state.fidelity(recovered_state)
return TeleportationResult(..., fidelity=fidelity, success=bool(abs(fidelity - 1.0) < 1e-5))
```
Computes $F = |\langle\psi_{\text{original}} | \psi_{\text{recovered}}\rangle|^2$. In the absence of channel noise, the code confirms **$F = 1.000000$ (100% exact reconstruction)**.

---

## 🔗 5. How This File Connects to the Next File in the Pipeline

Now that Bob has reconstructed Alice's signature qubit in his laboratory:
How does Bob verify that this qubit represents a genuine signature and not an attacker's fake?

In the next step, [`quantum/measure.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/measure.py):
1. Bob performs **projective Born-rule verification measurements** on the recovered qubit against Alice's expected Pauli eigenstate.
2. He repeats this across $N$ stochastic trials.
3. If the qubit was teleported honestly, the error rate matches baseline channel noise ($p_0 \approx 3\%$).
4. If an attacker tampered with the link or classical bits, the error rate spikes to $\approx 50\%$, triggering the Q-STAT alarm!

---

## 🎓 6. Professor's Viva / Hackathon Defense Guide

> **Judge:** *"Does quantum teleportation violate Einstein's Special Relativity by transmitting information faster than light?"*  
> **Your Answer:** *"No, sir/ma'am. Quantum teleportation strictly adheres to the **No-Communication Theorem**. Even though the wave function collapse across the Bell pair is instantaneous, Bob's qubit remains in a maximally mixed state ($\rho = \frac{1}{2}I_2$) containing zero decipherable information until he receives the 2 classical correction bits $(b_1, b_2)$ from Alice. Because those classical bits must travel through a classical channel at or below the speed of light $c$, the total communication speed cannot exceed $c$."*

> **Judge:** *"What happens if an attacker intercepts the 2 classical bits $(b_1, b_2)$ on the internet?"*  
> **Your Answer:** *"The 2 classical bits carry zero mutual information about Alice's secret quantum state. Each of the four bit-pairs $(00, 01, 10, 11)$ occurs with equal probability $p = 0.25$, independent of $\alpha$ and $\beta$. Without possessing Bob's half of the entangled Bell pair, the classical bits are completely uninformative random noise."*

---
*(End of Lesson 03. Whenever you are ready, reply with **"next"** to proceed to **Lesson 04: quantum/measure.py**!)*
