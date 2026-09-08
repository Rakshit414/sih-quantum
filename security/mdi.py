"""
Q-Sentinel: Measurement-Device-Independent (MDI) QDS Architecture & Untrusted Relay Watchtower
Stage 15: Phase 36 (Q-MDI)

Implements Measurement-Device-Independent (MDI) Quantum Digital Signature protocol:
Alice and Bob transmit quantum states to an untrusted relay (Charles/Eve) who performs
Bell-State Measurements (BSM) via Hong-Ou-Mandel (HOM) two-photon interference.

Guarantees 100% immunity against all detector side-channel attacks (blinding, spatial shift,
dead-time hacking, efficiency mismatch) on the relay node, and detects relay tampering via:
1. Hong-Ou-Mandel (HOM) two-photon interference visibility: V_HOM = (R_max - R_dip) / R_max
2. Symmetric state coincidence prohibition (Z-basis error rate e_Z)
3. Relay announcement bias and selective coincidence suppression
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple, Optional, List
import numpy as np

from security.detector import ThreatCategory
from quantum.state import PauliBasis


@dataclass
class MDIEvent:
    """
    Single MDI transmission trial: Alice and Bob states sent to relay.
    """
    trial_id: int
    alice_basis: str        # 'Z' or 'X'
    alice_bit: int          # 0 or 1
    bob_basis: str          # 'Z' or 'X'
    bob_bit: int            # 0 or 1
    relay_coincidence: bool # True if detectors D1 and D2 clicked simultaneously (Psi- projection)
    photons_indistinguishable: bool


@dataclass
class MDIAnalysisResult:
    """
    Cryptanalytic outcome of the MDI untrusted relay verification.
    """
    total_transmitted_trials: int
    total_bsm_coincidences: int
    bsm_success_rate: float
    hom_visibility: float
    z_basis_error_rate: float       # Error when Alice and Bob prepare identical states in Z
    x_basis_error_rate: float
    relay_bias_ratio: float
    detector_immune: bool           # Inherently immune to detector hacking
    verdict: ThreatCategory
    attack_classification: str
    cryptanalytic_proof: str


class MDIQuantumRelay:
    """
    Simulates a 50:50 beam splitter Bell-state analyzer at an untrusted relay node.
    Evaluates Hong-Ou-Mandel interference between Alice's and Bob's incoming photons.
    """

    def __init__(
        self,
        nominal_hom_visibility: float = 0.92,
        dark_count_prob: float = 1e-4,
        beam_splitter_transmittance: float = 0.50
    ):
        self.v_hom: float = float(nominal_hom_visibility)
        self.p_dark: float = float(dark_count_prob)
        self.bs_t: float = float(beam_splitter_transmittance)

    def simulate_bsm_trial(
        self,
        alice_bit: int,
        alice_basis: str,
        bob_bit: int,
        bob_basis: str,
        relay_compromised: bool = False,
        spectral_distinguishability: float = 0.0
    ) -> bool:
        """
        Simulates two-photon interference on a 50:50 beam splitter.
        A coincidence click between output detectors D1 and D2 announces projection onto |Psi->.
        For identical photons in identical states (e.g. |00> or |11>), HOM bunching suppresses
        coincidences to zero (dip). Coincidences only occur for anti-symmetric state |Psi-> = (|01> - |10>)/sqrt(2).
        """
        # Effective visibility reduced by spectral distinguishability or relay compromise
        eff_v = self.v_hom * (1.0 - spectral_distinguishability)

        if relay_compromised:
            # Compromised relay injects false coincidences on symmetric states
            # Violates the coincidence prohibition e_Z <= 8% while maintaining pseudo-interference
            if alice_basis == bob_basis:
                if alice_bit == bob_bit:
                    return bool(np.random.rand() < 0.15)
                else:
                    return bool(np.random.rand() < 0.45)
            return bool(np.random.rand() < 0.25)

        if alice_basis == 'Z' and bob_basis == 'Z':
            if alice_bit == bob_bit:
                # Symmetric states |00> or |11>: Coincidence is physically forbidden!
                # Clicks only occur via dark counts or imperfect visibility (1 - V_HOM)
                p_err = self.p_dark + (1.0 - eff_v) * 0.25
                return bool(np.random.rand() < p_err)
            else:
                # Anti-symmetric components (|01> and |10>): Contain 50% |Psi->
                # Ideal BSM efficiency is 50% for linear optics
                p_coinc = 0.50 * eff_v + self.p_dark
                return bool(np.random.rand() < p_coinc)
        elif alice_basis == 'X' and bob_basis == 'X':
            # In X basis, |+> and |-> states:
            # |+-> and |-+> contain |Psi-> with 50% probability
            if alice_bit != bob_bit:
                p_coinc = 0.50 * eff_v + self.p_dark
                return bool(np.random.rand() < p_coinc)
            else:
                p_err = self.p_dark + (1.0 - eff_v) * 0.25
                return bool(np.random.rand() < p_err)
        else:
            # Basis mismatch: 25% random coincidence
            return bool(np.random.rand() < 0.25)


class MDIRelayWatcher:
    """
    Watchtower analyzer for Measurement-Device-Independent QDS channels.
    Certifies that an untrusted relay is honestly announcing genuine two-photon BSM events
    and detects adversarial relay manipulation or photon distinguishability attacks.
    """

    def __init__(
        self,
        min_hom_visibility: float = 0.70,
        max_z_error_rate: float = 0.080,
        max_announcement_bias: float = 0.20
    ):
        self.min_visibility: float = float(min_hom_visibility)
        self.max_z_err: float = float(max_z_error_rate)
        self.max_bias: float = float(max_announcement_bias)
        self.relay_engine: MDIQuantumRelay = MDIQuantumRelay()

    def analyze_mdi_session(
        self,
        events: List[MDIEvent]
    ) -> MDIAnalysisResult:
        """
        Analyzes a batch of MDI transmission trials and assesses relay integrity.
        """
        if not events:
            raise ValueError("MDI session must contain at least 1 trial.")

        total_trials = len(events)
        total_coincidences = sum(1 for e in events if e.relay_coincidence)

        # 1. Evaluate Z-basis sifted trials (where both Alice and Bob used Z basis)
        z_same_trials = [e for e in events if e.alice_basis == 'Z' and e.bob_basis == 'Z' and e.alice_bit == e.bob_bit]
        z_diff_trials = [e for e in events if e.alice_basis == 'Z' and e.bob_basis == 'Z' and e.alice_bit != e.bob_bit]

        # In Z-same (|00> or |11>), any coincidence is an error
        z_errors = sum(1 for e in z_same_trials if e.relay_coincidence)
        z_err_rate = float(z_errors / max(1, len(z_same_trials)))

        # In Z-diff (|01> or |10>), coincidences represent legitimate BSM projections
        z_signals = sum(1 for e in z_diff_trials if e.relay_coincidence)
        z_sig_rate = float(z_signals / max(1, len(z_diff_trials)))

        # 2. Evaluate X-basis sifted trials
        x_same_trials = [e for e in events if e.alice_basis == 'X' and e.bob_basis == 'X' and e.alice_bit == e.bob_bit]
        x_diff_trials = [e for e in events if e.alice_basis == 'X' and e.bob_basis == 'X' and e.alice_bit != e.bob_bit]

        x_errors = sum(1 for e in x_same_trials if e.relay_coincidence)
        x_err_rate = float(x_errors / max(1, len(x_same_trials)))

        # 3. Hong-Ou-Mandel Interference Visibility Calculation:
        # V_HOM = (R_signal - R_error) / (R_signal + R_error)
        denom = z_sig_rate + z_err_rate
        if denom > 1e-6:
            v_hom = float(np.clip((z_sig_rate - z_err_rate) / denom, 0.0, 1.0))
        else:
            v_hom = 0.0

        # 4. Announcement Basis Bias Check
        z_total = len(z_same_trials) + len(z_diff_trials)
        x_total = len(x_same_trials) + len(x_diff_trials)
        rate_z = z_signals / max(1, z_total)
        rate_x = sum(1 for e in x_diff_trials if e.relay_coincidence) / max(1, x_total)
        bias_ratio = float(abs(rate_z - rate_x) / max(1e-6, (rate_z + rate_x) / 2.0))

        # Overall BSM success rate across all trials
        bsm_rate = float(total_coincidences / max(1, total_trials))

        # 5. Security Verdict & Attack Discrimination
        if v_hom >= self.min_visibility and z_err_rate <= self.max_z_err and bias_ratio <= self.max_bias:
            verdict = ThreatCategory.LEGITIMATE
            classification = "CERTIFIED_MDI_RELAY_HONEST"
            proof = (
                f"LEGITIMATE: Hong-Ou-Mandel two-photon visibility V_HOM = {v_hom*100:.1f}% exceeds threshold "
                f"({self.min_visibility*100:.1f}%). Z-basis error e_Z = {z_err_rate*100:.2f}% confirms genuine "
                f"quantum interference. Untrusted relay verified honest. 100% detector side-channel immune."
            )
        elif z_err_rate > self.max_z_err and v_hom >= 0.35:
            verdict = ThreatCategory.MALICIOUS
            classification = "UNTRUSTED_RELAY_TAMPERING"
            proof = (
                f"MALICIOUS: Forbidden symmetric coincidence error e_Z = {z_err_rate*100:.2f}% exceeds safe limit "
                f"({self.max_z_err*100:.1f}%). Relay node is faking BSM announcements or applying malicious triggering."
            )
        elif v_hom < 0.40:
            verdict = ThreatCategory.MALICIOUS
            classification = "DISTINGUISHABLE_PHOTON_SPOOF"
            proof = (
                f"MALICIOUS: Two-photon interference collapsed (V_HOM = {v_hom*100:.1f}% < 40.0%). "
                f"Adversary injected distinguishable classical photons or disrupted channel temporal/spectral alignment."
            )
        elif z_err_rate > self.max_z_err:
            verdict = ThreatCategory.MALICIOUS
            classification = "UNTRUSTED_RELAY_TAMPERING"
            proof = (
                f"MALICIOUS: Forbidden symmetric coincidence error e_Z = {z_err_rate*100:.2f}% exceeds safe limit "
                f"({self.max_z_err*100:.1f}%). Relay node is faking BSM announcements or applying malicious triggering."
            )
        else:
            verdict = ThreatCategory.SUSPICIOUS
            classification = "ELEVATED_RELAY_NOISE_OR_BIAS"
            proof = (
                f"SUSPICIOUS: Relay announcement bias ({bias_ratio*100:.1f}%) or marginal HOM visibility "
                f"({v_hom*100:.1f}%) detected. Channel alignment requires auto-calibration."
            )

        return MDIAnalysisResult(
            total_transmitted_trials=total_trials,
            total_bsm_coincidences=total_coincidences,
            bsm_success_rate=round(bsm_rate, 4),
            hom_visibility=round(v_hom, 4),
            z_basis_error_rate=round(z_err_rate, 4),
            x_basis_error_rate=round(x_err_rate, 4),
            relay_bias_ratio=round(bias_ratio, 4),
            detector_immune=True,
            verdict=verdict,
            attack_classification=classification,
            cryptanalytic_proof=proof
        )

    def simulate_mdi_session(
        self,
        scenario: str = "Honest Untrusted Relay",
        num_trials: int = 1500
    ) -> MDIAnalysisResult:
        """
        Simulates an MDI transmission session across honest, compromised, and spoofed relays.
        """
        trials = max(300, num_trials)
        events: List[MDIEvent] = []

        is_compromised = "Compromised" in scenario or "Tampering" in scenario
        spectral_skew = 0.70 if ("Distinguishable" in scenario or "Interference Collapse" in scenario) else 0.0

        for i in range(1, trials + 1):
            # Random basis choice: 50% Z, 50% X
            a_basis = 'Z' if np.random.rand() < 0.50 else 'X'
            b_basis = 'Z' if np.random.rand() < 0.50 else 'X'

            # Random bit choice: 0 or 1
            a_bit = int(np.random.randint(0, 2))
            b_bit = int(np.random.randint(0, 2))

            coinc = self.relay_engine.simulate_bsm_trial(
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
                photons_indistinguishable=(spectral_skew < 0.2)
            ))

        return self.analyze_mdi_session(events)
