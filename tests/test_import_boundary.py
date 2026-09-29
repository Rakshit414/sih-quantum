"""
Test Suite for Stage 22 (Phase 43): Import Boundary Verification & Multi-Process Transport

Enforces the non-negotiable architectural invariant:
Bob's verifier process (transport/bob_node.py) and its entire transitive import graph
must have ZERO dependency on adversarial attack injection code (security.attacks or transport.eve_channel).
"""

import ast
import os
import sys
import time
from pathlib import Path
import pytest

from transport.bob_node import BobVerifierNode
from transport.eve_channel import EveChannelRelay
from transport.alice_node import AliceSignerNode
from security.detector import ThreatCategory


def get_all_imported_modules(file_path: Path, workspace_root: Path, visited: set = None) -> set:
    """
    Recursively parses AST of file_path and all local workspace modules it imports,
    building the complete transitive import graph.
    """
    if visited is None:
        visited = set()

    resolved_path = file_path.resolve()
    if resolved_path in visited:
        return set()
    visited.add(resolved_path)

    imported_names = set()
    try:
        content = resolved_path.read_text(encoding="utf-8")
        tree = ast.parse(content, filename=str(resolved_path))
    except Exception:
        return imported_names

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_names.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported_names.add(node.module)

    # Recursively check internal project modules
    for mod_name in list(imported_names):
        # Convert module to relative file path, e.g. security.sequential -> security/sequential.py
        parts = mod_name.split(".")
        potential_py = workspace_root / ("/".join(parts) + ".py")
        potential_init = workspace_root / ("/".join(parts) + "/__init__.py")

        if potential_py.exists():
            imported_names |= get_all_imported_modules(potential_py, workspace_root, visited)
        elif potential_init.exists():
            imported_names |= get_all_imported_modules(potential_init, workspace_root, visited)

    return imported_names


class TestImportBoundaryAndTransport:
    """Rigorous AST import isolation and multi-node transport regression tests."""

    def test_bob_node_strict_import_boundary(self):
        """
        Validates that transport/bob_node.py contains ZERO direct or transitive imports
        of security.attacks or transport.eve_channel.
        """
        workspace_root = Path(__file__).resolve().parent.parent
        bob_node_path = workspace_root / "transport" / "bob_node.py"
        assert bob_node_path.exists(), "transport/bob_node.py is missing"

        full_import_graph = get_all_imported_modules(bob_node_path, workspace_root)

        forbidden_prefixes = (
            "security.attacks",
            "transport.eve_channel",
            "eve_channel"
        )

        violations = [
            mod for mod in full_import_graph
            if any(mod == f or mod.startswith(f + ".") for f in forbidden_prefixes)
        ]

        assert len(violations) == 0, (
            f"CRITICAL ARCHITECTURAL LEAK: Bob's import graph contains forbidden modules: {violations}"
        )

    def test_multi_node_transport_session(self):
        """
        Tests live inter-process communication:
        Alice transmits a session through Eve relay to Bob verifier sink.
        """
        bob = BobVerifierNode(port=8092)
        bob.start_server()

        eve = EveChannelRelay(bob_url="http://127.0.0.1:8092/trial", initial_scenario="LEGITIMATE", port=8091)
        eve.start_server()

        try:
            # Let servers initialize
            time.sleep(0.1)

            alice = AliceSignerNode(signer_id="Alice")
            res = alice.transmit_session(
                message="PAYMENT_AUTHORIZED_TX_99",
                relay_url="http://127.0.0.1:8091/relay",
                trials_per_token=5,
                inter_packet_delay_sec=0.0
            )

            assert res["delivered"] > 0
            assert res["failed"] == 0

            # Bob must have ingested trials
            bob_status = bob.get_current_status()
            assert bob_status["n_trials"] > 0
            assert bob_status["verdict"] == ThreatCategory.LEGITIMATE.value

        finally:
            eve.stop_server()
            bob.stop_server()

    def test_eve_forgery_injection_triggers_bob_alert(self):
        """
        Tests that when Eve switches to FORGERY, Bob's SequentialQStat
        detects the attack and updates verdict to MALICIOUS.
        """
        bob = BobVerifierNode(port=8094)
        bob.start_server()

        eve = EveChannelRelay(bob_url="http://127.0.0.1:8094/trial", initial_scenario="FORGERY", port=8093)
        eve.start_server()

        try:
            time.sleep(0.1)
            alice = AliceSignerNode(signer_id="Alice")
            alice.transmit_session(
                message="TRANSFER_FUNDS_TO_VAULT",
                relay_url="http://127.0.0.1:8093/relay",
                trials_per_token=25,
                inter_packet_delay_sec=0.0
            )

            bob_status = bob.get_current_status()
            assert bob_status["n_trials"] > 0
            # Forgery attack induces ~50% errors, triggering CUSUM/SPRT
            assert bob_status["verdict"] == ThreatCategory.MALICIOUS.value

        finally:
            eve.stop_server()
            bob.stop_server()
