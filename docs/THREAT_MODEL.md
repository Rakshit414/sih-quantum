# Q-SENTINEL: Formal Threat Model & Adversary Specification
**Document ID:** `SEC-TM-2026-01`  
**Classification:** Open Scientific Architecture / Hackathon Defense Asset  
**Standard Compliance:** NIST SP 800-53 Rev. 5, ISO/IEC 27001, OASIS STIX 2.1  

---

## 1. Executive Summary & Security Objectives

**Q-Sentinel** is a continuous, quantum-inspired threat detection and non-repudiation framework designed to safeguard **Teleportation-Based Quantum Digital Signatures (QDS)** over lossy, potentially hostile optical and classical networks.

The core security objectives of Q-Sentinel are:
1. **Existential Unforgeability**: Guarantee that no computationally bounded or unbounded adversary lacking Alice's private key state can produce a signature accepted by any verifier.
2. **Transferability & Non-Repudiation**: Prevent dispute attacks wherein a malicious or compromised signer (Alice) signs a message such that Verifier 1 (Bob) accepts while Verifier 2 (Charlie) rejects.
3. **Runtime Anomaly Surveillance**: Detect physical eavesdropping, channel manipulation, laser blinding, and Trojan-horse optical probes trial-by-trial without relying on non-deterministic AI/ML black boxes.
4. **Deterministic Auditability**: Maintain an append-only, tamper-evident cryptographic log of all signature transactions sealed via NIST FIPS 202 SHA3-256 hash chaining.

---

## 2. System Decomposition & Attack Surface

The system operates across three distinct domains:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. TRUSTED SIGNER ZONE (Alice)                                              │
│    • Private key state generation (Pauli basis selection: X, Y, Z)          │
│    • 3-Qubit Bell State Measurement (BSM) Engine                            │
│    • NIST FIPS 202 HMAC-SHA3-512 session nonce generator                    │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Quantum Fiber & Classical Network
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. UNTRUSTED ADVERSARIAL ZONE (Eve Channel / Untrusted Relays)              │
│    • Attacker capability: Active injection, beam-splitting, delay, tap      │
│    • Classical IP relay: Replay, packet modification, spoofing              │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Optical Receiver & Classical Sockets
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 3. TRUSTED VERIFIER SINK (Bob / Charlie)                                    │
│    • Pauli feed-forward correction: U = Z^{m1} · X^{m2}                     │
│    • Born-rule projective measurement array                                 │
│    • 14 Physical Optical Watchtowers (CHSH, Decoy, Trojan, APD Blinding)    │
│    • Dual-Tier Statistical Surveillance: Page CUSUM + Wald SPRT + Q-STAT    │
│    • Multi-Recipient Cross-Verification & Arbiter Exchange                  │
│    • OASIS STIX 2.1 SIEM Exporter & SHA3-256 Audit Ledger                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Adversary Profile & Threat Capabilities

We adopt a comprehensive threat model synthesizing classical network adversaries (Dolev-Yao) and physical quantum eavesdropping adversaries (Gottesman-Chuang, Ekert, Gisin):

| Threat Vector | Adversary Profile | Channel | Physics / Protocol Mechanism | Q-Sentinel Detection Watchtower |
| :--- | :--- | :--- | :--- | :--- |
| **T1: State Forgery** | Active Adversary | Quantum | Eve constructs fake quantum tokens without key; measures or fabricates random Pauli eigenstates. | **Projective Q-STAT & Wald SPRT** ($\hat{e} \approx 50\%$, $z > +50\sigma$, stop at $N \le 6$). |
| **T2: Signer Impersonation** | Rogue Signer | Quantum + Classical | Mallory claims to be Alice using unauthorized keys or random basis assignments. | **Dual-Basis Projection** ($\hat{e} \approx 33.3\%$, $z > +35\sigma$, SPRT stop at $N \le 18$). |
| **T3: Stale Token Replay** | Passive Interceptor | Classical IP | Eve retransmits valid past classical correction bits $(m_1, m_2)$ and token payloads. | **Freshness Registry** ($60\text{s}$ sliding time-window, monotonic UUID/SHA-256 nonces). |
| **T4: Photon Number Splitting (PNS)** | Eavesdropper | Quantum Fiber | Eve splits multi-photon pulses from attenuated coherent states, storing one copy in quantum memory. | **Decoy-State Watchtower** (3-intensity $\mu, \nu, \omega$ statistics, verifies $Y_0, Y_1, e_1$). |
| **T5: Detector Blinding** | Optical Attacker | Optical Diode | Eve shines high-power continuous-wave laser light into Bob's APD, forcing linear Geiger-mode operation. | **APD Current Watchtower** (Monitors bias voltage drops & photocurrent surges $> 50\,\mu\text{A}$). |
| **T6: Trojan-Horse Probing** | State Snooper | Alice's Tx | Eve fires bright laser pulses into Alice's transmitter to read internal phase modulator settings. | **Trojan Filter Watchtower** (Spectral optical bandpass & isolation monitoring $< 0.01\,\mu\text{W}$). |
| **T7: Intercept-Resend / Device Spoof** | Untrusted Hardware | Quantum Node | Eve tampers with detector hardware or performs classical intercept-resend. | **CHSH Bell Watchtower** (Evaluates $S = \|E(a,b) - E(a,b') + E(a',b) + E(a',b')\| > 2.0$). |
| **T8: WDM Raman Jamming** | Optical Co-prop | Shared Fiber | High-power classical telecom traffic produces spontaneous Raman scattering into 1550nm quantum band. | **WDM Raman Watchtower** (Monitors background noise power and Raman scattering threshold). |
| **T9: Signer Repudiation** | Malicious Signer | Verification Exchange | Alice crafts asymmetric tokens so Bob accepts, but Charlie later rejects during wire dispute. | **Multi-Recipient Cross-Verifier** ($\Delta e = \|e_{\text{Bob}} - e_{\text{Charlie}}\| \le 5.0\%$). |

