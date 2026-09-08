# 📘 Q-SENTINEL Masterclass | Lesson 17: MDI-QDS & Untrusted Relay Watchtower (Q-MDI)

> **File in Focus:** [`security/mdi.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/mdi.py)  
> **Pipeline Position:** Step 17 of the entire Q-Sentinel architecture (Physical Hardware Watchtowers — Phase 36)  
> **Target Audience:** Fresher needing understanding of untrusted relay networks, two-photon interference, and 100% detector side-channel immunity.

---

## 🧭 1. What Is This File and Why Does It Exist?

In Lesson 14 ([`security/blind.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/blind.py)), we saw how sophisticated hackers can attack single-photon detectors using lasers to blind and manipulate them.
Even though we added monitors for bias current, beam centering, and timing entropy, an uncomfortable question remains for cybersecurity purists:
> *"What if an attacker discovers a brand-new detector side-channel attack that no one has ever seen before?"*

In 2012, physicists Hoi-Kwong Lo, Marcos Curty, and Bing Qi invented the ultimate solution:
**Measurement-Device-Independent (MDI) Quantum Cryptography.**

### The MDI Paradigm Shift: Outsource the Detectors to the Enemy!
- In standard quantum communication, Alice sends photons and Bob measures them with his detectors.
- In **MDI architecture**, **neither Alice nor Bob holds any detectors!** Alice and Bob are strictly *senders* (they only shoot photons).
- Both Alice and Bob send their photons into the network to a central **Untrusted Relay** (called Charles, who could be an untrusted telecom operator, or even the adversary Eve herself!).
- The relay performs a joint Bell-state measurement and publicly shouts out the results: *"I saw a coincidence click!"*

Why is this revolutionary?
**Because even if the untrusted relay is 100% owned, controlled, and hacked by an adversary, the adversary CANNOT steal the digital signature!**
MDI architecture provides **100% mathematical immunity against ALL present and future detector side-channel attacks by construction**!

