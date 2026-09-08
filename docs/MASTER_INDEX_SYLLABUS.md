# 🗺️ Q-SENTINEL Masterclass: Complete 37-Lesson Syllabus & Master Index

> **Framework:** Q-SENTINEL (Quantum-Inspired Cyber Threat Detection for Teleportation-based QDS)  
> **Problem Statement ID:** SIH-26141 | Smart India Hackathon Grand Finale  
> **Purpose:** Comprehensive navigation manual and exhaustive syllabus. Use this guide to locate any topic, formula, code module, attack vector, or defense question without reading through all 37 lesson files.

---

## 🧭 How to Use This Master Index
1. **Need a quick answer for a judge question?** Jump to the [Topic Finder & Fast-Lookup Matrix](#-1-topic-finder--fast-lookup-matrix) to find the exact lesson.
2. **Short on time before presentation?** Follow the [Targeted Learning Pathways](#-2-targeted-learning-pathways).
3. **Want to know exactly what is inside a specific lesson?** Read the [Exhaustive Lesson-by-Lesson Directory (01–37)](#-3-exhaustive-lesson-by-lesson-directory).

---

## ⚡ 1. Topic Finder & Fast-Lookup Matrix

| If You Need to Learn / Explain / Defend... | Exact Lesson to Study | Primary Source File | Key Concepts & Formulas |
|---|---|---|---|
| **Qubits, Pauli matrices, Bloch sphere, state normalization** | [Lesson 01](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_01_quantum_state.md) | [`quantum/state.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/state.py) | $\langle \psi \mid \psi \rangle = 1$, Pauli $\sigma_X, \sigma_Y, \sigma_Z$, 6 eigenstates, fidelity $F$, density matrix $\rho$ |
| **Entanglement, 4 Bell states, partial trace, purity** | [Lesson 02](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_02_quantum_bell.md) | [`quantum/bell.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/bell.py) | $|\Phi^+\rangle, |\Phi^-\rangle, |\Psi^+\rangle, |\Psi^-\rangle$, CNOT gate, $\text{Tr}_B(\rho_{AB}) = \frac{1}{2}I_2$, purity $\gamma = 0.5$ |
| **Quantum Teleportation protocol, Bell measurement, Pauli correction** | [Lesson 03](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_03_quantum_teleport.md) | [`quantum/teleport.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/teleport.py) | 3-qubit state space ($8 \times 1$), Bell State Measurement, $U = Z^{b_1} X^{b_2}$, 100% state recovery |
| **Born rule projection, quantum measurement, shot-noise sampling** | [Lesson 04](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_04_quantum_measure.md) | [`quantum/measure.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/measure.py) | $P(m) = \|\langle m \mid \psi \rangle\|^2$, Bernoulli trial simulation, single-click vs $N$-shot empirical convergence |
| **Quantum State Tomography (QST), Stokes parameters, density matrices** | [Lesson 05](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_05_quantum_tomography.md) | [`quantum/tomography.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/tomography.py) | Stokes $S_1, S_2, S_3$, $\rho = \frac{1}{2}(I + \vec{S}\cdot\vec{\sigma})$, Purity $\gamma = \text{Tr}(\rho^2)$, Von Neumann entropy |
| **Multi-hop quantum networks, entanglement swapping, rogue repeaters** | [Lesson 06](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_06_quantum_mesh.md) | [`quantum/mesh.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/mesh.py) | 4-qubit entanglement swapping, BSM at repeater, end-to-end Bell link, rogue repeater fault localization |
| **QDS architecture, signature token generation, SHA-256 digest binding** | [Lesson 07](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_07_security_signature.md) | [`security/signature.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/signature.py) | `QDSKeyManager`, `SignatureToken`, SHA-256 hash bit-pair mapping to Pauli eigenstates |
| **Anti-replay defense, freshness registries, sliding time windows** | [Lesson 08](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_08_security_freshness.md) | [`security/freshness.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/freshness.py) | `FreshnessRegistry`, 60s sliding window, monotonic nonce tracking, garbage collection |
| **Threat modeling: Forgery, Impersonation, Replay, Channel Noise** | [Lesson 09](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_09_security_attacks.md) | [`security/attacks.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/attacks.py) | `ThreatOrchestrator`, Forgery ($e \approx 50\%$), Impersonation ($e \ge 18\%$), Replay metadata, channel disturbance $\epsilon$ |
| **Exact Binomial hypothesis testing, standardized z-score, 3-tier verdicts** | [Lesson 10](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_10_security_detector.md) | [`security/detector.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/detector.py) | Q-STAT engine, `scipy.stats.binomtest`, $z = \frac{\hat{e}-p_0}{\sigma_0}$, Green ($z<2$), Yellow ($2 \le z < 4$), Red ($z \ge 4$) |
| **Dynamic baseline noise calibration, EMA filter, thermal drift tripwire** | [Lesson 11](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_11_security_calibrate.md) | [`security/calibrate.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/calibrate.py) | Q-CALIBRATE, EMA $\bar{p}_t = \alpha p_t + (1-\alpha)\bar{p}_{t-1}$ ($\alpha=0.25$), drift velocity anomaly detection |
| **Photon Number Splitting (PNS), 3-intensity decoy-state protocol** | [Lesson 12](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_12_security_decoy.md) | [`security/decoy.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/decoy.py) | Q-DECOY, Poisson statistics $P(n\mid\mu)$, Hwang-Lo bounds: single-photon yield $Y_1$, error rate $e_1$ |
| **Trojan-Horse optical probes, multi-spectral sensors, Lindblad decay** | [Lesson 13](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_13_security_trojan.md) | [`security/trojan.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/trojan.py) | Q-TROJAN, 4-sensor defense, back-reflection $P_{\text{refl}} \ge 1.5\text{ nW}$, Helstrom-Holevo mutual info $I_E \le 0.01\text{ bits}$ |
| **APD detector blinding, CW laser takeover, inter-arrival entropy** | [Lesson 14](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_14_security_blind.md) | [`security/blind.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/blind.py) | Q-BLIND, Makarov-Lydersen attack, APD DC current $I_{\text{bias}} \ge 5\mu\text{A}$, spatial beam shift, Shannon timing entropy |
| **Device-Independent Bell test, CHSH inequality, Tsirelson bound** | [Lesson 15](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_15_security_chsh.md) | [`security/chsh.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/chsh.py) | Q-CHSH, correlation $S$, classical bound $S \le 2.0$, quantum Tsirelson bound $S \le 2\sqrt{2} \approx 2.8284$, separable spoofing |
| **Composable finite-key security, Serfling martingale, key extraction** | [Lesson 16](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_16_security_finite.md) | [`security/finite.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/finite.py) | Q-FINITE, composable security $\varepsilon \le 10^{-10}$, Serfling deviation $\xi$, Leftover Hash Lemma extractable length $\ell$ |
| **Measurement-Device-Independent (MDI) QDS, untrusted relay, HOM dip** | [Lesson 17](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_17_security_mdi.md) | [`security/mdi.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/mdi.py) | Q-MDI, untrusted relay, Hong-Ou-Mandel visibility $V_{\text{HOM}} \ge 70\%$, symmetric coincidence error bound $e_Z \le 8\%$ |
| **WDM co-propagation, spontaneous Raman scattering (SpRS), FBG filters** | [Lesson 18](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_18_security_wdm.md) | [`security/wdm.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/wdm.py) | Q-WDM, ITU-T G.652 SMF-28 fiber, effective length $L_{\text{eff}}$, Raman cross-talk, 0.05nm FBG, 200ps temporal gating, SNR |
| **Multi-recipient non-repudiation, token symmetrization, arbiter dispute** | [Lesson 19](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_19_security_multirecipient.md) | [`security/multirecipient.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/multirecipient.py) | Q-REPUDIATE, Andersson-Curty-Jex protocol, Bob-Charlie cross discrepancy $D_{\text{cross}} \le 12.5\%$, dispute arbitration |
| **Post-Quantum Hybrid defense, HMAC-SHA3-512 + QDS, constant-time compare** | [Lesson 20](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_20_security_hybrid.md) | [`security/hybrid.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/hybrid.py) | Q-HYBRID, NIST FIPS 202 Keccak sponge ($b=1600$), constant-time comparison, 4-case dual-layer decision matrix |
| **Automated SOAR containment, nonce revocation, quarantine, CEF logs** | [Lesson 21](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_21_security_mitigation.md) | [`security/mitigation.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/mitigation.py) | Q-MITIGATE, automated revocation blacklist, CKW monogamy Bell buffer purge, ArcSight Common Event Format (CEF) |
| **SQLite datastore, schema design, ACID transactions, parameterized queries** | [Lesson 22](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_22_analytics_history.md) | [`analytics/history.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/analytics/history.py) | `TelemetryStore`, `data/qsentinel.db`, 15-column schema, SQL injection immunity, pandas DataFrame conversions |
| **FAR, FRR, statistical Z-separation, balanced accuracy, confusion matrix** | [Lesson 23](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_23_analytics_metrics.md) | [`analytics/metrics.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/analytics/metrics.py) | `BenchmarkReport`, FAR=0.00%, FRR=0.00%, balanced accuracy 100%, sub-2ms latency, Z-separation $\Delta z \approx 44.8\sigma$ |
| **Real-time quantum traffic simulation, stochastic attack injection** | [Lesson 24](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_24_analytics_stream.md) | [`analytics/stream.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/analytics/stream.py) | `QuantumTrafficGenerator`, stochastic attack probability $\theta=0.35$, enterprise payloads, stateful replay caching |
| **Enterprise SOC integration, OASIS STIX 2.1 CTI bundles, Elastic ECS 8.x** | [Lesson 25](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_25_analytics_soc.md) | [`analytics/soc.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/analytics/soc.py) | `QSOCIntegrator`, STIX 2.1 JSON (Identity, Indicator, Attack-Pattern CAPEC, Observed-Data), Elastic Common Schema |
| **Audit reports, SIH-26141 V2.0 JSON certificates, monospace ASCII certs** | [Lesson 26](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_26_analytics_reports.md) | [`analytics/reports.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/analytics/reports.py) | `AuditReportGenerator`, Clopper-Pearson 95% binomial CI, 80-column monospace ASCII audit certificates, JSON signing |
| **Plotly interactive dashboard visualizations, threat gauge, trend charts** | [Lesson 27](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_27_dashboard_charts.md) | [`dashboard/charts.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/dashboard/charts.py) | `build_threat_gauge`, `build_outcome_distribution_chart`, `build_telemetry_trend_chart`, institutional navy/slate palette |
| **HTML5/CSS interactive 4-stage quantum teleportation pipeline visualizer** | [Lesson 28](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_28_dashboard_visualizer.md) | [`dashboard/visualizer.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/dashboard/visualizer.py) | `render_teleportation_pipeline_html`, Alice $\to$ BSM $\to$ Classical Bits $\to$ Pauli Unitary $\to$ Bob Reconstructed State |
| **Master Streamlit web application, left/right layout, 15-tab defense inventory** | [Lesson 29](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_29_app_dashboard.md) | [`app.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/app.py) | 1,886-line master UI, Orange/Navy institutional theme, sidebar verification console, 15 watchtower tabs |
| **Standalone CLI Monte Carlo benchmark runner, argparse, ASCII summary** | [Lesson 30](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_30_benchmark_cli.md) | [`benchmark.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/benchmark.py) | CLI benchmarking flags (`--runs`, `--trials`, `--noise`), automated pass/fail gating, tabular terminal summaries |
| **14-Watchtower automated rehearsal suite, 100-run Monte Carlo sweep** | [Lesson 31](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_31_rehearsal_suite.md) | [`rehearsal.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/rehearsal.py) | `QuantumRehearsalRunner`, 14-watchtower health check in <2.5s, 0 False Negatives, structured JSON rehearsal reports |
| **Grand Unified Release Auditor, 8 pillars, zero ML/emojis, SHA-256 seal** | [Lesson 32](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_32_release_audit.md) | [`release_audit.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/release_audit.py) | `GrandUnifiedReleaseAuditor`, AST inspection, zero PyTorch/TensorFlow, 24-file chained SHA-256 Release Seal |
| **Live demonstration validator, 5 canonical demo scenarios, speaking points** | [Lesson 33](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_33_presentation_scripts.md) | [`verify_demo.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/verify_demo.py) & [`verify_release.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/verify_release.py) | 5 live demo scenarios (Clean, Forgery, Impersonation, Replay, Dynamic Noise), judge-facing narration, 0.22s release verification |
| **Automated submission packaging engine, build sanitization, SHA-256 seal** | [Lesson 34](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_34_package_submission.md) | [`package_submission.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/package_submission.py) | Whitelist packaging, bytecode exclusion (`.pyc`), POSIX path normalization (`as_posix()`), `Q-SENTINEL_...zip.sha256` |
| **Native batch scripts, shell launchers, hardened non-root Docker container** | [Lesson 35](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_35_launchers_containerization.md) | `run_*.bat`, `run_*.sh`, `Dockerfile`, `docker-compose.yml` | One-click Windows/Linux execution, NIST SP 800-190 non-root user (UID 1001), healthcheck probe, persistent volume storage |
| **Automated regression test suite, 22 test modules, 97 passing tests in 2.6s** | [Lesson 36](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_36_regression_test_suite.md) | [`tests/`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/tests/) directory | 5-tier testing taxonomy, 97 tests passing in 2.61s, edge case stress boundaries ($N=10$ to $10,000$, $59.9\text{s}$ vs $60.1\text{s}$) |
| **Championship pitch deck, judge defense manual, NQM technical whitepaper** | [Lesson 37](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_37_grand_finale_documentation.md) | `docs/` (`PITCH_DECK`, `DEFENSE_MANUAL`, `NQM_WHITEPAPER`) | 12-slide pitch deck, 4 whiteboard formulas, 5 tough judge Q&As, complete 37-lesson architecture synthesis |

---

## 🎯 2. Targeted Learning Pathways

Choose the pathway that matches your immediate objective:

```
                                SELECT YOUR LEARNING PATHWAY
                                             │
      ┌──────────────────────┬───────────────┴───────────────┬──────────────────────┐
      │                      │                               │                      │
   Path A                 Path B                          Path C                 Path D
15-Min Judge Cram      Whiteboard Math                 Adversarial Defense    Full Engineering
Jury Defense Q&As      Quantum Physics Proofs          14 Physical Threats    Architecture & DevOps
Lessons 10, 33, 37     Lessons 01, 02, 03, 10, 15, 16  Lessons 07 to 21       All 37 Lessons in Order
```

### Path A: The 15-Minute Judge Defense Cram Path
*Objective: Prepare for rapid-fire questioning from hackathon evaluators.*
1. **[Lesson 10](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_10_security_detector.md)** — Master the exact binomial hypothesis test and standardized $z$-score thresholds.
2. **[Lesson 33](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_33_presentation_scripts.md)** — Memorize the 5 canonical demo scenarios and verbatim speaker notes.
3. **[Lesson 37](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_37_grand_finale_documentation.md)** — Learn the 4 whiteboard formulas and top 5 winning answers.

### Path B: The Whiteboard Math & Quantum Physics Path
*Objective: Master the mathematical equations and physical theorems.*
1. **[Lesson 01](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_01_quantum_state.md)** & **[Lesson 02](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_02_quantum_bell.md)** — State vectors, Pauli eigenstates, Bell pairs, partial trace.
2. **[Lesson 03](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_03_quantum_teleport.md)** — 3-qubit teleportation expansion and Pauli corrections $U = Z^{b1}X^{b2}$.
3. **[Lesson 05](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_05_quantum_tomography.md)** — Stokes parameter tomography and Von Neumann entropy.
4. **[Lesson 15](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_15_security_chsh.md)** — CHSH Bell inequality and Tsirelson quantum bound ($2\sqrt{2}$).
5. **[Lesson 16](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_16_security_finite.md)** — Serfling Martingale bound and composable finite-key extraction.

### Path C: The Cyber Threat & Adversarial Modeling Path
*Objective: Understand how each physical and protocol attack is simulated and defeated.*
1. **[Lesson 07](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_07_security_signature.md)**, **[Lesson 08](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_08_security_freshness.md)**, **[Lesson 09](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_09_security_attacks.md)** — Core QDS protocols, anti-replay, and threat models.
2. **[Lesson 12](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_12_security_decoy.md)** — Photon Number Splitting (PNS) and decoy states.
3. **[Lesson 13](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_13_security_trojan.md)** — Trojan-Horse optical memory probes and Helstrom bounds.
4. **[Lesson 14](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_14_security_blind.md)** — APD laser blinding and timing jitter entropy.
5. **[Lesson 17](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_17_security_mdi.md)** & **[Lesson 18](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_18_security_wdm.md)** — Untrusted MDI relays and Raman scattering noise.
6. **[Lesson 20](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_20_security_hybrid.md)** & **[Lesson 21](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_21_security_mitigation.md)** — Post-quantum hybrid HMAC and automated SOAR containment.

### Path D: The Full Software Architecture & DevOps Path
*Objective: Master how the system is engineered, containerized, and certified.*
1. **[Lesson 22](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_22_analytics_history.md)** & **[Lesson 25](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_25_analytics_soc.md)** — SQLite datastore, STIX 2.1 CTI bundles, and Elastic Common Schema.
2. **[Lesson 27](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_27_dashboard_charts.md)**, **[Lesson 28](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_28_dashboard_visualizer.md)**, **[Lesson 29](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_29_app_dashboard.md)** — Plotly graphics, HTML5 teleportation visualizer, master Streamlit UI.
3. **[Lesson 31](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_31_rehearsal_suite.md)** & **[Lesson 32](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_32_release_audit.md)** — 14-watchtower rehearsal suite and 8-pillar cryptographic release audit.
4. **[Lesson 34](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_34_package_submission.md)** & **[Lesson 35](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_35_launchers_containerization.md)** — Deterministic zip packager and hardened Docker containerization.
5. **[Lesson 36](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_36_regression_test_suite.md)** — Automated 97-test regression suite architecture.

---

## 📚 3. Exhaustive Lesson-by-Lesson Directory

---

### [Lesson 01: Quantum State Vectors, Pauli Operators & Hilbert Spaces](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_01_quantum_state.md)
* **File in Focus:** [`quantum/state.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/state.py)
* **What is it?** Foundational quantum linear algebra engine modeling 1-qubit and 2-qubit Hilbert space vectors without relying on heavy external SDKs.
* **Analogy (ELI5):** The 3D Compass on a Spherical Globe (Bloch sphere) where North/South is $|0\rangle/|1\rangle$, Equator is $|+\rangle/|-\rangle$, and East/West is $|+i\rangle/|-i\rangle$.
* **Key Math:** State normalization $\langle \psi \mid \psi \rangle = 1.0$, Pauli matrices ($\sigma_X, \sigma_Y, \sigma_Z$), state fidelity $F = |\langle \phi \mid \psi \rangle|^2$, density operator $\rho = |\psi\rangle\langle\psi|$.
* **Key Code:** [`QubitState`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/state.py#L38), `get_pauli_eigenstate()`, `tensor_product()`.
* **Viva Question:** *"Why build a custom linear algebra simulator instead of importing Qiskit?"* $\to$ Eliminates hundreds of megabytes of heavy C-extensions and version fragility for microsecond-speed matrix multiplications.

---

### [Lesson 02: Bell Entangled States & Maximal Superposition](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_02_quantum_bell.md)
* **File in Focus:** [`quantum/bell.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/bell.py)
* **What is it?** Circuit synthesis of the 4 canonical EPR Bell pairs and proof of maximal entanglement via partial trace.
* **Analogy (ELI5):** The Magic Twin Coins (entangled pair): flipping coin A in Delhi instantly forces coin B in London to show the exact matching face.
* **Key Math:** 4 Bell states $|\Phi^+\rangle, |\Phi^-\rangle, |\Psi^+\rangle, |\Psi^-\rangle$, partial trace $\text{Tr}_B(\rho_{AB}) = \frac{1}{2}I_2$, entanglement purity $\gamma = \text{Tr}(\rho_A^2) = 0.5000$.
* **Key Code:** [`BellStateEngine`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/bell.py#L22), `create_bell_pair()`, `partial_trace_subsystem_b()`.
* **Viva Question:** *"How do you prove a state is maximally entangled mathematically?"* $\to$ By taking the partial trace over subsystem B; if the reduced density matrix is the maximally mixed identity state ($\frac{1}{2}I_2$) with purity exactly $0.5$, entanglement is maximal.

---

### [Lesson 03: The 3-Qubit Quantum Teleportation Protocol](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_03_quantum_teleport.md)
* **File in Focus:** [`quantum/teleport.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/teleport.py)
* **What is it?** The core carrier transmission mechanism: teleporting an unknown qubit from Alice to Bob using pre-shared entanglement and 2 classical bits.
* **Analogy (ELI5):** The Quantum Fax Machine: the original paper shredder destroys the document while 2 classical numbers tell the receiver which lens to use to reassemble the exact photons.
* **Key Math:** 3-qubit composite expansion $|\Psi_{123}\rangle = \frac{1}{2}\sum_{i=1}^4 |\Phi_i\rangle_{12} \otimes (U_i |\psi\rangle)_3$, Bob's Pauli correction $U = Z^{b_1} X^{b_2}$, 100% fidelity verification ($F=1.0000$).
* **Key Code:** [`TeleportationCircuit`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/teleport.py#L25), `execute_teleportation()`.
* **Viva Question:** *"Does quantum teleportation violate Einstein's speed-of-light limit?"* $\to$ No, Bob cannot reconstruct the quantum state until Alice sends her 2 classical bits over a standard classical channel.

---

### [Lesson 04: Max Born Measurement & Shot-Noise Sampling](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_04_quantum_measure.md)
* **File in Focus:** [`quantum/measure.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/measure.py)
* **What is it?** Simulates realistic photon detectors: single-click projective collapse according to Born's rule and $N$-trial empirical convergence.
* **Analogy (ELI5):** The Single-Lens Camera vs The Long-Exposure Photo: a single click gives a grainy 0 or 1, while 500 shots reveal the true probability cloud.
* **Key Math:** Born projection postulate $P(m) = |\langle m \mid \psi \rangle|^2 = \text{Tr}(\Pi_m \rho)$, Bernoulli shot-noise variance $\sigma^2 = \frac{p(1-p)}{N}$.
* **Key Code:** [`ProjectiveMeasurementEngine`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/measure.py#L20), `measure_state_in_basis()`, `sample_repeated_measurements()`.
* **Viva Question:** *"Why do we need 50 to 500 trials per token?"* $\to$ Single quantum clicks carry stochastic shot noise; repeated sampling allows exact binomial hypothesis testing with negligible variance.

---

### [Lesson 05: Quantum State Tomography (QST) & Stokes Parameters](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_05_quantum_tomography.md)
* **File in Focus:** [`quantum/tomography.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/tomography.py)
* **What is it?** Full empirical reconstruction of an unknown density matrix $\rho$ from projective measurements across all 3 Pauli bases ($X, Y, Z$).
* **Analogy (ELI5):** The Medical CT Scan: taking multiple X-ray projections from different angles to reconstruct a 3D model of an organ.
* **Key Math:** Stokes parameters $S_1 = P(+)-P(-)$, $S_2 = P(+i)-P(-i)$, $S_3 = P(0)-P(1)$, density matrix $\rho = \frac{1}{2}(I + \vec{S}\cdot\vec{\sigma})$, Purity $\gamma = \text{Tr}(\rho^2)$, Von Neumann entropy $S(\rho) = -\text{Tr}(\rho \log_2 \rho)$.
* **Key Code:** [`QuantumStateTomography`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/tomography.py#L22), `reconstruct_density_matrix()`.
* **Viva Question:** *"How does QST prove whether an eavesdropper was active?"* $\to$ Eavesdropping causes decoherence, turning pure states ($\gamma = 1.0$) into mixed states ($\gamma < 1.0$), which QST reveals through Stokes parameter shrinkage.

---

### [Lesson 06: Multi-Hop Quantum Mesh & Entanglement Swapping](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_06_quantum_mesh.md)
* **File in Focus:** [`quantum/mesh.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/mesh.py)
* **What is it?** Extends quantum teleportation across multiple intermediate repeater nodes using 4-qubit entanglement swapping without trusting the repeaters.
* **Analogy (ELI5):** The High-Speed Train Coupling Station: connecting two separate train lines at an intermediate hub without the passengers needing to exit.
* **Key Math:** 4-qubit state space, joint Bell measurement at intermediate repeater, end-to-end entanglement fidelity, rogue repeater isolation.
* **Key Code:** [`QuantumMeshRouter`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/quantum/mesh.py#L24), `swap_entanglement()`, `localize_rogue_repeater()`.
* **Viva Question:** *"Can a malicious quantum repeater read our signature data?"* $\to$ No, the repeater only performs an entanglement swap; it holds no classical key material and never receives the payload qubit.

---

### [Lesson 07: Quantum Digital Signature (QDS) Token Synthesis](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_07_security_signature.md)
* **File in Focus:** [`security/signature.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/signature.py)
* **What is it?** The cryptographic core: maps a message's SHA-256 digest into an array of Pauli eigenstates to create an unforgeable quantum signature.
* **Analogy (ELI5):** The Wax Signet Ring made of Quantum Glass: if an attacker touches or copies the stamp, the glass shatters irrecoverably.
* **Key Math:** Deterministic key derivation via SHA-256 digest bit-pairs, mapping to $\{|0\rangle, |1\rangle, |+\rangle, |-\rangle, |+i\rangle, |-i\rangle\}$.
* **Key Code:** [`QDSKeyManager`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/signature.py#L25), `generate_signature()`, [`SignatureToken`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/signature.py#L15).
* **Viva Question:** *"Why can't an attacker duplicate a quantum signature?"* $\to$ The Wootters-Zurek No-Cloning Theorem states that unknown quantum states cannot be cloned; attempting to measure them forces state collapse.

---

### [Lesson 08: Anti-Replay Defense & Freshness Registry](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_08_security_freshness.md)
* **File in Focus:** [`security/freshness.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/freshness.py)
* **What is it?** Dual-layer anti-replay defense combining sliding UTC time windows and monotonic nonce tracking.
* **Analogy (ELI5):** The Movie Theater Ticket with a 15-Minute Expiry: even if an attacker steals your ticket, the barcode scanner rejects it once it has already been scanned.
* **Key Math:** Monotonic timestamp comparison, sliding window $\Delta t \le 60.0\text{s}$, garbage collection of expired session nonces.
* **Key Code:** [`FreshnessRegistry`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/freshness.py#L18), `verify_and_register()`, `prune_stale_nonces()`.
* **Viva Question:** *"Why does Q-Sentinel catch replay attacks through bookkeeping rather than quantum noise?"* $\to$ Replayed quantum states were originally authentic, so their physical error rate is low; catching them requires classical nonce freshness tracking.

---

### [Lesson 09: Adversarial Threat Modeling & Attack Orchestration](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_09_security_attacks.md)
* **File in Focus:** [`security/attacks.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/attacks.py)
* **What is it?** The cyber adversarial simulation suite: injects Signature Forgery, Signer Impersonation, Replay attacks, and continuous channel noise.
* **Analogy (ELI5):** The Military Red Team War-Games: simulating real adversary strikes (spies, forged passports, jammer planes) to test base defenses.
* **Key Math:** Forgery error rate $e \approx 50\%$ (random basis guess), Impersonation error rate $e \ge 18.75\%$, depolarizing channel perturbation $\epsilon$.
* **Key Code:** [`ThreatOrchestrator`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/attacks.py#L22), `execute_scenario()`, `inject_channel_noise()`.
* **Viva Question:** *"Why does Eve's forgery attempt produce ~50% error?"* $\to$ Because Alice's states are prepared in mutually unbiased bases; measuring in the wrong basis yields orthogonal projection probabilities of exactly $0.5$.

---

### [Lesson 10: The Q-STAT Engine & Exact Hypothesis Testing](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_10_security_detector.md)
* **File in Focus:** [`security/detector.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/detector.py)
* **What is it?** The core mathematical detection watchtower: evaluates exact binomial hypothesis tests and standardized $z$-scores to classify signatures into 3 tiers.
* **Analogy (ELI5):** The Geiger Counter with a Calibrated Alarm: ticking at natural background radiation ($p_0=3\%$), but sounding a siren when radiation jumps.
* **Key Math:** Exact binomial test via `scipy.stats.binomtest`, $z = \frac{\hat{e}-p_0}{\sqrt{p_0(1-p_0)/N}}$, 3-tier thresholds: Green ($z<2.0$), Yellow ($2.0 \le z < 4.0$), Red ($z \ge 4.0$).
* **Key Code:** [`QStatDetector`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/detector.py#L38), `evaluate()`, `verify_signature_session()`.
* **Viva Question:** *"Why use exact binomial testing instead of machine learning?"* $\to$ The problem statement mandates auditable detection; exact binomial tests provide mathematically provable $p$-values with zero black-box hallucinations.

---

### [Lesson 11: Dynamic Noise Baseline Calibration (Q-CALIBRATE)](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_11_security_calibrate.md)
* **File in Focus:** [`security/calibrate.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/calibrate.py)
* **What is it?** Adaptive baseline tracking using an Exponential Moving Average (EMA) to prevent false alarms caused by diurnal fiber thermal drift.
* **Analogy (ELI5):** Noise-Cancelling Headphones: listening to continuous airplane cabin hum and filtering it out, but passing sudden speech through.
* **Key Math:** EMA formula $\bar{p}_t = \alpha p_t + (1-\alpha)\bar{p}_{t-1}$ ($\alpha = 0.25$), drift velocity tripwire $|v_{\text{drift}}| \ge 0.01\text{ s}^{-1}$.
* **Key Code:** [`BaselineCalibrator`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/calibrate.py#L22), `update_baseline()`, `detect_drift_anomaly()`.
* **Viva Question:** *"What prevents an attacker from slowly increasing channel noise to evade detection?"* $\to$ The drift-velocity tripwire detects if the rate of error increase exceeds physical thermal expansion limits.

---

### [Lesson 12: Decoy-State Watchtower (Q-DECOY)](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_12_security_decoy.md)
* **File in Focus:** [`security/decoy.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/decoy.py)
* **What is it?** Detects Photon Number Splitting (PNS) attacks on weak coherent pulses using the Hwang-Lo 3-intensity decoy-state protocol ($\mu, \nu, \text{vacuum}$).
* **Analogy (ELI5):** The Trojan Horse Trap with Decoy Soldiers: sending decoy platoons with different numbers of soldiers so if an enemy ambushes only multi-soldier groups, the yields expose them.
* **Key Math:** Poisson distribution $P(n \mid \mu) = \frac{\mu^n e^{-\mu}}{n!}$, analytical lower bound on single-photon yield $Y_1$, upper bound on single-photon error $e_1$.
* **Key Code:** [`DecoyStateWatcher`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/decoy.py#L26), `estimate_single_photon_bounds()`, `detect_pns_attack()`.
* **Viva Question:** *"How does an attacker exploit multi-photon pulses?"* $\to$ In a PNS attack, Eve splits off one photon from a multi-photon pulse, stores it in quantum memory, and measures it after the basis is announced. Decoy states mathematically bound $Y_1$ to detect this.

---

### [Lesson 13: Trojan-Horse Probe Watchtower (Q-TROJAN)](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_13_security_trojan.md)
* **File in Focus:** [`security/trojan.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/trojan.py)
* **What is it?** Defends against bright optical probe pulses injected by an adversary to read internal modulator memory via back-reflections.
* **Analogy (ELI5):** The Burglar Shining a High-Beam Flashlight Through Keyholes: looking for internal reflections to see what key is in the lock.
* **Key Math:** Optical back-reflection power $P_{\text{refl}} \ge 1.5\text{ nW}$, Lindblad decoherence decay, Helstrom-Holevo mutual information bound $I_E \le 0.01\text{ bits}$.
* **Key Code:** [`TrojanHorseWatcher`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/trojan.py#L28), `inspect_probe_telemetry()`.
* **Viva Question:** *"What is the physical countermeasure against Trojan-Horse attacks?"* $\to$ Optical bandpass filters, narrow fiber Bragg gratings, and passive optical isolators providing $>60\text{ dB}$ attenuation.

---

### [Lesson 14: Detector Blinding Watchtower (Q-BLIND)](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_14_security_blind.md)
* **File in Focus:** [`security/blind.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/blind.py)
* **What is it?** Neutralizes the Makarov-Lydersen continuous-wave (CW) laser blinding attack on Avalanche Photo Diodes (APDs).
* **Analogy (ELI5):** Blinding the Security Guard with a Spotlight: blinding the guard so they only see bright flashcards held right in front of their eyes.
* **Key Math:** APD anode DC bias current surge ($I_{\text{bias}} \ge 5.0\,\mu\text{A}$), 4-quadrant beam displacement ($r \le 2.5\,\mu\text{m}$), click inter-arrival Shannon entropy ($H(\Delta t) \ge 1.0\text{ nats}$).
* **Key Code:** [`BlindAttackWatcher`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/blind.py#L25), `evaluate_detector_telemetry()`.
* **Viva Question:** *"How does an APD behave when blinded?"* $\to$ The continuous laser forces the APD from Geiger mode into linear mode; clicks are no longer single-photon avalanches but classical current thresholds dictated by Eve.

---

### [Lesson 15: Device-Independent Bell-CHSH Watchtower (Q-CHSH)](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_15_security_chsh.md)
* **File in Focus:** [`security/chsh.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/chsh.py)
* **What is it?** Certifies quantum entanglement without trusting source hardware using Clauser-Horne-Shimony-Holt (CHSH) Bell inequalities.
* **Analogy (ELI5):** The Interrogation Room Lie Detector: two suspects in separate rooms cannot coordinate their answers unless they share true telepathic entanglement.
* **Key Math:** Correlation parameter $S = |E(A_0, B_0) + E(A_0, B_1) + E(A_1, B_0) - E(A_1, B_1)|$, Classical LHV bound $S \le 2.0$, Quantum Tsirelson bound $S \le 2\sqrt{2} \approx 2.8284$.
* **Key Code:** [`CHSHBellWatcher`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/chsh.py#L24), `verify_chsh_violation()`.
* **Viva Question:** *"What attack does CHSH prevent?"* $\to$ Device-Independent certification prevents classical separable state spoofing where an untrusted manufacturer builds fake quantum hardware.

---

### [Lesson 16: Composable Finite-Key Security Watchtower (Q-FINITE)](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_16_security_finite.md)
* **File in Focus:** [`security/finite.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/finite.py)
* **What is it?** Guarantees information-theoretic security over finite sample blocks ($N < 10^5$) using the Serfling Martingale large-deviation inequality.
* **Analogy (ELI5):** The Polling Margin of Error: surveying 500 voters gives a statistical margin of error; Serfling provides the exact rigorous margin for quantum sampling.
* **Key Math:** Serfling parameter $\xi(N, n, \varepsilon_{\text{PE}}) = \sqrt{\frac{(N-n+1)\ln(1/\varepsilon_{\text{PE}})}{2nN}}$, Leftover Hash Lemma extractable length $\ell = n[1-h_2(e+\xi)] - f_{\text{EC}}nh_2(e) - \text{leakage}$.
* **Key Code:** [`FiniteKeyWatcher`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/finite.py#L24), `compute_extractable_key_length()`.
* **Viva Question:** *"Why are asymptotic security proofs insufficient for real-world QDS?"* $\to$ Real signatures use finite block lengths; asymptotic assumptions ignore statistical sampling fluctuations that an adversary can exploit.

---

### [Lesson 17: Measurement-Device-Independent Watchtower (Q-MDI)](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_17_security_mdi.md)
* **File in Focus:** [`security/mdi.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/mdi.py)
* **What is it?** Eliminates 100% of detector side-channels by routing photons through an untrusted intermediate relay using Hong-Ou-Mandel (HOM) interference.
* **Analogy (ELI5):** The Blind Drop Box: Alice and Bob drop envelopes into a locked box; even if the box custodian is a criminal, they cannot forge the transaction.
* **Key Math:** Hong-Ou-Mandel visibility $V_{\text{HOM}} = \frac{R_{\max}-R_{\min}}{R_{\max}} \ge 70\%$, symmetric coincidence error bound $e_Z \le 8\%$.
* **Key Code:** [`MDIRelayWatcher`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/mdi.py#L28), `simulate_mdi_session()`.
* **Viva Question:** *"Why is MDI immune to detector blinding?"* $\to$ Because the measurement detectors are located in the untrusted relay; even if completely compromised, the relay cannot extract key information without collapsing the HOM dip.

---

### [Lesson 18: WDM Co-Propagation & Raman Watchtower (Q-WDM)](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_18_security_wdm.md)
* **File in Focus:** [`security/wdm.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/wdm.py)
* **What is it?** Models quantum channel co-existence in single-mode fiber alongside 100G/400G classical DWDM lasers subject to Spontaneous Raman Scattering (SpRS).
* **Analogy (ELI5):** Whispering in a Rock Concert: the quantum single-photon channel is a whisper while classical 400G lasers are stadium loudspeakers; narrow filtering silences the guitars.
* **Key Math:** Effective interaction length $L_{\text{eff}} = \frac{1-e^{-\alpha L}}{\alpha} \to 21.71\text{ km}$, Raman photon noise $P_{\text{Raman}}$, 0.05nm FBG filtering, 200ps temporal gating, SNR bound.
* **Key Code:** [`WDMRamanWatcher`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/wdm.py#L25), `evaluate_co_propagation()`.
* **Viva Question:** *"Can QDS share existing commercial telecom fiber?"* $\to$ Yes, by deploying 1550nm/1310nm wavelength separation, 0.05nm FBG filtering, and 200ps temporal gating to suppress Raman noise.

---

### [Lesson 19: Multi-Recipient Non-Repudiation (Q-REPUDIATE)](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_19_security_multirecipient.md)
* **File in Focus:** [`security/multirecipient.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/multirecipient.py)
* **What is it?** Implements Andersson-Curty-Jex multi-recipient token symmetrization to achieve non-repudiation without violating the No-Cloning Theorem.
* **Analogy (ELI5):** The 3-Carbon-Copy Contract: Bob and Charlie exchange random subsets of Alice's signature; Alice cannot forge one copy without triggering a cross-check mismatch.
* **Key Math:** Symmetrization token permutation, cross-recipient discrepancy threshold $D_{\text{cross}} \le 12.5\%$, dispute resolution cross $z$-score.
* **Key Code:** [`MultiRecipientEngine`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/multirecipient.py#L24), `symmetrize_tokens()`, `arbitrate_dispute()`.
* **Viva Question:** *"How do you sign for multiple recipients if quantum states cannot be cloned?"* $\to$ By distributing separate token sets to Bob and Charlie and having them exchange half of their keys over classical channels before transmission.

---

### [Lesson 20: Post-Quantum Hybrid Defense Engine (Q-HYBRID)](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_20_security_hybrid.md)
* **File in Focus:** [`security/hybrid.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/hybrid.py)
* **What is it?** Dual-layer defense-in-depth binding NIST FIPS 202 HMAC-SHA3-512 with quantum digital signatures and constant-time digest verification.
* **Analogy (ELI5):** The Bank Vault with a Biometric Palm Scanner AND a High-Security Steel Key: opening the vault requires both the classical key and the quantum biometric.
* **Key Math:** Keccak sponge ($b=1600$), constant-time comparison `hmac.compare_digest`, 4-case dual-layer decision matrix.
* **Key Code:** [`HybridQDSVerifier`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/hybrid.py#L22), `verify_hybrid_signature()`.
* **Viva Question:** *"What happens if an attacker breaks the HMAC-SHA3-512 layer?"* $\to$ The quantum layer still rejects the forged state; both layers must pass independently for signature acceptance.

---

### [Lesson 21: Automated SOAR Mitigation Engine (Q-MITIGATE)](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_21_security_mitigation.md)
* **File in Focus:** [`security/mitigation.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/mitigation.py)
* **What is it?** Sub-millisecond Security Orchestration, Automation, and Response (SOAR): automated nonce revocation, signer quarantine, and Bell buffer purging.
* **Analogy (ELI5):** The Automated Circuit Breaker in a Power Station: if a lightning bolt hits the transformer, the breaker trips in milliseconds to save the city.
* **Key Math:** Nonce revocation blacklist, Coffman-Kundu-Wootters (CKW) entanglement monogamy buffer purging, ArcSight Common Event Format (CEF) logging.
* **Key Code:** [`MitigationOrchestrator`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/mitigation.py#L26), `contain_incident()`, `purge_entanglement_buffer()`.
* **Viva Question:** *"Why purge pre-shared Bell pairs upon detecting an attack?"* $\to$ Entanglement monogamy dictates that if an attacker gained correlations with a shared pair, the fidelity is permanently tainted and must be destroyed.

---

### [Lesson 22: SQLite Datastore & Persistence Schema](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_22_analytics_history.md)
* **File in Focus:** [`analytics/history.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/analytics/history.py)
* **What is it?** Relational persistence datastore managing verified transactions, threat telemetry, and audit histories at `data/qsentinel.db`.
* **Analogy (ELI5):** The Black Box Flight Data Recorder: recording every sensor reading, engine temperature, and throttle position for accident investigation.
* **Key Math:** 15-column relational schema, SQL injection immunity via parameterized bindings, indexed queries, pandas DataFrame export.
* **Key Code:** [`TelemetryStore`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/analytics/history.py#L20), `record_verification()`, `get_historical_dataframe()`.
* **Viva Question:** *"How do you protect the telemetry database against tampering?"* $\to$ Parameterized queries eliminate SQL injection, while audit certificates compute SHA-256 digests over database state snapshots.

---

### [Lesson 23: Empirical Benchmark Telemetry & Z-Separation](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_23_analytics_metrics.md)
* **File in Focus:** [`analytics/metrics.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/analytics/metrics.py)
* **What is it?** Statistical benchmarking engine calculating False Acceptance Rate (FAR), False Rejection Rate (FRR), balanced accuracy, and statistical Z-Separation.
* **Analogy (ELI5):** The Airport Security Body Scanner Benchmark: verifying that 1,000 harmless travelers pass without delay (0% FRR) and 1,000 concealed weapons are caught (0% FAR).
* **Key Math:** $\text{FAR} = \frac{\text{FP}}{\text{FP}+\text{TN}} = 0.00\%$, $\text{FRR} = \frac{\text{FN}}{\text{TP}+\text{FN}} = 0.00\%$, Z-Separation $\Delta z = \bar{z}_{\text{attack}} - \bar{z}_{\text{honest}} \approx 44.8\sigma$.
* **Key Code:** [`BenchmarkReport`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/analytics/metrics.py#L18), `compute_benchmark()`.
* **Viva Question:** *"What does a 44-sigma Z-Separation mean?"* $\to$ It proves that honest and adversarial states are separated by 44 standard deviations; the distributions have zero overlap, mathematically guaranteeing zero false alarms.

---

### [Lesson 24: Real-Time Quantum Traffic Simulation Engine](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_24_analytics_stream.md)
* **File in Focus:** [`analytics/stream.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/analytics/stream.py)
* **What is it?** Stochastic traffic generator modeling continuous banking wire transfers, defense C2 payloads, and randomized cyber attack bursts.
* **Analogy (ELI5):** The Cyber Defense Cyber-Range: firing live dummy missiles and electronic jamming signals at military radar systems to train operators.
* **Key Math:** Stochastic attack probability $\theta = 0.35$, stateful replay caching (`_prev_legit_sig`), randomized seed reproducibility.
* **Key Code:** [`QuantumTrafficGenerator`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/analytics/stream.py#L22), `generate_traffic_stream()`.
* **Viva Question:** *"How do you test replay attacks realistically in real-time streams?"* $\to$ The stream engine caches authentic past signatures and re-injects them 10 seconds later with duplicate nonces.

---

### [Lesson 25: Enterprise SOC SIEM Integration (STIX 2.1 & ECS 8.x)](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_25_analytics_soc.md)
* **File in Focus:** [`analytics/soc.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/analytics/soc.py)
* **What is it?** Converts quantum physical breaches into OASIS STIX 2.1 Cyber Threat Intelligence JSON bundles and Elastic Common Schema (ECS 8.x) SIEM payloads.
* **Analogy (ELI5):** The United Nations Universal Translator: taking a message written in quantum physics and translating it into standard English and French for the global defense council.
* **Key Math:** STIX 2.1 Domain Objects (Identity, Indicator, Attack-Pattern with CAPEC mapping, Observed-Data, Course-of-Action), ECS 8.x severity rating ($7/10$).
* **Key Code:** [`QSOCIntegrator`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/analytics/soc.py#L248), `process_incident_and_export()`.
* **Viva Question:** *"Can Q-Sentinel feed into Splunk or Microsoft Sentinel?"* $\to$ Yes, native ECS 8.x formatting allows instant JSON ingestion into any standard enterprise SIEM.

---

### [Lesson 26: Cryptographic Audit Reports & SIH Certificates](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_26_analytics_reports.md)
* **File in Focus:** [`analytics/reports.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/analytics/reports.py)
* **What is it?** Generates formal verification audit certificates: machine-readable JSON under SIH-26141 Protocol V2.0 and 80-column monospace ASCII plaintext certificates.
* **Analogy (ELI5):** The Government Notary Stamp: stamping a formal legal deed with a seal, ribbon, and registration number proving authenticity.
* **Key Math:** Clopper-Pearson 95% exact binomial confidence intervals, multi-party non-repudiation binding hashes.
* **Key Code:** [`AuditReportGenerator`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/analytics/reports.py#L22), `generate_certificate_json()`, `generate_ascii_report()`.
* **Viva Question:** *"How do you represent error rate uncertainty in audit certificates?"* $\to$ We compute exact Clopper-Pearson 95% binomial confidence intervals, reporting $[\text{CI}_{\text{lower}}, \text{CI}_{\text{upper}}]$.

---

### [Lesson 27: Interactive Visualizations & Plotly Chart Engine](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_27_dashboard_charts.md)
* **File in Focus:** [`dashboard/charts.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/dashboard/charts.py)
* **What is it?** The Plotly rendering engine creating real-time visual threat gauges, Born-rule outcome distributions, and historical telemetry trendlines.
* **Analogy (ELI5):** The Jet Fighter Cockpit Heads-Up Display (HUD): displaying airspeed, altitude, and missile lock in high-contrast institutional colors.
* **Key Math:** Standardized $z$-score threat gauge mapping, grouped bar charts comparing theoretical vs empirical Born distributions, 30-session scatter trends.
* **Key Code:** [`build_threat_gauge()`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/dashboard/charts.py#L18), `build_outcome_distribution_chart()`, `build_telemetry_trend_chart()`.
* **Viva Question:** *"Why use Plotly instead of static Matplotlib images?"* $\to$ Plotly generates responsive, interactive JavaScript visualizations that allow judges to hover over data points and inspect confidence intervals.

---

### [Lesson 28: Interactive Teleportation Pipeline Visualizer](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_28_dashboard_visualizer.md)
* **File in Focus:** [`dashboard/visualizer.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/dashboard/visualizer.py)
* **What is it?** Generates a zero-dependency HTML5/CSS 4-stage visual quantum pipeline showing Alice's state, joint Bell measurement, classical bits, and Bob's Pauli reconstruction.
* **Analogy (ELI5):** The Transparent Glass Subway System: watching a train leave station A, pass through the central junction, and arrive safely at station B.
* **Key Math:** 4-stage state representation: Alice $|\psi\rangle \to$ BSM $(m_1, m_2) \to$ Unitary $U=Z^{m_1}X^{m_2} \to$ Bob reconstructed state, dynamic anomaly alert badges.
* **Key Code:** [`render_teleportation_pipeline_html()`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/dashboard/visualizer.py#L18).
* **Viva Question:** *"How does the visualizer demonstrate eavesdropping?"* $\to$ When an attack is executed, the classical bit conduit flashes red, and Bob's state box displays state corruption with a failure badge.

---

### [Lesson 29: The Master Streamlit Web Application](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_29_app_dashboard.md)
* **File in Focus:** [`app.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/app.py)
* **What is it?** The master web dashboard (1,886 lines) integrating all 14 watchtowers, execution consoles, live noise sliders, and SOC panels into an institutional UI.
* **Analogy (ELI5):** The NASA Mission Control Center Main Screen: flight controllers at their consoles monitoring every sensor, valve, and telemetry stream in real time.
* **Key Math:** Left/right dual-pane layout, session state quarantine tripwires, unified 15-tab defense inventory, national identity branding (`#ff671f` / `#0b2545`).
* **Key Code:** Master Streamlit application components, tab renderers, sidebar controls.
* **Viva Question:** *"How does the UI handle emergency containment?"* $\to$ If an attack is verified, the sidebar console locks into QUARANTINE mode, disabling transmission and displaying the SOAR revocation status.

---

### [Lesson 30: Standalone CLI Monte Carlo Benchmark Suite](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_30_benchmark_cli.md)
* **File in Focus:** [`benchmark.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/benchmark.py)
* **What is it?** Headless command-line benchmarking engine for automated performance evaluation, parameter sweeps, and terminal ASCII reporting.
* **Analogy (ELI5):** The Dynamometer Auto Engine Dyno Test: strapping a vehicle to an automated roller bench and running it at top speed to measure horsepower and emissions.
* **Key Math:** Monte Carlo parameter sweeping via `argparse` (`--runs`, `--trials`, `--tokens`, `--noise`), automated pass/fail gating, tabular ASCII terminal output.
* **Key Code:** [`main()`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/benchmark.py#L22), `parse_args()`, `run_benchmark_suite()`.
* **Viva Question:** *"Can Q-Sentinel be evaluated without launching a browser?"* $\to$ Yes, `python benchmark.py --runs 100` executes the full Monte Carlo verification sweep directly in the terminal in under 2 seconds.

---

### [Lesson 31: 14-Watchtower Automated Rehearsal Suite](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_31_rehearsal_suite.md)
* **File in Focus:** [`rehearsal.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/rehearsal.py)
* **What is it?** Automated pre-flight rehearsal runner executing a synchronized sweep across all 14 physical watchtowers and 100 Monte Carlo stress iterations in <2.5 seconds.
* **Analogy (ELI5):** The NASA "Wet Dress Rehearsal": running the full countdown sequence, testing every sensor and valve, right before the astronauts board the rocket.
* **Key Math:** 14/14 sweep pass verification, 100-run Monte Carlo stress sweep, zero false negatives (0 FN), zero false alarms (0 FP), JSON report synthesis.
* **Key Code:** [`QuantumRehearsalRunner`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/rehearsal.py#L32), `rehearse_all_watchtowers()`, `run_monte_carlo_stress_test()`.
* **Viva Question:** *"How do you prove that all 14 defense modules work right now?"* $\to$ Run `python rehearsal.py`; it evaluates all 14 detectors live in under 2.5 seconds and returns a 100% pass certificate.

---

### [Lesson 32: Grand Unified Release Auditor & SHA-256 Release Seal](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_32_release_audit.md)
* **File in Focus:** [`release_audit.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/release_audit.py)
* **What is it?** The master 8-pillar regulatory certification engine: validates AST syntax, enforces zero ML/emojis policies, and seals the codebase with chained SHA-256 digests.
* **Analogy (ELI5):** The FAA Aircraft Type Certificate & Tamper-Evident Wax Seal: a formal regulatory audit proving airworthiness, sealed so any change voids the certificate.
* **Key Math:** AST parsing, zero-ML regex validation, chained SHA-256 hash over 24 core files, outputting [`docs/RELEASE_MANIFEST.md`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/RELEASE_MANIFEST.md) and [`docs/RELEASE_AUDIT_CERTIFICATE.json`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/RELEASE_AUDIT_CERTIFICATE.json).
* **Key Code:** [`GrandUnifiedReleaseAuditor`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/release_audit.py#L90), `execute_grand_unified_audit()`.
* **Viva Question:** *"What happens if someone tampers with a physics equation after release?"* $\to$ The chained SHA-256 digest mismatches the release certificate, instantly flagging unauthorized tampering.

---

### [Lesson 33: Presentation Kits & Live Stage Demonstration Scripts](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_33_presentation_scripts.md)
* **Files in Focus:** [`verify_demo.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/verify_demo.py) & [`verify_release.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/verify_release.py)
* **What is it?** Live presentation drivers executing the 5 canonical demo scenarios alongside verbatim judge-facing speaking points and 0.22s release verification.
* **Analogy (ELI5):** The TED Talk Teleprompter: guiding the speaker through live experiments while showing the exact sentences to deliver to the audience.
* **Key Math:** 5 canonical demo scenarios (Clean, Forgery, Impersonation, Replay, Dynamic Noise), judge-facing narration, hard fail-safe exit codes.
* **Key Code:** [`run_live_demonstration()`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/verify_demo.py#L14), [`main()`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/verify_release.py#L16).
* **Viva Question:** *"Can you run this presentation completely offline if the venue Wi-Fi fails?"* $\to$ Yes, 100%; both scripts run completely offline in under 2.5 seconds with zero internet connectivity.

---

### [Lesson 34: Automated Submission Packaging Engine](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_34_package_submission.md)
* **File in Focus:** [`package_submission.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/package_submission.py)
* **What is it?** Deterministic packaging pipeline compiling certified source code, tests, docs, and launchers into `dist/Q-SENTINEL_SIH26141_FINAL_SUBMISSION.zip`.
* **Analogy (ELI5):** The Sterile Surgical Tool Kit: strictly packing only clean instruments into an autoclave pouch, excluding coffee cups and pencil shavings.
* **Key Math:** Affirmative whitelisting, bytecode exclusion (`.pyc`), POSIX path normalization (`as_posix()`), GNU-compatible `.sha256` checksum generation.
* **Key Code:** [`create_submission_package()`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/package_submission.py#L17).
* **Viva Question:** *"Why don't you bundle a virtual environment (`venv`) inside the zip archive?"* $\to$ Virtualenvs contain platform-specific C-binaries that break across operating systems; instead, we provide pinned dependencies and Docker containers.

---

### [Lesson 35: Native Launchers & Enterprise Containerization](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_35_launchers_containerization.md)
* **Files in Focus:** `run_qsentinel.bat`, `run_tests.bat`, `run_audit.bat`, `run_qsentinel.sh`, `Dockerfile`, `docker-compose.yml`
* **What is it?** Zero-configuration client deployment: one-click Windows/Linux native launchers paired with hardened, non-root Docker containerization.
* **Analogy (ELI5):** The Fighter Jet "Master Start" Switch & The Intermodal Shipping Container: one-click ignition on local laptops, and universal container portability across clouds.
* **Key Math:** Debian Slim base image, non-root user `qsentinel` (UID 1001) under NIST SP 800-190, container healthcheck probes, persistent named volume `qsentinel-data`.
* **Key Code:** Launch scripts and container configuration files.
* **Viva Question:** *"What happens to telemetry data when the Docker container is restarted?"* $\to$ The named volume `qsentinel-data` mounted at `/app/data` preserves `data/qsentinel.db` across container rebuilds.

---

### [Lesson 36: Automated Regression Test Suite Architecture](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_36_regression_test_suite.md)
* **Directory in Focus:** [`tests/`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/tests/) (22 test modules, 97 passing tests)
* **What is it?** The 5-tier test hierarchy verifying every quantum formula, optical detector, security protocol, and stress boundary in **2.61 seconds**.
* **Analogy (ELI5):** The Automotive Crash-Test Facility (Euro NCAP): subjecting the vehicle to extreme, destructive collisions to prove that safety systems hold.
* **Key Math:** 5-tier taxonomy (Foundations, Watchtowers, Protocols, SOC, Stress), asymptotic sample sizes ($N=10$ to $10,000$), payload extremes (empty to 10,000 chars), clock skew boundaries ($59.9\text{s}$ vs $60.1\text{s}$).
* **Key Code:** 22 test files in `tests/`, `python -m pytest tests/`.
* **Viva Question:** *"How can you test quantum mechanics deterministically in Python unit tests?"* $\to$ By testing algebraic matrix invariants ($\langle \psi \mid \psi \rangle = 1.0$, $U^\dagger U = I$) and using deterministic seeds with bounded confidence intervals for shot sampling.

---

### [Lesson 37: The Grand Finale Documentation Kit & Championship Defense](file:///c:/Users/Rakshit%20Jain/Downloads/sih/docs/lessons/lesson_37_grand_finale_documentation.md)
* **Files in Focus:** `docs/SIH26141_FINAL_PITCH_DECK.md`, `docs/JUDGE_DEFENSE_MANUAL.md`, `docs/NQM_EXECUTIVE_WHITEPAPER.md`
* **What is it?** The crowning championship documentation: 12-slide presentation deck, timed pitch scripts, 4 whiteboard formulas, tough judge Q&A playbook, and National Quantum Mission technical whitepaper.
* **Analogy (ELI5):** The NASA Mission Operations Handbook & Supreme Court Defense Brief: authoritative scientific treatise backed by a tactical pocket cheat sheet.
* **Key Math:** Complete 37-lesson architecture map, the 4 whiteboard formulas, the top 5 judge defense questions.
* **Key Code:** Documentation kit files in `docs/`.
* **Viva Question:** *"What makes your framework uniquely qualified to win Problem Statement SIH-26141?"* $\to$ Complete 40-phase architectural coverage, whiteboard mathematical physics with zero black boxes, sub-2ms latency, 97 passing tests, and cryptographic release certification.

---

## 🏁 Quick Reference: File-to-Lesson Index

```text
quantum/state.py               -> Lesson 01
quantum/bell.py                -> Lesson 02
quantum/teleport.py            -> Lesson 03
quantum/measure.py             -> Lesson 04
quantum/tomography.py          -> Lesson 05
quantum/mesh.py                -> Lesson 06
security/signature.py          -> Lesson 07
security/freshness.py          -> Lesson 08
security/attacks.py            -> Lesson 09
security/detector.py           -> Lesson 10
security/calibrate.py          -> Lesson 11
security/decoy.py              -> Lesson 12
security/trojan.py             -> Lesson 13
security/blind.py              -> Lesson 14
security/chsh.py               -> Lesson 15
security/finite.py             -> Lesson 16
security/mdi.py                -> Lesson 17
security/wdm.py                -> Lesson 18
security/multirecipient.py     -> Lesson 19
security/hybrid.py             -> Lesson 20
security/mitigation.py         -> Lesson 21
analytics/history.py           -> Lesson 22
analytics/metrics.py           -> Lesson 23
analytics/stream.py            -> Lesson 24
analytics/soc.py               -> Lesson 25
analytics/reports.py           -> Lesson 26
dashboard/charts.py            -> Lesson 27
dashboard/visualizer.py        -> Lesson 28
app.py                         -> Lesson 29
benchmark.py                   -> Lesson 30
rehearsal.py                   -> Lesson 31
release_audit.py               -> Lesson 32
verify_demo.py & release.py    -> Lesson 33
package_submission.py          -> Lesson 34
run_*.bat / Dockerfile         -> Lesson 35
tests/ (97 tests)              -> Lesson 36
docs/ (Documentation Kit)      -> Lesson 37
```
