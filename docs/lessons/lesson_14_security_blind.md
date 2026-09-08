# 📘 Q-SENTINEL Masterclass | Lesson 14: Detector Blinding & Spatial Side-Channel Watchtower (Q-BLIND)

> **File in Focus:** [`security/blind.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/blind.py)  
> **Pipeline Position:** Step 14 of the entire Q-Sentinel architecture (Physical Hardware Watchtowers — Phase 33)  
> **Target Audience:** Fresher needing hardware side-channel intuition, single-photon avalanche diode physics, and timing entropy analysis.

---

## 🧭 1. What Is This File and Why Does It Exist?

In 2010, an elite team of quantum hackers led by Vadim Makarov and Lars Lydersen published a landmark paper that sent shockwaves through the cybersecurity community:
**They successfully hacked commercial quantum cryptosystems in real physical laboratories without being detected!**

How did they do it? They didn't break quantum physics; they attacked the **single-photon detector hardware**.

### The Makarov-Lydersen Detector Blinding Attack
Bob uses **Avalanche Photodiodes (APDs)** to detect Alice's incoming signature photons. 
- Normally, an APD operates in **Geiger Mode**: biased slightly above its breakdown voltage. In this mode, a single incoming photon triggers a massive electrical avalanche (a "click").
- The adversary (Eve) shines a continuous-wave (CW) bright light (e.g., a standard 1 mW laser pointer) into Bob's detector.
- The bright light draws a strong continuous DC current through the APD's internal circuit resistor, dropping the diode's voltage below its breakdown threshold.
- The APD transitions from ultra-sensitive Geiger mode into **Classical Linear Mode**!
- In linear mode, the detector is **completely blind to single quantum photons**. It will only click if Eve fires a bright classical pulse exceeding a specific intensity threshold.
- Eve can now remotely control Bob's detectors: she chooses which detector clicks and when, forging any signature she wants with **0% quantum error rate**!

[`security/blind.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/blind.py) is the **Q-BLIND Watchtower**. It acts as an electrical and temporal monitor on Bob's single-photon detectors. By continuously monitoring the **DC anode bias current**, **spatial beam centering**, **click interval Shannon entropy**, and **physical dead-time violations**, Q-BLIND intercepts detector blinding and faked-state attacks in under 1 millisecond!

---

## 💡 2. Plain English Real-World Analogies

### Analogy 1: The Night-Vision Goggles and the Stadium Spotlight
Imagine a sentry guarding a military base at night using ultra-sensitive night-vision goggles:
* In the dark, the goggles can spot a single glowing firefly 100 meters away (Geiger mode).
* An intruder approaches with a blinding 50,000-watt stadium spotlight and shines it directly into the sentry's face.
* The goggles automatically dim and wash out into a white glare. The sentry is blinded!
* The intruder now holds up huge flashing cardboard signs that force the sentry to see whatever the intruder wants.
* **Q-BLIND** is an electrical sensor inside the goggles that measures the current drawn by the screen: if the current spikes because of blinding light, it immediately triggers the base alarm!

### Analogy 2: The Robotic Heartbeat (Timing Entropy)
* In a living human, the time between heartbeats has natural, healthy statistical micro-variations (high entropy).
* If a patient's heartbeat suddenly locks into an exact, rigid, robotic interval down to 0.0001 microseconds with zero variation, doctors know that an external machine or pacemaker has taken over!
* In quantum mechanics, natural photons arrive randomly according to a Poisson process (high Shannon entropy).
* When a hacker injects periodic faked-state pulses to control Bob's detectors, the time between clicks becomes completely deterministic. The entropy crashes to zero, exposing the attack!

---

## 📐 3. The Physics & Cryptanalysis of Q-BLIND

```
                        [Single-Photon APD Receiver Channel]
                                         │
        ┌────────────────────────────────┼────────────────────────────────┐
        ▼                                ▼                                ▼
[DC Bias Current I_bias]       [Spatial Displacement r]      [Click Interval Entropy H]
 Is I_bias >= 5.0 uA?           Is sqrt(dx^2+dy^2) > 2.5um?    Is H(Delta t) < 1.0 nats?
 (Linear-Mode Blinding)         (Spatial Efficiency Mismatch)  Or Dead-Time Violation?
        │                                │                                │
        └────────────────────────────────┼────────────────────────────────┘
                                         ▼
                     [Any Hardware Anomaly Breached?]
                     ├── YES ──► 🔴 MALICIOUS (Hardware Tampering Intercepted!)
                     └── NO  ──► 🟢 LEGITIMATE (Certified Geiger-Mode Operation)
```

