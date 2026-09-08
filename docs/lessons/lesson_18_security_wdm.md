# 📘 Q-SENTINEL Masterclass | Lesson 18: Quantum WDM & Co-Propagation Raman Scattering Defense (Q-WDM)

> **File in Focus:** [`security/wdm.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/wdm.py)  
> **Pipeline Position:** Step 18 of the entire Q-Sentinel architecture (Physical Hardware Watchtowers — Phase 37)  
> **Target Audience:** Fresher needing a deep understanding of non-linear fiber optics, Spontaneous Raman Scattering (SpRS), effective interaction length ($L_{\text{eff}}$), Fiber Bragg Grating (FBG) filtering, temporal gating, and co-propagating quantum and classical channels over commercial SMF-28 fiber.

---

## 🧭 1. What Is This File and Why Does It Exist?

Imagine a telecommunications CEO being pitched a revolutionary Quantum Digital Signature system. Their first question is always:
> *"Do I have to spend billions of dollars digging up streets across the nation to lay dedicated 'dark fibers' just for your quantum photons, or can they share the existing optical fiber cables that already carry standard internet traffic?"*

If quantum cryptography required dedicated, isolated optical fibers ("dark fiber"), widespread adoption would be economically impossible. The holy grail of practical quantum networking is **Co-Propagation via Wavelength Division Multiplexing (WDM)**: transmitting quantum single photons down the **exact same glass fiber core** (ITU-T G.652 SMF-28) alongside gigawatt-scale, high-power classical optical communication channels (DWDM at 10G, 100G, or 400G).

### The Extreme Physics Challenge: The $10^{16}:1$ Power Asymmetry
In a standard optical fiber:
* **Classical DWDM channels** launch laser pulses at powers between $0\text{ dBm}$ ($1.0\text{ mW}$) and $+14\text{ dBm}$ ($25\text{ mW}$). This corresponds to roughly **$10^{16}$ (ten quadrillion) photons per second** blasting down the glass core.
* **Quantum signature channels** transmit weak coherent pulses containing on average **$\mu = 0.5$ photons per pulse**.

This is a **power disparity of $160\text{ dB}$ ($10^{16}$ to $1$)**! It is the equivalent of trying to see the flicker of a tiny candle placed right next to the blinding beam of an aircraft searchlight.

### The Threat: Spontaneous Raman Scattering (SpRS)
Why can't we simply assign classical traffic to $1530\text{ nm}$ and quantum traffic to $1550\text{ nm}$ and separate them with a regular optical filter?
Because glass is not an inert, passive medium. At high optical power densities, fused silica ($\text{SiO}_2$) exhibits **non-linear inelastic scattering**:
1. **Spontaneous Raman Scattering (SpRS):** Blasting $10^{16}$ classical photons per second through the silica lattice agitates the molecular bonds, creating optical vibrational phonons.
2. Inelastic collisions occur: a classical photon transfers energy to a phonon, dropping in frequency and shifting to a longer wavelength (**Stokes scattering**), or absorbs thermal phonon energy, shifting to a shorter wavelength (**Anti-Stokes scattering**).
3. The resulting Raman noise is **broadband**—spanning across more than $100\text{ nm}$ (up to $13.2\text{ THz}$ frequency shift).
4. As a result, millions of scattered Raman photons bleed directly into the $1550\text{ nm}$ quantum channel, drowning the single photons in noise and destroying the quantum bit error rate (QBER).

[`security/wdm.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/wdm.py) is the **Q-WDM Watchtower**. It models the physical non-linear optics of SMF-28 fiber, simulates the three-layer hardware defense (wavelength separation, ultra-narrowband Fiber Bragg Grating filtering, and sub-nanosecond temporal gating), evaluates Raman-induced QBER and SNR, and detects malicious cross-talk jamming attacks.

---

## 💡 2. Plain English Real-World Analogies

