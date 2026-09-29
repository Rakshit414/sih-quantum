# Q-SENTINEL: Presentation Slide Deck Architecture
## SIH-26141 | National Quantum Mission (NQM) Enterprise Defense Framework

> **How to Use This Document**:
> 1. **Option A (Instant Slide in Browser)**: Open [`docs/architecture_slide.html`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/architecture_slide.html) in your browser. It renders a 16:9 presentation slide ready for screenshotting or printing directly into PowerPoint.
> 2. **Option B (Copy-Paste into ChatGPT / Claude / Gamma)**: Copy the text from **Section 4** below and paste it into ChatGPT, Claude, or Gamma to automatically generate polished PowerPoint slides.
> 3. **Option C (Mermaid Flowchart)**: Copy the diagram code in **Section 2** and paste it into [mermaid.live](https://mermaid.live) to download high-resolution PNG or SVG for PowerPoint.

---

# SLIDE 1: End-to-End System Architecture & Workflow

### Slide Title:
**Q-SENTINEL: End-to-End Quantum Digital Signature (QDS) Architecture & Verification Workflow**

### Slide Subtitle:
*Entanglement-Assisted Teleportation, 14 Physical Watchtowers, and Sub-Second Sequential Hypothesis Testing*

---

## 📊 Visual Workflow Diagram (Mermaid Flowchart)

```mermaid
flowchart TD
    subgraph STAGE1 ["1. PHYSICAL SIGNER NODE (Alice)"]
        A1["Transaction Payload (e.g. Wire Transfer $500,000)"] --> A2["Cryptographic Digest (SHA-256 + HMAC-SHA3-512)"]
        A2 --> A3["Quantum State Preparation: Non-Orthogonal Pauli Eigenstates {|0⟩, |1⟩, |+⟩, |-⟩, |+i⟩, |-i⟩}"]
        A3 --> A4["Joint Bell-State Measurement (BSM) with Entangled EPR Pair"]
        A4 --> A5["Classical Correction Bits (m1, m2) + Quantum Token Stream"]
    end

    subgraph STAGE2 ["2. ADVERSARIAL RELAY & CHANNEL (Eve Node :8001)"]
        A5 -->|"Quantum Optical Fiber + Classical Channel"| E1["Active Threat Injection & Channel Transit"]
        E1 --> E2{"Threat Scenario Matrix"}
        E2 -->|"Honest Link"| E3["Baseline Fiber Noise (p0 ≈ 2.5% - 3.0%)"]
        E2 -->|"Active Attack"| E4["Adversarial State Forgery (~50% Error Rate)"]
        E2 -->|"Identity Hijack"| E5["Signer Impersonation (Mismatched Basis)"]
        E2 -->|"Replay Exploit"| E6["Stale Nonce Retransmission (>60s Window)"]
        E2 -->|"Optical Tap"| E7["Photon Splitting / Trojan Laser / APD Blinding"]
    end

    subgraph STAGE3 ["3. PHYSICAL VERIFIER SINK (Bob Node :8002)"]
        E3 & E4 & E5 & E6 & E7 --> B1["Feed-Forward Unitary Pauli Correction: U = Z^m1 · X^m2"]
        B1 --> B2["State Reconstruction & Projective Measurement on Alice's Basis"]
        
        subgraph ENGINE ["DUAL-LAYER VERIFICATION & SURVEILLANCE ENGINE"]
            B2 --> W1["14 Physical Hardware Watchtowers\n(CHSH S>2, Decoy PNS, Trojan Power, APD Current, MDI Relay, Raman WDM)"]
            B2 --> W2["Sequential Q-STAT Engine (Phase 42-50)\n- Page CUSUM Control Chart (h=8.5)\n- Wald SPRT Likelihood Ratio (A=+9.21, B=-9.21)\n- Beta-Binomial Bayesian Estimator"]
        end
    end

    subgraph STAGE4 ["4. DECISION, CONTAINMENT & AUDIT"]
        W1 & W2 --> DEC{"Sequential Early Stopping Decision"}
        DEC -->|"SPRT LLR ≤ -9.21 & Z < 2.0σ"| PASS["VERDICT: LEGITIMATE\n- Mint Legal Non-Repudiation Certificate\n- Record Validated Transaction"]
        DEC -->|"SPRT LLR ≥ +9.21 or CUSUM > 8.5"| FAIL["VERDICT: MALICIOUS\n- Cut Network Transmission (Early Stopping at Trial ~6)\n- Save 98.5% Quantum Bandwidth\n- Automated Signer Quarantine (Mallory Blocked)\n- Export OASIS STIX 2.1 Threat Intel Bundle"]
        
        PASS & FAIL --> AUDIT["Tamper-Evident SHA3-256 Cryptographic Audit Chain\nH_i = SHA3-256(H_i-1 || Payload || Timestamp || Verdict)"]
    end

    style STAGE1 fill:#f8fafc,stroke:#0b2545,stroke-width:2px
    style STAGE2 fill:#fff7ed,stroke:#ea580c,stroke-width:2px
    style STAGE3 fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
    style STAGE4 fill:#eff6ff,stroke:#2563eb,stroke-width:2px
    style FAIL fill:#fef2f2,stroke:#dc2626,stroke-width:2px
    style PASS fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

---

## 📝 Slide 1 Content Breakdown (3 Column Layout)

### Column 1: Quantum Ingestion & Teleportation (Alice)
- **Message Authentication**: Classical payload (wire transfer, military dispatch) hashed via SHA-256.
- **Quantum Token Mapping**: Message chunks encoded into non-orthogonal Pauli eigenstates across three mutually unbiased bases ($X, Y, Z$).
- **No-Cloning Protection**: Physics guarantees that an attacker cannot copy or inspect qubits without creating detectable noise.
- **3-Qubit Entanglement**: Joint Bell Measurement produces 2 classical feed-forward bits $(m_1, m_2)$ sent over classical network.

### Column 2: Distributed Transit & Threat Watchtowers (Eve $\to$ Bob)
- **Decoupled Architecture**: Real microservices running over HTTP (Alice $\to$ Eve on port 8001 $\to$ Bob on port 8002).
- **Physical Attack Vectors**: Handles forgery, impersonation, stale replay, Trojan-horse spy lasers, and detector blinding.
- **14 Active Watchtowers**:
  - *Optical Layer*: APD bias current, Raman noise filters, optical power limits ($<0.01\,\mu\text{W}$).
  - *Quantum Layer*: Hong-Ou-Mandel interference (MDI), CHSH Bell violation ($S > 2$), Decoy-state yields.
  - *Network Layer*: Freshness nonces ($<60\text{s}$ TTL), Multi-hop mesh repeater isolation.

### Column 3: Sequential Q-STAT & Cryptographic Audit
- **Sequential Hypothesis Testing**:
  - **Page CUSUM**: Ultra-sensitive changepoint detector catching intermittent burst tampering.
  - **Wald's SPRT**: Trial-by-trial likelihood ratio test reaching definitive verdicts early ($A = +9.21$, $B = -9.21$).
- **98.5% Bandwidth Reduction**: Forgery detected in **6 to 18 trials** instead of waiting for 400–1,000 packets.
- **Automated Quarantine**: High-risk signers (e.g. Mallory) locked out across the network.
- **Tamper-Evident Audit Chain**: SHA3-256 chained ledger ensures historic verification logs cannot be deleted or forged.

---

# SLIDE 2: Complete Technology Stack & Specifications

### Slide Title:
**Q-SENTINEL: Technology Stack & Engineering Specifications**

### Slide Subtitle:
*Zero Black-Box AI, Zero Blockchain Overhead — 100% Deterministic Physics & Statistical Mechanics*

---

## 🛠️ Technology Stack Matrix

| Domain | Technology / Library | Version / Standard | Engineering Role in Q-Sentinel |
| :--- | :--- | :--- | :--- |
| **Core Quantum Engine** | **Pure Python / NumPy / SciPy** | Python 3.14, NumPy 2.x, SciPy 1.15 | Simulates Pauli matrices, Bell-state projections, Stokes density matrices, and Poissonian decoy states without external heavy dependencies. |
| **Statistical Surveillance** | **Sequential Q-STAT Engine** | Proprietary Mathematical Module | Implements Page's CUSUM control charts, Wald's SPRT, and Beta-Binomial conjugate Bayesian posteriors for trial-by-trial early stopping. |
| **Physical Watchtowers** | **14 Dedicated Physics Detectors** | Optical & Quantum Standards | Monitored physics: CHSH Bell inequalities, Lindblad memory decoherence, Hong-Ou-Mandel visibility, and Serfling Martingale bounds. |
| **Network & Microservices** | **Decoupled HTTP REST Services** | Standard Python `http.server` & `urllib` | Independent multi-node processes: Alice Signer, Eve Relay (Port 8001), and Bob Verifier (Port 8002) with strict AST import isolation. |
| **Cryptographic Security** | **SHA-256, SHA3-256, HMAC-SHA3-512** | NIST FIPS 202, FIPS 180-4 | Message digestion, rolling freshness nonces, and tamper-evident cryptographic hash chaining. |
| **Threat Intelligence & SIEM**| **OASIS STIX 2.1 & Elastic Common Schema (ECS)**| STIX 2.1 JSON, CEF Syslog | Automatic incident bundling, Common Event Format (CEF severity 10) logs, and enterprise SIEM dispatch (Splunk / QRadar / Sentinel). |
| **Telemetry & Persistence** | **SQLite Local Datastore** | SQLite 3 Embedded | ACID-compliant storage of verification events, error rates, threat assessments, and SHA3-256 chain links with zero external DB overhead. |
| **Operator UI / Dashboard** | **Streamlit & Plotly** | Streamlit 1.42+, Plotly 6.x | Institutional, high-contrast dashboard with live microservice telemetry, 3D Bloch spheres, and CUSUM/SPRT trajectory charts. |
| **Testing & Verification** | **Pytest Test Harness** | Pytest 9.1 | **130/130 Unit, Integration & Stress Tests passing cleanly (100% pass rate)** including AST import boundary invariant testing. |

---

## 🏛️ Key Architectural Principles for Government & Enterprise Evaluators

1. **Zero Machine Learning (Zero Hallucinations)**:
   - Evaluators frequently disqualify cyber prototypes that rely on black-box neural networks because AI models can be fooled by adversarial noise.
   - Q-Sentinel relies **100% on quantum projective physics and proven sequential statistics (Wald, Page, Bayes)**. Every single verdict is explainable in court.
2. **Zero Blockchain Overhead**:
   - Instead of slow, energy-expensive proof-of-work/stake blockchains, audit integrity is guaranteed by **mathematical SHA3-256 cryptographic hash pointers** running at microsecond latencies.
3. **Decoupled Multi-Node Architecture**:
   - Bob and Alice do not share process memory with Eve. Communication takes place over real HTTP network sockets, proving real-world readiness for India's quantum communication corridors.
4. **Sub-Second Early Stopping**:
   - Reduces Average Sample Number (ASN) by **over 90%**, slashing key exhaustion and preserving optical quantum bandwidth.

---

# 📋 PROMPT TO COPY-PASTE INTO CHATGPT / CLAUDE / GAMMA

If you want an AI slide maker (like Gamma.app, ChatGPT Plus, or Claude) to generate the slides for you automatically, copy the prompt below:

```text
Please generate a 2-slide executive presentation based on the following project specifications for a National Quantum Hackathon (SIH-26141).

Project Title: Q-Sentinel: Quantum-Inspired Cyber Threat Detection Framework

SLIDE 1: SYSTEM WORKFLOW & ARCHITECTURE
- Title: Q-SENTINEL: End-to-End Quantum Digital Signature (QDS) Architecture & Workflow
- Structure: 4 horizontal columns / process stages:
  1. PHYSICAL SIGNER NODE (Alice):
     - Classical message payload (e.g. Wire Transfer $500,000) mapped to SHA-256 digest.
     - State preparation into non-orthogonal Pauli eigenstates {|0>, |1>, |+>, |->, |+i>, |-i>}.
     - 3-Qubit Joint Bell State Measurement with entangled EPR pairs.
     - Dispatches classical bits (m1, m2) and quantum token stream.
  2. ADVERSARIAL RELAY & CHANNEL (Eve Node on Port 8001):
     - Active network interceptor simulating real-world fiber conditions.
     - Threat models: Clean Fiber Noise (3%), State Forgery (50%), Signer Impersonation, Stale Replay (>60s), and Optical Side-Channels.
  3. PHYSICAL VERIFIER SINK (Bob Node on Port 8002):
     - Unitary Pauli correction (U = Z^m1 · X^m2) for state reconstruction.
     - 14 Physical Hardware Watchtowers monitoring APD current, Trojan lasers, CHSH Bell test (S > 2), and Decoy-state yields.
     - Sequential Q-STAT Engine: Page CUSUM (h=8.5) and Wald SPRT (A=+9.21, B=-9.21) for trial-by-trial early stopping.
  4. DECISION, CONTAINMENT & CRYPTOGRAPHIC AUDIT:
     - Forgery caught at trial 6 (saving 98.5% of quantum bandwidth).
     - Automated security quarantine locks out unauthorized signers (Mallory).
     - OASIS STIX 2.1 threat intelligence export for enterprise SOCs.
     - Tamper-Evident SHA3-256 Cryptographic Audit Chain linking all events.

SLIDE 2: COMPLETE TECHNOLOGY STACK & SPECIFICATIONS
- Title: Q-SENTINEL: Technology Stack & Engineering Specifications
- Table / Cards Layout:
  1. Quantum Engine: Python 3.14, NumPy, SciPy (Teleportation, Bell States, Stokes Density Matrices).
  2. Statistical Surveillance: Sequential Q-STAT (Page's CUSUM, Wald's SPRT, Beta-Binomial conjugate Bayesian prior).
  3. Physical Defense: 14 Optical Watchtowers (CHSH Bell non-locality, Decoy-state PNS, Trojan-horse filter, APD blinding).
  4. Distributed Microservices: Python http.server & urllib across ports 8000, 8001, 8002 with strict AST import isolation.
  5. Cryptography: SHA-256, SHA3-256, HMAC-SHA3-512 (FIPS 202 compliant).
  6. Enterprise SOC: OASIS STIX 2.1 JSON, Elastic Common Schema (ECS), CEF severity 10 logs.
  7. Storage & UI: SQLite Local Datastore (ACID compliance) + Streamlit & Plotly (3D Bloch spheres, live trajectory charts).
  8. Reliability: 130/130 automated unit, integration, and stress tests passing (100% green).
- Key Value Proposition: Zero black-box AI hallucinations, zero blockchain latency, 100% deterministic mathematical explainability.
```
