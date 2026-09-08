# 📘 Q-SENTINEL Masterclass | Lesson 25: Enterprise SOC SIEM Integration & STIX 2.1 CTI Bundles (Q-SOC)

> **File in Focus:** [`analytics/soc.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/analytics/soc.py)  
> **Pipeline Position:** Step 25 of the entire Q-Sentinel architecture (Enterprise SOC & Threat Intelligence Layer — Phase 38)  
> **Target Audience:** Fresher needing to understand how quantum threat detection bridges to enterprise Security Operations Centers (SOCs), what OASIS STIX 2.1 Cyber Threat Intelligence (CTI) is, how SDOs and SROs model quantum attacks, and how events are formatted for Elastic Common Schema (ECS 8.x) and Splunk.

---

## 🧭 1. What Is This File and Why Does It Exist?

Imagine a state-sponsored cyber adversary launching a sophisticated optical attack against a bank's quantum digital signature channel:
* They inject continuous-wave blinding lasers into the Single-Photon Avalanche Diodes ([`security/blind.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/blind.py)).
* They launch high-power out-of-band pump lasers into adjacent fiber channels to saturate quantum detectors with Raman noise ([`security/wdm.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/wdm.py)).
* Q-Sentinel’s physical watchtowers detect the attack, calculate $z = +6.52\sigma$, and block the signature.

Now comes the enterprise question:
> *"How does the bank notify national CERT teams (CERT-In, CISA), allied defense agencies, and enterprise security platforms (Splunk, Elastic SIEM, IBM QRadar, Microsoft Sentinel) about this attack?"*

If Q-Sentinel only printed a message in a terminal or displayed a local Streamlit chart, the enterprise SOC would be completely blind to the incident.
Enterprise cyber defense requires standardized, machine-readable threat intelligence:
1. **OASIS STIX 2.1 (Structured Threat Information Expression):** The globally recognized open standard for Cyber Threat Intelligence (CTI). It uses graph-based JSON structures to define *who* detected the attack, *what* technique was used, *what* mathematical indicators triggered the alert, and *how* it was mitigated.
2. **Elastic Common Schema (ECS 8.x):** The unified data model used by Elastic SIEM, Logstash, and Splunk HTTP Event Collector (HEC) to ingest, index, and query security logs.

[`analytics/soc.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/analytics/soc.py) is the **Q-SOC Integration Engine**. It automatically transforms raw quantum hypothesis tests and incident reports into fully compliant OASIS STIX 2.1 CTI bundles and ECS 8.x documents.

---

## 💡 2. Plain English Real-World Analogies

### Analogy 1: The Interpol Red Notice
Imagine a bank robber escapes across international borders:
* If the local police department writes a handwritten memo in their local dialect, police forces in other countries cannot easily understand or act upon it.
* Instead, they file an **Interpol Red Notice**: a globally standardized document formatted with universal fields: Identity of the suspect, Fingerprints, Crime Classification, and Recommended Action (Arrest and Extradite).
* **STIX 2.1 is the Interpol Red Notice of cyberspace.**  
  When Q-Sentinel catches an adversary performing a Trojan probe or CW blinding attack, it creates a standardized STIX bundle. Any security agency in the world running Splunk or Elastic can ingest the bundle and immediately know:
  - What quantum attack technique occurred (`Attack-Pattern`)
  - The exact $z$-score and error rate pattern to watch for (`Indicator`)
  - What automated actions were taken to isolate the attacker (`Course-Of-Action`)

### Analogy 2: The Hospital Emergency Triage Code
When an ambulance brings an injured patient into an emergency room:
* The paramedics do not give a long, confusing story.
* They call out standardized medical triage codes: *"Code Red, Trauma Level 1, Heart Rate 140, BP 80/50."*
* Every doctor in the hospital instantly knows what to do because the format is standardized.
* **Elastic Common Schema (ECS 8.x)** is the triage code for IT security: it maps quantum telemetry into standard fields (`@timestamp`, `event.severity = 7`, `event.action = "quantum-threat-blocked"`, `quantum.z_score = 6.52`).

---

## 📐 3. The OASIS STIX 2.1 & ECS Architecture

```
                    ThreatAssessment (z-score, p-value, error_rate)
                                          │
                                          ▼
                       ┌─────────────────────────────────────┐
                       │ QSOCIntegrator                      │
                       │ process_incident_and_export()       │
                       └──────────────────┬──────────────────┘
                                          │
         ┌────────────────────────────────┴────────────────────────────────┐
         ▼                                                                 ▼
┌─────────────────────────────────┐                       ┌─────────────────────────────────┐
│ STIXBundleGenerator             │                       │ ECSEventFormatter               │
│ Generates OASIS STIX 2.1 Bundle │                       │ Formats Elastic Common Schema   │
└────────────────┬────────────────┘                       └────────────────┬────────────────┘
                 │                                                         │
                 ▼                                                         ▼
     ┌───────────────────────┐                                 ┌───────────────────────┐
     │ 1. Identity SDO       │                                 │ @timestamp (ISO 8601) │
     │ 2. Attack-Pattern SDO │                                 │ event.severity (1/3/7)│
     │ 3. Indicator SDO      │                                 │ event.action          │
     │ 4. Observed-Data SDO  │                                 │ user.id / host.name   │
     │ 5. Course-Of-Action   │                                 │ quantum.* (z-score)   │
     │ 6. Relationship SROs  │                                 │ threat.* (CAPEC id)   │
     └───────────┬───────────┘                                 └───────────┬───────────┘
                 │                                                         │
                 └────────────────────────┬────────────────────────────────┘
                                          │
                                          ▼
                      ┌────────────────────────────────────────┐
                      │ SIEM Dispatch Result (HTTP 200 OK)     │
                      │ Ingested into Splunk / Elastic SIEM    │
                      └────────────────────────────────────────┘
```

### 1. The Anatomy of a STIX 2.1 Bundle
In OASIS STIX 2.1, a Threat Intelligence Bundle is a JSON document containing **STIX Domain Objects (SDOs)** connected by **STIX Relationship Objects (SROs)**:

#### A. SDO: Identity (`identity--<UUID>`)
Identifies the reporting entity. In Q-Sentinel:
```json
{
  "type": "identity",
  "name": "Q-Sentinel Quantum Threat Watchtower Sensor",
  "identity_class": "system",
  "sectors": ["defense", "government", "financial-services"]
}
```

#### B. SDO: Attack-Pattern (`attack-pattern--<UUID>`)
Maps the detected attack to formal cyber defense taxonomies (MITRE ATT&CK and CAPEC):
* `FORGERY` $\to$ `CAPEC-QDS-FORGERY` (Quantum Digital Signature Forgery)
* `DETECTOR_BLINDING` $\to$ `CAPEC-QDS-BLINDING` (Lydersen-Makarov CW Blinding)
* `RAMAN_CROSS_TALK_JAMMING` $\to$ `CAPEC-QDS-WDM-JAMMING` (WDM Raman Jamming)
* `PHOTON_NUMBER_SPLITTING` $\to$ `CAPEC-QDS-PNS` (Decoy-State PNS)
* `CHSH_BELL_VIOLATION_COLLAPSE` $\to$ `CAPEC-QDS-CHSH-SPOOF` (Separable State Spoofing)

#### C. SDO: Indicator (`indicator--<UUID>`)
Defines the mathematical detection pattern using the formal STIX pattern syntax:
```text
[quantum-threat-telemetry:z_score >= 6.52 AND quantum-threat-telemetry:observed_error_rate >= 0.1800]
```
This pattern can be ingested by any SIEM rule engine to alert on matching quantum telemetry across the network.

#### D. SDO: Observed-Data (`observed-data--<UUID>`)
Records the raw empirical measurements:
```json
{
  "type": "x-quantum-telemetry",
  "signer_identity": "Alice",
  "standardized_z_score": 6.52,
  "exact_p_value": 0.000012,
  "observed_error_rate": 0.18,
  "baseline_noise_p0": 0.03,
  "total_measurement_trials": 400
}
```

#### E. SDO: Course-Of-Action (`course-of-action--<UUID>`)
Specifies the automated mitigation steps executed by Q-MITIGATE:
* `[NONCE_REVOCATION]` Session nonce revoked and blacklisted.
* `[SIGNER_QUARANTINE]` Signer endpoint placed under administrative quarantine.
* `[BELL_POOL_PURGE]` Purged shared Bell entanglement memory buffers.

#### F. SRO: Relationship (`relationship--<UUID>`)
Creates directed graph edges linking the objects:
1. `indicator` $\xrightarrow{\text{indicates}}$ `attack-pattern`
2. `course-of-action` $\xrightarrow{\text{mitigates}}$ `attack-pattern`

---

### 2. Elastic Common Schema (ECS 8.x) Mapping
For ingestion into Elasticsearch, Logstash, Kibana, or Splunk, [`ECSEventFormatter`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/analytics/soc.py#L316) formats the event with standard ECS severity codes:

| Q-STAT Verdict | ECS Severity Code | `event.action` | `event.outcome` | Description |
| :---: | :---: | :---: | :---: | :--- |
| **`LEGITIMATE`** | **1** (Low / Info) | `quantum-signature-verified` | `success` | Normal signature verification under baseline noise. |
| **`SUSPICIOUS`** | **3** (Medium) | `quantum-anomaly-flagged` | `unknown` | Elevated noise ($2 \le z < 4$) requiring elevated audit. |
| **`MALICIOUS`** | **7** (High / Critical) | `quantum-threat-blocked` | `failure` | Active attack ($z \ge 4$), signature blocked, SOAR containment. |

---

## 🔬 4. Architectural Breakdown of `analytics/soc.py`

Let's examine the Python classes and methods line by line.

### Class 1: `STIXBundleGenerator` (Lines 62–314)
The generator responsible for synthesizing compliant STIX 2.1 JSON:
* `QUANTUM_ATTACK_PATTERNS`: Dictionary mapping 9 quantum threat categories to CAPEC IDs and kill chain phases.
* `generate_bundle(assessment, signer_id, scenario_name, message_payload, incident_report)`:
  - Generates ISO 8601 UTC timestamps with microsecond precision (`now_iso`).
  - Creates 5 SDOs: `identity`, `attack-pattern`, `indicator`, `observed-data`, and `course-of-action`.
  - Creates 2 SROs: `indicates` and `mitigates`.
  - Assembles all objects into a single `bundle` object with a unique UUID.
  - Returns `STIXBundleSummary` with metadata counts and the formatted JSON string.

### Class 2: `ECSEventFormatter` (Lines 316–399)
Formats telemetry for the Elastic stack and Splunk HEC:
* Maps `assessment.verdict` to ECS `severity` ($1$, $3$, or $7$).
* Structures data into standard ECS namespaces:
  - `event`: `category = ["network", "intrusion_detection"]`, `kind = "alert"`, `module = "qsentinel_qds"`
  - `host`: `name = "quantum-node-01.gov.in"`, `architecture = "quantum-hybrid-soc"`
  - `user`: `id = signer_id`, `roles = ["qds_signer"]`
  - `quantum`: Dedicated namespace containing `standardized_z_score`, `exact_p_value`, `observed_error_rate`, and `stix_bundle_ref`.
  - `threat`: MITRE ATT&CK / CAPEC technique metadata.

### Class 3: `QSOCIntegrator` (Lines 401–456)
The master orchestrator for enterprise dispatch:
```python
def process_incident_and_export(
    self,
    assessment: ThreatAssessment,
    signer_id: str,
    scenario_name: str,
    message_payload: str,
    incident_report: Optional[IncidentReport] = None
) -> Tuple[STIXBundleSummary, SIEMDispatchResult]:
```
1. Calls `STIXBundleGenerator.generate_bundle()` $\to$ creates CTI bundle.
2. Calls `ECSEventFormatter.format_ecs_event()` $\to$ creates ECS document referencing the STIX bundle ID.
3. Simulates enterprise dispatch and returns `SIEMDispatchResult` with status `"DELIVERED (HTTP 200 OK)"`.

---

## ⚡ 5. Step-by-Step Code Execution Walkthrough

Let's trace test `test_stix_bundle_generation_conformance` from [`tests/test_soc.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/tests/test_soc.py#L60-L89):

```
Input Assessment:
  verdict = ThreatCategory.MALICIOUS
  observed_error_rate = 0.18 (18.00%)
  z_score = 6.52 sigma, p_value = 1.2e-8
  scenario = "FORGERY", signer = "Alice"
```

### Step 1: STIX Object Synthesis
1. **Identity SDO:** Created with `id = "identity--<uuid>"`, `name = "Q-Sentinel Quantum Threat Watchtower Sensor"`.
2. **Attack-Pattern SDO:** `"FORGERY"` matches `QUANTUM_ATTACK_PATTERNS["FORGERY"]`:
   - `name = "Quantum Digital Signature Forgery"`
   - `external_id = "CAPEC-QDS-FORGERY"`
   - `phase_name = "credential-forgery"`
3. **Indicator SDO:**
   - Pattern string: `[quantum-threat-telemetry:z_score >= 6.52 AND quantum-threat-telemetry:observed_error_rate >= 0.1800]`
   - `indicator_types = ["anomalous-activity", "malicious-activity"]`
4. **Observed-Data SDO:**
   - Records $400$ trials, $z = 6.52$, $p = 1.2 \times 10^{-8}$, and error rate $18.0\%$.
5. **Course-Of-Action SDO:**
   - Actions: `Nonce Revocation`, `Signer Quarantine`, `Bell Buffer Purge`.
6. **Relationships SRO:**
   - Relates `indicator` $\to$ `attack-pattern` (`indicates`).
   - Relates `course-of-action` $\to$ `attack-pattern` (`mitigates`).

### Step 2: Validation
* Asserts `summary.spec_version == "2.1"` ✅
* Asserts `summary.bundle_id.startswith("bundle--")` ✅
* Asserts `summary.object_count == 7` (5 SDOs + 2 SROs) ✅
* All JSON schemas parse cleanly with zero syntax errors.

---

## ⚔️ 6. Hackathon Judge Defense & Viva Voce Q&A

### Q1: "Why did you implement OASIS STIX 2.1 instead of just sending regular syslog or JSON?"
**Defense:**  
> *"Syslog and unstructured JSON are proprietary and lack semantic relationships. When a national security agency or enterprise SOC receives an unstructured log, human analysts have to manually figure out what attack technique occurred and what steps to take.  
> **OASIS STIX 2.1** is the global international standard for Cyber Threat Intelligence (CTI). By structuring detections into standardized SDOs (Attack-Patterns, Indicators, Observed-Data, Courses-of-Action) and SROs (Relationships), Q-Sentinel alerts can be ingested directly into automated threat-sharing platforms like MISP (Malware Information Sharing Platform) and national CERT warning feeds with zero human translation."*

### Q2: "What is Elastic Common Schema (ECS), and why is ECS 8.x important?"
**Defense:**  
> *"Elastic Common Schema (ECS) is an open-source specification that defines a common set of field names and data types for event data ingested into Elasticsearch and Splunk.  
> Without ECS, one sensor might log `client_ip`, another logs `source_address`, and another logs `src_ip`, forcing analysts to write complex query conversions.  
> With ECS 8.x, Q-Sentinel events map seamlessly into standard fields (`@timestamp`, `event.severity`, `host.name`, `user.id`), while encapsulating quantum-specific metrics inside a dedicated `quantum.*` namespace. This allows SOC analysts to query quantum threats using standard KQL (Kibana Query Language) or Splunk SPL."*

### Q3: "How does Q-Sentinel map quantum attacks to classical cyber frameworks like MITRE ATT&CK or CAPEC?"
**Defense:**  
> *"In [`analytics/soc.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/analytics/soc.py#L68-L124), we created the **Quantum Adversarial Attack Taxonomy**, mapping each physical quantum attack to its CAPEC counterpart:  
> * Quantum Forgery $\to$ `CAPEC-QDS-FORGERY` (Credential Forgery)  
> * Detector Blinding $\to$ `CAPEC-QDS-BLINDING` (Hardware Tampering)  
> * Decoy PNS $\to$ `CAPEC-QDS-PNS` (Eavesdropping)  
> * Raman Jamming $\to$ `CAPEC-QDS-WDM-JAMMING` (Denial of Service)  
> This bridges the gap between quantum physicists and cybersecurity analysts, enabling SOC teams without a physics background to immediately understand threat severity."*

### Q4: "What is the role of the Course-Of-Action (COA) SDO in automated defense?"
**Defense:**  
> *"In STIX 2.1, a Course-Of-Action SDO specifies remediation steps.  
> When Q-MITIGATE ([`security/mitigation.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/security/mitigation.py)) executes automated countermeasures (quarantining a signer, revoking a nonce, or purging Bell buffers), those containment actions are serialized directly into the STIX COA object.  
> When the CTI bundle arrives at downstream firewall orchestrators or software-defined network (SDN) controllers, those external systems can automatically execute network-level blocking based on the COA instructions."*

### Q5: "How does `QSOCIntegrator` simulate enterprise SIEM delivery?"
**Defense:**  
> *"`QSOCIntegrator.process_incident_and_export()` generates the STIX bundle, formats the ECS document, and builds a `SIEMDispatchResult`. It records a unique dispatch ID, target platform endpoint, timestamp, severity code, and returns `DELIVERED (HTTP 200 OK)`.  
> In production deployment, this payload is POSTed via HTTPS REST API to Splunk HEC or Elastic Fleet ingestion endpoints."*

---

## 🔗 7. The Next Step in the Pipeline

With [`analytics/soc.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/analytics/soc.py), Q-Sentinel is now fully integrated with enterprise SOCs and global threat intelligence sharing platforms.

Now, what about human auditors, compliance officers, and legal teams who need an official signed certificate for a transaction?
👉 **Lesson 26:** [`analytics/reports.py`](file:///c:/Users/Rakshit%20Jain/Downloads/sih/analytics/reports.py)  
*(Official Audit Certificate Generator: Synthesizing cryptographically sealed JSON certificates and formatted plaintext audit reports with National Quantum Mission standard specification compliance).*