---

### 1. DC Anode Bias Current & Geiger-to-Linear Phase Transition
Under nominal operation in single-photon Geiger mode:
- Dark current is microscopic: $I_{\text{bias}} < 1.0\,\mu\text{A}$ (typically $0.1 - 0.4\,\mu\text{A}$).
- When blinding light is injected, the avalanche current transitions to continuous linear photodiode conduction:
  $$I_{\text{bias}} \ge 5.0\,\mu\text{A} \implies \text{Linear Mode Blinding!}$$

### 2. Spatial-Mode Beam Displacement on Quadrant Sensors
Bob's optical receiver contains a 4-quadrant photodiode sensor measuring beam centroid coordinates $(dx, dy)$ in micrometers ($\mu\text{m}$):
$$r = \sqrt{dx^2 + dy^2}$$
- If an adversary shifts the beam angle to exploit spatial efficiency mismatch between detectors:
  $$r > 2.5\,\mu\text{m} \implies \text{Spatial-Mode Beam Shift Attack!}$$

### 3. Shannon Entropy of Inter-Arrival Times ($H(\Delta t)$)
Let $\Delta t_k = t_k - t_{k-1}$ be the time elapsed between consecutive detector clicks.
We bin the intervals into a discrete probability distribution $p_i$:
$$H(\Delta t) = -\sum_{i} p_i \ln p_i \quad (\text{units in nats})$$
- **Legitimate Poissonian Arrivals:** High entropy ($H > 1.5\text{ nats}$).
- **Adversarial Periodic Faked States:** Deterministic pulse trains collapse the distribution into a single histogram bin:
  $$p_{\text{target}} \approx 1.0 \implies H(\Delta t) \to 0.00\text{ nats} \implies \text{Timing Attack!}$$

### 4. Detector Dead-Time Violations
After an APD registers a photon, the internal voltage must be quenched and restored. This takes a physical hold-off period called the **Dead Time** ($\tau_{\text{dead}} \approx 1.0\,\mu\text{s}$):
- In normal physics, a detector **cannot click twice within $0.90 \tau_{\text{dead}}$**.
- Any click occurring inside this dead-time window is physically impossible for a genuine photon and proves external electrical or optical tampering!

---

## 🔍 4. Line-by-Line Technical Breakdown of `security/blind.py`

```
┌─────────────────────────────────────────────────────────────┐
│                     security/blind.py                       │
├─────────────────────────────────────────────────────────────┤
│  1. DetectorTelemetry Dataclass                             │
│  2. BlindingDetectionResult Dataclass                       │
│  3. DetectorBlindingWatcher Class                           │
│     - __init__(current_thresh=5.0uA, spatial_limit=2.5um)   │
│     - calculate_interarrival_entropy() (Shannon Entropy)    │
│     - evaluate_detector_state() (4-Sensor Diagnostic Logic) │
│     - simulate_detector_scan() (Realistic Telemetry Engine) │
└─────────────────────────────────────────────────────────────┘
```

---

### Component A: The Telemetry Dataclasses ([Lines 18–48](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/blind.py#L18-L48))

```python
@dataclass
class DetectorTelemetry:
    channel_id: str
    bias_current_ua: float              # DC anode current (nominally < 1.0 uA in Geiger mode)
    spatial_offset_x_um: float          # Quadrant sensor X displacement (micrometers)
    spatial_offset_y_um: float          # Quadrant sensor Y displacement (micrometers)
    inter_arrival_times_us: List[float] # List of photon detection inter-arrival times
    double_click_count: int             # Simultaneous dual-detector clicks
    total_clicks: int                   # Total registered clicks

@dataclass
class BlindingDetectionResult:
    blinding_detected: bool
    bias_current_ua: float
    operating_mode: str
    spatial_displacement_um: float
    spatial_breach: bool
    inter_arrival_entropy: float
    dead_time_violation: bool
    double_click_ratio: float
    verdict: ThreatCategory
    attack_classification: str
    cryptanalytic_proof: str
```

---

### Component B: Shannon Timing Entropy ([Lines 68–93](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/blind.py#L68-L93))

```python
@staticmethod
def calculate_interarrival_entropy(intervals_us: List[float], bins: int = 15) -> float:
    arr = np.asarray(intervals_us, dtype=float)
    arr = arr[arr > 0]
    hist, _ = np.histogram(arr, bins=bins, density=True)
    p = hist / np.sum(hist) if np.sum(hist) > 0 else np.zeros_like(hist)
    p = p[p > 1e-12]
    entropy = -np.sum(p * np.log(p))
    return float(round(entropy, 4))
```
Constructs a probability density histogram over photon arrival intervals and computes the continuous Shannon entropy in nats.