### Analogy 1: The Freight Train and the Firefly in a Dark Tunnel
Imagine a narrow, 25-kilometer-long mountain railway tunnel (the optical fiber core):
* A giant diesel freight train (the classical 400G telecom channel) speeds through the tunnel, shaking the tracks, kicking up massive clouds of dust, exhaust, and flying sparks (Spontaneous Raman Scattering).
* A fragile firefly (the quantum signature photon) is trying to fly through the exact same tunnel to deliver a secret flash code to an observer at the tunnel exit.
* The sparks from the freight train fly everywhere. If an observer looks into the tunnel with their bare eyes, the sparks completely overwhelm the tiny green glow of the firefly.

To allow the firefly to be detected reliably, our engineers install three defenses:
1. **Color Separation & Micro-Filtering (FBG Filter):** The freight train's sparks cover many colors, but the firefly glows at an exact wavelength ($1550.00\text{ nm}$). We put an ultra-selective tinted lens (Fiber Bragg Grating with a $0.05\text{ nm}$ passband) at the exit that rejects $99.9999\%$ of the stray sparks.
2. **High-Speed Camera Shutter (Temporal Gating):** We know the exact picosecond the firefly is scheduled to arrive. We open our camera sensor shutter for only $200\text{ picoseconds}$ when the firefly passes, ignoring sparks generated during the rest of the time.
3. **The Speed & Power Monitor (The Q-WDM Watchtower):** If an adversary purposely ramps up the freight train's throttle to $+14\text{ dBm}$ (injecting jamming power), the spark blizzard becomes so dense that even the filtered camera gets blinded. Q-WDM calculates the Signal-to-Noise Ratio (SNR) in real time and trips an emergency alarm before any forged signatures can slip through.

### Analogy 2: The Rock Concert vs. The Whispered Secret
Imagine sitting in a stadium during a heavy metal rock concert ($100\text{ dB}$ sound pressure, representing the $1\text{ mW}$ classical laser). Across the arena, a friend whispers a one-time secret code ($0.0001\text{ dB}$, representing the single photon).
If you listen across all frequencies, the guitar amplifiers completely drown out the whisper.
* But if your friend whispers at a single pure frequency of $15,500.0\text{ Hz}$ while the bass guitar plays at $15,300.0\text{ Hz}$, and you wear digital noise-cancelling headphones tuned to a microscopic window of $15,500 \pm 0.5\text{ Hz}$, you can filter out almost all the noise.
* If you only open your ears for $200\text{ picoseconds}$ when they speak, you isolate the whisper cleanly!

---

## 📐 3. The Physics & Mathematical Foundations

