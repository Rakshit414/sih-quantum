"""
Q-Sentinel: Real-Time Network Threat Stream Engine
Stage 8: Phase 26
Simulates continuous multi-session QDS traffic over quantum teleportation links,
generating real-time transactions with stochastic adversarial attack injections.
"""

from __future__ import annotations
import time
import numpy as np
from dataclasses import dataclass
from typing import Iterator, Tuple, Optional, List

from security.signature import QDSKeyManager, QuantumDigitalSignature
from security.attacks import AttackScenario, ThreatOrchestrator
from security.detector import QStatDetector, ThreatAssessment, ThreatCategory
from security.freshness import FreshnessRegistry


@dataclass
class StreamEvent:
    event_id: int
    timestamp: float
    scenario: AttackScenario
    scenario_description: str
    message: str
    signer_id: str
    assessment: ThreatAssessment
    latency_ms: float


class QuantumTrafficGenerator:
    """
    Generates realistic transactional streams for testing real-time watchtower capabilities.
    """

    SAMPLE_MESSAGES = [
        "Financial Wire #10492 - $250,000",
        "Defense Grid Command - Access Authorization",
        "Inter-Bank Liquidity Settlement #9021",
        "Satellite Telemetry Uplink Packet #8812",
        "Public Key Infrastructure Renewal Token",
        "Core Network Routing Table Update #401",
        "Confidential Data Vault Clearance Request"
    ]

    def __init__(
        self,
        base_signer_id: str = "Alice",
        detector: Optional[QStatDetector] = None,
        random_seed: Optional[int] = None
    ):
        self.signer_id = base_signer_id
        self.mgr = QDSKeyManager(signer_id=base_signer_id, private_seed="stream_alice_secret_2026")
        self.detector = detector or QStatDetector(
            baseline_noise_p0=0.03,
            freshness_registry=FreshnessRegistry(max_time_window_seconds=60.0)
        )
        self.rng = np.random.default_rng(random_seed)
        self._prev_legit_sig: Optional[QuantumDigitalSignature] = None

    def generate_next_event(
        self,
        event_id: int,
        attack_probability: float = 0.35,
        trials_per_token: int = 50,
        ambient_noise: float = 0.03
    ) -> StreamEvent:
        """
        Generates a single transactional event in the stream, with probabilistic attack injection.
        """
        msg = str(self.rng.choice(self.SAMPLE_MESSAGES))
        legit_sig = self.mgr.generate_signature(msg, num_tokens=8)

        if self._prev_legit_sig is None:
            self._prev_legit_sig = legit_sig

        # Roll for scenario
        if self.rng.random() < attack_probability:
            # Inject an attack
            attack_choices = [
                AttackScenario.FORGERY,
                AttackScenario.IMPERSONATION,
                AttackScenario.REPLAY,
                AttackScenario.CHANNEL_NOISE
            ]
            scenario = self.rng.choice(attack_choices)
        else:
            scenario = AttackScenario.LEGITIMATE

        if scenario == AttackScenario.REPLAY:
            target_sig = self._prev_legit_sig
            # Register once in freshness to guarantee replay interception
            self.detector.freshness.seen_nonces.add((target_sig.signer_id, target_sig.nonce))
            self.detector.freshness.nonce_timestamps[(target_sig.signer_id, target_sig.nonce)] = target_sig.timestamp
            rx_sig, desc = ThreatOrchestrator.execute_scenario(scenario, target_sig)
        elif scenario == AttackScenario.CHANNEL_NOISE:
            noise_val = float(self.rng.uniform(0.15, 0.40))
            rx_sig, desc = ThreatOrchestrator.execute_scenario(
                scenario, legit_sig, channel_noise_level=noise_val, random_seed=int(self.rng.integers(1, 100000))
            )
            rx_sig.nonce = f"stream_nonce_{event_id}_{time.time_ns()}"
            rx_sig.timestamp = time.time()
        else:
            rx_sig, desc = ThreatOrchestrator.execute_scenario(
                scenario, legit_sig, random_seed=int(self.rng.integers(1, 100000))
            )
            if scenario != AttackScenario.REPLAY:
                rx_sig.nonce = f"stream_nonce_{event_id}_{time.time_ns()}"
                rx_sig.timestamp = time.time()

        if scenario == AttackScenario.LEGITIMATE:
            self._prev_legit_sig = rx_sig

        # Verify via Q-STAT
        t0 = time.perf_counter()
        assessment = self.detector.verify_signature_session(
            received_signature=rx_sig,
            expected_signature=legit_sig,
            trials_per_token=trials_per_token,
            ambient_noise=ambient_noise
        )
        latency_ms = (time.perf_counter() - t0) * 1000.0

        return StreamEvent(
            event_id=event_id,
            timestamp=time.time(),
            scenario=scenario,
            scenario_description=desc,
            message=msg,
            signer_id=rx_sig.signer_id,
            assessment=assessment,
            latency_ms=latency_ms
        )

    def generate_stream(
        self,
        count: int = 10,
        attack_probability: float = 0.35,
        trials_per_token: int = 50,
        ambient_noise: float = 0.03
    ) -> List[StreamEvent]:
        """
        Batch-generates a sequence of stream events.
        """
        events: List[StreamEvent] = []
        for i in range(1, count + 1):
            ev = self.generate_next_event(
                event_id=i,
                attack_probability=attack_probability,
                trials_per_token=trials_per_token,
                ambient_noise=ambient_noise
            )
            events.append(ev)
        return events
