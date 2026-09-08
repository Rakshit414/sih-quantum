"""
Q-Sentinel: Enterprise SOC SIEM Integration & Automated STIX 2.1 Threat Intelligence Bundle
Stage 17: Phase 38 (Q-SOC)

Integrates Q-Sentinel with enterprise Security Operations Centers (SOC) and SIEM platforms
(Splunk, Microsoft Sentinel, IBM QRadar, Elastic SIEM).

Implements:
1. OASIS STIX 2.1 (Structured Threat Information Expression) compliant Cyber Threat Intelligence (CTI) Bundles:
   - SDO: Identity (Q-Sentinel Quantum SOC Sensor)
   - SDO: Attack-Pattern (Mapped to Quantum Adversarial ATT&CK / CAPEC taxonomy)
   - SDO: Indicator (Formal STIX Pattern with quantum z-scores, QBER, optical power thresholds)
   - SDO: Observed-Data (Empirical measurement parameters and trial timestamps)
   - SDO: Course-Of-Action (Automated quantum containment and quarantine procedures)
   - SRO: Relationship (indicates, mitigates, targets)
2. Elastic Common Schema (ECS 8.x) & Splunk HTTP Event Collector (HEC) Event Formatter
3. Automated CTI Bundle Dispatch and SIEM Ingestion Pipeline
"""

from __future__ import annotations
import uuid
import json
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

from security.detector import ThreatAssessment, ThreatCategory
from security.mitigation import IncidentReport


@dataclass
class STIXBundleSummary:
    """
    Metadata summary of a generated STIX 2.1 Threat Intelligence Bundle.
    """
    bundle_id: str
    spec_version: str = "2.1"
    created: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    object_count: int = 0
    attack_pattern_id: str = ""
    attack_pattern_name: str = ""
    indicator_id: str = ""
    course_of_action_id: str = ""
    bundle_json: str = ""


@dataclass
class SIEMDispatchResult:
    """
    Telemetry dispatch record for enterprise SIEM ingestion.
    """
    dispatch_id: str
    target_platform: str  # e.g. "Elastic SIEM (ECS 8.x)", "Splunk HEC", "IBM QRadar CEF"
    event_timestamp: str
    severity_code: int    # 1=Low, 3=Medium, 7=High, 10=Critical
    threat_classification: str
    stix_bundle_id: str
    raw_payload_json: str
    dispatch_status: str


