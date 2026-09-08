# 📘 Q-SENTINEL Masterclass | Lesson 11: Dynamic Noise Auto-Calibration (Q-CALIBRATE)

> **File in Focus:** [`security/calibrate.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/calibrate.py)  
> **Pipeline Position:** Step 11 of the entire Q-Sentinel architecture (Adaptive Baseline Calibration Layer)  
> **Target Audience:** Fresher needing physical understanding of fiber thermal drift, adaptive algorithms, and false-positive prevention.

---

## 🧭 1. What Is This File and Why Does It Exist?

In Lesson 10 ([`security/detector.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/detector.py)), we learned that the Q-STAT detection engine calculates the anomaly score:
$$z = \frac{\hat{e} - p_0}{\sigma_0}$$
Notice the variable **$p_0$**: the baseline background noise floor. In our initial experiments, we assumed $p_0 = 3\%$ ($0.03$).

However, **in real-world optical fiber networks, the baseline noise is NEVER constant**!
- Fiber-optic cables buried alongside highways or railways experience daily temperature swings (diurnal thermal cycles).
- In the cold pre-dawn hours (4:00 AM), optical fiber is colder and exhibits lower attenuation ($p_0 \approx 2.1\%$).
- Under the scorching afternoon sun (2:00 PM), the glass warms up, causing micro-strain and thermal refractive index drift ($p_0 \approx 3.8\%$).

### The Dual Danger of a Static Baseline:
1. **False Alarm Danger:** If $p_0$ is locked at $3.0\%$ and the afternoon heat pushes natural errors to $3.8\%$, Q-STAT might falsely flag honest banking transactions as attacks!
2. **Stealth Attack Danger:** At 4:00 AM when the true background noise is only $2.1\%$, an attacker could inject $0.9\%$ of eavesdropping noise, and a static $3.0\%$ detector would completely miss the thief!

