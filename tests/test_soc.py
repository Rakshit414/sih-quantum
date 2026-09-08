"""
Test Suite for Stage 17 (Phase 38): Enterprise SOC SIEM Integration & Automated STIX 2.1 Threat Intelligence Bundle (Q-SOC)
Validates OASIS STIX 2.1 JSON CTI schema, Elastic Common Schema (ECS 8.x) compliance,
quantum threat taxonomy mapping, and automated SOC incident dispatch.
"""

import json
import pytest
from security.detector import ThreatAssessment, ThreatCategory
from security.mitigation import IncidentReport, MitigationAction
from analytics.soc import (
    STIXBundleGenerator,
    ECSEventFormatter,
    QSOCIntegrator,
    STIXBundleSummary,
    SIEMDispatchResult,
)


class TestQSOCIntegration:
    """
    Unit and conformance tests for Phase 38 Q-SOC integration.
    """

    def setup_method(self):
        self.assessment_malicious = ThreatAssessment(
            verdict=ThreatCategory.MALICIOUS,
            error_rate=0.18,
            z_score=6.52,
            p_value=1.2e-8,
            confidence=0.9999,
            baseline_noise_p0=0.03,
            total_trials=400,
            error_count=72,
            match_count=328,
            ci_lower=0.145,
            ci_upper=0.220,
            freshness_passed=True,
            freshness_reason="Fresh token registered.",
            diagnostic_text="Malicious disturbance detected: observed QBER 18.00% exceeds 3.00% baseline."
        )

        self.assessment_legitimate = ThreatAssessment(
            verdict=ThreatCategory.LEGITIMATE,
            error_rate=0.025,
            z_score=0.45,
            p_value=0.35,
            confidence=0.95,
            baseline_noise_p0=0.03,
            total_trials=400,
            error_count=10,
            match_count=390,
            ci_lower=0.012,
            ci_upper=0.045,
            freshness_passed=True,
            freshness_reason="Fresh token registered.",
            diagnostic_text="Signature verified under calibrated noise floor."
        )

    def test_stix_bundle_generation_conformance(self):
        """
        Tests that STIXBundleGenerator produces a valid OASIS STIX 2.1 compliant bundle
        with Identity, Attack-Pattern, Indicator, Observed-Data, Course-Of-Action, and Relationships.
        """
        summary = STIXBundleGenerator.generate_bundle(
            assessment=self.assessment_malicious,
            signer_id="Alice",
            scenario_name="FORGERY",
            message_payload="Authorize Fund Transfer #990"
        )

        assert summary.spec_version == "2.1"
        assert summary.bundle_id.startswith("bundle--")
        assert summary.object_count >= 7

        # Parse JSON and test STIX schema
        data = json.loads(summary.bundle_json)
        assert data["type"] == "bundle"
        assert data["id"] == summary.bundle_id
        assert len(data["objects"]) >= 7

        types = [obj["type"] for obj in data["objects"]]
        assert "identity" in types
        assert "attack-pattern" in types
        assert "indicator" in types
        assert "observed-data" in types
        assert "course-of-action" in types
        assert "relationship" in types

    def test_ecs_event_formatter_schema(self):
        """
        Tests that ECSEventFormatter formats valid Elastic Common Schema (ECS 8.x) JSON documents.
        """
        ecs_doc = ECSEventFormatter.format_ecs_event(
            assessment=self.assessment_malicious,
            signer_id="Mallory",
            scenario_name="IMPERSONATION",
            message_payload="Unauthorized Wire Transfer",
            stix_bundle_id="bundle--test-uuid"
        )

        assert ecs_doc["ecs"]["version"] == "8.11.0"
        assert "network" in ecs_doc["event"]["category"]
        assert "intrusion_detection" in ecs_doc["event"]["category"]
        assert ecs_doc["event"]["severity"] == 7  # Malicious = High severity
        assert ecs_doc["event"]["action"] == "quantum-threat-blocked"
        assert ecs_doc["quantum"]["verdict"] == "MALICIOUS"
        assert ecs_doc["quantum"]["standardized_z_score"] == 6.52

        # Test Legitimate Severity Mapping
        ecs_legit = ECSEventFormatter.format_ecs_event(
            assessment=self.assessment_legitimate,
            signer_id="Alice",
            scenario_name="LEGITIMATE",
            message_payload="Standard Message"
        )
        assert ecs_legit["event"]["severity"] == 1
        assert ecs_legit["event"]["outcome"] == "success"

    def test_qsoc_integrator_pipeline(self):
        """
        Tests the end-to-end QSOCIntegrator pipeline producing both CTI bundle and SIEM dispatch.
        """
        integrator = QSOCIntegrator(enterprise_soc_endpoint="https://soc.test.gov.in")
        stix_summary, dispatch_result = integrator.process_incident_and_export(
            assessment=self.assessment_malicious,
            signer_id="Alice",
            scenario_name="RAMAN_CROSS_TALK_JAMMING",
            message_payload="WDM Telecom Stream Payload"
        )

        assert dispatch_result.dispatch_status == "DELIVERED (HTTP 200 OK)"
        assert dispatch_result.severity_code == 7
        assert dispatch_result.threat_classification == "MALICIOUS"
        assert dispatch_result.stix_bundle_id == stix_summary.bundle_id
        assert "Elastic SIEM" in dispatch_result.target_platform

        # Parse raw payload
        raw = json.loads(dispatch_result.raw_payload_json)
        assert raw["quantum"]["verdict"] == "MALICIOUS"

    def test_stix_attack_pattern_taxonomy_mapping(self):
        """
        Tests that different quantum threat scenarios map correctly to their CAPEC / ATT&CK taxonomy entries.
        """
        for scn in ["FORGERY", "IMPERSONATION", "REPLAY", "DETECTOR_BLINDING", "RAMAN_CROSS_TALK_JAMMING"]:
            bundle = STIXBundleGenerator.generate_bundle(
                assessment=self.assessment_malicious,
                signer_id="TestNode",
                scenario_name=scn,
                message_payload="Payload"
            )
            data = json.loads(bundle.bundle_json)
            ap_obj = next(o for o in data["objects"] if o["type"] == "attack-pattern")
            assert ap_obj["name"] != ""
            assert len(ap_obj["external_references"]) > 0

    def test_incident_mitigation_actions_in_stix_course_of_action(self):
        """
        Verifies that automated containment actions from an IncidentReport are mirrored in the STIX Course-Of-Action SDO.
        """
        report = IncidentReport(
            incident_id="INC-2026-TEST-01",
            timestamp="2026-09-07T12:00:00Z",
            verdict=ThreatCategory.MALICIOUS,
            threat_category_name="MALICIOUS",
            signer_id="Mallory",
            observed_z_score=5.8,
            error_rate=0.15,
            mitigation_actions=[
                MitigationAction(action_id="act-01", action_type="SIGNER_QUARANTINE", target="Mallory", status="EXECUTED", details="Signer quarantined."),
                MitigationAction(action_id="act-02", action_type="NONCE_REVOCATION", target="nonce_9823", status="EXECUTED", details="Revoked nonce.")
            ],
            cef_log_entry="CEF:0|Q-Sentinel|QDS|1.0|MALICIOUS|Threat Blocked|7|"
        )

        bundle = STIXBundleGenerator.generate_bundle(
            assessment=self.assessment_malicious,
            signer_id="Mallory",
            scenario_name="FORGERY",
            message_payload="Attack Payload",
            incident_report=report
        )

        data = json.loads(bundle.bundle_json)
        coa_obj = next(o for o in data["objects"] if o["type"] == "course-of-action")
        assert "SIGNER_QUARANTINE" in coa_obj["action"]
        assert "NONCE_REVOCATION" in coa_obj["action"]