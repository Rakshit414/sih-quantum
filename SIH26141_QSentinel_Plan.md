# SIH26141 — Q-SENTINEL: Full Battle Plan

---

## 1. The Problem, In Plain Words

**What's actually broken?** Digital signatures (the math that proves "this message really came from me and wasn't altered") today rely on problems like factoring large numbers. A powerful-enough quantum computer can break that math. So the world is moving toward **Quantum Digital Signatures (QDS)** — signatures built out of quantum states instead of number theory, so they stay secure even against quantum attackers.

But QDS introduces a *new* problem: quantum systems are noisy, physically fragile, and can be attacked in ways classical crypto never had to worry about — someone intercepting a qubit mid-flight, replaying an old quantum state, or subtly disturbing the channel. **Nobody has asked "how do we monitor a QDS system for attacks in real time?"** SIH26141 wants exactly that: a **threat-detection layer that sits on top of a teleportation-based QDS system** and statistically flags forgery, impersonation, replay, and channel tampering — without using AI/ML (because ML models are black boxes and, ironically, themselves attackable; the judges want something mathematically transparent).

**Who faces this?** Any organization planning ahead for the "harvest now, decrypt later" quantum threat — banks, defense, telecom, PKI infrastructure providers (like Egreen Quanta itself, who sets the PS).

**Why are classical signatures insufficient?** RSA/ECDSA security rests on integer factorization / discrete log being hard *for classical computers*. Shor's algorithm breaks both in polynomial time on a sufficiently large quantum computer. QDS instead relies on the laws of quantum mechanics (no-cloning, measurement disturbance) — provably secure regardless of the attacker's compute power.

**What is a QDS?** A signature scheme where the "key" is a quantum state (e.g., a set of qubits in specific Pauli eigenstates) held by the signer and shared with verifiers. Verification is done by measuring your copy of the state and checking statistical agreement — not by checking a mathematical inverse.

**Why teleportation?** Quantum teleportation is the standard mechanism for moving a quantum state from signer to verifier without physically transporting the qubit — it uses a shared **Bell pair** + classical communication + a **Pauli correction**. It's the natural "transport layer" for a QDS. It's also where an attacker gets their only foothold: they can only interfere with the *classical* bits or the *entangled* pair, and both leave statistical fingerprints.

**What does "quantum-inspired" mean here?** We don't need real quantum hardware. We build a faithful **mathematical/software simulation** of qubits, Bell states, teleportation, and measurement — using real quantum mechanics equations, just executed on classical numpy arrays instead of a quantum chip. This is completely standard for hackathons and even for academic prototyping of quantum protocols.

**What are we expected to build?** A working simulator + detector + dashboard that demonstrates: legitimate signature acceptance, and detection of forgery / impersonation / replay / channel manipulation, backed by real statistics (error rates, thresholds, confidence).

