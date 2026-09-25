"""
Q-Sentinel: Session Mode Selector & MDI Untrusted Relay Integration
Stage 25: Phase 46

Provides selectable operating architectures for QDS verification sessions:
1. TRUSTED_DETECTOR:
   Standard teleportation-based QDS where Verifier (Bob) houses calibrated single-photon
   detectors. Delivers maximal single-photon throughput, but requires trusting Bob's
   detector hardware against physical side-channel blinding/dead-time attacks.

2. MDI_RELAY (Measurement-Device-Independent):
   Alice and Bob simultaneously transmit quantum states to an untrusted central relay
   (Charles / Eve) who performs two-photon Bell-State Measurements (BSM).
   100% immune to all detector side-channel hacking (blinding, spatial shift, time-jitter),
   even if the relay is malicious. Operates at lower photon coincidence yield (Hong-Ou-Mandel
   two-photon interference constraint).

Adapts MDI Hong-Ou-Mandel coincidence error streams into Bernoulli trials for
SequentialQStat (CUSUM / SPRT), enabling rapid early stopping in MDI mode.

References:
- Lo, H.-K., Curty, M., & Qi, B. (2012). Measurement-device-independent quantum
  key distribution. Physical Review Letters, 108(13), 130503.
- Puthoor, I. V., et al. (2016). Measurement-device-independent quantum digital
  signatures. Physical Review A, 94(2), 022328.
- Yin, H.-L., et al. (2017). Experimental measurement-device-independent quantum
  digital signatures over a 200 km fiber. Physical Review A, 95(4), 042338.
"""

from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple

import numpy as np
from security.detector import ThreatCategory, ThreatAssessment, QStatDetector
from security.sequential import SequentialQStat, SequentialVerdict
from security.mdi import MDIRelayWatcher, MDIQuantumRelay, MDIEvent, MDIAnalysisResult


class SessionMode(Enum):
    """
    Physical architecture configuration for signature verification sessions.
    """
    TRUSTED_DETECTOR = "TRUSTED_DETECTOR"
    MDI_RELAY = "MDI_RELAY"


@dataclass
class SessionModeResult:
    """
    Unified verification result encapsulating physical mode, detector immunity,
    and sequential threat assessment.
    """
    mode: SessionMode
    verdict: ThreatCategory
    detector_immune: bool
    trials_evaluated: int
    sequential_verdict: SequentialVerdict
    mdi_analysis: Optional[MDIAnalysisResult]
    tradeoff_explanation: str


