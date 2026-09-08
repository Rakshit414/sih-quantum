"""
Q-Sentinel: Quantum Trojan-Horse Attack (THA) & Key Memory Decoherence Watchtower
Stage 12: Phase 32 (Q-TROJAN)

Provides continuous quantum key memory buffer simulation with finite coherence times
(T1 relaxation, T2 dephasing) and detects optical Trojan-Horse probe pulses via:
1. Multi-wavelength Optical Power Metering (OPM)
2. Spectral Bandpass Filtering (1550 nm C-band validation)
3. Time-Domain Synchronous Gating (TOF arrival jitter)
4. Helstrom-Holevo Mutual Information Leakage Bounds (I_Eve)
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple, Optional
import numpy as np

from security.detector import ThreatCategory


@dataclass
class StoredQubitState:
    """
    Represents a quantum signature state stored in a physical quantum memory register.
    Tracks Lindblad decoherence (T1 relaxation, T2 dephasing) over elapsed storage time.
    """
    initial_state_label: str
    initial_density_matrix: np.ndarray
    elapsed_storage_us: float
    t1_relaxation_us: float
    t2_dephasing_us: float
    current_density_matrix: np.ndarray
    memory_fidelity: float
    decoherence_error_rate: float


@dataclass
class TrojanProbeSignal:
    """
    Physical characteristics of an optical pulse detected at the optical ingress port.
    """
    optical_power_uw: float         # Injected / incident optical power in microwatts
    wavelength_nm: float            # Optical wavelength in nanometers (nominally 1550 nm)
    arrival_offset_ns: float        # Arrival timing offset relative to clock gate (nominally 0.0 ns)
    pulse_duration_ns: float        # Pulse duration (nominally 1.0 ns)
    internal_reflectivity_r: float  # Internal component reflection coefficient (e.g. 0.02)


@dataclass
class TrojanDetectionResult:
    """
    Comprehensive diagnostic result of the Q-TROJAN watchtower.
    """
    probe_detected: bool
    optical_power_uw: float
    back_reflected_photons: float
    wavelength_nm: float
    arrival_offset_ns: float
    spectral_breach: bool
    temporal_breach: bool
    information_leakage_bits: float
    storage_time_us: float
    memory_fidelity: float
    expected_decoherence_error: float
    observed_total_error: float
    anomaly_z_score: float
    verdict: ThreatCategory
    attack_classification: str
    cryptanalytic_proof: str


class QuantumMemoryBuffer:
    """
    Simulates a physical quantum memory buffer (e.g. trapped ion, NV center, or optical delay)
    subject to T1 (longitudinal relaxation) and T2 (transverse dephasing) decoherence.
    """

    def __init__(self, t1_us: float = 1000.0, t2_us: float = 200.0):
        """
        Parameters:
            t1_us: Longitudinal relaxation time in microseconds.
            t2_us: Transverse dephasing time in microseconds (must satisfy T2 <= 2*T1).
        """
        if t2_us > 2.0 * t1_us:
            raise ValueError(f"Physical constraint violated: T2 ({t2_us} us) cannot exceed 2*T1 ({2*t1_us} us).")
        self.t1: float = float(t1_us)
        self.t2: float = float(t2_us)

    def evolve_state(
        self,
        pure_state_vector: np.ndarray,
        elapsed_us: float,
        label: str = "Psi"
    ) -> StoredQubitState:
        """
        Evolves a pure qubit state |psi> through the T1/T2 Lindblad decoherence master equation.
        """
        psi = np.asarray(pure_state_vector, dtype=complex).reshape(2, 1)
        rho_0 = psi @ psi.conj().T

        # Lindblad / Bloch decoherence evolution:
        # rho_00(t) = 1 - (1 - rho_00(0)) * exp(-t / T1)
        # rho_11(t) = rho_11(0) * exp(-t / T1)
        # rho_01(t) = rho_01(0) * exp(-t / T2)
        # rho_10(t) = rho_10(0) * exp(-t / T2)
        decay_t1 = np.exp(-elapsed_us / self.t1)
        decay_t2 = np.exp(-elapsed_us / self.t2)

        rho_t = np.zeros((2, 2), dtype=complex)
        rho_t[0, 0] = 1.0 - (1.0 - rho_0[0, 0].real) * decay_t1
        rho_t[1, 1] = rho_0[1, 1].real * decay_t1
        rho_t[0, 1] = rho_0[0, 1] * decay_t2
        rho_t[1, 0] = rho_0[1, 0] * decay_t2

        # Trace preservation check
        tr = np.trace(rho_t).real
        if tr > 0:
            rho_t = rho_t / tr

        # Compute quantum state fidelity F = <psi| rho(t) |psi>
        fidelity = float(np.clip((psi.conj().T @ rho_t @ psi).real[0, 0], 0.0, 1.0))

        # Expected error rate due purely to memory decay
        error_rate = float(np.clip(1.0 - fidelity, 0.0, 1.0))

        return StoredQubitState(
            initial_state_label=label,
            initial_density_matrix=rho_0,
            elapsed_storage_us=elapsed_us,
            t1_relaxation_us=self.t1,
            t2_dephasing_us=self.t2,
            current_density_matrix=rho_t,
            memory_fidelity=round(fidelity, 5),
            decoherence_error_rate=round(error_rate, 5)
        )


class TrojanHorseDetector:
    """
    Multi-sensor Quantum Trojan-Horse Watchtower.
    Analyzes optical energy, spectral wavelength, arrival timing, and memory decoherence
    to protect QDS phase modulators and quantum memory buffers from bright-pulse eavesdropping.
    """

    def __init__(
        self,
        safe_power_threshold_uw: float = 0.010,     # Max allowable back-reflected optical power (10 nW)
        passband_center_nm: float = 1550.0,          # Telecom C-band center
        passband_width_nm: float = 10.0,             # Filter FWHM width (+/- 5.0 nm)
        gate_window_ns: float = 1.0,                 # Synchronous temporal gate (+/- 1.0 ns)
        baseline_channel_noise: float = 0.03         # Nominal channel error rate (3%)
    ):
        self.power_threshold: float = safe_power_threshold_uw
        self.passband_center: float = passband_center_nm
        self.passband_width: float = passband_width_nm
        self.gate_window: float = gate_window_ns
        self.base_noise: float = baseline_channel_noise
        self.memory_buffer: QuantumMemoryBuffer = QuantumMemoryBuffer(t1_us=1000.0, t2_us=200.0)

    @staticmethod
    def calculate_helstrom_information_leakage(back_reflected_photons: float) -> float:
        """
        Computes the theoretical upper bound on Eve's mutual information I_Eve
        extracted via back-reflected Trojan-horse photons using the Helstrom/Holevo bound:
        I_Eve <= 1 - h2((1 - sqrt(1 - exp(-4 * mu_refl))) / 2)
        """
        mu = max(0.0, float(back_reflected_photons))
        if mu <= 1e-9:
            return 0.0

        # Bound parameter d = (1 - sqrt(1 - exp(-4*mu))) / 2
        exp_factor = np.exp(-4.0 * min(mu, 20.0))
        sqrt_term = np.sqrt(max(0.0, 1.0 - exp_factor))
        d = 0.5 * (1.0 - sqrt_term)

        # Binary entropy h2(d)
        d = np.clip(d, 1e-12, 0.5)
        h2 = -d * np.log2(d) - (1.0 - d) * np.log2(1.0 - d)
        info_leak = float(np.clip(1.0 - h2, 0.0, 1.0))
        return round(info_leak, 6)

    def analyze_probe(
        self,
        probe: Optional[TrojanProbeSignal],
        elapsed_storage_us: float = 0.0,
        observed_trial_errors: Optional[int] = None,
        total_trials: int = 200
    ) -> TrojanDetectionResult:
        """
        Performs unified multi-sensor evaluation of incoming optical signals and stored memory state.
        """
        # 1. Evaluate memory buffer decoherence
        # Ground state |0> reference vector
        pure_ref = np.array([1.0, 0.0], dtype=complex)
        mem_state = self.memory_buffer.evolve_state(pure_ref, elapsed_storage_us, label="|0>")
        expected_error = self.base_noise + mem_state.decoherence_error_rate

        # 2. Analyze probe signal (if present)
        if probe is None:
            # Clean baseline scenario (no external optical probe)
            probe_power = 0.0001  # Thermal dark noise 0.1 nW
            wavelength = self.passband_center
            arr_offset = 0.0
            refl_photons = 0.0
            refl_power = 0.0
        else:
            probe_power = probe.optical_power_uw
            wavelength = probe.wavelength_nm
            arr_offset = probe.arrival_offset_ns
            # Planck's energy per 1550nm photon: E_ph = h * c / lambda = 1.28e-19 J
            # Scaled model: 1 uW * 1 ns ~ 7800 photons
            photons_injected = (probe.optical_power_uw * 1e-6) * (probe.pulse_duration_ns * 1e-9) / 1.28e-19
            refl_photons = max(0.0, photons_injected * probe.internal_reflectivity_r)
            refl_power = probe.optical_power_uw * probe.internal_reflectivity_r

        # 3. Sensor checks:
        # A) Spectral passband filter check
        half_band = self.passband_width / 2.0
        spectral_breach = abs(wavelength - self.passband_center) > half_band

        # B) Temporal gating check
        temporal_breach = abs(arr_offset) > self.gate_window

        # C) Optical power metering check
        power_breach = refl_power > self.power_threshold

        # D) Helstrom information leakage calculation
        info_leak = self.calculate_helstrom_information_leakage(refl_photons)

        # 4. Statistical anomaly calculation (Q-STAT)
        if observed_trial_errors is not None:
            k = observed_trial_errors
            n = total_trials
            p_exp = np.clip(expected_error, 0.001, 0.999)
            z_score = (k - n * p_exp) / np.sqrt(n * p_exp * (1.0 - p_exp))
            obs_error = k / max(1, n)
        else:
            # Synthesize observed error from expected error + probe perturbation
            perturbation = 0.40 if power_breach else (0.15 if (spectral_breach or temporal_breach) else 0.0)
            obs_error = float(np.clip(expected_error + perturbation, 0.0, 1.0))
            k = int(np.round(obs_error * total_trials))
            n = total_trials
            p_exp = np.clip(expected_error, 0.001, 0.999)
            z_score = (k - n * p_exp) / np.sqrt(n * p_exp * (1.0 - p_exp))

        # 5. Determine Threat Verdict and Classification
        probe_detected = power_breach or spectral_breach or temporal_breach or (info_leak > 0.005)

        if spectral_breach:
            verdict = ThreatCategory.MALICIOUS
            attack_type = "OUT_OF_BAND_SPECTRAL_PROBE"
            proof = (
                f"MALICIOUS: Out-of-band optical injection at lambda = {wavelength:.1f} nm outside calibrated "
                f"passband [{self.passband_center - half_band:.1f}, {self.passband_center + half_band:.1f}] nm. "
                f"Adversary attempting spectral evasion of single-photon detectors."
            )
        elif temporal_breach:
            verdict = ThreatCategory.MALICIOUS
            attack_type = "ASYNC_TIME_DOMAIN_PROBE"
            proof = (
                f"MALICIOUS: Optical pulse arrived at timing offset {arr_offset:+.2f} ns outside synchronous "
                f"gate window [{-self.gate_window:+.1f}, {+self.gate_window:+.1f}] ns. Unauthorized asynchronous probe."
            )
        elif power_breach or info_leak > 0.01:
            verdict = ThreatCategory.MALICIOUS
            attack_type = "BRIGHT_PULSE_TROJAN_HORSE"
            proof = (
                f"MALICIOUS: High-intensity optical probe detected (Reflected Power = {refl_power*1e3:.2f} nW > "
                f"Threshold {self.power_threshold*1e3:.1f} nW). Eve mutual information leakage bound "
                f"I_E = {info_leak:.4f} bits/pulse threatens phase-modulator confidentiality."
            )
        elif z_score >= 2.0 or info_leak > 0.001:
            verdict = ThreatCategory.SUSPICIOUS
            attack_type = "ELEVATED_PROBE_NOISE"
            proof = (
                f"SUSPICIOUS: Elevated optical anomaly score (z = {z_score:+.2f} sigma, I_E = {info_leak:.6f} bits). "
                f"Near-threshold optical fluctuation observed on ingress channel."
            )
        else:
            verdict = ThreatCategory.LEGITIMATE
            attack_type = "CLEAN_CHANNEL"
            proof = (
                f"LEGITIMATE: Channel ingress verified secure. Back-reflected power {refl_power*1e3:.2f} nW "
                f"below safety floor. Eve information leakage bound I_E = {info_leak:.6f} bits. "
                f"Memory decoherence (F={mem_state.memory_fidelity*100:.1f}%) within physical T1/T2 model."
            )

        return TrojanDetectionResult(
            probe_detected=probe_detected,
            optical_power_uw=round(probe_power, 4),
            back_reflected_photons=round(refl_photons, 2),
            wavelength_nm=round(wavelength, 1),
            arrival_offset_ns=round(arr_offset, 2),
            spectral_breach=spectral_breach,
            temporal_breach=temporal_breach,
            information_leakage_bits=info_leak,
            storage_time_us=elapsed_storage_us,
            memory_fidelity=mem_state.memory_fidelity,
            expected_decoherence_error=round(expected_error, 4),
            observed_total_error=round(obs_error, 4),
            anomaly_z_score=round(float(z_score), 2),
            verdict=verdict,
            attack_classification=attack_type,
            cryptanalytic_proof=proof
        )