[`security/mdi.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/mdi.py) is the **Q-MDI Watchtower**. It analyzes the announcements from the untrusted relay using **Hong-Ou-Mandel (HOM) two-photon interference visibility** and **symmetric coincidence error bounds ($e_Z \le 8\%$)**, instantly catching the relay if it attempts to lie, cheat, or spoof results!

---

## 💡 2. Plain English Real-World Analogies

### Analogy 1: The Corrupt Postmaster & The Invisible Ink Spark
Imagine Alice and Bob want to verify a signature contract across a war zone:
* They don't trust the local postmaster (Eve) who runs the central mail hub.
* Alice writes her bit on a letter with blue chemical ink; Bob writes his bit with red chemical ink.
* They both drop their sealed letters into Eve's mail sorting machine.
* The chemistry of the two inks has a magical property:
  - If Alice's bit and Bob's bit are **identical** (e.g. both 0 or both 1), the inks neutralize each other peacefully (**Zero sparks!**).
  - If Alice's bit and Bob's bit are **opposites** (one is 0, one is 1), the chemicals react and produce a bright purple spark!
* All Eve can see or shout is: *"I saw a purple spark!"* 
* Even if Eve tries to lie about seeing sparks, Alice and Bob cross-check their records later. If Eve claimed she saw a spark when Alice and Bob both sent `0`, **Eve is caught red-handed committing fraud!**

### Analogy 2: Why MDI Eliminates Detector Hacks
* If a burglar is trying to pick the lock on your front door, the best security isn't a thicker lock.
* The best security is **removing the lock entirely** and placing it in the middle of a public town square where everyone can watch!
* If you don't own any detectors, no hacker on Earth can blind your detectors.

---

## 📐 3. The Physics & Cryptanalysis of MDI-QDS

```
[Sender: Alice] ──► (Photon a) ──┐
                                  ├──► [50:50 Beam Splitter] ──► [Detector D1]
[Sender: Bob]   ──► (Photon b) ──┘           (At Untrusted Relay)    ──► [Detector D2]
                                                       │
                                                       ▼
                               [Coincidence Click between D1 and D2?]
                                                       │
                  ┌────────────────────────────────────┴────────────────────────────────────┐
                  ▼                                                                         ▼
     [Hong-Ou-Mandel Interference]                                            [Symmetric State Prohibition]
      Two identical photons BUNCH together!                                    If Alice=0 and Bob=0:
      Coincidence clicks physically FORBIDDEN!                                 Coincidence is physically impossible!
      V_HOM = (R_diff - R_same) / (R_diff + R_same) >= 70%                     Error rate e_Z <= 8.0%
                  │                                                                         │
                  └────────────────────────────────────┬────────────────────────────────────┘
                                                       ▼
                                   [Is Untrusted Relay Honest?]
                                   ├── YES ──► 🟢 CERTIFIED MDI RELAY HONEST (100% Detector Immune)
                                   └── NO  ──► 🔴 UNTRUSTED RELAY TAMPERING (Relay Faking Clicks)
```

---

### 1. Hong-Ou-Mandel (HOM) Two-Photon Interference (Bose-Einstein Bunching)
When two identical single photons enter the two input ports of a 50:50 beam splitter simultaneously:
- Because photons are **bosons**, their quantum probability amplitudes for both being transmitted or both being reflected cancel each other out by destructive interference!
- The two photons **always bunch together** and exit out of the *same* output port (either both hit $D_1$ or both hit $D_2$).
- **A simultaneous coincidence click (where $D_1$ clicks and $D_2$ clicks at the same instant) is strictly forbidden!**

### 2. Projecting onto the Singlet Bell State ($|\Psi^-\rangle$)
A coincidence click between detectors $D_1$ and $D_2$ announces that the incoming two-photon state was projected onto the anti-symmetric singlet Bell state:
$$|\Psi^-\rangle = \frac{|01\rangle - |10\rangle}{\sqrt{2}}$$

This leads to the foundational physical rule of MDI-QDS:
- If Alice and Bob send **identical states** in the Z-basis ($|00\rangle$ or $|11\rangle$): coincidence is **forbidden ($P = 0$)**!
- If Alice and Bob send **different states** in the Z-basis ($|01\rangle$ or $|10\rangle$): coincidence occurs with **$50\%$ probability**!

### 3. The 3 Relay Auditing Metrics in Q-MDI
Alice and Bob audit the relay using three mathematical tripwires:
1. **Hong-Ou-Mandel Visibility ($V_{\text{HOM}}$):**
   $$V_{\text{HOM}} = \frac{R_{\text{diff}} - R_{\text{same}}}{R_{\text{diff}} + R_{\text{same}}} \ge 70.0\%$$
   If $V_{\text{HOM}} < 40\%$, the photons are distinguishable (Eve injected fake classical light).
2. **Forbidden Symmetric Error Rate ($e_Z$):**
   $$e_Z = \frac{N_{\text{coinc}}(00) + N_{\text{coinc}}(11)}{N_{\text{total}}(00) + N_{\text{total}}(11)} \le 8.0\%$$
   If $e_Z > 8\%$, the relay is fabricating false Bell-state announcements!
3. **Announcement Basis Bias:**
   $$\text{Bias} = \frac{|R_Z - R_X|}{(R_Z + R_X)/2} \le 20.0\%$$

---

## 🔍 4. Line-by-Line Technical Breakdown of `security/mdi.py`

```
┌─────────────────────────────────────────────────────────────┐
│                      security/mdi.py                        │
├─────────────────────────────────────────────────────────────┤
│  1. MDIEvent & MDIAnalysisResult Dataclasses                │
│  2. MDIQuantumRelay Class (50:50 Beam Splitter Engine)      │
│     - simulate_bsm_trial() (HOM bunching & projection)      │
│  3. MDIRelayWatcher Class                                   │
│     - __init__(min_hom=0.70, max_z_err=0.08, max_bias=0.20)│
│     - analyze_mdi_session()                                 │
│       • Step 1: Sift Z-basis same vs diff trials            │
│       • Step 2: Sift X-basis same vs diff trials            │
│       • Step 3: Compute HOM Visibility V_HOM                │
│       • Step 4: Compute Z-basis forbidden error e_Z         │
│       • Step 5: Check announcement basis bias               │
│       • Step 6: Certify 100% detector side-channel immunity │
└─────────────────────────────────────────────────────────────┘
```

---

### Component A: The 50:50 Beam Splitter Simulation ([Lines 73–124](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/mdi.py#L73-L124))

```python
def simulate_bsm_trial(self, alice_bit: int, alice_basis: str, bob_bit: int, bob_basis: str, ...):
    eff_v = self.v_hom * (1.0 - spectral_distinguishability)

    if alice_basis == 'Z' and bob_basis == 'Z':
        if alice_bit == bob_bit:
            # Symmetric states |00> or |11>: Coincidence is physically forbidden!
            p_err = self.p_dark + (1.0 - eff_v) * 0.25
            return bool(np.random.rand() < p_err)
        else:
            # Anti-symmetric components (|01> and |10>): 50% |Psi-> projection
            p_coinc = 0.50 * eff_v + self.p_dark
            return bool(np.random.rand() < p_coinc)
```
Accurately models the quantum optics of Hong-Ou-Mandel bunching: identical inputs produce near-zero coincidences, while orthogonal inputs produce 50% coincidences.

---

### Component B: Auditing the Relay in `analyze_mdi_session` ([Lines 144–244](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/mdi.py#L144-L244))

```python
# 1. Z-basis error rate (coincidences on symmetric states |00> or |11>)
z_errors = sum(1 for e in z_same_trials if e.relay_coincidence)
z_err_rate = float(z_errors / max(1, len(z_same_trials)))

# 2. Z-basis signal rate (coincidences on orthogonal states |01> or |10>)
z_signals = sum(1 for e in z_diff_trials if e.relay_coincidence)
z_sig_rate = float(z_signals / max(1, len(z_diff_trials)))

# 3. Hong-Ou-Mandel Visibility
denom = z_sig_rate + z_err_rate
v_hom = float(np.clip((z_sig_rate - z_err_rate) / denom, 0.0, 1.0)) if denom > 1e-6 else 0.0

# 4. Threat Decision Tree:
if v_hom >= self.min_visibility and z_err_rate <= self.max_z_err and bias_ratio <= self.max_bias:
    verdict = ThreatCategory.LEGITIMATE
    classification = "CERTIFIED_MDI_RELAY_HONEST"
elif z_err_rate > self.max_z_err:
    verdict = ThreatCategory.MALICIOUS
    classification = "UNTRUSTED_RELAY_TAMPERING"
    proof = f"MALICIOUS: Forbidden symmetric coincidence error e_Z = {z_err_rate*100:.2f}% exceeds limit (8.0%). Relay is faking BSM announcements."
elif v_hom < 0.40:
    verdict = ThreatCategory.MALICIOUS
    classification = "DISTINGUISHABLE_PHOTON_SPOOF"
```

- When the relay is honest: $V_{\text{HOM}} \ge 70\%$, $e_Z \le 8\%$, certified **100% detector side-channel immune**!
- If the relay injects fabricated clicks: $e_Z$ spikes, immediately catching the rogue relay!

---

## 🔗 5. How This File Connects to the Rest of the Framework

1. **The Ultimate Detector Defense:**
   While [`security/blind.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/blind.py) monitors physical detectors, `security/mdi.py` provides the **architectural proof** that quantum digital signatures can be routed through completely untrusted central hubs without losing confidentiality.
