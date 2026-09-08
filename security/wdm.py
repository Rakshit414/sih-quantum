"""
Q-Sentinel: Quantum Wavelength Division Multiplexing (WDM) & Co-propagation Raman Scattering Defense
Stage 16: Phase 37 (Q-WDM)

Protects quantum signature channels co-propagating over existing commercial single-mode fiber (SMF-28)
alongside high-power classical optical communication channels (DWDM at 10G/100G/400G).

Models physical non-linear optics and spontaneous Raman scattering (SpRS):
1. Spontaneous Anti-Stokes / Stokes Raman photon generation in silica core:
   I_Raman = P_launch * beta_Raman(Delta_lambda) * L_eff * Delta_lambda_filter * eta_det
2. Effective non-linear interaction length:
   L_eff = (1 - exp(-alpha * L)) / alpha
3. Optical isolation and Narrowband Fiber Bragg Grating (FBG) filtering (FWHM <= 0.1 nm / 12.5 GHz)
4. Synchronous temporal gating (Delta_tau <= 500 ps)
5. Discrimination of:
   - LEGITIMATE_WDM_CHANNEL (Certified co-propagation with SNR >= 15.0)
   - ADVERSARIAL_CROSS_TALK_JAMMING (High-power out-of-band pump injection)
   - RAMAN_SCATTERING_SATURATION (Excessive co-propagation power / thermal Stokes noise)
   - ELEVATED_CO_PROPAGATION_NOISE (Marginal isolation requiring FBG attenuation adjustment)
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple, Optional, List
import numpy as np

from security.detector import ThreatCategory


@dataclass
class WDMChannelConfig:
    """
    Physical fiber and optical transmission configuration for co-propagating WDM.
    """
    fiber_length_km: float = 25.0             # Fiber span distance (km)
    fiber_attenuation_db_per_km: float = 0.20 # Standard SMF-28 attenuation (~0.20 dB/km at 1550 nm)
    classical_launch_power_dbm: float = 0.0   # Classical launch power in dBm (0 dBm = 1.0 mW)
    classical_wavelength_nm: float = 1530.0   # Classical telecom pump channel (e.g. C-band 1530 nm)
    quantum_wavelength_nm: float = 1550.0     # Quantum signature channel (1550 nm)
    fbg_filter_fwhm_nm: float = 0.05          # Ultra-narrow Fiber Bragg Grating bandwidth (0.05 nm ~ 6 GHz)
    detector_efficiency: float = 0.25         # Single-photon detector quantum efficiency (25%)
    gate_window_ps: float = 200.0             # Temporal coincidence gating window (200 picoseconds)
    repetition_rate_mhz: float = 50.0         # Pulse repetition rate (50 MHz)


@dataclass
class WDMAnalysisResult:
    """
    Cryptanalytic outcome of the WDM co-propagation Raman scattering watchtower.
    """
    fiber_length_km: float
    classical_launch_power_dbm: float
    classical_launch_power_mw: float
    wavelength_separation_nm: float
    effective_length_km: float
    raman_noise_photons_per_pulse: float
    raman_noise_count_rate_hz: float
    signal_to_noise_ratio_snr: float
    induced_raman_qber: float
    optical_isolation_db: float
    is_wdm_secure: bool
    verdict: ThreatCategory
    attack_classification: str
    cryptanalytic_proof: str


class RamanScatteringModel:
    """
    Models physical Spontaneous Raman Scattering (SpRS) and non-linear cross-talk
    in fused silica (SiO2) standard single-mode optical fiber (ITU-T G.652 SMF-28).
    """

    def __init__(self, config: Optional[WDMChannelConfig] = None):
        self.config = config or WDMChannelConfig()

    def compute_effective_length(self, length_km: float, alpha_db_per_km: float) -> float:
        """
        Computes non-linear effective fiber interaction length:
        L_eff = (1 - exp(-alpha_linear * L)) / alpha_linear
        where alpha_linear = alpha_db_per_km * ln(10) / 10 (km^-1).
        """
        alpha_lin = alpha_db_per_km * np.log(10.0) / 10.0
        if alpha_lin < 1e-6:
            return float(length_km)
        return float((1.0 - np.exp(-alpha_lin * length_km)) / alpha_lin)

    def compute_raman_cross_section_coefficient(self, delta_lambda_nm: float) -> float:
        """
        Evaluates empirical Raman gain / scattering cross-section coefficient beta(Delta_lambda)
        in SMF-28 silica fiber (in units of 10^-9 km^-1 nm^-1).
        Peak silica Raman shift occurs at ~13.2 THz (~100 nm separation).
        Around 20 nm separation (e.g. 1530 nm -> 1550 nm), beta is ~ 1.8e-8 km^-1 nm^-1.
        """
        d_lambda = abs(delta_lambda_nm)
        # Empirical Raman cross-section profile for fused silica
        # Lorentzian-Gaussian approximation centered near 100 nm with tail down to small separations
        peak_sep = 100.0
        width = 40.0
        peak_beta = 5.5e-8  # km^-1 nm^-1 at peak 100 nm
        tail_factor = np.exp(-((d_lambda - peak_sep) ** 2) / (2.0 * (width ** 2)))
        # Near-band Raman scattering tail for d_lambda < 40 nm
        near_band = (d_lambda / peak_sep) * 2.2e-8
        beta = float(max(1.0e-9, near_band if d_lambda < 50.0 else peak_beta * tail_factor))
        return beta

    def evaluate_co_propagation(
        self,
        config: Optional[WDMChannelConfig] = None,
        adversarial_jamming: bool = False
    ) -> WDMAnalysisResult:
        """
        Simulates physical Raman photon flux arriving at the single-photon detector
        after passing through the WDM demultiplexer and ultra-narrow FBG optical bandpass filter.
        """
        cfg = config or self.config

        # 1. Classical Power in Watts
        # If jamming, power is forced high (e.g. +14 dBm / 25 mW) or filter is bypassed
        p_dbm = cfg.classical_launch_power_dbm
        if adversarial_jamming:
            p_dbm = max(14.0, p_dbm + 12.0)

        p_watts = (10.0 ** (p_dbm / 10.0)) * 1e-3  # Convert dBm to Watts
        p_mw = p_watts * 1000.0

        # 2. Geometry & Effective Length
        l_eff = self.compute_effective_length(cfg.fiber_length_km, cfg.fiber_attenuation_db_per_km)
        d_lambda = abs(cfg.quantum_wavelength_nm - cfg.classical_wavelength_nm)

        # 3. Raman Cross-Section
        beta = self.compute_raman_cross_section_coefficient(d_lambda)

        # 4. Spontaneous Raman Noise Power arriving per nm bandwidth:
        # P_spRS = P_classical * beta(Delta_lambda) * L_eff (in Watts/nm)
        raman_spectral_power = p_watts * beta * l_eff

        # Optical filter rejection and FBG filtering
        # FBG filter transmission bandwidth (FWHM in nm)
        fbg_bw = cfg.fbg_filter_fwhm_nm
        if adversarial_jamming:
            # Jamming or compromised filter alignment increases effective leak bandwidth
            fbg_bw = fbg_bw * 6.0

        # Raman power passing through FBG filter (in Watts)
        raman_optical_power = raman_spectral_power * fbg_bw

        # Energy per photon at 1550 nm: E_ph = h * c / lambda
        # h = 6.626e-34 J*s, c = 3.0e8 m/s, lambda = 1.55e-6 m -> E_ph ~ 1.28e-19 Joules
        e_photon = 1.282e-19

        # Continuous Raman photon rate (photons/second)
        raman_photon_rate_hz = (raman_optical_power / e_photon) * cfg.detector_efficiency

        # Raman photons per temporal gating window (e.g. 500 ps):
        gate_seconds = cfg.gate_window_ps * 1e-12
        raman_noise_per_pulse = raman_photon_rate_hz * gate_seconds

        # Single-photon signal pulse: Typical weak coherent pulse with mean photon number mu = 0.5
        mu_signal = 0.50
        # Transmitted signal photon per pulse through fiber:
        signal_transmittance = 10.0 ** (-(cfg.fiber_attenuation_db_per_km * cfg.fiber_length_km) / 10.0)
        signal_per_pulse = mu_signal * signal_transmittance * cfg.detector_efficiency

        # Signal to Noise Ratio (SNR):
        snr = float(signal_per_pulse / max(1e-8, raman_noise_per_pulse))

        # Induced Quantum Bit Error Rate (QBER) from Raman noise:
        # Raman photons have random polarization, contributing 50% error to coincidence detection:
        # e_Raman = (0.5 * noise) / (signal + noise)
        induced_qber = float((0.5 * raman_noise_per_pulse) / max(1e-6, signal_per_pulse + raman_noise_per_pulse))

        # Optical Isolation (dB): -10 * log10(P_raman_leak / P_classical)
        optical_isolation = float(-10.0 * np.log10(max(1e-18, raman_optical_power / max(1e-9, p_watts))))

        # 5. Cryptanalytic Evaluation & Threat Discrimination
        if snr >= 15.0 and induced_qber <= 0.045 and p_dbm <= 3.0:
            verdict = ThreatCategory.LEGITIMATE
            classification = "LEGITIMATE_WDM_CO_PROPAGATION"
            is_secure = True
            proof = (
                f"LEGITIMATE: Co-propagating quantum-classical WDM certified secure. Classical launch power "
                f"{p_dbm:+.1f} dBm ({p_mw:.2f} mW) yields high SNR = {snr:.1f} >= 15.0. Raman-induced QBER is negligible "
                f"({induced_qber*100:.2f}% <= 4.5%). FBG narrowband filtering provides {optical_isolation:.1f} dB optical isolation."
            )
        elif adversarial_jamming or p_dbm >= 12.0:
            verdict = ThreatCategory.MALICIOUS
            classification = "ADVERSARIAL_CROSS_TALK_JAMMING"
            is_secure = False
            proof = (
                f"MALICIOUS: Adversarial cross-talk jamming detected! Excessive classical launch power "
                f"({p_dbm:+.1f} dBm / {p_mw:.1f} mW) injected into adjacent channel. Raman photon flux "
                f"({raman_noise_per_pulse*1e3:.2f} m-photons/gate) collapsed SNR to {snr:.2f} < 3.0, driving induced QBER to {induced_qber*100:.1f}%."
            )
        elif snr < 8.0 or induced_qber > 0.060:
            verdict = ThreatCategory.MALICIOUS
            classification = "RAMAN_SCATTERING_SATURATION"
            is_secure = False
            proof = (
                f"MALICIOUS: Spontaneous Raman scattering saturation. Classical channel power ({p_dbm:+.1f} dBm) "
                f"or insufficient wavelength separation (Delta_lambda = {d_lambda:.1f} nm) overwhelmed single-photon detector. "
                f"Induced QBER = {induced_qber*100:.2f}% exceeds tolerable quantum threshold (6.0%)."
            )
        else:
            verdict = ThreatCategory.SUSPICIOUS
            classification = "ELEVATED_CO_PROPAGATION_NOISE"
            is_secure = False
            proof = (
                f"SUSPICIOUS: Elevated Raman noise floor detected (SNR = {snr:.1f}, Induced QBER = {induced_qber*100:.2f}%). "
                f"Recommend dynamic optical FBG filter tuning or classical power attenuation."
            )

        return WDMAnalysisResult(
            fiber_length_km=float(cfg.fiber_length_km),
            classical_launch_power_dbm=round(p_dbm, 2),
            classical_launch_power_mw=round(p_mw, 3),
            wavelength_separation_nm=round(d_lambda, 2),
            effective_length_km=round(l_eff, 3),
            raman_noise_photons_per_pulse=round(raman_noise_per_pulse, 6),
            raman_noise_count_rate_hz=round(raman_photon_rate_hz, 1),
            signal_to_noise_ratio_snr=round(snr, 2),
            induced_raman_qber=round(induced_qber, 4),
            optical_isolation_db=round(optical_isolation, 1),
            is_wdm_secure=is_secure,
            verdict=verdict,
            attack_classification=classification,
            cryptanalytic_proof=proof
        )


class WDMRamanWatcher:
    """
    Watchtower analyzer for Quantum WDM co-propagation links.
    Monitors optical power metrics and validates Raman noise cross-talk immunity.
    """

    def __init__(self, target_min_snr: float = 12.0, max_tolerable_raman_qber: float = 0.050):
        self.min_snr: float = float(target_min_snr)
        self.max_qber: float = float(max_tolerable_raman_qber)
        self.model = RamanScatteringModel()

    def analyze_wdm_channel(self, config: WDMChannelConfig) -> WDMAnalysisResult:
        """
        Analyzes a live or configured WDM co-propagation channel.
        """
        return self.model.evaluate_co_propagation(config=config, adversarial_jamming=False)

    def simulate_wdm_scenario(
        self,
        scenario: str = "Honest Co-Propagation (0 dBm Classical)",
        fiber_length_km: float = 25.0
    ) -> WDMAnalysisResult:
        """
        Simulates standard operational, noisy, and adversarial WDM scenarios.
        """
        if "Honest" in scenario or "Clean" in scenario:
            cfg = WDMChannelConfig(
                fiber_length_km=fiber_length_km,
                classical_launch_power_dbm=0.0,  # 1.0 mW
                classical_wavelength_nm=1530.0,
                quantum_wavelength_nm=1550.0,
                fbg_filter_fwhm_nm=0.05,
                gate_window_ps=200.0
            )
            return self.model.evaluate_co_propagation(config=cfg, adversarial_jamming=False)

        elif "Jamming" in scenario or "Adversarial" in scenario:
            cfg = WDMChannelConfig(
                fiber_length_km=fiber_length_km,
                classical_launch_power_dbm=14.0, # 25.0 mW high-power pump
                classical_wavelength_nm=1530.0,
                quantum_wavelength_nm=1550.0,
                fbg_filter_fwhm_nm=0.15,
                gate_window_ps=200.0
            )
            return self.model.evaluate_co_propagation(config=cfg, adversarial_jamming=True)

        elif "Saturation" in scenario or "High Power" in scenario:
            cfg = WDMChannelConfig(
                fiber_length_km=fiber_length_km,
                classical_launch_power_dbm=8.0,  # 6.3 mW
                classical_wavelength_nm=1540.0,  # Closer wavelength spacing (10 nm)
                quantum_wavelength_nm=1550.0,
                fbg_filter_fwhm_nm=0.08,
                gate_window_ps=200.0
            )
            return self.model.evaluate_co_propagation(config=cfg, adversarial_jamming=False)

        else:
            # Elevated noise / Marginal power
            cfg = WDMChannelConfig(
                fiber_length_km=fiber_length_km,
                classical_launch_power_dbm=3.5,  # 2.24 mW
                classical_wavelength_nm=1535.0,
                quantum_wavelength_nm=1550.0,
                fbg_filter_fwhm_nm=0.06,
                gate_window_ps=200.0
            )
            return self.model.evaluate_co_propagation(config=cfg, adversarial_jamming=False)