---

### Component C: Multi-Sensor Hardware Evaluation in `evaluate_detector_state` ([Lines 94–180](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/blind.py#L94-L180))

Let us trace the 4 hardware checks:

```python
# 1. Bias Current Check (Linear-Mode Blinding)
current_breach = bias_ua >= self.current_threshold  # 5.0 uA

# 2. Spatial Alignment Check (Quadrant Sensor)
radial_displacement = float(np.sqrt(dx**2 + dy**2))
spatial_breach = radial_displacement > self.spatial_limit  # 2.5 um

# 3. Inter-arrival Timing Entropy Check
entropy = self.calculate_interarrival_entropy(telemetry.inter_arrival_times_us)
entropy_breach = entropy < self.min_entropy  # 1.0 nats

# 4. Dead-Time Violation Check (Impossible Clicks)
dead_time_violations = sum(1 for t in telemetry.inter_arrival_times_us if 0 < t < (self.dead_time * 0.90))
dead_time_breach = dead_time_violations > 0
```

#### The Threat Classification Logic:
- If `current_breach` $\to$ **`DETECTOR_BLINDING_CW_ATTACK`** (Makarov attack: continuous-wave laser forced APD into classical linear mode).
- If `spatial_breach` $\to$ **`SPATIAL_MODE_BEAM_SHIFT_ATTACK`** (Adversary shifted the beam off-center to exploit detector efficiency differences).
- If `dead_time_breach` or `entropy_breach` $\to$ **`FAKED_STATE_TIMING_ATTACK`** (Non-Poissonian deterministic pulse train injected).
- If `bias_ua > 3.0 uA` (approaching threshold) $\to$ **`ELEVATED_BIAS_CURRENT`** (Suspicious yellow alert).
- Otherwise $\to$ **`NOMINAL_GEIGER_OPERATION`** (Legitimate green).

---

## 🔗 5. How This File Connects to the Rest of the Framework

1. **Receiver-Side Hardware Guard:**
   While [`security/trojan.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/trojan.py) guards Alice's laser transmitter, `security/blind.py` guards **Bob's single-photon receiver**.
2. **The Road to MDI-QDS:**
   Because detector blinding has historically been the #1 physical vulnerability of quantum hardware, physicists developed **Measurement-Device-Independent (MDI) QDS** (which we will study in Lesson 16), which completely eliminates detector side-channel vulnerabilities by design!
3. **Dashboard UI ([`app.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/app.py)):**
   Renders real-time APD bias currents, spatial displacement vectors, and arrival entropy gauges on the Q-BLIND scorecard.

---

## 🎓 6. Professor's Viva / Hackathon Defense Guide

> **Judge:** *"How does the Makarov-Lydersen blinding attack allow an adversary to forge signatures without triggering errors?"*  
> **Your Answer:** *"In a blinding attack, the adversary shines continuous-wave (CW) light onto the avalanche photodiode (APD). This draws continuous current through the biasing resistor, reducing the bias voltage below breakdown. The APD transitions from single-photon Geiger mode into classical linear mode. In linear mode, the detector is blind to single quantum photons, but can be forced to click by bright classical trigger pulses sent by the attacker. Eve can therefore intercept the real quantum signature and selectively trigger only the detectors that confirm her desired fraudulent signature.  
> Q-Sentinel defeats this in `security/blind.py` by monitoring the APD's DC anode bias current $I_{\text{bias}}$. When blinding light is applied, $I_{\text{bias}}$ spikes from $< 1.0\,\mu\text{A}$ to $> 10\,\mu\text{A}$, triggering an immediate malicious hardware alert before the attack can succeed."*

> **Judge:** *"What is the significance of the Shannon entropy calculation in your detector monitor?"*  
> **Your Answer:** *"Genuine quantum photons emitted by thermal or coherent sources arrive following a memoryless Poisson point process, where inter-arrival times $\Delta t$ follow an exponential distribution with high Shannon entropy ($H > 1.5\text{ nats}$). In contrast, an attacker attempting a faked-state timing attack must synchronize their optical control pulses with rigid, periodic clock timing. This collapses the arrival distribution into a deterministic spike with entropy $H \to 0\text{ nats}$, allowing Q-Sentinel to catch timing manipulation even if the optical power is kept low."*

---
*(End of Lesson 14. Whenever you are ready, reply with **"next"** to proceed to the Device-Independent Bell Test in **Lesson 15: security/chsh.py**!)*