class STIXBundleGenerator:
    """
    Generates OASIS STIX 2.1 compliant Cyber Threat Intelligence JSON bundles
    for detected quantum eavesdropping, hardware blinding, and replay attacks.
    """

    # Quantum Attack Taxonomy mapping to MITRE ATT&CK / CAPEC equivalents
    QUANTUM_ATTACK_PATTERNS: Dict[str, Dict[str, Any]] = {
        "FORGERY": {
            "name": "Quantum Digital Signature Forgery",
            "description": "Adversary generates fabricated quantum Pauli eigenstates to forge authentication on teleported signature tokens.",
            "external_id": "CAPEC-QDS-FORGERY",
            "kill_chain_phase": "credential-forgery"
        },
        "IMPERSONATION": {
            "name": "Signer Key Mismatch & Authority Impersonation",
            "description": "Adversary impersonates legitimate signing authority by submitting quantum tokens encoded with mismatched master keys.",
            "external_id": "CAPEC-QDS-IMPERSONATION",
            "kill_chain_phase": "identity-theft"
        },
        "REPLAY": {
            "name": "Quantum Signature Token Replay Attack",
            "description": "Adversary captures and retransmits stale teleportation tokens past the sliding freshness acceptance window.",
            "external_id": "CAPEC-QDS-REPLAY",
            "kill_chain_phase": "replay"
        },
        "CHANNEL_NOISE": {
            "name": "Adversarial Quantum Channel Manipulation",
            "description": "Adversary introduces bit-flip, phase-flip, or depolarization noise into the quantum teleportation channel.",
            "external_id": "CAPEC-QDS-NOISE",
            "kill_chain_phase": "tampering"
        },
        "DETECTOR_BLINDING": {
            "name": "Continuous-Wave Single-Photon Detector Blinding",
            "description": "Adversary injects high-power continuous-wave laser light to drive APDs from Geiger mode into linear mode (Lydersen-Makarov attack).",
            "external_id": "CAPEC-QDS-BLINDING",
            "kill_chain_phase": "hardware-tampering"
        },
        "PHOTON_NUMBER_SPLITTING": {
            "name": "Decoy-State Photon Number Splitting (PNS)",
            "description": "Adversary selectively splits multi-photon pulses on weak coherent channels to intercept key bits without inducing QBER.",
            "external_id": "CAPEC-QDS-PNS",
            "kill_chain_phase": "eavesdropping"
        },
        "RAMAN_CROSS_TALK_JAMMING": {
            "name": "WDM Co-Propagation Raman Scattering Jamming",
            "description": "Adversary launches high-power out-of-band telecom pump pulses into adjacent WDM channels to flood quantum detectors with spontaneous Raman noise.",
            "external_id": "CAPEC-QDS-WDM-JAMMING",
            "kill_chain_phase": "denial-of-service"
        },
        "UNTRUSTED_RELAY_TAMPERING": {
            "name": "Measurement-Device-Independent Untrusted Relay Tampering",
            "description": "Untrusted central relay fabricates coincidence announcements or manipulates Bell-state measurement projections.",
            "external_id": "CAPEC-QDS-MDI-TAMPER",
            "kill_chain_phase": "relay-hijacking"
        },
        "CHSH_BELL_VIOLATION_COLLAPSE": {
            "name": "Device-Independent Entanglement Verification Failure",
            "description": "Entangled pairs fail Clauser-Horne-Shimony-Holt (CHSH) Bell inequality bound (S <= 2.0), indicating classical separable state spoofing.",
            "external_id": "CAPEC-QDS-CHSH-SPOOF",
            "kill_chain_phase": "entanglement-spoofing"
        }
    }

    @classmethod
    def generate_bundle(
        cls,
        assessment: ThreatAssessment,
        signer_id: str,
        scenario_name: str,
        message_payload: str,
        incident_report: Optional[IncidentReport] = None
    ) -> STIXBundleSummary:
        """
        Creates a valid OASIS STIX 2.1 JSON Bundle containing all SDOs and SROs.
        """
        now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-4] + "Z"
        bundle_uuid = str(uuid.uuid4())
        bundle_id = f"bundle--{bundle_uuid}"

        # 1. Identity SDO: Sensor Identity
        identity_id = f"identity--{uuid.uuid4()}"
        identity_sdo = {
            "type": "identity",
            "spec_version": "2.1",
            "id": identity_id,
            "created": now_iso,
            "modified": now_iso,
            "name": "Q-Sentinel Quantum Threat Watchtower Sensor",
            "description": "Autonomous quantum cyber-threat detection and teleportation-based QDS monitoring system.",
            "identity_class": "system",
            "sectors": ["defense", "government", "financial-services"]
        }

        # 2. Attack-Pattern SDO
        # Map scenario name to taxonomy key
        tax_key = "FORGERY"
        for k in cls.QUANTUM_ATTACK_PATTERNS.keys():
            if k in scenario_name.upper():
                tax_key = k
                break
        attack_info = cls.QUANTUM_ATTACK_PATTERNS.get(tax_key, cls.QUANTUM_ATTACK_PATTERNS["FORGERY"])

        attack_pattern_id = f"attack-pattern--{uuid.uuid4()}"
        attack_pattern_sdo = {
            "type": "attack-pattern",
            "spec_version": "2.1",
            "id": attack_pattern_id,
            "created": now_iso,
            "modified": now_iso,
            "name": attack_info["name"],
            "description": attack_info["description"],
            "external_references": [
                {
                    "source_name": "capec",
                    "external_id": attack_info["external_id"]
                }
            ],
            "kill_chain_phases": [
                {
                    "kill_chain_name": "quantum-threat-matrix",
                    "phase_name": attack_info["kill_chain_phase"]
                }
            ]
        }

        # 3. Indicator SDO: Formal STIX Pattern
        indicator_id = f"indicator--{uuid.uuid4()}"
        stix_pattern = (
            f"[quantum-threat-telemetry:z_score >= {assessment.z_score:.2f} AND "
            f"quantum-threat-telemetry:observed_error_rate >= {assessment.error_rate:.4f}]"
        )
        indicator_sdo = {
            "type": "indicator",
            "spec_version": "2.1",
            "id": indicator_id,
            "created": now_iso,
            "modified": now_iso,
            "name": f"Quantum Anomaly Pattern - {assessment.verdict.value}",
            "description": (
                f"Empirical hypothesis test rejection: observed error rate {assessment.error_rate*100:.2f}% "
                f"exceeds calibrated baseline noise (z={assessment.z_score:+.2f} sigma, p={assessment.p_value:.4e})."
            ),
            "indicator_types": ["anomalous-activity", "malicious-activity" if assessment.verdict == ThreatCategory.MALICIOUS else "suspicious-activity"],
            "pattern": stix_pattern,
            "pattern_type": "stix",
            "valid_from": now_iso
        }

        # 4. Observed-Data SDO: Empirical Projective Telemetry
        observed_data_id = f"observed-data--{uuid.uuid4()}"
        observed_data_sdo = {
            "type": "observed-data",
            "spec_version": "2.1",
            "id": observed_data_id,
            "created": now_iso,
            "modified": now_iso,
            "first_observed": now_iso,
            "last_observed": now_iso,
            "number_observed": assessment.total_trials,
            "objects": {
                "0": {
                    "type": "x-quantum-telemetry",
                    "signer_identity": signer_id,
                    "evaluated_payload": message_payload,
                    "verdict": assessment.verdict.value,
                    "standardized_z_score": round(assessment.z_score, 4),
                    "exact_p_value": round(assessment.p_value, 6),
                    "confidence_score": round(assessment.confidence, 4),
                    "observed_error_rate": round(assessment.error_rate, 4),
                    "baseline_noise_p0": round(assessment.baseline_noise_p0, 4),
                    "total_measurement_trials": assessment.total_trials,
                    "freshness_passed": assessment.freshness_passed
                }
            }
        }

        # 5. Course-Of-Action SDO: Mitigation Actions
        coa_id = f"course-of-action--{uuid.uuid4()}"
        coa_actions = [
            "Revoke compromised signature token nonces in FreshnessRegistry",
            "Purge shared Bell entanglement memory buffers across affected nodes",
            "Apply security quarantine to targeted signer identity",
            "Trigger automated dynamic noise re-calibration (Q-CALIBRATE)"
        ]
        if incident_report and incident_report.mitigation_actions:
            coa_actions = [f"[{a.action_type}] {a.details}" for a in incident_report.mitigation_actions]

        coa_sdo = {
            "type": "course-of-action",
            "spec_version": "2.1",
            "id": coa_id,
            "created": now_iso,
            "modified": now_iso,
            "name": f"Automated Quantum Incident Containment - {assessment.verdict.value}",
            "description": "Autonomous containment actions executed by Q-MITIGATE upon hypothesis test threshold breach.",
            "action": "\n".join(coa_actions)
        }

        # 6. Relationship SROs: Linking STIX Objects
        rel1_id = f"relationship--{uuid.uuid4()}"
        rel1_sro = {
            "type": "relationship",
            "spec_version": "2.1",
            "id": rel1_id,
            "created": now_iso,
            "modified": now_iso,
            "relationship_type": "indicates",
            "source_ref": indicator_id,
            "target_ref": attack_pattern_id
        }

        rel2_id = f"relationship--{uuid.uuid4()}"
        rel2_sro = {
            "type": "relationship",
            "spec_version": "2.1",
            "id": rel2_id,
            "created": now_iso,
            "modified": now_iso,
            "relationship_type": "mitigates",
            "source_ref": coa_id,
            "target_ref": attack_pattern_id
        }

        # Assemble STIX 2.1 Bundle
        bundle_dict = {
            "type": "bundle",
            "id": bundle_id,
            "objects": [
                identity_sdo,
                attack_pattern_sdo,
                indicator_sdo,
                observed_data_sdo,
                coa_sdo,
                rel1_sro,
                rel2_sro
            ]
        }

        bundle_json_str = json.dumps(bundle_dict, indent=2)

        return STIXBundleSummary(
            bundle_id=bundle_id,
            spec_version="2.1",
            created=now_iso,
            object_count=len(bundle_dict["objects"]),
            attack_pattern_id=attack_pattern_id,
            attack_pattern_name=attack_info["name"],
            indicator_id=indicator_id,
            course_of_action_id=coa_id,
            bundle_json=bundle_json_str
        )


