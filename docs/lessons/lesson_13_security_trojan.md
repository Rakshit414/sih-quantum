# 📘 Q-SENTINEL Masterclass | Lesson 13: Trojan-Horse Optical Attack & Memory Watchtower (Q-TROJAN)

> **File in Focus:** [`security/trojan.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/trojan.py)  
> **Pipeline Position:** Step 13 of the entire Q-Sentinel architecture (Physical Hardware Watchtowers — Phase 32)  
> **Target Audience:** Fresher needing understanding of optical side-channel probing, quantum memory decoherence, and Helstrom information leakage.

---

## 🧭 1. What Is This File and Why Does It Exist?

In classical spy thrillers, a bugging device is planted in an office to listen to private conversations.
In quantum communications, an attacker doesn't need to break into the laboratory to plant a bug — they can shine an **Optical Trojan-Horse Probe** through the fiber-optic cable!

### What Is an Optical Trojan-Horse Attack (THA)?
Inside Alice's transmitter, there are physical optical components: electro-optic phase modulators, beam splitters, and variable attenuators that Alice uses to set her secret quantum states ($|0\rangle, |+\rangle, |i+\rangle$).
An adversary (Eve) shoots a bright, high-intensity laser pulse backwards into Alice's optical output port:
1. The bright pulse enters Alice's lab.
2. It reflects off Alice's internal phase modulators.
3. The back-reflected light travels back out through the fiber into Eve's receiver.
4. By measuring the phase shift of the reflected light, **Eve directly reads Alice's internal secret key settings** without touching the delicate quantum signature photons!

Furthermore, when qubits are held in a **Quantum Memory Buffer** (e.g., trapped ions or optical delay loops) waiting for verification, they undergo natural physical decay (**$T_1$ relaxation and $T_2$ dephasing**).

[`security/trojan.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/trojan.py) is the **optical guard at the laboratory door**. It combines a **4-sensor optical watchtower** (power, wavelength, timing, and Helstrom information leakage) with a **Lindblad quantum memory decay simulator** to guarantee that neither bright-light probes nor memory decay compromise signature security!

---

## 💡 2. Plain English Real-World Analogies

### Analogy 1: The Flashlight Through the Keyhole
Imagine Alice is inside her bedroom setting the combination dials of a secret safe:
* A thief stands outside in the dark hallway.
* The thief shines a powerful laser pointer through the tiny keyhole.
* The beam bounces off the shiny chrome dials of the safe and reflects back through the keyhole onto the hallway wall.
* By analyzing the angle of the reflected beam, the thief reads the combination!
* This is an **Optical Trojan-Horse Attack**.
* Q-TROJAN acts as a light sensor over the keyhole that detects the intruder's laser and slams a shutter closed!

### Analogy 2: The Melting Ice Cube (Quantum Memory Decoherence)
Imagine storing an ice sculpture in a commercial freezer:
* Even with the door closed, tiny thermal leaks cause the sharp edges of the ice to slowly soften and round off over time.
* If you leave a quantum signature qubit in a memory buffer for 500 microseconds, it naturally degrades due to ambient room temperature.
* If your security system is dumb, it might mistake this natural melting for a hacker attack!
* Q-TROJAN mathematically models the exact melting rate ($T_1$ and $T_2$), subtracting it from the error count so that only *genuine* hacker attacks trigger alarms.

---

## 📐 3. The Mathematics of Trojan-Horse Defense & Memory Decoherence

```
                           [Incoming Ingress Optical Signal]
                                          │
        ┌───────────────────┬─────────────┴─────────────┬───────────────────┐
        ▼                   ▼                           ▼                   ▼
 [Optical Power]   [Spectral Bandpass]        [Temporal Gating]     [Helstrom Bound]
 Is P_refl > 10nW?  Is |lambda-1550| > 5nm?    Is |Delta t| > 1ns?   Is I_Eve > 0.01 bits?
        │                   │                           │                   │
        └───────────────────┼───────────────────────────┴───────────────────┘
                            ▼
          [Any Physical Boundary Breached?]
          ├── YES ──► 🔴 MALICIOUS (Trojan Probe Intercepted!)
          └── NO  ──► 🟢 CLEAN CHANNEL (Within Physical Limits)
                            │
                            ▼
            [Quantum Memory Decoherence Model]
             Lindblad T1 Relaxation & T2 Dephasing Master Equations
             rho_00(t) = 1 - (1 - rho_00) * exp(-t/T1)
             rho_01(t) = rho_01 * exp(-t/T2)
```

---