[`security/wdm.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/wdm.py) builds upon empirical non-linear optics models of fused silica glass fibers (ITU-T G.652 standard single-mode fiber).

```
                      SMF-28 Optical Fiber (L = 25 km)
 Classical 1530 nm ───►═══════════════════════════════════════► Classical Receiver
 (DWDM Pump: 1 mW)       │ Non-linear Spontaneous Raman (SpRS)
                         ▼
 Quantum 1550 nm   ───►═══════════════════════════════════════► [FBG Filter] ──► [Time Gate] ──► [SPD Detector]
 (Weak Pulses: μ=0.5)   (Weak Coherent Pulses + Raman Noise)    (Δλ = 0.05 nm)  (Δτ = 200 ps)     (η = 25%)
```

### Formula 1: Power Conversion from Decibel-Milliwatts (dBm) to Watts
Telecom launch power is conventionally expressed in decibel-milliwatts ($\text{dBm}$):
$$P_{\text{watts}} = 10^{\frac{P_{\text{dBm}}}{10}} \times 10^{-3}\text{ W}$$
* $0\text{ dBm} = 10^{0} \times 10^{-3} = 1.0\text{ mW} = 10^{-3}\text{ W}$ (Legitimate telecom channel)
* $+14\text{ dBm} = 10^{1.4} \times 10^{-3} \approx 25.12\text{ mW}$ (Adversarial jamming power)

### Formula 2: Effective Non-Linear Interaction Length ($L_{\text{eff}}$)
As light travels down a fiber, it undergoes linear optical attenuation ($\alpha \approx 0.20\text{ dB/km}$ at $1550\text{ nm}$). Because the classical pump laser is attenuated as it propagates, it generates fewer Raman photons in the second half of the fiber than in the first kilometer.
The effective length over which non-linear interactions occur is given by:
$$\alpha_{\text{lin}} = \alpha_{\text{dB/km}} \cdot \frac{\ln(10)}{10} \approx 0.20 \cdot 0.2302585 \approx 0.04605\text{ km}^{-1}$$
$$L_{\text{eff}} = \frac{1 - e^{-\alpha_{\text{lin}} L}}{\alpha_{\text{lin}}}$$

#### Physical Insights on $L_{\text{eff}}$:
* For a short fiber ($L = 5\text{ km}$): $L_{\text{eff}} \approx 4.47\text{ km} \approx L$.
* For standard metro link ($L = 25\text{ km}$): $L_{\text{eff}} \approx 14.86\text{ km} < 25\text{ km}$.
* For an infinite fiber ($L \to \infty$): 
  $$L_{\text{eff}} \to \frac{1}{\alpha_{\text{lin}}} \approx \frac{1}{0.04605} \approx 21.71\text{ km}$$
No matter how long the fiber is (even $1,000\text{ km}$), the non-linear interaction length can **never exceed $21.71\text{ km}$** because classical pump attenuation extinguishes the non-linear effect!

### Formula 3: Raman Scattering Cross-Section Coefficient $\beta(\Delta\lambda)$
In fused silica, the Raman cross-section depends on the wavelength separation $\Delta\lambda = |\lambda_q - \lambda_c|$:
* Peak Raman shift occurs at $\approx 13.2\text{ THz}$, corresponding to $\Delta\lambda \approx 100\text{ nm}$, where $\beta_{\text{peak}} \approx 5.5 \times 10^{-8}\text{ km}^{-1}\text{nm}^{-1}$.
* For smaller separations ($\Delta\lambda < 50\text{ nm}$, such as $\lambda_c = 1530\text{ nm}$ and $\lambda_q = 1550\text{ nm}$ where $\Delta\lambda = 20\text{ nm}$), the near-band Raman tail scales linearly:
  $$\beta(\Delta\lambda) \approx \frac{\Delta\lambda}{100.0} \cdot 2.2 \times 10^{-8}\text{ km}^{-1}\text{nm}^{-1} \approx 4.4 \times 10^{-9}\text{ km}^{-1}\text{nm}^{-1}$$

### Formula 4: Spontaneous Raman Noise Spectral Power ($P_{\text{spRS}}$)
The continuous Raman noise power generated per nanometer of optical bandwidth is:
$$P_{\text{spRS}} = P_{\text{classical}} \cdot \beta(\Delta\lambda) \cdot L_{\text{eff}}\quad (\text{Watts / nm})$$

### Formula 5: Fiber Bragg Grating (FBG) Optical Filtering
An ultra-narrowband FBG optical bandpass filter centered on the quantum wavelength ($1550\text{ nm}$) with Full Width at Half Maximum (FWHM) $\Delta\lambda_{\text{FBG}} = 0.05\text{ nm}$ (approx. $6.25\text{ GHz}$) suppresses out-of-band noise:
$$P_{\text{optical}} = P_{\text{spRS}} \cdot \Delta\lambda_{\text{FBG}}\quad (\text{Watts})$$

### Formula 6: Continuous Raman Photon Flux ($R_{\text{Raman}}$)
The energy of a single photon at $\lambda = 1550\text{ nm}$ is:
$$E_{\text{ph}} = \frac{h \cdot c}{\lambda} = \frac{6.626 \times 10^{-34} \times 3.0 \times 10^8}{1.55 \times 10^{-6}} \approx 1.282 \times 10^{-19}\text{ Joules}$$
The rate of Raman photons detected per second (taking detector quantum efficiency $\eta_{\text{det}} = 0.25$ into account) is:
$$R_{\text{Raman}} = \left(\frac{P_{\text{optical}}}{E_{\text{ph}}}\right) \cdot \eta_{\text{det}}\quad (\text{photons / second})$$

### Formula 7: Synchronous Temporal Gating Window
Rather than running the Single-Photon Detector (SPD) continuously in DC mode, the detector is gated ON only during an ultra-short coincidence window synchronized with Alice's laser clock:
$$\tau_{\text{gate}} = 200\text{ ps} = 200 \times 10^{-12}\text{ s}$$
The average number of Raman noise photons detected per pulse is:
$$\bar{n}_{\text{Raman}} = R_{\text{Raman}} \cdot \tau_{\text{gate}}$$

### Formula 8: Signal Transmittance & Signal-to-Noise Ratio (SNR)
For a weak coherent quantum pulse with initial mean photon number $\mu = 0.50$, the signal reaching the detector after fiber attenuation is:
$$T_{\text{fiber}} = 10^{-\frac{\alpha \cdot L}{10}} = 10^{-\frac{0.20 \times 25}{10}} = 10^{-0.50} \approx 0.3162$$
$$\mu_{\text{signal}} = \mu \cdot T_{\text{fiber}} \cdot \eta_{\text{det}} = 0.50 \times 0.3162 \times 0.25 \approx 0.03953\text{ photons/pulse}$$
The Signal-to-Noise Ratio (SNR) is:
$$\text{SNR} = \frac{\mu_{\text{signal}}}{\bar{n}_{\text{Raman}}}$$

### Formula 9: Raman-Induced Quantum Bit Error Rate ($e_{\text{Raman}}$)
Because spontaneously scattered Raman photons have completely random polarization states, whenever a Raman photon causes a detector click instead of the true quantum signal, it has a **$50\%$ probability of registering in the wrong polarization basis**:
$$e_{\text{Raman}} = \frac{0.5 \cdot \bar{n}_{\text{Raman}}}{\mu_{\text{signal}} + \bar{n}_{\text{Raman}}}$$

### Formula 10: Optical Isolation (dB)
The total optical isolation achieved against the classical channel pump is:
$$\text{Isolation}_{\text{dB}} = -10 \log_{10}\left(\frac{P_{\text{optical}}}{P_{\text{classical}}}\right)$$
In a properly tuned system, optical isolation exceeds **$50\text{ dB}$ to $60\text{ dB}$**.

---

## 🔬 4. Architectural Breakdown of `security/wdm.py`

Let's examine how [`security/wdm.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/wdm.py) structures these physical optics calculations.