class SessionModeCoordinator:
    """
    Orchestrates verification across either TRUSTED_DETECTOR or MDI_RELAY architectures.
    Bridges MDI two-photon interference error metrics into SequentialQStat.
    """

    def __init__(
        self,
        baseline_p0: float = 0.03,
        alt_p1: float = 0.20,
        min_hom_visibility: float = 0.70,
        max_z_error_rate: float = 0.080
    ):
        self.baseline_p0 = float(baseline_p0)
        self.alt_p1 = float(alt_p1)
        self.mdi_watcher = MDIRelayWatcher(
            min_hom_visibility=min_hom_visibility,
            max_z_error_rate=max_z_error_rate
        )

    def generate_mdi_events(
        self,
        scenario: str = "Honest Untrusted Relay",
        num_trials: int = 500
    ) -> List[MDIEvent]:
        """
        Generates simulated MDI events across honest, compromised, or spoofed relays.
        """
        trials = max(50, num_trials)
        events: List[MDIEvent] = []
        is_compromised = "Compromised" in scenario or "Tampering" in scenario
        spectral_skew = 0.70 if ("Distinguishable" in scenario or "Interference Collapse" in scenario) else 0.0

        for i in range(1, trials + 1):
            a_basis = 'Z' if np.random.rand() < 0.50 else 'X'
            b_basis = 'Z' if np.random.rand() < 0.50 else 'X'
            a_bit = int(np.random.randint(0, 2))
            b_bit = int(np.random.randint(0, 2))

            coinc = self.mdi_watcher.relay_engine.simulate_bsm_trial(
                alice_bit=a_bit,
                alice_basis=a_basis,
                bob_bit=b_bit,
                bob_basis=b_basis,
                relay_compromised=is_compromised,
                spectral_distinguishability=spectral_skew
            )

            events.append(MDIEvent(
                trial_id=i,
                alice_basis=a_basis,
                alice_bit=a_bit,
                bob_basis=b_basis,
                bob_bit=b_bit,
                relay_coincidence=coinc,
                photons_indistinguishable=(spectral_skew < 0.40)
            ))

        return events

    def verify_mdi_session(
        self,
        events: List[MDIEvent]
    ) -> SessionModeResult:
        """
        Executes verification in MDI_RELAY mode.
        1. Analyzes two-photon Hong-Ou-Mandel visibility and Z-basis forbidden coincidences.
        2. Streams symmetric-basis error events into SequentialQStat for early termination.
        """
        if not events:
            raise ValueError("MDI session requires at least one MDIEvent")

        # 1. Full batch cryptanalysis via MDIRelayWatcher
        mdi_res = self.mdi_watcher.analyze_mdi_session(events)

        # 2. Sequential conversion: map symmetric basis coincidence errors into Bernoulli stream
        # When Alice and Bob prepare identical states in Z (|00> or |11>), genuine Psi- projection
        # has 0 coincidence probability. An erroneous coincidence click indicates error (x=1).
        seq_detector = SequentialQStat(baseline_p0=self.baseline_p0, alt_p1=self.alt_p1)
        last_verdict: Optional[SequentialVerdict] = None
        eval_count = 0

        for ev in events:
            # Focus on diagnostic basis (Z same trials) or relay coincidence error
            if ev.alice_basis == "Z" and ev.bob_basis == "Z" and ev.alice_bit == ev.bob_bit:
                eval_count += 1
                outcome = 1 if ev.relay_coincidence else 0
                last_verdict = seq_detector.update(outcome)
                if last_verdict.decision_reached and last_verdict.verdict == ThreatCategory.MALICIOUS:
                    break

        if last_verdict is None:
            # Fall back to general coincidence stream
            for ev in events:
                eval_count += 1
                # If indistinguishable photons violated, record error
                outcome = 0 if ev.photons_indistinguishable else 1
                last_verdict = seq_detector.update(outcome)
                if last_verdict.decision_reached and last_verdict.verdict == ThreatCategory.MALICIOUS:
                    break

        if last_verdict is None:
            last_verdict = seq_detector.update(0)

        # Reconcile verdicts: if MDI watcher found attack (e.g. distinguishable photon spoof),
        # ensure overall verdict is MALICIOUS
        final_verdict = mdi_res.verdict
        if last_verdict.verdict == ThreatCategory.MALICIOUS:
            final_verdict = ThreatCategory.MALICIOUS

        tradeoff = (
            "MDI_RELAY Mode Active: 100% immune to detector blinding, spatial shifts, and detector "
            "side channels (Lo et al. 2012; Puthoor et al. 2016). Relay untrusted. Trade-off: Lower "
            f"two-photon coincidence yield (HOM visibility = {mdi_res.hom_visibility*100:.1f}%)."
        )

        return SessionModeResult(
            mode=SessionMode.MDI_RELAY,
            verdict=final_verdict,
            detector_immune=True,
            trials_evaluated=eval_count,
            sequential_verdict=last_verdict,
            mdi_analysis=mdi_res,
            tradeoff_explanation=tradeoff
        )

    def verify_trusted_detector_session(
        self,
        trial_outcomes: List[int]
    ) -> SessionModeResult:
        """
        Executes verification in TRUSTED_DETECTOR mode.
        """
        seq_detector = SequentialQStat(baseline_p0=self.baseline_p0, alt_p1=self.alt_p1)
        last_verdict: Optional[SequentialVerdict] = None

        for t in trial_outcomes:
            last_verdict = seq_detector.update(t)
            if last_verdict.decision_reached and last_verdict.verdict == ThreatCategory.MALICIOUS:
                break

        if last_verdict is None:
            last_verdict = seq_detector.update(0)

        tradeoff = (
            "TRUSTED_DETECTOR Mode Active: Maximal single-photon throughput and minimal loss. "
            "Requires trusting Verifier's local detector hardware against side-channel tampering "
            "(monitored via Q-BLIND watchtower)."
        )

        return SessionModeResult(
            mode=SessionMode.TRUSTED_DETECTOR,
            verdict=last_verdict.verdict,
            detector_immune=False,
            trials_evaluated=last_verdict.n_trials,
            sequential_verdict=last_verdict,
            mdi_analysis=None,
            tradeoff_explanation=tradeoff
        )
