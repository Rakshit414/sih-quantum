# 📘 Q-SENTINEL Masterclass | Lesson 05: Quantum State Tomography (QST)

> **File in Focus:** [`quantum/tomography.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/tomography.py)  
> **Pipeline Position:** Step 5 of the entire Q-Sentinel architecture (Tomography & State Reconstruction Layer)  
> **Target Audience:** Fresher needing physical intuition, 3D Bloch sphere geometry, and defense-grade explanations.

---

## 🧭 1. What Is This File and Why Does It Exist?

In Lesson 04 ([`quantum/measure.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/measure.py)), we measured qubits along one chosen direction. But what if a received qubit has an elevated error rate?
- Did natural summer heat in the fiber-optic cable degrade the particle (depolarizing noise)?
- Or did a hacker intercept the particle, measure it, and replace it with a fake (active eavesdropping)?

Measuring along only one axis cannot answer this question.
In medicine, a doctor cannot diagnose an internal illness from a single 2D X-ray photo; they use a **CT-Scan (Computed Tomography)** to take cross-sectional slices from multiple angles and build a complete 3D model of the patient's organ.

**Quantum State Tomography (QST)** is the medical CT-scan of quantum computing!
By measuring a stream of identical qubits along three perpendicular directions (the $X$, $Y$, and $Z$ axes), [`quantum/tomography.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/tomography.py) reconstructs the complete $2 \times 2$ **Density Matrix ($\rho$)** of the particle. 
It calculates the particle's **Purity ($\gamma$)**, **Entropy ($S$)**, and 3D **Bloch Sphere coordinates**, providing mathematical proof of whether the link is suffering from environmental decay or an active cyber-attack.

---

## 💡 2. Plain English Real-World Analogies

### Analogy 1: The Beach Ball and the Shriveled Balloon (The Bloch Sphere)
Every possible state of a single qubit can be mapped to a point on or inside a 3D sphere called the **Bloch Sphere**:
* **The Surface of the Sphere ($r = 1.0$):** Represents a **Pure Quantum State**. Like a fully inflated, perfectly round beach ball. The qubit has zero uncertainty.
* **Inside the Sphere ($r < 1.0$):** Represents a **Mixed State**. Like a deflated, wrinkled balloon. Environmental heat has leaked in, destroying some of the quantum information.
* **The Dead Center of the Sphere ($r = 0.0$):** Total thermal noise. Complete randomness ($\rho = \frac{1}{2}I$).

```
                |0⟩ (North Pole)
                 ▲
                 │
                 │   * Pure State (r = 1.0, Surface)
                 │  /
                 │ /
    ─────────────┼─────────────► |+⟩ (Equator)
                /│
               / │   * Mixed State (r < 1.0, Inside)
              ▼  │
            |i+⟩ │
                 ▼
                |1⟩ (South Pole)
```

### Analogy 2: The Mystery Crime Scene (Noise vs. Hacker)
Imagine a valuable painting in a museum:
* **Scenario A (Environmental Decoherence):** The room gets humid, causing the paint to slightly fade and blur. The painting is still in the same frame, but degraded. In quantum terms: **Purity drops ($\gamma < 0.75$), Entropy rises.**
* **Scenario B (Active Forgery / Eavesdropping):** A thief steals the painting and replaces it with a completely different, crisp, freshly painted forgery. The painting is not faded at all, but it is the wrong picture! In quantum terms: **Purity is still 100% ($\gamma \approx 1.0$), but Fidelity is 50% ($F \approx 0.5$).**

**This single equation allows Q-SENTINEL to distinguish between bad weather and an enemy spy!**

---

## 📐 3. The Mathematics of Quantum State Tomography

### 1. Stokes Parameters ($S_1, S_2, S_3$)
The 3D coordinates of a qubit on the Bloch sphere are called the **Stokes Parameters**. They are the expectation values of the three Pauli matrices:
$$\begin{aligned}
S_1 &= \langle\sigma_x\rangle = P(+_x) - P(-_x) \\
S_2 &= \langle\sigma_y\rangle = P(+_y) - P(-_y) \\
S_3 &= \langle\sigma_z\rangle = P(+_z) - P(-_z)
\end{aligned}$$
The length of the Bloch vector is:
$$r = \sqrt{S_1^2 + S_2^2 + S_3^2} \le 1.0$$

### 2. Synthesizing the Density Matrix ($\rho$)
Once the three Stokes parameters are measured, the full $2 \times 2$ density matrix is reconstructed using the Pauli expansion:
$$\rho = \frac{1}{2} \Big( I + S_1 X + S_2 Y + S_3 Z \Big) = \frac{1}{2} \begin{pmatrix} 1 + S_3 & S_1 - i S_2 \\ S_1 + i S_2 & 1 - S_3 \end{pmatrix}$$
This matrix must satisfy two fundamental laws of physics:
1. **Hermiticity:** $\rho = \rho^\dagger$ (real eigenvalues).
2. **Unit Trace:** $\text{Tr}(\rho) = \rho_{00} + \rho_{11} = 1.0$ (probabilities sum to 1).

### 3. State Purity ($\gamma$)
$$\gamma = \text{Tr}(\rho^2) \in [0.5, 1.0]$$
- For a **Pure State** ($|\psi\rangle\langle\psi|$): $\gamma = 1.0$.
- For a **Maximally Mixed State** ($\frac{1}{2}I$): $\gamma = \frac{1}{2} = 0.5$.

### 4. Von Neumann Entropy ($S$)
Measures the amount of missing quantum information in bits:
$$S(\rho) = -\text{Tr}(\rho \log_2 \rho) = -\sum_{i} \lambda_i \log_2 \lambda_i$$
where $\lambda_i$ are the eigenvalues of $\rho$.
- Pure state: $\lambda = \{1, 0\} \implies S(\rho) = 0.0\text{ bits}$ (zero uncertainty).
- Maximally mixed noise: $\lambda = \{0.5, 0.5\} \implies S(\rho) = 1.0\text{ bit}$ (maximum uncertainty).

---

## 🔍 4. Line-by-Line Technical Breakdown of `quantum/tomography.py`

```
┌─────────────────────────────────────────────────────────────┐
│                   quantum/tomography.py                     │
├─────────────────────────────────────────────────────────────┤
│  1. TomographyResult Dataclass                              │
│  2. QuantumStateTomography Class                            │
│     - sample_pauli_expectation() (Estimates <sigma>)        │
│     - reconstruct_state() (Synthesizes rho and diagnostics) │
│       • Step A: Sample S1, S2, S3                           │
│       • Step B: Physical radius boundary check (r <= 1.0)   │
│       • Step C: Construct 2x2 density matrix rho            │
│       • Step D: Enforce Hermiticity & Unit Trace            │
│       • Step E: Calculate Purity gamma = Tr(rho^2)          │
│       • Step F: Calculate Von Neumann Entropy S(rho)        │
│       • Step G: Compute Fidelity F = <psi|rho|psi>          │
│       • Step H: Classify Attack vs Thermal Noise            │
└─────────────────────────────────────────────────────────────┘
```

---

### Component A: The `TomographyResult` Dataclass ([Lines 25–38](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/tomography.py#L25-L38))

```python
@dataclass
class TomographyResult:
    density_matrix: np.ndarray
    stokes_parameters: Tuple[float, float, float]  # (S1, S2, S3)
    bloch_vector_length: float
    fidelity: float
    purity: float
    von_neumann_entropy: float
    is_pure: bool
    diagnostic: str
```
Stores the reconstructed $2 \times 2$ matrix, the $(S_1, S_2, S_3)$ coordinates, the Bloch vector radius $r$, fidelity $F$, purity $\gamma$, entropy $S$, and the plain-English diagnostic verdict.

---

### Component B: Sampling Pauli Expectations ([Lines 45–62](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/tomography.py#L45-L62))

```python
@staticmethod
def sample_pauli_expectation(state: QubitState, pauli_matrix: np.ndarray, num_trials: int = 200) -> float:
    # 1. Theoretical expectation value <sigma> = <psi|sigma|psi>
    theo_val = float(np.real(np.vdot(state.vector, pauli_matrix @ state.vector)))
    
    # 2. Convert to probabilities for eigenvalues +1 and -1:
    p_plus = float(np.clip((1.0 + theo_val) / 2.0, 0.0, 1.0))
    p_minus = 1.0 - p_plus

    # 3. Simulate empirical sampling across num_trials
    outcomes = np.random.choice([1.0, -1.0], size=num_trials, p=[p_plus, p_minus])
    return float(np.mean(outcomes))
```
- For any Pauli matrix $\sigma$, its eigenvalues are strictly $+1$ and $-1$.
- The expectation value is $\langle\sigma\rangle = P(+1) - P(-1)$.
- Since $P(+1) + P(-1) = 1$, we can solve for $P(+1) = \frac{1 + \langle\sigma\rangle}{2}$.
- The code simulates $N = 200$ detector trials and takes the empirical mean, accurately mimicking physical hardware measurements.

---

### Component C: State Reconstruction & Physical Bounds ([Lines 65–136](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/tomography.py#L65-L136))

Let us trace how `reconstruct_state` operates:

#### 1. Measure Stokes Parameters & Clamp to Bloch Sphere ([Lines 75–91](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/tomography.py#L75-L91))
```python
s1 = cls.sample_pauli_expectation(target_state, PAULI_X, num_trials=num_trials_per_basis)
s2 = cls.sample_pauli_expectation(target_state, PAULI_Y, num_trials=num_trials_per_basis)
s3 = cls.sample_pauli_expectation(target_state, PAULI_Z, num_trials=num_trials_per_basis)

bloch_len = float(np.sqrt(s1**2 + s2**2 + s3**2))
if bloch_len > 1.0:
    scale = 1.0 / bloch_len
    s1_phys, s2_phys, s3_phys = s1 * scale, s2 * scale, s3 * scale
    bloch_len = 1.0
```
- In real experiments with finite trials ($N = 200$), random statistical fluctuations might yield $s_1 = 0.99, s_2 = 0.15, s_3 = 0.10 \implies r = 1.006 > 1.0$.
- In physics, a Bloch vector length cannot exceed $1.0$ (doing so would produce negative probabilities!).
- The code gracefully rescales the vector back onto the surface of the sphere ($r = 1.0$), ensuring physical validity.

#### 2. Synthesize $\rho$ and Enforce Hermiticity ([Lines 94–98](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/tomography.py#L94-L98))
```python
rho = 0.5 * (PAULI_I + s1_phys * PAULI_X + s2_phys * PAULI_Y + s3_phys * PAULI_Z)
rho = 0.5 * (rho + rho.conj().T)
rho = rho / np.trace(rho).real
```
Guarantees $\rho = \rho^\dagger$ and $\text{Tr}(\rho) = 1.0$ exactly.

#### 3. Purity, Entropy, and Fidelity ([Lines 100–117](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/tomography.py#L100-L117))
```python
purity = float(np.clip(np.real(np.trace(rho @ rho)), 0.5, 1.0))
eigenvals = np.linalg.eigvalsh(rho)
entropy = float(-np.sum(eigenvals * np.log2(np.clip(eigenvals, 1e-12, 1.0))))
fidelity = float(np.real(np.vdot(ref_state.vector, rho @ ref_state.vector)))
```

#### 4. The Diagnostic Rule Engine ([Lines 120–126](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/tomography.py#L120-L126))
```python
if fidelity > 0.92 and purity > 0.90:
    diagnostic = "High-fidelity pure state recovered. No channel decoherence."
elif purity < 0.75:
    diagnostic = "Mixed state detected. Characteristic of depolarizing channel noise."
else:
    diagnostic = "Pure state mismatch. Characteristic of active basis collapse or signature forgery."
```

---

## 🔗 5. How This File Connects to the Next File in the Pipeline

Now that we can reconstruct single quantum links:
What happens when Alice and Bob are separated by hundreds of kilometers across a multi-node network?

In Step 6, [`quantum/mesh.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/mesh.py):
1. We build a **Multi-Hop Quantum Mesh Network** with intermediate repeater nodes ($R_1, R_2, \dots$).
2. Repeaters perform **Entanglement Swapping** across independent Bell pairs.
3. If an intermediate repeater is rogue or compromised by an adversary, the hop-by-hop fidelity and purity metrics derived from tomography allow Q-Sentinel to **localize and quarantine the rogue repeater**!

---

## 🎓 6. Professor's Viva / Hackathon Defense Guide

> **Judge:** *"How does your framework prove whether a high error rate is caused by fiber temperature fluctuations or an active hacker?"*  
> **Your Answer:** *"Through Quantum State Tomography and Density Matrix reconstruction in `quantum/tomography.py`.  
> - If the disturbance is caused by thermal decoherence or fiber attenuation, the state becomes mixed: the Bloch vector length shrinks inside the sphere ($r < 0.7$), the Purity drops significantly ($\text{Tr}(\rho^2) < 0.75$), and the Von Neumann entropy spikes toward $1.0\text{ bit}$.  
> - Conversely, if an eavesdropper intercepts and forges the state, projective measurement collapses the state into another pure eigenstate on the surface of the sphere ($r \approx 1.0$, $\text{Tr}(\rho^2) \approx 1.0$), but the fidelity against Alice's expected basis collapses to $\approx 50\%$.  
> Comparing Purity $\gamma$ against Fidelity $F$ provides mathematical discrimination between noise and espionage."*

---
*(End of Lesson 05. Whenever you are ready, reply with **"next"** to proceed to **Lesson 06: quantum/mesh.py**!)*