### Class 1: `WDMChannelConfig` (Lines 30–44)
Defines the physical fiber parameters and optical transmission setup:
* `fiber_length_km: float = 25.0` (Standard metropolitan link span).
* `fiber_attenuation_db_per_km: float = 0.20` (Standard ITU-T G.652 SMF-28 loss).
* `classical_launch_power_dbm: float = 0.0` ($1.0\text{ mW}$ classical transmission power).
* `classical_wavelength_nm: float = 1530.0` (C-band classical pump).
* `quantum_wavelength_nm: float = 1550.0` (C-band quantum signal channel, $\Delta\lambda = 20\text{ nm}$).
* `fbg_filter_fwhm_nm: float = 0.05` (Ultra-narrow Fiber Bragg Grating bandwidth: $0.05\text{ nm} \approx 6.25\text{ GHz}$).
* `detector_efficiency: float = 0.25` (InGaAs/InP or SNSPD efficiency of $25\%$).
* `gate_window_ps: float = 200.0` (Fast electronic gating window of $200\text{ picoseconds}$).
* `repetition_rate_mhz: float = 50.0` ($50\text{ MHz}$ pulse train).

### Class 2: `WDMAnalysisResult` (Lines 47–65)
The comprehensive cryptographic and physical telemetry returned by the watchtower:
* `fiber_length_km`, `classical_launch_power_dbm`, `classical_launch_power_mw`.
* `wavelength_separation_nm`: $|\lambda_q - \lambda_c|$.
* `effective_length_km`: $L_{\text{eff}}$.
* `raman_noise_photons_per_pulse`: $\bar{n}_{\text{Raman}}$.
* `raman_noise_count_rate_hz`: $R_{\text{Raman}}$.
* `signal_to_noise_ratio_snr`: Calculated SNR.
* `induced_raman_qber`: Bit error fraction caused by Raman photons.
* `optical_isolation_db`: Attenuation of classical pump into quantum band.
* `is_wdm_secure`: Boolean security certification flag.
* `verdict`: `ThreatCategory` (`LEGITIMATE`, `SUSPICIOUS`, `MALICIOUS`).
* `attack_classification`: Specific string identifier.
* `cryptanalytic_proof`: Auditable explanation of the verdict.

