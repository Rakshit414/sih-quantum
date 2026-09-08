"""
Unit Tests for Phase 30: Multi-Hop Quantum Mesh Network & Entanglement Swapping
"""

import pytest
from quantum.mesh import EntanglementSwapper, QuantumMeshRouter, MeshRouteVerificationResult
from security.detector import ThreatCategory


class TestQuantumMeshNetwork:

    def test_entanglement_swapping_honest_fidelity(self):
        """Honest entanglement swapping between A and B via R1 should produce high fidelity."""
        swapped = EntanglementSwapper.execute_swapping(
            node_a="Alice",
            node_b="Bob",
            repeater_id="Repeater_R1",
            repeater_tampering=False,
            link_noise=0.01
        )
        assert swapped.is_compromised is False
        assert swapped.fidelity_with_phi_plus >= 0.85
        assert swapped.bell_measurement_bits in [(0, 0), (0, 1), (1, 0), (1, 1)]

    def test_entanglement_swapping_tampering_caught(self):
        """A rogue repeater tampering with BSM swapping bits drops fidelity to 50%."""
        swapped = EntanglementSwapper.execute_swapping(
            node_a="Alice",
            node_b="Bob",
            repeater_id="Rogue_R1",
            repeater_tampering=True
        )
        assert swapped.is_compromised is True
        assert swapped.fidelity_with_phi_plus <= 0.55

    def test_multi_hop_mesh_routing_honest_path(self):
        """3-hop path Alice -> R1 -> R2 -> Bob under honest conditions should pass."""
        router = QuantumMeshRouter()
        result = router.route_and_verify_mesh(
            source="Alice",
            destination="Bob",
            intermediate_repeaters=["Repeater_R1", "Repeater_R2"],
            compromised_node=None,
            base_link_noise=0.01,
            trials_per_token=40
        )
        assert len(result.path) == 4
        assert len(result.hop_telemetry) == 3
        assert result.rogue_node_identified is None
        assert result.assessment.verdict in [ThreatCategory.LEGITIMATE, ThreatCategory.SUSPICIOUS]
        assert result.end_to_end_fidelity >= 0.80

    def test_multi_hop_mesh_rogue_repeater_isolated(self):
        """If intermediate repeater R2 is rogue, hop telemetry must isolate R2 and trigger MALICIOUS."""
        router = QuantumMeshRouter()
        result = router.route_and_verify_mesh(
            source="Alice",
            destination="Bob",
            intermediate_repeaters=["Repeater_R1", "Repeater_R2"],
            compromised_node="Repeater_R2",
            trials_per_token=40
        )
        assert result.rogue_node_identified == "Repeater_R2"
        assert result.assessment.verdict == ThreatCategory.MALICIOUS
        assert any(h.is_compromised for h in result.hop_telemetry)
        assert "Mesh Routing Breach" in result.mesh_status_summary
