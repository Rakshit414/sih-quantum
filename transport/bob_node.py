"""
Q-Sentinel: Distributed Bob Node (Verifier Sink & Sequential Watchtower)
Stage 22: Phase 43

Implements the physical verifier node in the decoupled multi-process architecture:
- Ingests incoming measurement trials sequentially from the quantum channel
- Evaluates real-time anomaly status via SequentialQStat (Beta-Binomial, CUSUM, SPRT)
- Exposes live telemetry, cumulative statistics, and current verdict to the SOC dashboard

STRICT ARCHITECTURAL INVARIANT:
Must contain ZERO import path — direct or transitive — to security.attacks or transport.eve_channel.
Verified continuously by AST import boundary testing (tests/test_import_boundary.py).
"""

from __future__ import annotations
import os
import sys
import json
import time
import http.server
import threading
from typing import Dict, Any, Optional, List
from dataclasses import asdict

from security.sequential import SequentialQStat, SequentialVerdict
from security.detector import ThreatCategory
from security.streaming import MultiArmFusion, FusedVerdict


class BobVerifierHandler(http.server.BaseHTTPRequestHandler):
    """
    HTTP Request handler for Bob's verifier sink node.
    """
    verifier_service: Optional['BobVerifierNode'] = None

    def log_message(self, format: str, *args: Any) -> None:
        return

    def do_POST(self) -> None:
        if self.path == "/trial":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                packet = json.loads(body.decode("utf-8"))
                if self.verifier_service is not None:
                    verdict_dict = self.verifier_service.ingest_trial(packet)
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(verdict_dict).encode("utf-8"))
                else:
                    self.send_response(500)
                    self.end_headers()
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        elif self.path == "/reset":
            if self.verifier_service is not None:
                self.verifier_service.reset()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "RESET_COMPLETED"}).encode("utf-8"))
            else:
                self.send_response(500)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self) -> None:
        if self.path == "/verdict":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            if self.verifier_service is not None:
                data = self.verifier_service.get_current_status()
            else:
                data = {"status": "UNINITIALIZED"}
            self.wfile.write(json.dumps(data).encode("utf-8"))
        elif self.path == "/history":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            if self.verifier_service is not None:
                data = {"history": self.verifier_service.trial_history[-100:]}
            else:
                data = {"history": []}
            self.wfile.write(json.dumps(data).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()


class BobVerifierNode:
    """
    Physical verifier node processing incoming measurement outcomes via SequentialQStat.
    Strictly isolated from attack simulator code.
    """

    def __init__(
        self,
        baseline_p0: float = 0.03,
        alt_p1: float = 0.20,
        port: int = 8002
    ):
        self.port = port
        self.detector = SequentialQStat(baseline_p0=baseline_p0, alt_p1=alt_p1)
        self.fusion = MultiArmFusion()
        self.latest_verdict: Optional[SequentialVerdict] = None
        self.trial_history: List[Dict[str, Any]] = []
        self.lock = threading.Lock()
        self.server: Optional[http.server.HTTPServer] = None
        self.server_thread: Optional[threading.Thread] = None

    def ingest_trial(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes an individual incoming packet, extracting the projective trial
        outcome and feeding it to SequentialQStat and concurrent watchtower arms.
        """
        trial_outcome = int(packet.get("trial_outcome", 0))
        packet_id = packet.get("packet_id", "UNKNOWN")

        with self.lock:
            verdict = self.detector.update(trial_outcome)
            self.latest_verdict = verdict

            # Update multi-arm watchtower fusion if telemetry samples present
            if "watchtower_samples" in packet and isinstance(packet["watchtower_samples"], dict):
                fused = self.fusion.update_all(packet["watchtower_samples"])
            else:
                fused = self.fusion.get_fused_verdict()

            summary = {
                "packet_id": packet_id,
                "trial_outcome": trial_outcome,
                "verdict": verdict.verdict.value,
                "fused_verdict": fused.verdict.value,
                "fired_arm": fused.fired_arm,
                "trigger": verdict.trigger,
                "n_trials": verdict.n_trials,
                "posterior_mean": verdict.posterior_mean,
                "cusum_stat": verdict.cusum_stat,
                "sprt_llr": verdict.sprt_llr,
                "decision_reached": verdict.decision_reached,
                "timestamp": time.time()
            }
            self.trial_history.append(summary)

        return summary

    def get_current_status(self) -> Dict[str, Any]:
        """Returns the current real-time sequential verdict and telemetry."""
        with self.lock:
            fused = self.fusion.get_fused_verdict()
            if self.latest_verdict is None:
                return {
                    "node": "bob_verifier_sink",
                    "status": "AWAITING_TRIALS",
                    "n_trials": 0,
                    "verdict": ThreatCategory.LEGITIMATE.value,
                    "fused_verdict": fused.verdict.value,
                    "fired_arm": fused.fired_arm,
                    "joint_alpha": fused.joint_alpha
                }
            return {
                "node": "bob_verifier_sink",
                "verdict": self.latest_verdict.verdict.value,
                "fused_verdict": fused.verdict.value,
                "fired_arm": fused.fired_arm,
                "joint_alpha": fused.joint_alpha,
                "effective_alpha_per_arm": fused.effective_alpha_per_arm,
                "trigger": self.latest_verdict.trigger,
                "n_trials": self.latest_verdict.n_trials,
                "posterior_mean": self.latest_verdict.posterior_mean,
                "posterior_ci": self.latest_verdict.posterior_ci,
                "cusum_stat": self.latest_verdict.cusum_stat,
                "sprt_llr": self.latest_verdict.sprt_llr,
                "decision_reached": self.latest_verdict.decision_reached,
                "evidence_ratio": self.latest_verdict.evidence_ratio
            }

    def reset(self) -> None:
        """Resets detector accumulators and trial history."""
        with self.lock:
            self.detector.reset()
            self.fusion.reset()
            self.latest_verdict = None
            self.trial_history.clear()

    def start_server(self, host: str = "127.0.0.1") -> None:
        BobVerifierHandler.verifier_service = self
        self.server = http.server.HTTPServer((host, self.port), BobVerifierHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()

    def stop_server(self) -> None:
        if self.server:
            self.server.shutdown()
            self.server.server_close()


if __name__ == "__main__":
    node = BobVerifierNode(port=8002)
    node.start_server()
    print("Bob Verifier Node running on port 8002...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        node.stop_server()