### 1. Lindblad Decoherence Master Equation
A stored qubit density matrix $\rho(t)$ evolves over elapsed storage time $t$ according to two physical decay constants:
- **$T_1$ (Longitudinal Relaxation Time, $\approx 1000\,\mu\text{s}$):** The time it takes for excited state $|1\rangle$ to decay down to ground state $|0\rangle$ (energy loss to the environment).
  $$\rho_{11}(t) = \rho_{11}(0) e^{-t/T_1}, \quad \rho_{00}(t) = 1 - (1 - \rho_{00}(0)) e^{-t/T_1}$$
- **$T_2$ (Transverse Dephasing Time, $\approx 200\,\mu\text{s}$):** The time it takes for quantum phase coherence between $|0\rangle$ and $|1\rangle$ to randomize.
  $$\rho_{01}(t) = \rho_{01}(0) e^{-t/T_2}, \quad \rho_{10}(t) = \rho_{10}(0) e^{-t/T_2}$$
- **Fundamental Physical Constraint:** In nature, dephasing can never be slower than half of energy relaxation:
  $$T_2 \le 2 T_1$$

### 2. The Helstrom-Holevo Information Leakage Bound ($I_E$)
If Eve's probe pulse reflects $n_{\text{refl}}$ photons off Alice's phase modulator, how much secret information does Eve actually gain?
Carl W. Helstrom and Alexander Holevo derived the exact mathematical upper bound on Eve's mutual information $I_E$:

$$d = \frac{1 - \sqrt{1 - e^{-4 \mu_{\text{refl}}}}}{2}$$
$$I_E \le 1 - h_2(d) = 1 - \Big[ -d \log_2 d - (1 - d)\log_2 (1 - d) \Big]$$

- If reflected photons $\mu_{\text{refl}} \to 0 \implies d \to 0 \implies I_E \to 0.0000\text{ bits}$ (Zero leakage!).
- If reflected photons $\mu_{\text{refl}} > 10 \implies I_E \to 1.0\text{ bit}$ (Full compromise!).
- **Security Tripwire:** If $I_E > 0.01\text{ bits/pulse}$, the protocol halts immediately!

---

## 🔍 4. Line-by-Line Technical Breakdown of `security/trojan.py`

```
┌─────────────────────────────────────────────────────────────┐
│                     security/trojan.py                      │
├─────────────────────────────────────────────────────────────┤
│  1. Dataclasses: StoredQubitState, TrojanProbe, Result      │
│  2. QuantumMemoryBuffer Class                               │
│     - evolve_state() (Lindblad T1/T2 Master Equation)       │
│  3. TrojanHorseDetector Class                               │
│     - calculate_helstrom_information_leakage()             │
│     - analyze_probe() (Multi-Sensor 4-Pillar Evaluation)    │
│       • Pillar A: Spectral Passband Check (1550 +/- 5nm)    │
│       • Pillar B: Temporal Gating Window (+/- 1.0ns)        │
│       • Pillar C: Optical Power Metering (Threshold 10nW)   │
│       • Pillar D: Helstrom Mutual Information Leakage Bound │
└─────────────────────────────────────────────────────────────┘
```

---

### Component A: The `QuantumMemoryBuffer` Engine ([Lines 72–136](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/trojan.py#L72-L136))

```python
class QuantumMemoryBuffer:
    def __init__(self, t1_us: float = 1000.0, t2_us: float = 200.0):
        if t2_us > 2.0 * t1_us:
            raise ValueError(f"Physical constraint violated: T2 cannot exceed 2*T1.")
        self.t1 = float(t1_us)
        self.t2 = float(t2_us)

    def evolve_state(self, pure_state_vector: np.ndarray, elapsed_us: float, ...) -> StoredQubitState:
        decay_t1 = np.exp(-elapsed_us / self.t1)
        decay_t2 = np.exp(-elapsed_us / self.t2)

        rho_t = np.zeros((2, 2), dtype=complex)
        rho_t[0, 0] = 1.0 - (1.0 - rho_0[0, 0].real) * decay_t1
        rho_t[1, 1] = rho_0[1, 1].real * decay_t1
        rho_t[0, 1] = rho_0[0, 1] * decay_t2
        rho_t[1, 0] = rho_0[1, 0] * decay_t2
        ...
        fidelity = float(np.clip((psi.conj().T @ rho_t @ psi).real[0, 0], 0.0, 1.0))
        error_rate = float(np.clip(1.0 - fidelity, 0.0, 1.0))
```
Enforces physical $T_1/T_2$ decay, computes the memory fidelity $F$, and calculates the exact error rate expected from natural storage decay alone.

---

### Component B: The Helstrom Leakage Formula ([Lines 161–180](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/trojan.py#L161-L180))