[`security/calibrate.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/calibrate.py) implements **Q-CALIBRATE**: an adaptive, sliding-window auto-calibration engine. It uses periodic pilot probe pulses and an Exponential Moving Average (EMA) to continuously track slow environmental drift, while sounding an immediate alarm if the error rate changes unnaturally fast!

---

## 💡 2. Plain English Real-World Analogies

### Analogy 1: The Smart Digital Bathroom Scale (The Tare Button)
Imagine a digital scale at a grocery store:
* In the morning, a tiny layer of dust settles on the scale.
* Before placing apples on the scale, the scale automatically recalibrates its "zero" mark (the tare weight).
* If the baseline zero changes slowly over the day, the scale adapts so that 1 kg of apples always reads exactly 1 kg.
* But if someone suddenly slams a 5 kg brick onto the scale in 1 second, the scale doesn't treat that as "recalibration" — it screams an overload error!

### Analogy 2: The Frog in Warm Water (Drift Velocity)
There is a famous biology fable about a frog:
* If you place a frog in water and heat it up very slowly over many hours, it slowly adapts to the temperature.
* But if you drop the water temperature by $10^\circ\text{C}$ in 5 seconds, the frog instantly reacts.
* In quantum fiber, temperature changes at a rate of **less than $0.5\%$ per hour**.
* If the error rate on our quantum link jumps by **$+4\%$ in 30 seconds**, that is physically impossible for weather to cause! That is an active cyber-attacker tapping the line!

---

## 📐 3. The Mathematics of Q-CALIBRATE

```
[Periodic Pilot Probe Pulses] ──► (num_trials, n_errors)
                                           │
                                           ▼
                       [Empirical Error Rate: e_hat = n1 / N]
                                           │
                                           ▼
            [Exponential Moving Average (EMA) Baseline Update]
             p0(t) = alpha * e_hat + (1 - alpha) * p0(t-1)
                                           │
               ┌───────────────────────────┴───────────────────────────┐
               ▼                                                       ▼
 [95% Wilson Confidence Interval]                             [Drift Velocity Monitor]
  SE = sqrt(p0(1 - p0) / N_total)                             v_drift = (Delta e / Delta t) * 60
  CI = [p0 - 1.96*SE, p0 + 1.96*SE]                           Is |v_drift| > 4%/min?
               │                                                       │
               ▼                                                       ▼
   [Feed Updated p0 to Q-STAT]                                [TAMPERING ALERT]
```

---

### 1. Exponential Moving Average (EMA) Update Rule
Every time a pilot probe pulse is measured, the calibrator updates the running baseline $p_0$:
$$p_0^{(t)} = \alpha_{\text{ema}} \hat{e}_{\text{pilot}} + (1 - \alpha_{\text{ema}}) p_0^{(t-1)}$$
- $\alpha_{\text{ema}} = 0.25$: Gives 25% weight to the latest measurement and 75% weight to past history.
- This creates smooth, stable tracking that ignores single random Poisson shot-noise spikes while adapting to real physical temperature trends.
- Physical Clamping: $p_0$ is strictly constrained to the physical bounds:
  $$0.005 \le p_0^{(t)} \le 0.200 \quad (0.5\% \text{ to } 20.0\%)$$

### 2. Drift Velocity Calculation ($\Delta p / \Delta t$)
To detect stealthy tampering, the calibrator calculates the **drift rate per minute**:
$$\text{drift\_rate} = \left( \frac{\hat{e}_{\text{latest}} - \hat{e}_{\text{oldest}}}{t_{\text{latest}} - t_{\text{oldest}}} \right) \times 60.0$$

- **Physical Bound:** Standard underground SMF-28 fiber cannot heat or cool faster than $0.04$ ($4.0\%$) per minute.
- **Anomalous Drift Tripwire:**
  $$\text{if } |\text{drift\_rate}| > 4.0\%/\text{min} \implies \text{Active Tampering Detected!}$$

---

## 🔍 4. Line-by-Line Technical Breakdown of `security/calibrate.py`

```
┌─────────────────────────────────────────────────────────────┐
│                    security/calibrate.py                    │
├─────────────────────────────────────────────────────────────┤
│  1. CalibrationSample Dataclass                             │
│  2. CalibrationStatus Dataclass                             │
│  3. DynamicNoiseCalibrator Class                            │
│     - __init__(nominal_p0=0.03, window_size=10, alpha=0.25) │
│     - ingest_pilot_measurement()                            │
│       • Step 1: Record pilot sample in sliding window       │
│       • Step 2: Compute EMA update of baseline p0           │
│       • Step 3: Calculate 95% Wilson confidence interval    │
│       • Step 4: Calculate drift rate per minute             │
│       • Step 5: Check anomalous drift tripwire              │
│     - get_current_baseline() (Exports live p0 to Q-STAT)    │
│     - reset() (Flushes history back to nominal)             │
└─────────────────────────────────────────────────────────────┘
```

---

### Component A: The Telemetry Dataclasses ([Lines 16–38](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/calibrate.py#L16-L38))

```python
@dataclass
class CalibrationSample:
    timestamp: float
    num_trials: int
    n_errors: int
    empirical_error: float

@dataclass
class CalibrationStatus:
    calibrated_p0: float
    confidence_interval_95: Tuple[float, float]
    sample_window_size: int
    drift_rate_per_min: float
    is_drift_anomalous: bool
    status_summary: str
```
- `CalibrationSample`: Records an individual pilot pulse measurement.
- `CalibrationStatus`: Packages the current health of the optical channel, the latest calibrated $p_0$, its 95% confidence interval, and the drift rate.

---

### Component B: The `DynamicNoiseCalibrator` Engine ([Lines 40–122](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/calibrate.py#L40-L122))

Let us trace what happens inside `ingest_pilot_measurement`:

#### 1. Sliding-Window Buffer Management ([Lines 63–71](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/calibrate.py#L63-L71))
```python
emp_err = n_errors / max(1, num_trials)
sample = CalibrationSample(timestamp=ts, num_trials=num_trials, n_errors=n_errors, empirical_error=emp_err)
self.history.append(sample)

if len(self.history) > self.window_size:
    self.history = self.history[-self.window_size:]
```
Maintains a rolling window of the last 10 pilot measurements (`window_size = 10`), discarding ancient data.

#### 2. EMA Filter & Boundary Clamping ([Lines 73–76](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/calibrate.py#L73-L76))
```python
self.current_calibrated_p0 = (self.alpha_ema * emp_err) + ((1.0 - self.alpha_ema) * self.current_calibrated_p0)
self.current_calibrated_p0 = float(np.clip(self.current_calibrated_p0, 0.005, 0.20))
```
Applies the EMA formula and clamps $p_0 \in [0.5\%, 20\%]$.

#### 3. 95% Confidence Interval ([Lines 78–82](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/calibrate.py#L78-L82))
```python
total_n = sum(s.num_trials for s in self.history)
se = float(np.sqrt(self.current_calibrated_p0 * (1.0 - self.current_calibrated_p0) / max(10, total_n)))
ci_lower = float(max(0.0, self.current_calibrated_p0 - 1.96 * se))
ci_upper = float(min(1.0, self.current_calibrated_p0 + 1.96 * se))
```
Uses the standard normal approximation ($1.96\sigma$) to output a formal 95% confidence interval for the current noise floor.

#### 4. Drift Velocity Tripwire ([Lines 84–98](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/calibrate.py#L84-L98))
```python
if len(self.history) >= 2:
    time_delta_sec = self.history[-1].timestamp - self.history[0].timestamp
    err_delta = self.history[-1].empirical_error - self.history[0].empirical_error
    if time_delta_sec > 0.01:
        drift_rate_per_min = float((err_delta / time_delta_sec) * 60.0)

is_drift_anomalous = abs(drift_rate_per_min) > self.max_allowable_drift
```
If the error rate is climbing or falling faster than $4\%$ per minute, `is_drift_anomalous = True`, triggering an active tampering warning!

---

## 🔗 5. How This File Connects to the Rest of the Framework

1. **Direct Integration with Q-STAT ([`security/detector.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/detector.py)):**
   Whenever Q-STAT performs verification, it requests the live noise floor:
   ```python
   active_p0 = calibrator.get_current_baseline()
   detector = QStatDetector(baseline_noise_p0=active_p0)
   ```