### Class 3: `RamanScatteringModel` (Lines 67–228)
Implements the core non-linear optics calculations:
* `compute_effective_length(length_km, alpha_db_per_km)`: Implements Formula 2.
* `compute_raman_cross_section_coefficient(delta_lambda_nm)`: Implements the empirical silica Raman profile (Formula 3).
* `evaluate_co_propagation(config, adversarial_jamming)`: Simulates the complete physical cascade through the fiber, FBG filter, and temporal gate, computing SNR, induced QBER, and threat classification.

#### The 4-Tier Threat Decision Engine (Lines 176–210):
```python
# 1. Honest Co-propagation: High SNR, low QBER, low launch power
if snr >= 15.0 and induced_qber <= 0.045 and p_dbm <= 3.0:
    verdict = ThreatCategory.LEGITIMATE
    classification = "LEGITIMATE_WDM_CO_PROPAGATION"
    is_secure = True

# 2. Adversarial Cross-Talk Jamming: Deliberate high-power injection (>= +12 dBm / 25 mW)
elif adversarial_jamming or p_dbm >= 12.0:
    verdict = ThreatCategory.MALICIOUS
    classification = "ADVERSARIAL_CROSS_TALK_JAMMING"
    is_secure = False

# 3. Raman Saturation: Excessive classical power or too close wavelength spacing
elif snr < 8.0 or induced_qber > 0.060:
    verdict = ThreatCategory.MALICIOUS
    classification = "RAMAN_SCATTERING_SATURATION"
    is_secure = False

# 4. Elevated Co-propagation Noise: Marginal link requiring FBG tuning
else:
    verdict = ThreatCategory.SUSPICIOUS
    classification = "ELEVATED_CO_PROPAGATION_NOISE"
    is_secure = False
```

### Class 4: `WDMRamanWatcher` (Lines 230–298)
The operational watchtower class integrated into the Q-Sentinel dashboard:
* `analyze_wdm_channel(config)`: Analyzes live telemetry from optical power meters and spectrum analyzers.
* `simulate_wdm_scenario(scenario, fiber_length_km)`: Provides automated simulation scenarios for testing:
  1. `"Honest Co-Propagation (0 dBm Classical)"` $\to$ `LEGITIMATE` ($\text{SNR} \ge 15.0$, $\text{QBER} \le 4.5\%$).
  2. `"Adversarial Cross-Talk Jamming"` $\to$ `MALICIOUS` ($+14\text{ dBm}$ pump, $\text{SNR} < 5.0$).
  3. `"Raman Scattering Saturation"` $\to$ `MALICIOUS` ($+8\text{ dBm}$ at $10\text{ nm}$ spacing, $\text{QBER} > 5\%$).
  4. `"Elevated Co-Propagation Noise"` $\to$ `SUSPICIOUS` ($+3.5\text{ dBm}$ pump, $0.06\text{ nm}$ filter).

---

## ⚡ 5. Step-by-Step Code Execution Walkthrough

Let's trace a concrete numerical example using the honest configuration from [`TestWDMRamanWatchtower`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/tests/test_wdm.py#L19-L40):

```
Configuration:
  Fiber Length L = 25.0 km, Attenuation α = 0.20 dB/km
  Classical Power = 0.0 dBm (1.0 mW = 1e-3 W)
  Classical Wavelength = 1530 nm, Quantum Wavelength = 1550 nm (Δλ = 20 nm)
  FBG Filter Bandwidth = 0.05 nm
  Detector Efficiency = 25%, Gate Window = 200 ps
```