class ECSEventFormatter:
    """
    Formats quantum threat events into Elastic Common Schema (ECS 8.x) JSON
    for direct ingestion into Elastic SIEM, Logstash, or Splunk HTTP Event Collector.
    """

    @classmethod
    def format_ecs_event(
        cls,
        assessment: ThreatAssessment,
        signer_id: str,
        scenario_name: str,
        message_payload: str,
        stix_bundle_id: str = ""
    ) -> Dict[str, Any]:
        """
        Creates an Elastic Common Schema (ECS 8.x) compliant event document.
        """
        now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-4] + "Z"
        
        # Determine ECS severity code
        if assessment.verdict == ThreatCategory.MALICIOUS:
            severity = 7
            event_outcome = "failure"
            event_action = "quantum-threat-blocked"
        elif assessment.verdict == ThreatCategory.SUSPICIOUS:
            severity = 3
            event_outcome = "unknown"
            event_action = "quantum-anomaly-flagged"
        else:
            severity = 1
            event_outcome = "success"
            event_action = "quantum-signature-verified"

        ecs_doc: Dict[str, Any] = {
            "@timestamp": now_iso,
            "ecs": {
                "version": "8.11.0"
            },
            "event": {
                "id": str(uuid.uuid4()),
                "category": ["network", "intrusion_detection"],
                "type": ["indicator", "compromise" if assessment.verdict == ThreatCategory.MALICIOUS else "info"],
                "kind": "alert" if assessment.verdict != ThreatCategory.LEGITIMATE else "event",
                "action": event_action,
                "outcome": event_outcome,
                "severity": severity,
                "module": "qsentinel_qds"
            },
            "host": {
                "name": "quantum-node-01.gov.in",
                "architecture": "quantum-hybrid-soc"
            },
            "user": {
                "id": signer_id,
                "name": signer_id,
                "roles": ["qds_signer"]
            },
            "message": f"Q-Sentinel Alert: {assessment.verdict.value} on signer '{signer_id}' - {assessment.diagnostic_text}",
            "quantum": {
                "protocol": "Teleportation-Based QDS",
                "verdict": assessment.verdict.value,
                "standardized_z_score": float(round(assessment.z_score, 4)),
                "exact_p_value": float(round(assessment.p_value, 6)),
                "observed_error_rate": float(round(assessment.error_rate, 4)),
                "baseline_noise_p0": float(round(assessment.baseline_noise_p0, 4)),
                "confidence_score": float(round(assessment.confidence, 4)),
                "measurement_trials": int(assessment.total_trials),
                "stix_bundle_ref": stix_bundle_id
            },
            "threat": {
                "framework": "MITRE ATT&CK / CAPEC Quantum Taxonomy",
                "technique": {
                    "id": "CAPEC-QDS-01",
                    "name": scenario_name
                },
                "indicator": {
                    "type": "statistical-anomaly",
                    "description": assessment.diagnostic_text
                }
            }
        }
        return ecs_doc


