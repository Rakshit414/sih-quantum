"""
Q-Sentinel: Distributed Eve Channel Relay (Adversarial Attack Injector)
Stage 22: Phase 43

Implements the active adversarial channel relay in the decoupled multi-process architecture:
- Intercepts packet stream flowing from Alice to Bob
- Applies configurable physical attack vectors via security.attacks:
  1. LEGITIMATE: Undisturbed channel transmission under baseline decoherence
  2. FORGERY: State fabrication / guessing without private key seed (~50% error rate)
  3. IMPERSONATION: Mismatched identity assertion under Mallory's basis
  4. REPLAY: Transmission of stale session timestamps / replayed nonces
  5. CHANNEL_NOISE: Controlled bit-flip / phase-flip decoherence
- Forwards disturbed trials to Bob's verifier sink over HTTP

Strict Architectural Constraint:
This is the ONLY file in the transport/ package permitted to import security.attacks.
"""

from __future__ import annotations
import os
import sys
import json
import time
import random
import http.server
import threading
import urllib.request
import urllib.error
from typing import Dict, Any, Optional

# Sole permitted import of security.attacks in transport package
from security.attacks import AttackScenario, ThreatOrchestrator


class EveRelayHandler(http.server.BaseHTTPRequestHandler):
    """
    HTTP Request handler for Eve's active intercept-and-relay node.
    """
    relay_service: Optional['EveChannelRelay'] = None

    def log_message(self, format: str, *args: Any) -> None:
        # Suppress noisy standard HTTP access logs
        return

    def do_POST(self) -> None:
        if self.path == "/relay":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                packet = json.loads(body.decode("utf-8"))
                if self.relay_service is not None:
                    forwarded_res = self.relay_service.process_and_forward(packet)
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(forwarded_res).encode("utf-8"))
                else:
                    self.send_response(500)
                    self.end_headers()
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        elif self.path == "/scenario":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode("utf-8"))
                new_scenario = data.get("scenario", "LEGITIMATE")
                noise_level = float(data.get("noise_level", 0.0))
                if self.relay_service is not None:
                    self.relay_service.set_scenario(new_scenario, noise_level)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "SCENARIO_UPDATED", "scenario": new_scenario}).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self) -> None:
        if self.path == "/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            status = {
                "node": "eve_channel_relay",
                "active_scenario": self.relay_service.active_scenario.value if self.relay_service else "UNKNOWN",
                "noise_level": self.relay_service.noise_level if self.relay_service else 0.0,
                "packets_intercepted": self.relay_service.packets_intercepted if self.relay_service else 0
            }
            self.wfile.write(json.dumps(status).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()


class EveChannelRelay:
    """
    Adversarial channel relay orchestrating physical perturbations on transmitted packets.
    """

    def __init__(
        self,
        bob_url: str = "http://127.0.0.1:8002/trial",
        initial_scenario: str = "LEGITIMATE",
        noise_level: float = 0.0,
        port: int = 8001
    ):
        self.bob_url = bob_url
        self.port = port
        self.noise_level = float(noise_level)
        self.packets_intercepted = 0
        self.set_scenario(initial_scenario, noise_level)
        self.server: Optional[http.server.HTTPServer] = None
        self.server_thread: Optional[threading.Thread] = None

    def set_scenario(self, scenario_str: str, noise_level: float = 0.0) -> None:
        scenario_upper = scenario_str.upper()
        if scenario_upper == "FORGERY":
            self.active_scenario = AttackScenario.FORGERY
        elif scenario_upper == "IMPERSONATION":
            self.active_scenario = AttackScenario.IMPERSONATION
        elif scenario_upper == "REPLAY":
            self.active_scenario = AttackScenario.REPLAY
        elif scenario_upper == "CHANNEL_NOISE":
            self.active_scenario = AttackScenario.CHANNEL_NOISE
            self.noise_level = max(0.01, noise_level if noise_level > 0 else 0.25)
        else:
            self.active_scenario = AttackScenario.LEGITIMATE
            self.noise_level = noise_level

    def process_and_forward(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        """
        Intercepts incoming packet from Alice, injects attack disturbance according
        to active scenario, and forwards trial to Bob.
        """
        self.packets_intercepted += 1
        disturbed_packet = dict(packet)

        # Baseline channel decoherence probability (p0 = 0.03)
        baseline_err = random.random() < 0.03
        trial_err = 1 if baseline_err else 0

        if self.active_scenario == AttackScenario.FORGERY:
            # Adversary guesses random eigenstate: ~50% projective error
            is_err = random.random() < 0.50
            trial_err = 1 if is_err else 0
            disturbed_packet["adversarial_tag"] = "FORGERY_INJECTED"

        elif self.active_scenario == AttackScenario.IMPERSONATION:
            # Impersonator Mallory uses mismatched basis: ~50% projective error
            disturbed_packet["signer_id"] = "Mallory"
            is_err = random.random() < 0.50
            trial_err = 1 if is_err else 0
            disturbed_packet["adversarial_tag"] = "IMPERSONATION_MALLORY"

        elif self.active_scenario == AttackScenario.REPLAY:
            # Stale timestamp (> 120 seconds old)
            disturbed_packet["timestamp"] = time.time() - 3600.0
            disturbed_packet["nonce"] = "STALE_REPLAYED_NONCE_2026"
            disturbed_packet["adversarial_tag"] = "REPLAY_STALE_SESSION"

        elif self.active_scenario == AttackScenario.CHANNEL_NOISE:
            # Bit-flip channel with parameter noise_level
            p_flip = self.noise_level if self.noise_level > 0 else 0.25
            is_err = (random.random() < p_flip) or baseline_err
            trial_err = 1 if is_err else 0
            disturbed_packet["adversarial_tag"] = f"CHANNEL_NOISE_EPS_{self.noise_level:.2f}"

        disturbed_packet["trial_outcome"] = trial_err
        disturbed_packet["channel_scenario"] = self.active_scenario.value

        # Forward to Bob
        forward_res = self._forward_to_bob(disturbed_packet)
        return {
            "relay_status": "FORWARDED",
            "active_scenario": self.active_scenario.value,
            "bob_response": forward_res
        }

    def _forward_to_bob(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        data = json.dumps(packet).encode("utf-8")
        req = urllib.request.Request(
            self.bob_url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=5.0) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            return {"error": str(e)}

    def start_server(self, host: str = "127.0.0.1") -> None:
        EveRelayHandler.relay_service = self
        self.server = http.server.HTTPServer((host, self.port), EveRelayHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()

    def stop_server(self) -> None:
        if self.server:
            self.server.shutdown()
            self.server.server_close()


if __name__ == "__main__":
    scenario = os.getenv("EVE_ATTACK_SCENARIO", "LEGITIMATE")
    relay = EveChannelRelay(initial_scenario=scenario, port=8001)
    relay.start_server()
    print(f"Eve Channel Relay running on port 8001 (Scenario: {scenario})...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        relay.stop_server()