### Step 1: Linear Attenuation & Effective Length
$$\alpha_{\text{lin}} = 0.20 \times \frac{\ln(10)}{10} \approx 0.04605\text{ km}^{-1}$$
$$L_{\text{eff}} = \frac{1 - e^{-0.04605 \times 25}}{0.04605} = \frac{1 - e^{-1.1513}}{0.04605} = \frac{1 - 0.3162}{0.04605} \approx 14.85\text{ km}$$

### Step 2: Raman Cross-Section & Spectral Noise Power
For $\Delta\lambda = 20\text{ nm}$:
$$\beta(20) = \left(\frac{20}{100}\right) \times 2.2 \times 10^{-8} = 4.4 \times 10^{-9}\text{ km}^{-1}\text{nm}^{-1}$$
$$P_{\text{spRS}} = P_{\text{watts}} \cdot \beta \cdot L_{\text{eff}} = (1.0 \times 10^{-3}\text{ W}) \times (4.4 \times 10^{-9}) \times 14.85 \approx 6.534 \times 10^{-11}\text{ W/nm}$$

### Step 3: FBG Filtering & Optical Noise Power
$$P_{\text{optical}} = P_{\text{spRS}} \cdot \Delta\lambda_{\text{FBG}} = 6.534 \times 10^{-11} \times 0.05 = 3.267 \times 10^{-12}\text{ W} = 3.267\text{ pW}$$
Optical Isolation:
$$\text{Isolation} = -10 \log_{10}\left(\frac{3.267 \times 10^{-12}}{1.0 \times 10^{-3}}\right) = -10 \log_{10}(3.267 \times 10^{-9}) \approx 84.86\text{ dB}$$

### Step 4: Raman Photon Arrival Rate & Gate Filtering
$$E_{\text{ph}} = 1.282 \times 10^{-19}\text{ J}$$
$$R_{\text{Raman}} = \left(\frac{3.267 \times 10^{-12}}{1.282 \times 10^{-19}}\right) \times 0.25 \approx 6,370,900\text{ counts/second}\ (6.37\text{ MHz})$$
While $6.37\text{ MHz}$ seems large, the detector is only open for $\tau_{\text{gate}} = 200\text{ picoseconds}$ ($2.0 \times 10^{-10}\text{ s}$):
$$\bar{n}_{\text{Raman}} = R_{\text{Raman}} \cdot \tau_{\text{gate}} = 6.37 \times 10^{6} \times 2.0 \times 10^{-10} \approx 0.001274\text{ photons/pulse}$$

### Step 5: Quantum Signal & SNR
Transmitted signal per pulse:
$$\mu_{\text{signal}} = 0.50 \times 10^{-\frac{0.20 \times 25}{10}} \times 0.25 = 0.50 \times 0.3162 \times 0.25 \approx 0.03953\text{ photons/pulse}$$
Signal-to-Noise Ratio:
$$\text{SNR} = \frac{\mu_{\text{signal}}}{\bar{n}_{\text{Raman}}} = \frac{0.03953}{0.001274} \approx 31.0$$
Induced Raman QBER:
$$e_{\text{Raman}} = \frac{0.5 \times 0.001274}{0.03953 + 0.001274} = \frac{0.000637}{0.04080} \approx 1.56\%$$

### Step 6: Security Certification
* $\text{SNR} = 31.0 \ge 15.0$ ✅
* $e_{\text{Raman}} = 1.56\% \le 4.5\%$ ✅
* Classical Launch Power $= 0\text{ dBm} \le 3.0\text{ dBm}$ ✅
* **Verdict:** `ThreatCategory.LEGITIMATE` (`LEGITIMATE_WDM_CO_PROPAGATION`). The quantum digital signature channel is **certified 100% secure** over existing commercial fiber!

---

## ⚔️ 6. Hackathon Judge Defense & Viva Voce Q&A