class QSOCIntegrator:
    """
    High-level Enterprise SOC SIEM Integration controller.
    Dispatches automated CTI bundles and ECS events to security operations centers.
    """

    def __init__(self, enterprise_soc_endpoint: str = "https://soc.qsentinel.gov.in/api/v1/telemetry"):
        self.endpoint: str = enterprise_soc_endpoint

    def process_incident_and_export(
        self,
        assessment: ThreatAssessment,
        signer_id: str,
        scenario_name: str,
        message_payload: str,
        incident_report: Optional[IncidentReport] = None
    ) -> Tuple[STIXBundleSummary, SIEMDispatchResult]:
        """
        Processes a verification run, generates full STIX 2.1 CTI bundle and ECS event,
        and simulates enterprise SIEM ingestion.
        """
        # 1. Generate STIX 2.1 CTI Bundle
        stix_summary = STIXBundleGenerator.generate_bundle(
            assessment=assessment,
            signer_id=signer_id,
            scenario_name=scenario_name,
            message_payload=message_payload,
            incident_report=incident_report
        )

        # 2. Format Elastic Common Schema (ECS 8.x) Event Document
        ecs_event = ECSEventFormatter.format_ecs_event(
            assessment=assessment,
            signer_id=signer_id,
            scenario_name=scenario_name,
            message_payload=message_payload,
            stix_bundle_id=stix_summary.bundle_id
        )

        # 3. Simulate Enterprise SIEM Dispatch
        dispatch_id = f"disp-{uuid.uuid4().hex[:10]}"
        severity_code = ecs_event["event"]["severity"]
        dispatch_status = "DELIVERED (HTTP 200 OK)"

        dispatch_result = SIEMDispatchResult(
            dispatch_id=dispatch_id,
            target_platform="Elastic SIEM / Splunk HEC (ECS 8.x)",
            event_timestamp=ecs_event["@timestamp"],
            severity_code=severity_code,
            threat_classification=assessment.verdict.value,
            stix_bundle_id=stix_summary.bundle_id,
            raw_payload_json=json.dumps(ecs_event, indent=2),
            dispatch_status=dispatch_status
        )

        return stix_summary, dispatch_result