**What are we NOT expected to build?** Real quantum hardware integration, a production PKI, blockchain, AI/ML anything, post-quantum classical crypto (that's a different PS), a multi-user distributed system.

**What can be simulated vs. must be "real"?** Everything can be simulated — that's the whole point of "quantum-inspired." What must be *real* is the **math**: actual state vectors, actual Pauli operators, actual measurement probability rules (Born rule), and actual statistical hypothesis testing on the outcomes. Judges will forgive "it's a simulator" but not "the math is hand-waved."

**What will a judge want to see?** (1) A live demo where clicking "Forge" visibly changes numbers and flips a status light. (2) You explaining *why* the numbers change, tied to real quantum mechanics. (3) A defensible statistical threshold, not a magic number.

### Input → Processing → Detection → Output

| Stage | What happens |
|---|---|
| **Input** | Message + claimed signer identity + a chosen scenario (normal / forge / impersonate / replay / channel-noise) |
| **Processing** | Signer prepares qubits in Pauli eigenstates → Bell pair generated → teleportation protocol run (Bell measurement + classical bits sent + Pauli correction applied) → verifier ends up with a (possibly disturbed) state |
| **Detection** | Verifier performs projective measurements over N repetitions → compares observed outcome distribution to the expected theoretical distribution → computes error rate → runs a statistical test against a calibrated threshold |
| **Output** | Threat category (LEGITIMATE / SUSPICIOUS / MALICIOUS), a numeric anomaly score with confidence, an explanation of which statistic tripped, and a dashboard visualization of the whole pipeline |

---

## 2. Our One Solution: **Q-SENTINEL**

> **"We are building Q-Sentinel — a quantum-inspired statistical watchtower that sits on a teleportation-based Quantum Digital Signature system and catches forgery, impersonation, replay, and channel tampering by proving, with hypothesis testing, that an attacker's measurement statistics can never look identical to a legitimate signer's."**

**Why this wins:**
- **Problem relevance** — it directly implements every bullet in the PS: Pauli eigenstates, Bell states, teleportation, Pauli correction, projective measurement, statistical/threshold detection. Nothing bolted on, nothing missing.
- **Innovation** — most teams will build "a QDS demo." We build the **security monitor for a QDS** — a genuinely under-explored angle, closer to what Egreen Quanta (a security company) actually cares about.
- **Technical depth** — real linear algebra (state vectors, Pauli matrices, Born rule), real statistics (binomial hypothesis testing), not just a UI wrapper.
- **Demo potential** — five buttons, five visibly different outcomes, in under 2 minutes.
- **Mathematical depth** — every number on screen traces back to a formula you can defend on a whiteboard.
- **Security relevance** — it's explainable (no ML black box) — matches the "no AI/ML" constraint as a *feature*, not a limitation: "our decisions are auditable one-formula-at-a-time."
- **Feasibility** — pure Python/NumPy, no GPU, no real quantum SDK dependency required, fits 2 days easily.
- **Differentiation** — ordinary "digital signature verification" is a binary pass/fail. We produce a *graded, statistically-quantified* threat score with a named test behind it — this is the actual novel contribution.

---

## 3. MVP Scope (Ruthless Cut)

### MUST HAVE (the demo dies without these)
- Qubit / state-vector simulator (NumPy, 2x2 and 4x4 complex matrices)
- Pauli eigenstate preparation (signature "key" states)
- Bell-state generation
- Teleportation simulation (Bell measurement + classical bits + Pauli correction)
- Projective measurement with repeated trials (N measurements → outcome counts)
- Statistical detector: error rate + binomial hypothesis test → threat score + category
- 4 attack simulators: forgery, impersonation, replay, channel noise
- A minimal working dashboard (even a single Streamlit page) with buttons for each scenario and live status + charts

### SHOULD HAVE (do these if Day 1 finishes early)
- Nicer dashboard layout (3-panel: input / circuit visualization / results)
- Measurement-outcome histogram + running threat-score-over-time chart
- Attack history log / table
- Confidence interval display alongside the point estimate
- A short animated/step-highlighted teleportation diagram

### NICE TO HAVE (touch only if everything above is rock solid)
- SQLite persistence of past runs
- Adjustable threshold sliders for live "what-if" demos
- Multiple simultaneous "sessions" to show replay detection across sessions
- Exportable PDF report of a run
- Circuit diagram rendered with an actual quantum library (Qiskit) instead of custom drawing

**Explicitly cut, and why:** real quantum hardware (no time, no need), blockchain ledger of signatures (irrelevant to PS, pure scope creep), AI/ML anomaly detection (PS forbids it), multi-user auth system (distracts from the core ask), post-quantum classical signature comparison (interesting but a different PS's job — mention only in the "future scope" slide).

---

## 4. System Architecture

```
                         ┌────────────────────┐
                         │        User          │
                         │ (message + scenario) │
                         └─────────┬───────────┘
                                   ▼
                      ┌────────────────────────┐
                      │ Signature Generation     │
                      │ (Pauli-eigenstate key)   │
                      └─────────┬───────────────┘
                                   ▼
                      ┌────────────────────────┐
                      │ Bell-State Generator     │  ← entanglement resource
                      └─────────┬───────────────┘
                                   ▼
                 ┌───────────────────────────────────┐
                 │ Teleportation Engine                │
                 │ (Bell measurement → classical bits  │
                 │  → Pauli correction)                │  ← ATTACK INJECTION POINT
                 └─────────┬───────────────────────────┘
                                   ▼
                      ┌────────────────────────┐
                      │ Projective Measurement    │
                      │ (N repeated trials)        │
                      └─────────┬───────────────┘
                                   ▼
                      ┌────────────────────────┐
                      │ Statistical Engine         │
                      │ (error rate, hypothesis    │
                      │  test, anomaly score)      │
                      └─────────┬───────────────┘
                                   ▼
                      ┌────────────────────────┐
                      │ Threat Classifier          │
                      │ LEGITIMATE / SUSPICIOUS /  │
                      │ MALICIOUS                  │
                      └─────────┬───────────────┘
                                   ▼
                      ┌────────────────────────┐
                      │ Dashboard                  │
                      └────────────────────────┘
```

### Component breakdown

| Component | Purpose | Input | Output | Math | Library | Difficulty | Essential? |
|---|---|---|---|---|---|---|---|
| Qubit engine | Represent quantum states as vectors | basis choice | state vector | `\|ψ⟩=α\|0⟩+β\|1⟩` | NumPy | Low | Yes |
| Signature generator | Encode message → Pauli eigenstate | message + key seed | prepared qubit(s) | Pauli eigenstates | NumPy | Low | Yes |
| Bell-state generator | Create entangled resource | none | 2-qubit state | `\|Φ⁺⟩=(\|00⟩+\|11⟩)/√2` | NumPy (kron) | Low | Yes |
| Teleportation engine | Move state signer→verifier | qubit + Bell pair | classical bits + corrected state | CNOT/H + Pauli correction | NumPy | Medium | Yes |
| Attack injector | Perturb the protocol | attack type + strength | modified state/bits | bit-flip / phase-flip channel | NumPy | Medium | Yes |
| Measurement module | Sample outcomes | state + basis + N | outcome counts | Born rule `P=\|⟨φ\|ψ⟩\|²` | NumPy | Low | Yes |
| Statistical detector | Score anomalies | outcome counts | error rate, p-value, score | binomial test / z-score | SciPy | Medium | Yes |
| Threat classifier | Threshold decision | score | category + confidence | thresholds from test | Python | Low | Yes |
| Dashboard | Visualize + control | user clicks | live charts | — | Streamlit + Plotly | Medium | Yes |
| History/log | Store past runs | run results | table | — | SQLite/JSON | Low | Should have |

---

## 5. Mathematics — From Zero

### A. Classical probability you need
- **Probability**: fraction of times an outcome occurs over many trials.
- **Conditional probability** `P(A|B)`: probability of A given B already happened — we'll use this implicitly when we say "probability of outcome=1 *given* the state was tampered."
- **Error rate**: fraction of measurement outcomes that disagree with what a legitimate signature would produce.
- **False positive**: system flags a legitimate signature as an attack.
- **False negative**: system fails to flag a real attack.
- **Detection rate**: fraction of actual attacks correctly flagged.

### B. Qubit mathematics
A qubit's state is a vector: `|ψ⟩ = α|0⟩ + β|1⟩`, where α, β are complex numbers called **probability amplitudes**. `|0⟩ = [1,0]ᵀ`, `|1⟩ = [0,1]ᵀ`. **Normalization** requires `|α|² + |β|² = 1` — because `|α|²` is literally the probability of measuring 0, and `|β|²` the probability of measuring 1; probabilities must sum to 1.

### C. Pauli matrices
```
X = [[0,1],[1,0]]     Y = [[0,-i],[i,0]]     Z = [[1,0],[0,-1]]
```
- `X|0⟩ = |1⟩`, `X|1⟩ = |0⟩` — X is a bit-flip.
- `Z|0⟩ = |0⟩`, `Z|1⟩ = -|1⟩` — Z is a phase-flip.
- `Y = iXZ` combines both.

**Why Pauli corrections matter in teleportation:** the Bell measurement the sender performs randomly collapses the receiver's qubit into one of 4 possible states, each differing from the "true" state by exactly one Pauli operator (I, X, Z, or XY). The 2 classical bits from the Bell measurement tell the receiver *which* Pauli operator to apply to undo the disturbance and recover the original state. If those classical bits are tampered with, the *wrong* correction gets applied — this is our primary attack surface.

### D. Bell states
The four maximally entangled 2-qubit states:
```
|Φ⁺⟩ = (|00⟩+|11⟩)/√2      |Φ⁻⟩ = (|00⟩-|11⟩)/√2
|Ψ⁺⟩ = (|01⟩+|10⟩)/√2      |Ψ⁻⟩ = (|01⟩-|10⟩)/√2
```
**Entanglement** means the two qubits' measurement outcomes are perfectly correlated no matter how far apart they are — measuring one instantly tells you the other's value. This correlation, not any signal travelling faster than light, is what teleportation exploits. In simulation we build `|Φ⁺⟩` directly as a 4-entry complex vector and never need real hardware.

### E. Quantum teleportation, step by step
1. Signer has secret qubit `|ψ⟩` (the "signature key state").
2. Signer and verifier share a Bell pair `|Φ⁺⟩`.
3. Signer performs a **Bell measurement** on `|ψ⟩` + their half of the pair → gets one of 4 classical outcomes (2 classical bits).
4. Signer sends those 2 bits over a classical channel.
5. Verifier applies the **Pauli correction** indicated by those 2 bits to their half of the pair.
6. Verifier's qubit is now exactly `|ψ⟩` (up to global phase) — the state has been "teleported," no physical qubit moved.

**30-second version for judges:** "The signer never physically sends the quantum key. They send a recipe (2 classical bits) telling the verifier which simple flip to apply to a qubit they already share. If an attacker changes that recipe or the shared pair, the verifier ends up holding the *wrong* state — and that wrongness shows up statistically the moment they measure it."

### F. Projective measurement
Measuring in a basis `{|φ₀⟩, |φ₁⟩}` uses **projection operators** `P_i = |φ_i⟩⟨φ_i|`. The **Born rule** gives outcome probability `P(i) = ⟨ψ|P_i|ψ⟩ = |⟨φ_i|ψ⟩|²`. Because a legitimate teleported state collapses to the *expected* eigenstate with (theoretically) 100% probability under ideal conditions, any deviation in the *observed* frequency over N trials is direct evidence something upstream was disturbed — this is the entire basis of our detector.

### G. Statistical threat detection — the chosen method

Let `N` = number of measurement trials, `n₁` = number of "unexpected" outcomes (disagreeing with the expected eigenstate), `n₀ = N - n₁`.

**Error rate:** `ê = n₁ / N`

**Why binomial hypothesis testing (not Z-score alone, not Bayesian, not chi-square) is the right call for a 2-day build:**
- Confidence intervals and Z-scores are both *derived from* the binomial model — so we get them "for free" once we commit to binomial.
- Chi-square needs multiple outcome categories with enough expected counts per cell — overkill for a 2-outcome (correct/incorrect) measurement.
- Bayesian approaches need a prior we can't defensibly justify in 2 days and are harder to explain to judges live.
- Likelihood-ratio tests are mathematically nice but add complexity with no visible demo benefit.
- **Binomial testing is exact, has a closed-form formula, is trivially implementable with `scipy.stats.binomtest` or even by hand, and is *the* standard tool for "how many coin flips came up wrong."** This is genuinely the simplest mathematically defensible choice — not a cop-out.

Under the null hypothesis "channel is legitimate," each trial has expected error probability `p₀` (theoretically 0 for a perfect channel, but we calibrate a small realistic `p₀` like 0.02–0.05 to account for natural quantum noise). We test whether the observed `n₁` is statistically consistent with `Binomial(N, p₀)`.

We convert this into a **normal approximation z-score** for a smooth, continuous anomaly score (easier to show on a gauge/dial than a raw p-value):
```
z = (ê - p₀) / sqrt( p₀(1-p₀) / N )
```
Then map `z` → thresholds:
- `z < 2` → **LEGITIMATE** (within ~95% confidence of expected noise)
- `2 ≤ z < 4` → **SUSPICIOUS**
- `z ≥ 4` → **MALICIOUS**

These aren't arbitrary — `z=2` and `z=4` correspond to standard 95%/99.99% confidence cutoffs on the normal distribution, which we can state and defend directly to a judge instead of saying "we picked 0.2 because it looked right."

---

## 6. Forgery / Attack Models

| Attack | What happens | How we simulate | What statistic moves | How detector catches it |
|---|---|---|---|---|
| **Forgery** | Attacker fabricates a signature state without the real key | Prepare a random/incorrect eigenstate instead of the true one | Measurement outcomes scatter ~50/50 instead of matching expected eigenstate | `ê` jumps far above `p₀` → high z |
| **Impersonation** | Wrong signer's key state used | Swap in a different (valid-looking but wrong) Pauli eigenstate | Same signature-shape mismatch as forgery, but tagged with wrong identity | Detector flags mismatch + identity tag shown in dashboard |
| **Replay** | Old valid teleportation session reused | Reuse previous session's classical bits and check nonce/timestamp | Statistics *look* fine, but session ID / nonce fails freshness check | Separate freshness check (not statistical) rejects it — explicitly explain in dashboard as "replay ≠ statistical anomaly, it's a bookkeeping check" |
| **Channel manipulation** | Adversary injects noise on Bell pair / classical bits | Apply a controllable bit-flip/phase-flip probability to the shared state before measurement | `ê` rises proportionally with injected noise level | z-score rises smoothly — great demo: slider from 0% → 30% noise, watch status flip green→yellow→red |

---

## 7. Detection Algorithm — **Q-STAT (Quantum Statistical Threat Assessment)**

**Inputs:** message, claimed signature, expected eigenstate, list of N measurement outcomes, N, noise/attack parameters (for simulation only).
**Outputs:** error rate, z-score, threat category, confidence, plain-English explanation.

**Formulas:**
```
ê = n₁ / N
z = (ê - p₀) / sqrt(p₀(1-p₀)/N)
confidence = Φ(z)   (standard normal CDF, i.e., how extreme z is)
category = LEGITIMATE if z<2, SUSPICIOUS if 2≤z<4, MALICIOUS if z≥4
```

**Pseudocode:**
```
function Q_STAT(outcomes, expected_outcome, p0=0.03):
    N = len(outcomes)
    n1 = count(o != expected_outcome for o in outcomes)
    e_hat = n1 / N
    std = sqrt(p0 * (1 - p0) / N)
    z = (e_hat - p0) / std
    confidence = normal_cdf(z)
    if z < 2:      category = "LEGITIMATE"
    elif z < 4:    category = "SUSPICIOUS"
    else:          category = "MALICIOUS"
    explanation = f"Observed error rate {e_hat:.2%} vs expected {p0:.2%}; z={z:.2f}"
    return { e_hat, z, confidence, category, explanation }
```
**Line by line:** count trials disagreeing with the theoretically-expected outcome → normalize into an error rate → standardize against the expected noise floor's own standard deviation (this is what makes the score comparable across different N) → convert to a human-readable confidence via the normal CDF → bucket into 3 named categories using statistically-justified cutoffs → generate a plain-English reason string for the dashboard.

---

## 8. Simulation Choice: **Custom NumPy simulator**

Not Qiskit/Cirq/PennyLane. Reasoning: we only ever need 1–2 qubit systems (state vectors of length 2 or 4) — a full quantum SDK is designed for circuits with many qubits and gate-level compilation, which adds setup time, install headaches, and unpredictable library-version bugs, for zero benefit at this scale. A ~150-line NumPy module (state vectors, Pauli matrices, `kron` for tensor products, Born-rule sampling via `np.random.choice`) is faster to write, trivial to debug (you can print any intermediate vector), and just as mathematically correct, since we're already stating everything is a software simulation. This also removes any hardware/API/version dependency risk two days before a demo.

---

## 9. Tech Stack

| Layer | Choice | Why | Mandatory? | Time |
|---|---|---|---|---|
| Quantum sim | NumPy | see above | Yes | included in build |
| Stats | SciPy (`stats.binomtest`, `norm.cdf`) | exact, standard, no need to hand-roll | Yes | ~30 min to wire in |
| Backend/glue | Plain Python functions | no need for a separate API server for a single-user demo | Yes | — |
| Frontend/dashboard | **Streamlit** | fastest way to get a working reactive UI with buttons + live charts in Python, zero JS needed | Yes | ~3–4 hrs |
| Charts | **Plotly** (via Streamlit) | interactive bar/gauge charts, looks far less "student project" than static matplotlib | Should have | ~1–2 hrs |
| Storage | JSON file or in-memory list | a run history table doesn't need a real DB for a demo | Should have | ~30 min |
| Deployment | `localhost` + optionally Streamlit Community Cloud for a shareable link | zero-friction, no DevOps needed | Should have | ~15 min if needed |

---

## 10. Folder Structure

```
q-sentinel/
├── app.py                     # Streamlit dashboard entrypoint
├── quantum/
│   ├── state.py               # qubit/state-vector utilities, Pauli matrices
│   ├── bell.py                # Bell-state generation
│   ├── teleport.py            # teleportation protocol
│   └── measure.py             # projective measurement / Born-rule sampling
├── security/
│   ├── signature.py           # signature generation from message+key
│   ├── attacks.py             # forgery/impersonation/replay/noise injectors
│   └── detector.py            # Q-STAT statistical engine
├── dashboard/
│   └── charts.py              # Plotly chart builders
├── data/
│   └── history.json           # run log (should-have)
├── requirements.txt
└── README.md
```

---

## 11. Build Order & Timeline

### DAY 1 — Core quantum sim + signature + attacks
| Priority | Task | Time | Depends on | Output |
|---|---|---|---|---|
| P0 | `quantum/state.py`: qubit vectors, Pauli ops | 1.5h | — | tested state utilities |
| P0 | `quantum/bell.py`: Bell-pair construction | 0.5h | state.py | verified `\|Φ⁺⟩` |
| P0 | `quantum/teleport.py`: teleportation protocol | 2h | bell.py | working teleport function |
| P0 | `quantum/measure.py`: projective measurement sampling | 1h | state.py | outcome-count generator |
| P0 | `security/signature.py`: message → eigenstate mapping | 1h | state.py | signature generator |
| P0 | `security/attacks.py`: forge/impersonate/replay/noise | 2h | teleport.py | 4 attack functions |
| Buffer | debugging/integration | 1h | all above | pipeline runs end-to-end from CLI |

### DAY 2 — Detection + dashboard + polish
| Priority | Task | Time | Depends on | Output |
|---|---|---|---|---|
| P0 | `security/detector.py`: Q-STAT implementation | 2h | measure.py | scores + categories |
| P0 | `app.py`: basic Streamlit skeleton with scenario buttons | 2h | detector.py | clickable demo |
| P1 | `dashboard/charts.py`: histograms, gauge, threat light | 2h | app.py | visual polish |
| P1 | Run history table | 1h | detector.py | attack log |
| Buffer | full run-through, bug fixes | 1.5h | everything | stable demo |
| P0 | README, requirements.txt, slide talking points | 1h | — | submission-ready |
| Buffer | rehearse 30s/1min/3min pitch | 0.5h | — | confident presentation |

---

## 12. Dashboard Wireframe

```
┌──────────────────────────────────────────────────────────────────┐
│  Q-SENTINEL   |  SIH26141 — Quantum-Inspired QDS Threat Detection │
├───────────────┬──────────────────────────────┬───────────────────┤
│ INPUT PANEL   │   TELEPORTATION VISUALIZER    │  SECURITY STATUS  │
│ Message: [__] │  Signer ──Bell──> Verifier    │   🟢 LEGITIMATE   │
│ Signer ID:[_] │  [state] [correction] [state] │   z = 0.8         │
│ Scenario:     │                                │  Confidence: 97% │
│  ( ) Normal   ├──────────────────────────────┤├───────────────────┤
│  ( ) Forge    │   MEASUREMENT DISTRIBUTION     │  ANALYTICS        │
│  ( ) Imperson.│   [bar chart of outcomes]      │  Error rate: 2.1% │
│  ( ) Replay   │                                │  Threshold: z<2   │
│  ( ) Channel  │                                │  Attack: none     │
│  [Run] button │                                │                   │
├───────────────┴──────────────────────────────┴───────────────────┤
│  RUN HISTORY: [table of past runs — scenario | z | verdict]        │
└──────────────────────────────────────────────────────────────────┘
```

---

## 13. Demo Scenarios

| Scenario | Input | Attack | Expected outcome shape | z-score | Result |
|---|---|---|---|---|---|
| 1. Legitimate | "Approve payment #1023" | none | ~97% match expected | ~0.5–1.5 | 🟢 ACCEPTED |
| 2. Forgery | same message | random wrong eigenstate | ~50% match | ~15+ | 🔴 REJECTED |
| 3. Impersonation | same message, wrong signer key | swapped identity state | ~50% match, ID mismatch | ~15+ | 🔴 REJECTED |
| 4. Replay | previously used session | reused classical bits | stats look fine | ~0.5–1.5 | 🔴 REJECTED (freshness check, not statistics) |
| 5. Channel manipulation | same message | 0%→30% injected noise slider | error rate rises with slider | rises 0→10+ | 🟢→🟡→🔴 live transition |

---

## 14. Innovation Claims (defensible only)

1. **Measurement statistics as a live cyber-threat signal** — existing QDS literature focuses on protocol *design*; almost none focus on continuous *monitoring*. Our contribution: turning routine verification measurements into a security telemetry stream.
2. **Attack-specific disturbance modeling** — instead of one generic "error," we model 4 distinct attacker behaviors and show each produces a *distinguishable* statistical fingerprint.
3. **Statistically justified thresholds, not tuned magic numbers** — z=2/z=4 map to standard confidence levels, defensible on a whiteboard.
4. **Explainable-by-construction decision engine** — every verdict traces to one formula, addressing the "no AI/ML" constraint as an actual design virtue (auditability) rather than a limitation.
5. **Separation of statistical detection vs. bookkeeping detection** — explicitly distinguishing "replay is caught by freshness metadata, not statistics" shows mature threat-modeling, not just one hammer for every nail.

*(Dropped: "uses quantum computing" — not a real claim since we simulate; not listed as an innovation.)*

---

## 15. Performance Metrics (pick these 5)

| Metric | Definition | Why it matters |
|---|---|---|
| **Verification accuracy** | (correct verdicts)/(total runs) | overall system correctness |
| **False acceptance rate (FAR)** | attacks classified LEGITIMATE / total attacks | security risk if too high |
| **False rejection rate (FRR)** | legitimate runs classified MALICIOUS / total legitimate | usability risk if too high |
| **Detection latency** | time from measurement to verdict | shows real-time feasibility |
| **z-score separation** | avg z(attack) − avg z(legit) | shows how well-separated the classes are — a strong, visual "our detector actually works" number |

(Error rate and threshold are already shown live on the dashboard, so they don't need a separate "metrics slide" — fold them into the demo instead.)

---

## 16. Security Analysis

- **Guarantee provided:** statistical detection of protocol-level disturbances (forgery, impersonation, channel noise) with quantified confidence; a separate freshness check for replay.
- **Not claimed:** unconditional cryptographic security, protection against attacks outside the modeled threat set, real-world hardware-noise characterization.
- **Detected:** forgery, impersonation, channel tampering (all via statistics), replay (via freshness metadata).
- **Not detected:** attacks that perfectly reproduce expected statistics (theoretically excluded by quantum no-cloning, but not empirically tested against real adversarial hardware), side-channel attacks on classical infrastructure, denial-of-service.
- **Assumptions:** signer and verifier share an authenticated (not necessarily encrypted) classical channel for the 2 correction bits; a calibrated baseline noise floor `p₀` exists for the "quiet" channel.
- **Noisy channel handling:** `p₀` is exactly the parameter that absorbs expected natural noise, so honest noise doesn't trip false alarms — that's the point of testing against a *non-zero* baseline instead of a raw zero-tolerance check.
- **False positives prevented by:** calibrating `p₀` from real "no-attack" trial runs before demo, and using a two-tier (SUSPICIOUS before MALICIOUS) threshold so borderline noise doesn't instantly get treated as an attack.
- **Why statistics, not a hard pass/fail:** quantum measurement is inherently probabilistic — a single wrong outcome is not evidence, but a *pattern* of wrong outcomes over N trials is.

---

## 17. Limitations (state honestly, frame positively)

- No real quantum hardware — **framed as:** "protocol-correct simulation lets us test attack scenarios that would be destructive or infeasible on real noisy hardware."
- Simulated quantum channel — **framed as:** "parameterized noise model, tunable for live demonstration of graceful degradation."
- Simplified QDS protocol (single-qubit teleportation, not a full multi-party QDS scheme) — **framed as:** "MVP demonstrates the core statistical principle, which generalizes directly to larger multi-qubit QDS protocols."
- Thresholds calibrated on synthetic trial data, not field data — **framed as:** "the *method* (binomial testing) is what's novel; threshold values are a deployment-time calibration step, standard in any security system (e.g., IDS tuning)."
- No production PKI integration — **framed as:** "designed as a pluggable verification layer, not a monolith — could sit alongside any QDS key-management system."

---

## 18. Judge Q&A (honest, strong answers)

**Why quantum?** Classical signature security degrades under quantum attackers (Shor's algorithm); QDS security instead relies on physical laws that hold regardless of attacker compute.

**Why teleportation?** It's the standard way to transmit a quantum state using only a pre-shared entangled pair and classical bits — and it's exactly the mechanism the PS names, giving us a concrete, well-defined attack surface (the classical bits and the shared pair) to monitor.

**What is a Bell state?** A maximally entangled 2-qubit state where measuring one qubit instantly determines the other's outcome, e.g. `|Φ⁺⟩=(|00⟩+|11⟩)/√2`.

**Why Pauli correction?** Bell measurement randomly leaves the receiver's qubit off by one of 4 Pauli operators; the sent classical bits specify which correction undoes that — tampering with those bits misapplies the correction and detectably corrupts the recovered state.

**What are Pauli eigenstates?** The `+1`/`-1` eigenvectors of the Pauli matrices (e.g. `|0⟩,|1⟩` for Z; `|+⟩,|−⟩` for X) — we use them as our "key" basis states for signatures.

**What is projective measurement?** Measuring a state by projecting it onto basis vectors; the Born rule gives outcome probabilities as squared overlaps.

**Why does measurement reveal an attack?** Because any tampering with the state or the correction bits changes the probability distribution of measurement outcomes away from the theoretically expected one — and that shift is what we test for statistically.

**How exactly do you detect forgery/impersonation/replay/channel manipulation?** (See Part 6 table — answer per-attack with the specific mechanism.)

**Why can't an attacker bypass this?** Any attacker without the correct key state or correct classical bits necessarily produces a measurement distribution statistically distinguishable from the honest one, over enough trials — an attacker succeeding "by luck" has probability decaying exponentially with N (standard binomial tail bound).

**How did you select the threshold?** From the normal approximation to the binomial distribution: z=2 and z=4 correspond to standard 95%/99.99% confidence bounds, not arbitrarily tuned numbers.

**How many measurements are enough?** More N sharpens the standard deviation `sqrt(p₀(1-p₀)/N)`, shrinking it and making the z-score more sensitive; we can show this trade-off live by varying N in the demo.

**Why not AI/ML?** PS explicitly excludes it, and it would also undermine one of our biggest selling points: full auditability of every decision.

**Why not blockchain?** Out of scope for the PS's ask (threat detection, not ledger integrity) — would add complexity with zero relevance to signature/authenticity detection.

**Why not post-quantum classical crypto?** That's a different, complementary PS; ours is specifically about a QDS *system's* runtime security monitoring.

**Can this work in real systems? How would you scale it?** Yes conceptually — the statistical framework doesn't care whether the qubits are simulated or physical; scaling means calibrating `p₀` against real hardware noise floors and running the same hypothesis test per verification event.

**What's your contribution vs what exists?** Existing QDS research proposes protocols; we propose and implement the *monitoring layer* on top of one, with a concrete, named, math-backed detection algorithm (Q-STAT).

---

## 19. Pitches

**30 seconds:** "Quantum digital signatures will protect us once quantum computers break today's encryption — but nobody's watching *them* for attacks. Q-Sentinel is a security camera for quantum signatures: it watches the measurement statistics during signature verification and mathematically proves, with a confidence score, whether a signature is genuine or under attack — catching forgery, impersonation, replay, and channel tampering, live."

**1 minute:** Add — "It works by simulating the actual physics: Bell-state entanglement, quantum teleportation, and Pauli corrections, then applying a rigorous statistical hypothesis test (not AI, per the problem's requirement) to the measurement outcomes. Every verdict is fully explainable — you can trace any 'MALICIOUS' flag back to one formula."

**3 minutes (technical):** Walk through the pipeline diagram, the four attack models and what statistic each perturbs, and the binomial z-score threshold derivation — emphasizing that the thresholds correspond to standard 95%/99.99% confidence levels, not tuned constants.

**5 minutes (deep technical):** Add the full math from Part 5 (state vectors, Born rule, Pauli correction mechanics) plus the security-analysis caveats from Part 16/17, so the story stays internally consistent from the 30-second version all the way up.

---

## 20. Final Prototype Checklist

**CORE:** [ ] Quantum simulation [ ] Bell state [ ] Teleportation [ ] Pauli correction [ ] Measurement [ ] Signature verification [ ] Statistical detection [ ] Forgery [ ] Impersonation [ ] Replay [ ] Channel manipulation

**UI:** [ ] Dashboard [ ] Live result [ ] Graphs [ ] Attack simulator buttons [ ] Threat score display

**TECHNICAL:** [ ] Mathematical model documented [ ] Performance metrics [ ] Security analysis [ ] Limitations [ ] README [ ] requirements.txt

**PRESENTATION:** [ ] Problem [ ] Existing gap [ ] Proposed solution [ ] Architecture [ ] Innovation [ ] Mathematics [ ] Demo [ ] Results [ ] Future scope

---

**We have only 2 days.** Everything above is scoped to that. No blockchain, no real hardware, no AI/ML, no enterprise platform — a tight, mathematically defensible, visually clean simulator.