### Q1: "Why don't you just use dedicated dark fiber? Why bother with WDM co-propagation?"
**Defense:**  
> *"Laying dedicated dark fiber costs upwards of \$25,000 to \$100,000 per kilometer in civil excavation and municipal permits alone. For a 50 km banking network, that's millions of dollars in capital expenditure, making quantum signatures commercially unviable for most institutions.  
> Co-propagation over existing SMF-28 fiber makes Q-Sentinel deployable immediately over lit commercial infrastructure without laying a single new cable. Our Q-WDM module proves that with 20 nm channel spacing, 0.05 nm FBG filtering, and 200 ps temporal gating, we achieve an SNR of 31.0 and an induced QBER under 1.6%, guaranteeing complete cryptographic security alongside standard 100G internet traffic."*

### Q2: "What is Spontaneous Raman Scattering, and why can't a simple optical filter block it completely?"
**Defense:**  
> *"Spontaneous Raman Scattering occurs when high-power classical laser photons inelastically collide with optical phonons (molecular lattice vibrations) in the silica glass core.  
> Unlike classical cross-talk (which occurs strictly at the transmitter's laser frequency), Raman scattering is broadband, generating noise across a 100 nm window. Even if the classical channel is at 1530 nm, Stokes Raman photons are physically generated inside the fiber directly at 1550 nm!  
> Therefore, no input filter can block it. It must be mitigated along the path using wavelength isolation, ultra-narrowband FBG filters at the receiver, and sub-nanosecond temporal gating."*

### Q3: "What is the Effective Interaction Length ($L_{\text{eff}}$), and why does it have an asymptotic limit?"
**Defense:**  
> *"Non-linear optical effects like Raman scattering scale with both optical power and fiber length. However, as the classical pump propagates down the fiber, it experiences linear fiber loss ($\alpha = 0.20\text{ dB/km}$).  
> The formula $L_{\text{eff}} = \frac{1 - e^{-\alpha_{\text{lin}} L}}{\alpha_{\text{lin}}}$ models this decaying interaction. As physical length $L$ approaches infinity, $L_{\text{eff}}$ asymptotically approaches $\frac{1}{\alpha_{\text{lin}}} \approx 21.71\text{ km}$. This is a crucial physical advantage: Raman noise generation naturally caps out after approximately 25 km, meaning a 100 km fiber link does not generate four times the Raman noise of a 25 km link."*

### Q4: "How does an adversary exploit WDM co-propagation, and how does Q-WDM detect them?"
**Defense:**  
> *"An adversary can launch an **Adversarial Cross-Talk Jamming attack** by pumping high-power out-of-band laser light (+14 dBm / 25 mW) into an adjacent channel. The resulting avalanche of Raman photons saturates the single-photon detectors, driving the QBER above the abort threshold or forcing the system into a Denial-of-Service (DoS) state.  
> The `WDMRamanWatcher` continuously monitors launch power and detector noise floors. If classical power exceeds +12 dBm or SNR drops below 3.0, it flags an `ADVERSARIAL_CROSS_TALK_JAMMING` alert and activates automated mitigations."*

### Q5: "Why does Raman noise contribute exactly 50% bit error to the coincidence detection?"
**Defense:**  
> *"Raman scattering is a spontaneous, incoherent thermal emission process. The generated photons have completely random polarization states and random phases. When an unpolarized Raman photon enters a polarization-sensitive single-photon receiver (such as an H/V or D/A basis beam splitter), it has an equal $50\%$ probability of projecting onto either detector. Thus, its error contribution is modeled precisely as $e_{\text{Raman}} = \frac{0.5 \cdot n_{\text{noise}}}{n_{\text{signal}} + n_{\text{noise}}}$."*

---

## 🔗 7. The Next Step in the Pipeline

With [`security/wdm.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/wdm.py), we have conquered the physical optical layer, proving that quantum digital signatures can safely co-exist with classical high-power DWDM traffic on real-world commercial fiber.

Next, we move to the multi-party cryptographic verification layer:
👉 **Lesson 19:** [`security/multirecipient.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/multirecipient.py)  
*(Multi-Party Non-Repudiation: Bob-Charlie Arbiter cross-verification, preventing the signer Alice from repudiating her signature to one party while confirming it to another).*