---

## 4. Analytical Attack Bounds & Invariants

### 4.1 Full Forgery Attack Bound
When an attacker with zero knowledge of Alice's chosen Pauli basis ($X, Y, \text{ or } Z$) attempts to forge a signature token:
$$\langle \psi_{\text{expected}} | \psi_{\text{forged}} \rangle = \frac{1}{\sqrt{2}} \implies P(\text{error}) = 1 - |\langle \psi_{\text{expected}} | \psi_{\text{forged}} \rangle|^2 = 0.50$$
Under ambient noise baseline $p_0 = 0.030$ and $N = 400$ total trials:
$$\sigma_0 = \sqrt{\frac{p_0(1 - p_0)}{N}} = \sqrt{\frac{0.03 \times 0.97}{400}} \approx 0.008529$$
$$z_{\text{forgery}} = \frac{0.4915 - 0.030}{0.008529} \approx +54.11\sigma$$
The corresponding one-tailed binomial $p$-value satisfies $p < 10^{-15}$.

### 4.2 Partial-Token / Low-Rate Attacker Scenario
An advanced adaptive attacker might attempt to tamper with only $k < m$ tokens (e.g. only 1 token out of 8) in order to keep the session-averaged error rate below the $z = 2.0$ boundary.

**Q-Sentinel's Defense Invariant:**
1. **Per-Token Projective Partitioning**: Each token is evaluated individually across its $n_{\text{trials}} = 50$ projective measurements.
2. **Page's CUSUM Step-Detector**: The Cumulative Sum control chart tracks incremental log-likelihood ratio shifts:
   $$C_n = \max(0, C_{n-1} + x_n - k_{\text{ref}})$$
   where $k_{\text{ref}} = 0.18$. Even a single corrupted token generates an error burst with $\hat{e} \approx 50\%$, causing $C_n$ to breach the decision boundary $h = 8.5$ within 18 trials.
3. **Cryptographic Diffusion**: Because the message is compressed using NIST FIPS 202 SHA-256 / SHA3-256, altering even 1 bit of the signed transaction flips $\approx 50\%$ of the output hash digest bits (Avalanche Effect). Thus, an attacker cannot selectively tamper with just 1 token and produce a valid signature for an altered message.

---

## 5. Trust Assumptions & Out-of-Scope Boundaries

### 5.1 In-Scope (Protected by Q-Sentinel)
- Optical fiber attenuation, dispersion, and thermal birefringence.
- Active classical eavesdropping, packet alteration, and replay.
- Beam-splitting, intercept-resend, and detector blinding attacks on quantum channels.
- Rogue relay nodes in Measurement-Device-Independent (MDI) configuration.
- Single-point and burst error injection.

### 5.2 Out-of-Scope (Environmental Assumptions)
1. **Physical Endpoint Security**: We assume Alice's and Bob's local cryptographic host modules are enclosed within physical tamper-responding enclosures (FIPS 140-3 Level 4). Direct memory scraping or cold-boot attacks against local host RAM are outside the scope of optical communication watchtowers.
2. **True Random Number Generator (TRNG)**: We assume local basis selection is seeded by an uncompromised quantum or hardware physical RNG (e.g. QNu Labs Tropos QRNG, compliant with NIST SP 800-90B).
3. **Permanent DoS (Fiber Cut)**: Physical fiber cuts naturally result in complete loss of communication (verdict: Channel Broken / Aborted). Availability attacks that cut fiber cannot forge signatures.