```python
@staticmethod
def calculate_helstrom_information_leakage(back_reflected_photons: float) -> float:
    mu = max(0.0, float(back_reflected_photons))
    if mu <= 1e-9:
        return 0.0

    exp_factor = np.exp(-4.0 * min(mu, 20.0))
    sqrt_term = np.sqrt(max(0.0, 1.0 - exp_factor))
    d = 0.5 * (1.0 - sqrt_term)
    h2 = -d * np.log2(d) - (1.0 - d) * np.log2(1.0 - d)
    return round(float(np.clip(1.0 - h2, 0.0, 1.0)), 6)
```
Translates the physical photon count of reflected light directly into Shannon information bits leaked to Eve.

---

### Component C: Multi-Sensor Analysis in `analyze_probe` ([Lines 182–306](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/trojan.py#L182-L306))

Let us trace the 4 hardware sensor checks:

```python
# 1. Spectral Passband Check (Must be 1550 +/- 5 nm)
half_band = self.passband_width / 2.0
spectral_breach = abs(wavelength - self.passband_center) > half_band

# 2. Synchronous Time Gating Check (Must arrive within +/- 1.0 ns of clock)
temporal_breach = abs(arr_offset) > self.gate_window

# 3. Optical Power Metering Check (Must not exceed 10 nW reflected power)
power_breach = refl_power > self.power_threshold

# 4. Helstrom Information Leakage Bound
info_leak = self.calculate_helstrom_information_leakage(refl_photons)
```

#### The Threat Verdict:
- If `spectral_breach` $\to$ **`OUT_OF_BAND_SPECTRAL_PROBE`** (Eve attempted to inject light at an unusual wavelength to bypass filters).
- If `temporal_breach` $\to$ **`ASYNC_TIME_DOMAIN_PROBE`** (Eve shot a laser pulse between legitimate signal clock cycles).
- If `power_breach` or `info_leak > 0.01` $\to$ **`BRIGHT_PULSE_TROJAN_HORSE`** (High-intensity spy laser detected).
- Otherwise $\to$ **`CLEAN_CHANNEL`** (Certified safe).

---

## 🔗 5. How This File Connects to the Rest of the Framework

1. **Hardware Side-Channel Protection:**
   `security/trojan.py` safeguards the **transmitter side (Alice)** from optical back-reflection, while the next lesson ([`security/blind.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/blind.py)) will safeguard the **receiver side (Bob)** from detector blinding!
2. **Dashboard UI ([`app.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/app.py)):**
   Displays reflected optical power (nW), information leakage ($I_E$), spectral wavelengths, and memory retention curves in real time.
3. **Automated Audits ([`rehearsal.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/rehearsal.py)):**
   Rehearsal test #8 continuously verifies zero false negatives against Trojan-horse pulses.

---

## 🎓 6. Professor's Viva / Hackathon Defense Guide

> **Judge:** *"How does an optical Trojan-Horse attack bypass standard quantum digital signature defenses?"*  
> **Your Answer:** *"In a standard QDS exchange, security relies on detecting disturbances in the quantum states sent from Alice to Bob. An optical Trojan-Horse attack is an active **hardware side-channel exploit**: Eve shines a high-intensity laser into Alice's transmitter output port from the outside. The light reflects off Alice's internal phase modulators and returns to Eve, directly leaking Alice's secret key without modifying the signature photons.  
> Q-Sentinel stops this in `security/trojan.py` by deploying a 4-pillar defense: optical power metering (OPM threshold of 10 nW), narrowband spectral filtering ($1550 \pm 5\text{ nm}$), synchronous temporal gating ($\pm 1.0\text{ ns}$), and Helstrom-Holevo mutual information bounds ($I_E \le 0.01\text{ bits}$)."*

> **Judge:** *"Why is the Lindblad condition $T_2 \le 2T_1$ enforced in your code?"*  
> **Your Answer:** *"Under the laws of quantum statistical mechanics, transverse dephasing ($T_2$) represents the loss of relative phase information, while longitudinal relaxation ($T_1$) represents energy decay to the ground state. Because energy decay inherently randomizes phase, pure dephasing cannot occur slower than twice the energy lifetime: $1/T_2 = 1/(2T_1) + 1/T_\phi$. Therefore, $T_2 \le 2T_1$ is a strict physical law. Any simulation violating this constraint would produce non-positive density matrices and negative probabilities."*

---
*(End of Lesson 13. Whenever you are ready, reply with **"next"** to proceed to the Single-Photon Detector Blinding Watchtower in **Lesson 14: security/blind.py**!)*