2. **Dashboard UI ([`app.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/app.py)):**
   Renders real-time HOM visibility gauges ($V_{\text{HOM}}$), $e_Z$ error rates, and untrusted relay health statuses on the dedicated Q-MDI scorecard.
3. **Automated Audits ([`rehearsal.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/rehearsal.py)):**
   Rehearsal test #12 continuously validates that rogue untrusted relays are intercepted with zero false negatives.

---

## 🎓 6. Professor's Viva / Hackathon Defense Guide

> **Judge:** *"How can your protocol remain secure if the central relay performing the measurements is untrusted or controlled by the adversary?"*  
> **Your Answer:** *"In Measurement-Device-Independent (MDI) architecture, Alice and Bob never perform measurements; they only prepare and send quantum states to the relay. The untrusted relay performs a Bell-State Measurement (BSM) via Hong-Ou-Mandel two-photon interference and announces which detectors clicked.  
> Even if the relay is malicious and tampers with the detectors, it cannot gain information because it only measures the relative parity ($|\Psi^-\rangle$) of the two incoming photons, not their individual state values. Furthermore, in `security/mdi.py`, Alice and Bob cross-audit the relay: if the relay lies about coincidences, the forbidden symmetric error rate $e_Z$ exceeds $8\%$, immediately unmasking the rogue relay."*

> **Judge:** *"What is Hong-Ou-Mandel interference and why is it essential for MDI?"*  
> **Your Answer:** *"Hong-Ou-Mandel (HOM) interference is a quantum optical effect where two indistinguishable photons arriving at a 50:50 beam splitter bunch together and exit through the same port due to Bose-Einstein statistics. This suppresses coincidences between output detectors to zero. Coincidences only occur when photons are in the anti-symmetric singlet Bell state $|\Psi^-\rangle$. Measuring a high visibility ($V_{\text{HOM}} \ge 70\%$) confirms that genuine quantum two-photon interference took place at the relay, proving that the relay did not replace the quantum states with classical light."*

---
*(End of Lesson 17. Whenever you are ready, reply with **"next"** to proceed to Co-Propagation Fiber Defense in **Lesson 18: security/wdm.py**!)*