2. **Dashboard Visuals ([`app.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/app.py)):**
   The Streamlit top bar and sidebar display the live calibrated baseline $p_0(t)$, drift velocity, and confidence intervals to human operators in real time.

---

## 🎓 6. Professor's Viva / Hackathon Defense Guide

> **Judge:** *"Could a patient attacker slowly increase channel noise by 0.01% every hour to trick your auto-calibrator into accepting an eavesdropping attack?"*  
> **Your Answer:** *"No, sir/ma'am, for three mathematical reasons:  
> 1. **Hard Upper Bound:** The calibrator has a strict ceiling clamp at $p_0 \le 0.20$ (20%). An attacker can never push the baseline above 20%.  
> 2. **CHSH & Tomography Watchtowers:** Even if the attacker kept the error rate low, our device-independent CHSH Bell test (`security/chsh.py`) and Quantum State Tomography (`quantum/tomography.py`) monitor entanglement non-locality $S > 2.0$ and purity $\gamma$. An eavesdropper attempting intercept-and-resend immediately collapses state purity regardless of baseline calibration.  
> 3. **Information-Theoretic Security Bounds:** Under our finite-key analysis (`security/finite.py`), any baseline above 11% triggers key distillation starvation, terminating the session automatically."*

> **Judge:** *"Why use an Exponential Moving Average (EMA) rather than a simple moving average?"*  
> **Your Answer:** *"A simple moving average treats a measurement from 10 minutes ago with the exact same weight as a measurement from 2 seconds ago, introducing significant phase lag. An Exponential Moving Average (EMA) applies geometric weighting: $\alpha \hat{e} + (1-\alpha)p_0$, reacting faster to genuine environmental shifts while dampening high-frequency stochastic shot noise."*

---
*(End of Lesson 11. Whenever you are ready, reply with **"next"** to enter the Physical Hardware Defense Watchtowers starting with **Lesson 12: security/decoy.py**!)*
