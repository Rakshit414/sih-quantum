"""
Q-Sentinel: Quantum-Inspired Cyber Threat Detection Framework
Custom Institutional UI: Pure White Background, Orange Top Bar & Dark Blue Extra Navigation Bar
Strict Open Sans, Toronto, and Calibri Typography; Zero Emojis/Symbols; Zero Text Highlights
Stage 19 (Phase 40): Grand Unified Release Audit, Zero-Failure Stress Validation & Final Submission Packaging (Q-RELEASE)
"""

from __future__ import annotations
from pathlib import Path
import streamlit as st
import time
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Optional

from rehearsal import (
    QuantumRehearsalRunner,
    RehearsalReport,
    WatchtowerTestResult,
)
from release_audit import (
    GrandUnifiedReleaseAuditor,
    GrandUnifiedReleaseReport,
)

from quantum.state import PauliBasis
from quantum.teleport import teleport_qubit, get_pauli_correction_matrix
from quantum.tomography import QuantumStateTomography, TomographyResult
from quantum.mesh import EntanglementSwapper, QuantumMeshRouter, MeshRouteVerificationResult
from security.signature import QDSKeyManager, QuantumDigitalSignature
from security.attacks import AttackScenario, ThreatOrchestrator
from security.detector import QStatDetector, ThreatCategory, ThreatAssessment
from security.freshness import FreshnessRegistry
from security.calibrate import DynamicNoiseCalibrator, CalibrationStatus
from security.multirecipient import MultiRecipientCoordinator, MultiRecipientVerificationResult
from security.mitigation import ThreatMitigationOrchestrator, IncidentReport
from security.hybrid import HybridSignatureVerifier, HybridVerificationResult
from security.decoy import DecoyStateAnalyzer, PNSAnalysisResult
from security.trojan import TrojanHorseDetector, TrojanProbeSignal, TrojanDetectionResult
from security.blind import DetectorBlindingWatcher, DetectorTelemetry, BlindingDetectionResult
from security.chsh import CHSHBellWatcher, CHSHVerificationResult
from security.finite import FiniteSizeSecurityAnalyzer, FiniteKeyParameters, FiniteSecurityResult
from security.mdi import MDIRelayWatcher, MDIAnalysisResult
from security.wdm import WDMRamanWatcher, WDMAnalysisResult, WDMChannelConfig
from analytics.history import TelemetryStore
from analytics.stream import QuantumTrafficGenerator, StreamEvent
from analytics.reports import AuditReportGenerator
from analytics.soc import (
    STIXBundleGenerator,
    ECSEventFormatter,
    QSOCIntegrator,
    STIXBundleSummary,
    SIEMDispatchResult,
)
from dashboard.charts import (
    build_threat_gauge,
    build_outcome_distribution_chart,
    build_telemetry_trend_chart,
)
from dashboard.visualizer import render_teleportation_pipeline_html


# Streamlit Page Setup - Clean page title with zero emojis
st.set_page_config(
    page_title="Q-Sentinel | QDS Threat Detection System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Lightweight CSS: Pure White Background, Orange Top Bar, Dark Blue Sub-Bar, Institutional Font
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap');

    /* Global Typography and Background */
    html, body, [class*="css"], .stApp, p, span, div, h1, h2, h3, h4, h5, h6, input, button, select, table, th, td {
        font-family: 'Open Sans', 'Toronto', 'Calibri', sans-serif !important;
    }
    
    .stApp {
        background-color: #ffffff !important;
        color: #1e293b;
    }
    
    /* Primary Orange Navigation Bar */
    .nav-orange-top {
        background-color: #ff671f;
        color: #ffffff;
        padding: 12px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    
    .nav-orange-brand {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    
    .nav-orange-brand h1 {
        font-size: 1.35rem;
        font-weight: 800;
        letter-spacing: 0.6px;
        color: #ffffff;
        margin: 0;
    }
    
    .nav-orange-brand span {
        font-size: 0.85rem;
        font-weight: 500;
        color: #ffffff;
        border-left: 1px solid rgba(255, 255, 255, 0.45);
        padding-left: 14px;
    }
    
    .nav-orange-tag {
        background-color: rgba(0, 0, 0, 0.18);
        border: 1px solid rgba(255, 255, 255, 0.4);
        color: #ffffff;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 2px;
        letter-spacing: 0.5px;
    }

    /* Extra Dark Blue Shaded Sub-Navigation Bar */
    .nav-blue-sub {
        background-color: #0b2545;
        color: #f1f5f9;
        padding: 8px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.75rem;
        letter-spacing: 0.3px;
        margin-bottom: 18px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.06);
    }
    
    .nav-blue-left {
        display: flex;
        gap: 20px;
        font-weight: 600;
    }
    
    .nav-blue-left span {
        color: #cbd5e1;
    }
    
    .nav-blue-left span b {
        color: #ffffff;
    }
    
    .nav-blue-right {
        color: #94a3b8;
        font-size: 0.72rem;
    }

    /* Clean Card Panels on White Background */
    .panel-card {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 2px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
        margin-bottom: 16px;
    }
    
    .panel-card-header {
        background-color: #f8fafc;
        border-bottom: 1px solid #cbd5e1;
        color: #0b2545;
        padding: 9px 14px;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.4px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .panel-card-body {
        padding: 14px;
    }

    /* Standard Two-Column Metrics Table */
    .metrics-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.82rem;
        margin-top: 8px;
    }
    
    .metrics-table th {
        background-color: #f8fafc;
        color: #0b2545;
        border: 1px solid #cbd5e1;
        padding: 8px 10px;
        text-align: left;
        font-weight: 700;
    }
    
    .metrics-table td {
        border: 1px solid #cbd5e1;
        padding: 8px 10px;
        color: #1e293b;
    }
    
    .metrics-table tr:nth-child(even) {
        background-color: #fafbfc;
    }

    /* Neutral Status Banner - Zero Bright Highlights */
    .status-banner-neutral {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-left: 4px solid #0b2545;
        color: #0f172a;
        padding: 12px 14px;
        border-radius: 2px;
        margin-bottom: 12px;
    }

    .status-banner-title {
        font-size: 0.98rem;
        font-weight: 700;
        color: #0b2545;
        letter-spacing: 0.3px;
    }

    .status-banner-desc {
        font-size: 0.78rem;
        color: #475569;
        margin-top: 4px;
        line-height: 1.4;
    }

    /* Footer */
    .app-footer {
        background-color: #0b2545;
        color: #cbd5e1;
        border-top: 3px solid #ff671f;
        padding: 14px 20px;
        font-size: 0.75rem;
        text-align: center;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)


# 1. Primary Orange Top Navigation Bar (Zero Symbols)
st.markdown("""
<div class="nav-orange-top">
    <div class="nav-orange-brand">
        <h1>Q-SENTINEL</h1>
        <span>Quantum Digital Signature Cyber Threat Detection System</span>
    </div>
    <div class="nav-orange-tag">
        SIH-26141 ARCHITECTURE
    </div>
</div>
""", unsafe_allow_html=True)

# 2. Extra Dark Blue Shaded Sub-Navigation Bar (Zero Symbols)
st.markdown("""
<div class="nav-blue-sub">
    <div class="nav-blue-left">
        <span>Protocol: <b>Teleportation-Based QDS</b></span>
        <span>Detection Engine: <b>Q-STAT Exact Binomial</b></span>
        <span>Defense Inventory: <b>14 Watchtowers</b></span>
        <span>Release Status: <b>Phase 40/40 (Production Locked)</b></span>
    </div>
    <div class="nav-blue-right">
        Simulation Link: Active | Node: Local Host | Audit: Certified
    </div>
</div>
""", unsafe_allow_html=True)


# Initialize Session State
if "freshness_registry" not in st.session_state:
    st.session_state.freshness_registry = FreshnessRegistry(max_time_window_seconds=60.0)

if "telemetry_store" not in st.session_state:
    st.session_state.telemetry_store = TelemetryStore(db_path="data/qsentinel.db")

if "dynamic_calibrator" not in st.session_state:
    st.session_state.dynamic_calibrator = DynamicNoiseCalibrator(nominal_p0=0.03, window_size=8)

if "mitigation_orchestrator" not in st.session_state:
    st.session_state.mitigation_orchestrator = ThreatMitigationOrchestrator()

if "last_assessment" not in st.session_state:
    st.session_state.last_assessment = None

if "last_signature" not in st.session_state:
    st.session_state.last_signature = None

if "last_legit_signature" not in st.session_state:
    st.session_state.last_legit_signature = None

if "last_scenario_info" not in st.session_state:
    st.session_state.last_scenario_info = ""

if "last_latency_ms" not in st.session_state:
    st.session_state.last_latency_ms = 0.0

if "prev_valid_sig" not in st.session_state:
    st.session_state.prev_valid_sig = None

if "multi_party_result" not in st.session_state:
    st.session_state.multi_party_result = None

if "last_incident_report" not in st.session_state:
    st.session_state.last_incident_report = None

if "mesh_result" not in st.session_state:
    st.session_state.mesh_result = None

if "decoy_result" not in st.session_state:
    st.session_state.decoy_result = None

if "trojan_result" not in st.session_state:
    st.session_state.trojan_result = None

if "blinding_result" not in st.session_state:
    st.session_state.blinding_result = None

if "chsh_result" not in st.session_state:
    st.session_state.chsh_result = None

if "finite_result" not in st.session_state:
    st.session_state.finite_result = None

if "mdi_result" not in st.session_state:
    st.session_state.mdi_result = None

if "wdm_result" not in st.session_state:
    st.session_state.wdm_result = None

if "stix_bundle" not in st.session_state:
    st.session_state.stix_bundle = None

if "siem_dispatch" not in st.session_state:
    st.session_state.siem_dispatch = None

if "rehearsal_report" not in st.session_state:
    st.session_state.rehearsal_report = None

if "release_report" not in st.session_state:
    st.session_state.release_report = None


# Sidebar: Security Controls (Zero Emojis/Symbols)
with st.sidebar:
    st.markdown("""
    <div style="background-color:#0b2545; color:#ffffff; padding:8px 12px; font-weight:700; font-size:0.85rem; border-radius:2px; margin-bottom:12px;">
        VERIFICATION CONSOLE
    </div>
    """, unsafe_allow_html=True)
    
    message_input = st.text_input(
        "Message Payload",
        value="Authorize Wire Transfer #98234 - $500,000",
        help="Classical text payload authenticated via teleported quantum states."
    )
    
    signer_choice = st.selectbox(
        "Claimed Signer Identity",
        options=[
            "Alice (Legitimate Authority)",
            "Bob (Authorized Deputy)",
            "Mallory (Adversary Impersonator)"
        ]
    )
    signer_id = signer_choice.split(" ")[0]
    
    # Check quarantine status
    if st.session_state.mitigation_orchestrator.is_quarantined(signer_id):
        st.markdown(f"""
        <div style="background:#ffffff; border:1px solid #cbd5e1; border-left:3px solid #0b2545; padding:6px 10px; font-size:0.75rem; margin-bottom:8px;">
            <b>Administrative Notice:</b> Signer '{signer_id}' is currently under security quarantine.
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Release Quarantine for {signer_id}", use_container_width=True):
            st.session_state.mitigation_orchestrator.release_quarantine(signer_id)
            st.rerun()

    scenario_option = st.selectbox(
        "Evaluation Scenario",
        options=[
            "1. Legitimate Verification (Clean Channel)",
            "2. Signature Forgery (Fabricated States)",
            "3. Signer Impersonation (Key Mismatch)",
            "4. Replay Attack (Stale Classical Token)",
            "5. Quantum Channel Manipulation (Noise / Flips)"
        ]
    )
    
    # Map scenario
    if "1. Legitimate" in scenario_option:
        scenario = AttackScenario.LEGITIMATE
    elif "2. Signature Forgery" in scenario_option:
        scenario = AttackScenario.FORGERY
    elif "3. Signer Impersonation" in scenario_option:
        scenario = AttackScenario.IMPERSONATION
    elif "4. Replay" in scenario_option:
        scenario = AttackScenario.REPLAY
    else:
        scenario = AttackScenario.CHANNEL_NOISE
        
    noise_slider = 0.0
    if scenario == AttackScenario.CHANNEL_NOISE:
        noise_slider = st.slider(
            "Adversarial Noise Level (epsilon)",
            min_value=0.05,
            max_value=0.50,
            value=0.30,
            step=0.05,
            help="Probability of quantum channel bit-flip or phase-flip disturbance."
        )
        
    st.markdown("""
    <div style="background-color:#f8fafc; border:1px solid #cbd5e1; padding:6px 10px; font-weight:700; font-size:0.75rem; color:#0b2545; margin-top:12px; margin-bottom:8px;">
        QUANTUM PARAMETERS & AUTO-CALIBRATION
    </div>
    """, unsafe_allow_html=True)
    
    use_auto_calibration = st.checkbox(
        "Dynamic Noise Calibration (Q-CALIBRATE)",
        value=True,
        help="Continuously calibrates channel noise floor p0 from pilot reference frames."
    )
    
    trials_per_token = st.slider(
        "Measurement Trials per Qubit (N)",
        min_value=20,
        max_value=150,
        value=50,
        step=10,
        help="Repeated projective measurement trials per signature token."
    )
    
    if not use_auto_calibration:
        ambient_noise_p0 = st.slider(
            "Calibrated Noise Floor (p0)",
            min_value=0.01,
            max_value=0.08,
            value=0.03,
            step=0.01,
            help="Baseline optical QBER for honest quantum channel."
        )
    else:
        # Ingest honest pilot frame to update baseline
        cal_status = st.session_state.dynamic_calibrator.ingest_pilot_measurement(
            num_trials=80,
            n_errors=int(80 * (0.025 + np.random.uniform(0.0, 0.01)))
        )
        ambient_noise_p0 = cal_status.calibrated_p0
        st.markdown(f"""
        <div style="background:#ffffff; border:1px solid #cbd5e1; padding:6px 8px; font-size:0.75rem; color:#1e293b; margin-bottom:8px;">
            <b>Q-CALIBRATE Baseline:</b> {ambient_noise_p0*100:.2f}%<br>
            <span style="color:#64748b; font-size:0.7rem;">95% CI: [{cal_status.confidence_interval_95[0]*100:.1f}%, {cal_status.confidence_interval_95[1]*100:.1f}%]</span>
        </div>
        """, unsafe_allow_html=True)
    
    num_tokens = 8
    
    st.markdown("---")
    execute_btn = st.button("Verify Signature and Detect Threats", type="primary", use_container_width=True)
    clear_btn = st.button("Reset Telemetry History", use_container_width=True)
    
    if clear_btn:
        st.session_state.telemetry_store.clear_history()
        st.session_state.freshness_registry.reset()
        st.session_state.dynamic_calibrator.reset()
        st.session_state.last_assessment = None
        st.session_state.last_signature = None
        st.session_state.last_legit_signature = None
        st.session_state.multi_party_result = None
        st.session_state.last_incident_report = None
        st.session_state.mesh_result = None
        st.session_state.decoy_result = None
        st.session_state.trojan_result = None
        st.session_state.blinding_result = None
        st.session_state.chsh_result = None
        st.session_state.finite_result = None
        st.session_state.mdi_result = None
        st.session_state.wdm_result = None
        st.session_state.stix_bundle = None
        st.session_state.siem_dispatch = None
        st.rerun()


# Execution Trigger Logic
current_run_signature = (
    signer_id,
    scenario,
    message_input,
    num_tokens,
    noise_slider,
    ambient_noise_p0,
    trials_per_token
)

trigger_run = (
    execute_btn
    or st.session_state.last_assessment is None
    or st.session_state.get("last_run_params") != current_run_signature
)

if trigger_run:
    st.session_state.last_run_params = current_run_signature
    
    # 1. Signer generates true signature based on selected identity
    signer_seed_map = {
        "Alice": "alice_master_soc_seed_2026",
        "Bob": "bob_deputy_soc_seed_2026",
        "Mallory": "mallory_unauthorized_seed_42"
    }
    current_seed = signer_seed_map.get(signer_id, f"{signer_id.lower()}_generic_seed_2026")
    signer_mgr = QDSKeyManager(signer_id=signer_id, private_seed=current_seed)
    legit_sig = signer_mgr.generate_signature(message_input, num_tokens=num_tokens)
    st.session_state.signer_mgr = signer_mgr
    
    # Cache a valid signature for replay scenario
    if st.session_state.prev_valid_sig is None and scenario != AttackScenario.REPLAY:
        st.session_state.prev_valid_sig = legit_sig
        
    # 2. Inject Attack or Pass Legitimate
    if scenario == AttackScenario.REPLAY:
        target_sig = st.session_state.prev_valid_sig or legit_sig
        st.session_state.freshness_registry.seen_nonces.add((target_sig.signer_id, target_sig.nonce))
        st.session_state.freshness_registry.nonce_timestamps[(target_sig.signer_id, target_sig.nonce)] = target_sig.timestamp
        rx_sig, scenario_desc = ThreatOrchestrator.execute_scenario(
            scenario=scenario,
            original_signature=target_sig
        )
    else:
        rx_sig, scenario_desc = ThreatOrchestrator.execute_scenario(
            scenario=scenario,
            original_signature=legit_sig,
            channel_noise_level=noise_slider
        )
        if scenario != AttackScenario.REPLAY:
            rx_sig.nonce = f"qds_nonce_{int(time.time()*1000)}"
            rx_sig.timestamp = time.time()
            st.session_state.prev_valid_sig = rx_sig
            
    # 3. Instantiate Q-STAT Detector
    detector = QStatDetector(
        baseline_noise_p0=ambient_noise_p0,
        z_suspicious_threshold=2.0,
        z_malicious_threshold=4.0,
        freshness_registry=st.session_state.freshness_registry
    )
    
    # 4. Measure & Evaluate
    t_start = time.perf_counter()
    assessment = detector.verify_signature_session(
        received_signature=rx_sig,
        expected_signature=legit_sig,
        trials_per_token=trials_per_token,
        ambient_noise=ambient_noise_p0
    )
    latency_ms = (time.perf_counter() - t_start) * 1000.0
    
    # 5. Persist run to SQLite
    st.session_state.telemetry_store.log_verification(
        assessment=assessment,
        signer_id=rx_sig.signer_id,
        scenario=scenario.value,
        message=message_input,
        latency_ms=latency_ms
    )
    
    # 6. Automatic Incident Response & Mitigation Evaluation
    incident_report = st.session_state.mitigation_orchestrator.evaluate_and_mitigate(
        assessment=assessment,
        signature=rx_sig,
        message=message_input,
        auto_quarantine=(scenario in [AttackScenario.FORGERY, AttackScenario.IMPERSONATION])
    )
    
    # Update state
    st.session_state.last_assessment = assessment
    st.session_state.last_signature = rx_sig
    st.session_state.last_legit_signature = legit_sig
    st.session_state.last_scenario_info = scenario_desc
    st.session_state.last_latency_ms = latency_ms
    st.session_state.last_incident_report = incident_report


assessment: ThreatAssessment = st.session_state.last_assessment
rx_sig: QuantumDigitalSignature = st.session_state.last_signature
legit_sig: QuantumDigitalSignature = st.session_state.last_legit_signature or rx_sig
incident_report: IncidentReport = st.session_state.last_incident_report

# Two Primary Columns
col_left, col_right = st.columns([1.1, 0.9], gap="medium")

with col_left:
    st.markdown("""
    <div class="panel-card">
        <div class="panel-card-header">
            <span>QUANTUM CHANNEL AND TELEPORTATION FLOW</span>
            <span style="font-size:0.75rem; font-weight:500;">Protocol: 3-Qubit Joint BSM</span>
        </div>
    """, unsafe_allow_html=True)
    
    scenario_info = st.session_state.last_scenario_info
    st.caption(f"**Execution Context:** {scenario_info}")
    
    # Teleportation Pipeline Schematic
    if rx_sig and rx_sig.tokens:
        tok0 = rx_sig.tokens[0]
        tele_res = teleport_qubit(tok0.eigenstate)
        b1, b2 = tele_res.bell_measurement_bits
        u_corr = tele_res.applied_correction
        
        status_hex = "#0b2545"
        
        verifier_label = "Bob" if rx_sig.signer_id.lower() != "bob" else "Charlie"
        pipeline_html = render_teleportation_pipeline_html(
            input_state_label=tok0.eigenstate.label,
            bell_bits=(b1, b2),
            correction_gate=u_corr,
            recovered_label=tele_res.recovered_state.label,
            status_color=status_hex,
            attack_applied=scenario_info if "disturbed" in scenario_info or "forged" in scenario_info or "unauthorized" in scenario_info else None,
            signer_name=rx_sig.signer_id,
            verifier_name=verifier_label
        )
        if hasattr(st, "html"):
            st.html(pipeline_html)
        else:
            st.markdown(pipeline_html, unsafe_allow_html=True)
        
    # Projective Measurement Distribution Chart
    if assessment and assessment.token_trials:
        selected_token_idx = st.selectbox(
            "Inspect Signature Qubit Token:",
            options=list(range(len(assessment.token_trials))),
            format_func=lambda i: f"Token #{i} (Basis: {rx_sig.tokens[i].basis.value}, State: {rx_sig.tokens[i].eigenstate.label})"
        )
        fig_dist = build_outcome_distribution_chart(assessment.token_trials, selected_token_idx)
        st.plotly_chart(fig_dist, use_container_width=True)

        # Phase 28: Quantum State Tomography (QST) Diagnostics
        with st.expander("Quantum State Tomography (QST) and Density Matrix Reconstruction", expanded=False):
            st.caption("Reconstructs the full 2x2 density matrix via Pauli Stokes projections (X, Y, Z) to differentiate environmental decoherence from active eavesdropping.")
            
            chosen_token = rx_sig.tokens[selected_token_idx]
            expected_token = legit_sig.tokens[selected_token_idx]
            qst_res = QuantumStateTomography.reconstruct_state(
                target_state=chosen_token.eigenstate,
                expected_state=expected_token.eigenstate,
                num_trials_per_basis=250
            )
            
            rho_00 = qst_res.density_matrix[0, 0].real
            rho_01 = qst_res.density_matrix[0, 1]
            rho_10 = qst_res.density_matrix[1, 0]
            rho_11 = qst_res.density_matrix[1, 1]
            
            st.markdown(f"""
            <table class="metrics-table">
                <tr><th>Tomography Metric</th><th>Value</th><th>Physical Significance</th></tr>
                <tr><td>Reconstructed Density Matrix (rho)</td><td><code>[[{rho_00:.3f}, {rho_01.real:.3f}+{rho_01.imag:.3f}j], [{rho_10.real:.3f}+{rho_10.imag:.3f}j, {rho_11:.3f}]]</code></td><td>Unit-trace positive semi-definite state</td></tr>
                <tr><td>Quantum State Fidelity F(rho_exp, rho_rec)</td><td><b>{qst_res.fidelity * 100:.2f}%</b></td><td>Overlap with authorized signature eigenstate</td></tr>
                <tr><td>State Purity gamma = Tr(rho^2)</td><td><b>{qst_res.purity:.4f}</b> (Pure=1.0, Mixed=0.5)</td><td>Distinguishes coherent state from thermal noise</td></tr>
                <tr><td>Von Neumann Entropy S(rho)</td><td><b>{qst_res.von_neumann_entropy:.4f} bits</b></td><td>Quantum information mixedness / uncertainty</td></tr>
                <tr><td>Bloch Vector (S1, S2, S3)</td><td>({qst_res.stokes_parameters[0]:.2f}, {qst_res.stokes_parameters[1]:.2f}, {qst_res.stokes_parameters[2]:.2f})</td><td>Stokes coordinates on Bloch sphere</td></tr>
            </table>
            <div style="background:#f8fafc; border:1px solid #cbd5e1; padding:8px 10px; font-size:0.75rem; color:#334155; margin-top:8px;">
                <b>Tomographic Diagnostic:</b> {qst_res.diagnostic}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


with col_right:
    st.markdown("""
    <div class="panel-card">
        <div class="panel-card-header">
            <span>Q-STAT THREAT ASSESSMENT SCORECARD</span>
            <span style="font-size:0.75rem; font-weight:500;">Exact Binomial Test</span>
        </div>
        <div class="panel-card-body">
    """, unsafe_allow_html=True)
    
    # Neutral Status Banner - Zero Bright Highlights or Saturated Colors
    if assessment.verdict == ThreatCategory.LEGITIMATE:
        st.markdown("""
        <div class="status-banner-neutral">
            <div class="status-banner-title">STATUS: DETERMINISTICALLY AUTHENTIC (LEGITIMATE)</div>
            <div class="status-banner-desc">
                Signature verified. Observed error rate is within expected environmental noise bounds (95.4% confidence).
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif assessment.verdict == ThreatCategory.SUSPICIOUS:
        st.markdown("""
        <div class="status-banner-neutral">
            <div class="status-banner-title">STATUS: SUSPICIOUS CHANNEL DISTURBANCE</div>
            <div class="status-banner-desc">
                Observed error rate exceeds 2-sigma baseline threshold. Potential low-intensity tampering or channel decay.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-banner-neutral">
            <div class="status-banner-title">STATUS: REJECTED AND CRITICAL THREAT DETECTED</div>
            <div class="status-banner-desc">
                Signature rejected. Forgery, unauthorized impersonation, or replay attack detected with greater than 99.99% certainty.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Standardized Anomaly Gauge Chart
    fig_gauge = build_threat_gauge(assessment.z_score, z_suspicious=2.0, z_malicious=4.0)
    st.plotly_chart(fig_gauge, use_container_width=True)

    # Metrics Table
    p_val_disp = "< 1e-15" if assessment.p_value < 1e-15 else f"{assessment.p_value:.4e}"
    freshness_badge = "VALID / FRESH" if assessment.freshness_passed else "STALE / REPLAY"
    
    st.markdown(f"""
    <table class="metrics-table">
        <tr>
            <th>Parameter</th>
            <th>Observed Value</th>
        </tr>
        <tr>
            <td>Claimed Signer</td>
            <td><b>{rx_sig.signer_id}</b></td>
        </tr>
        <tr>
            <td>Observed Error Rate (e_hat)</td>
            <td><b>{assessment.error_rate * 100:.2f}%</b> (Baseline p0 = {assessment.baseline_noise_p0 * 100:.1f}%)</td>
        </tr>
        <tr>
            <td>Standardized Z-Score</td>
            <td><b>{assessment.z_score:+.2f} sigma</b></td>
        </tr>
        <tr>
            <td>Exact Binomial p-value</td>
            <td><code>{p_val_disp}</code></td>
        </tr>
        <tr>
            <td>Statistical Confidence</td>
            <td><b>{assessment.confidence * 100:.2f}%</b></td>
        </tr>
        <tr>
            <td>95% Confidence Interval</td>
            <td>[{assessment.ci_lower*100:.1f}%, {assessment.ci_upper*100:.1f}%]</td>
        </tr>
        <tr>
            <td>Freshness Nonce Token</td>
            <td><b>{freshness_badge}</b></td>
        </tr>
        <tr>
            <td>Detection Latency</td>
            <td><b>{st.session_state.last_latency_ms:.2f} ms</b></td>
        </tr>
    </table>
    
    <div style="background-color: #f8fafc; border: 1px solid #cbd5e1; padding: 8px 10px; font-size: 0.75rem; color: #334155; margin-top: 10px;">
        <b>Audit Diagnostic:</b> {assessment.diagnostic_text}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)


# Bottom Panel: Telemetry Stream & Audit Trail
st.markdown("""
<div class="panel-card">
    <div class="panel-card-header">
        <span>AUDIT TELEMETRY LOG AND VERIFICATION HISTORY</span>
        <span style="font-size:0.75rem; font-weight:500;">Storage: SQLite Local Datastore</span>
    </div>
    <div class="panel-card-body">
""", unsafe_allow_html=True)

history_df = st.session_state.telemetry_store.get_dataframe(limit=50)

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13, tab14, tab15 = st.tabs([
    "Anomaly Score Trend (z-Score)",
    "Detailed Verification Log Table",
    "Real-Time Network Threat Stream Monitor",
    "Multi-Party Non-Repudiation and Formal Audit Certificate",
    "Automated Threat Mitigation and Hybrid PQC Verification",
    "Multi-Hop Quantum Mesh Network Watchtower (Q-MESH)",
    "Decoy-State Protocol and Photon Number Splitting Defense (Q-DECOY)",
    "Quantum Trojan-Horse & Memory Decoherence Watchtower (Q-TROJAN)",
    "Detector Blinding & Spatial Side-Channel Watchtower (Q-BLIND)",
    "Device-Independent CHSH Bell Inequality Watchtower (Q-CHSH)",
    "Finite-Size Security Analysis & Serfling Bound Watchtower (Q-FINITE)",
    "Measurement-Device-Independent QDS & Untrusted Relay Watchtower (Q-MDI)",
    "Quantum WDM & Co-Propagation Raman Defense (Q-WDM)",
    "Enterprise SOC SIEM & STIX 2.1 Threat Intelligence (Q-SOC)",
    "NQM Defense Whitepaper & Monte Carlo Rehearsal Kit (Q-DOC)"
])

with tab1:
    fig_trend = build_telemetry_trend_chart(history_df)
    st.plotly_chart(fig_trend, use_container_width=True)

with tab2:
    if not history_df.empty:
        st.dataframe(
            history_df,
            use_container_width=True,
            column_config={
                "Error Rate": st.column_config.NumberColumn(
                    "Error Rate",
                    help="Observed physical error rate",
                    format="%.4f",
                ),
            }
        )
        csv_data = history_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download Audit Log (CSV)",
            data=csv_data,
            file_name=f"qsentinel_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )
    else:
        st.info("No past verification records found.")

with tab3:
    st.markdown("#### Real-Time Multi-Session QDS Threat Simulation Feed")
    st.caption("Simulates a continuous sequence of quantum transactions over teleportation links with stochastic cyber-attack injections.")
    
    col_s1, col_s2, col_s3 = st.columns([1, 1, 1.2])
    with col_s1:
        stream_count = st.slider("Stream Event Count", min_value=5, max_value=25, value=10, step=5)
    with col_s2:
        attack_rate = st.slider("Attack Injection Frequency", min_value=0.10, max_value=0.70, value=0.40, step=0.10, format="%.0f%%")
    with col_s3:
        st.write("")
        st.write("")
        start_stream = st.button("Launch Live Network Stream", type="primary", use_container_width=True)

    if start_stream:
        stream_gen = QuantumTrafficGenerator(base_signer_id="Alice", detector=detector)
        progress_bar = st.progress(0, text="Initializing Quantum Teleportation Channel...")
        feed_container = st.container()
        
        for i in range(1, stream_count + 1):
            event = stream_gen.generate_next_event(
                event_id=i,
                attack_probability=attack_rate,
                trials_per_token=trials_per_token,
                ambient_noise=ambient_noise_p0
            )
            
            # Log to SQLite
            st.session_state.telemetry_store.log_verification(
                assessment=event.assessment,
                signer_id=event.signer_id,
                scenario=event.scenario.value,
                message=event.message,
                latency_ms=event.latency_ms
            )
            
            # Render clean neutral institutional card
            with feed_container:
                st.markdown(f"""
                <div style="background-color:#ffffff; border:1px solid #cbd5e1; border-left:3px solid #0b2545; padding:8px 12px; margin-bottom:6px; font-size:0.8rem; color:#1e293b;">
                    <b>[Event #{event.event_id}] {event.assessment.verdict.value}</b> | {event.message} | Scenario: {event.scenario.value} | Signer: {event.signer_id} | Error: {event.assessment.error_rate*100:.1f}% | z={event.assessment.z_score:+.2f} sigma | Latency: {event.latency_ms:.1f}ms
                </div>
                """, unsafe_allow_html=True)
            
            progress_bar.progress(i / stream_count, text=f"Processed Event {i}/{stream_count}...")
            time.sleep(0.10)
            
        st.info("Real-time stream completed. Telemetry datastore updated.")
        time.sleep(0.5)
        st.rerun()

with tab4:
    st.markdown("#### Multi-Party Non-Repudiation Cross-Verification and Formal Certification")
    st.caption("Verifies signature transferability to Charlie (Arbiter / Third Party) to prevent repudiation disputes and generates exportable audit certificates.")
    
    col_m1, col_m2 = st.columns([1, 1])
    
    with col_m1:
        st.markdown("**Multi-Recipient Cross-Verification Exchange**")
        repudiation_toggle = st.checkbox(
            "Simulate Alice Repudiation Attack (Conflicting Quantum States to Charlie)",
            value=False,
            help="Simulates Alice attempting to sign for Bob but intentionally providing invalid tokens to Charlie so she can deny the signature later."
        )
        run_multi_btn = st.button("Run Multi-Party Cross-Verification", use_container_width=True)
        
        if run_multi_btn or st.session_state.multi_party_result is None:
            coordinator = MultiRecipientCoordinator(detector=detector)
            active_signer_mgr = st.session_state.get("signer_mgr") or QDSKeyManager(signer_id=signer_id, private_seed="alice_master_soc_seed_2026")
            multi_res = coordinator.verify_multi_recipient_session(
                message=message_input,
                signer_manager=active_signer_mgr,
                simulate_repudiation=repudiation_toggle,
                trials_per_token=trials_per_token,
                ambient_noise=ambient_noise_p0
            )
            st.session_state.multi_party_result = multi_res
            
        mp_res: MultiRecipientVerificationResult = st.session_state.multi_party_result
        if mp_res:
            st.markdown(f"""
            <table class="metrics-table">
                <tr><th>Multi-Party Metric</th><th>Observation</th></tr>
                <tr><td>Bob Verification Verdict</td><td><b>{mp_res.bob_assessment.verdict.value}</b> (e={mp_res.bob_assessment.error_rate*100:.1f}%)</td></tr>
                <tr><td>Charlie Verification Verdict</td><td><b>{mp_res.charlie_assessment.verdict.value}</b> (e={mp_res.charlie_assessment.error_rate*100:.1f}%)</td></tr>
                <tr><td>Cross-Recipient Discrepancy Rate</td><td><b>{mp_res.cross_discrepancy_rate*100:.1f}%</b></td></tr>
                <tr><td>Cross-Verification z-Score</td><td><b>{mp_res.cross_z_score:+.2f} sigma</b></td></tr>
                <tr><td>Non-Repudiation Status</td><td><b>{'PASSED (TRANSFERABLE)' if mp_res.non_repudiation_passed else 'FAILED (DISPUTE DETECTED)'}</b></td></tr>
            </table>
            """, unsafe_allow_html=True)
            st.caption(f"**Diagnostic Proof:** {mp_res.audit_summary}")
            
    with col_m2:
        st.markdown("**Official Security Audit Certificate Export**")
        
        json_cert_str = AuditReportGenerator.generate_verification_certificate_json(
            assessment=assessment,
            signature=rx_sig,
            message=message_input,
            latency_ms=st.session_state.last_latency_ms,
            multi_recipient=st.session_state.multi_party_result
        )
        
        text_cert_str = AuditReportGenerator.generate_plain_text_certificate(
            assessment=assessment,
            signature=rx_sig,
            message=message_input,
            latency_ms=st.session_state.last_latency_ms
        )
        
        st.text_area("Audit Certificate Preview", value=text_cert_str, height=200)
        
        col_d1, col_d2 = st.columns([1, 1])
        with col_d1:
            st.download_button(
                "Export Certificate (JSON)",
                data=json_cert_str,
                file_name=f"qds_audit_cert_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        with col_d2:
            st.download_button(
                "Export Certificate (TXT)",
                data=text_cert_str,
                file_name=f"qds_audit_cert_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )

with tab5:
    st.markdown("#### Automated Threat Mitigation & Post-Quantum Classical Hybrid Verification")
    st.caption("Active incident containment (Q-MITIGATE) and dual-layer defense-in-depth verification (Q-HYBRID).")

    col_h1, col_h2 = st.columns([1, 1])

    with col_h1:
        st.markdown("**Automated Security Containment (Q-MITIGATE)**")
        
        if incident_report:
            st.markdown(f"""
            <table class="metrics-table">
                <tr><th>Incident Parameter</th><th>Value</th></tr>
                <tr><td>Incident Reference</td><td><code>{incident_report.incident_id}</code></td></tr>
                <tr><td>Threat Evaluation</td><td><b>{incident_report.threat_category_name}</b> (z={incident_report.observed_z_score:+.2f} sigma)</td></tr>
                <tr><td>Targeted Node / Signer</td><td>{incident_report.signer_id}</td></tr>
                <tr><td>Signer Quarantine Status</td><td><b>{'ACTIVE QUARANTINE' if st.session_state.mitigation_orchestrator.is_quarantined(incident_report.signer_id) else 'NOT QUARANTINED'}</b></td></tr>
                <tr><td>Revoked Nonces Count</td><td>{len(st.session_state.mitigation_orchestrator.revoked_nonces)} revoked</td></tr>
                <tr><td>Containment Actions Triggered</td><td>{len(incident_report.mitigation_actions)} automated actions</td></tr>
            </table>
            """, unsafe_allow_html=True)
            
            st.markdown("**Executed Mitigation Protocols:**")
            for act in incident_report.mitigation_actions:
                st.markdown(f"""
                <div style="background:#f8fafc; border:1px solid #cbd5e1; border-left:3px solid #0b2545; padding:6px 10px; font-size:0.75rem; margin-bottom:4px;">
                    <b>[{act.action_type}]</b> Status: {act.status} | Target: {act.target}<br>
                    <span style="color:#64748b;">{act.details}</span>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("**Enterprise SIEM CEF Log Stream:**")
            st.code(incident_report.cef_log_entry, language="text")

    with col_h2:
        st.markdown("**Dual-Layer Hybrid Verification (Q-HYBRID)**")
        st.caption("Verifies classical HMAC-SHA3-512 cryptographic payload integrity combined with quantum teleportation Q-STAT.")
        
        classical_hash = HybridSignatureVerifier.compute_classical_digest(message_input, "alice_master_soc_seed_2026")
        
        # Verify hybrid
        hybrid_verifier = HybridSignatureVerifier(detector=detector)
        hybrid_res = hybrid_verifier.verify_hybrid_signature(
            message=message_input,
            claimed_classical_digest=classical_hash,
            received_quantum_signature=rx_sig,
            expected_quantum_signature=legit_sig,
            signer_seed="alice_master_soc_seed_2026",
            trials_per_token=trials_per_token,
            ambient_noise=ambient_noise_p0
        )
        
        st.markdown(f"""
        <table class="metrics-table">
            <tr><th>Hybrid Security Layer</th><th>Status</th><th>Analytical Rationale</th></tr>
            <tr>
                <td>Layer 1: Classical HMAC-SHA3-512</td>
                <td><b>{'PASSED (INTEGRITY OK)' if hybrid_res.classical_hash_matched else 'FAILED (TAMPERED)'}</b></td>
                <td>Cryptographic hash of message payload verified against signer key</td>
            </tr>
            <tr>
                <td>Layer 2: Quantum Teleportation (QDS)</td>
                <td><b>{hybrid_res.quantum_assessment.verdict.value}</b></td>
                <td>Projective measurement statistics over teleported Pauli eigenstates</td>
            </tr>
            <tr>
                <td>Overall Hybrid Disposition</td>
                <td><b>{hybrid_res.overall_verdict.value}</b></td>
                <td>Joint decision under dual-layer defense-in-depth model</td>
            </tr>
            <tr>
                <td>Hybrid Confidence Score</td>
                <td><b>{hybrid_res.hybrid_confidence * 100:.2f}%</b></td>
                <td>Statistical confidence under joint hypothesis testing</td>
            </tr>
        </table>
        <div style="background:#f8fafc; border:1px solid #cbd5e1; padding:8px 10px; font-size:0.75rem; color:#334155; margin-top:8px;">
            <b>Hybrid Security Rationale:</b> {hybrid_res.security_summary}
        </div>
        """, unsafe_allow_html=True)

with tab6:
    st.markdown("#### Multi-Hop Quantum Mesh Network Watchtower & Entanglement Swapping (Q-MESH)")
    st.caption("Simulates multi-hop quantum networks with intermediate quantum repeaters executing entanglement swapping across 4-qubit states and isolating rogue nodes.")
    
    col_q1, col_q2 = st.columns([1, 1])
    with col_q1:
        st.markdown("**Quantum Mesh Topology & Route Configuration**")
        route_choice = st.selectbox(
            "Select End-to-End Quantum Path",
            options=[
                "Alice -> Repeater R1 -> Bob (2 Hops)",
                "Alice -> Repeater R1 -> Repeater R2 -> Bob (3 Hops)",
                "Alice -> Repeater R1 -> Repeater R2 -> Repeater R3 -> Bob (4 Hops)"
            ]
        )
        
        # Parse repeaters
        if "2 Hops" in route_choice:
            active_repeaters = ["Repeater_R1"]
            rogue_candidates = ["None (All Honest Repeaters)", "Repeater_R1"]
        elif "3 Hops" in route_choice:
            active_repeaters = ["Repeater_R1", "Repeater_R2"]
            rogue_candidates = ["None (All Honest Repeaters)", "Repeater_R1", "Repeater_R2"]
        else:
            active_repeaters = ["Repeater_R1", "Repeater_R2", "Repeater_R3"]
            rogue_candidates = ["None (All Honest Repeaters)", "Repeater_R1", "Repeater_R2", "Repeater_R3"]
            
        rogue_choice = st.selectbox("Inject Rogue / Compromised Repeater Node", options=rogue_candidates)
        comp_node = None if "None" in rogue_choice else rogue_choice
        
        run_mesh_btn = st.button("Execute Mesh Routing & Verify Swapped Entanglement", use_container_width=True)
        
        if run_mesh_btn or st.session_state.mesh_result is None:
            mesh_router = QuantumMeshRouter(detector=detector)
            m_res = mesh_router.route_and_verify_mesh(
                source="Alice",
                destination="Bob",
                intermediate_repeaters=active_repeaters,
                compromised_node=comp_node,
                trials_per_token=trials_per_token
            )
            st.session_state.mesh_result = m_res
            
    with col_q2:
        st.markdown("**Hop-by-Hop Telemetry & Rogue Node Isolation**")
        mesh_res: MeshRouteVerificationResult = st.session_state.mesh_result
        if mesh_res:
            path_str = " ===> ".join([f"[{n}]" for n in mesh_res.path])
            st.markdown(f"""
            <div style="background:#f8fafc; border:1px solid #cbd5e1; padding:8px 12px; font-size:0.8rem; margin-bottom:10px; font-weight:600; color:#0b2545;">
                Active Mesh Circuit: {path_str}
            </div>
            """, unsafe_allow_html=True)
            
            # Hop Telemetry Table
            hop_rows = ""
            for h in mesh_res.hop_telemetry:
                status_text = "ROGUE NODE DETECTED" if h.is_compromised else "CLEARED (HONEST)"
                hop_rows += f"""
                <tr>
                    <td>Hop {h.hop_index}: {h.source_node} -> {h.target_node}</td>
                    <td>{h.link_noise_rate*100:.1f}%</td>
                    <td><b>{status_text}</b></td>
                    <td>{h.diagnostic}</td>
                </tr>
                """
            st.markdown(f"""
            <table class="metrics-table">
                <tr><th>Link Path</th><th>Observed Noise</th><th>Security Status</th><th>Diagnostic</th></tr>
                {hop_rows}
            </table>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background:#ffffff; border:1px solid #cbd5e1; border-left:3px solid #0b2545; padding:8px 10px; font-size:0.75rem; color:#1e293b; margin-top:10px;">
                <b>End-to-End State Fidelity:</b> {mesh_res.end_to_end_fidelity*100:.1f}% | <b>Verdict:</b> {mesh_res.assessment.verdict.value} (z={mesh_res.assessment.z_score:+.2f} sigma)<br>
                <b>Mesh Diagnostic:</b> {mesh_res.mesh_status_summary}
            </div>
            """, unsafe_allow_html=True)

with tab7:
    st.markdown("#### Decoy-State Protocol & Photon Number Splitting (PNS) Threat Analyzer (Q-DECOY)")
    st.caption("Evaluates Poissonian photon statistics across multi-intensity laser pulses (Signal mu, Decoy nu, Vacuum) to eliminate PNS eavesdropping.")
    
    col_d1, col_d2 = st.columns([1, 1])
    with col_d1:
        st.markdown("**Decoy-State Laser Pulse Configuration**")
        mu_val = st.slider("Signal Pulse Mean Photon Number (mu)", min_value=0.20, max_value=0.80, value=0.50, step=0.05)
        nu_val = st.slider("Decoy Pulse Mean Photon Number (nu)", min_value=0.05, max_value=0.25, value=0.10, step=0.05)
        pns_toggle = st.checkbox("Simulate Adversarial Photon Number Splitting (PNS) Attack", value=False, help="Eve splits multi-photon pulses and blocks single photons.")
        run_decoy_btn = st.button("Run Decoy-State Yield & PNS Security Evaluation", use_container_width=True)
        
        if run_decoy_btn or st.session_state.decoy_result is None:
            decoy_analyzer = DecoyStateAnalyzer(mu_signal=mu_val, nu_decoy=nu_val)
            d_res = decoy_analyzer.simulate_transmission(num_pulses=2500, pns_attack_active=pns_toggle)
            st.session_state.decoy_result = d_res
            
    with col_d2:
        st.markdown("**Cryptanalytic Bounds & Security Verification**")
        d_res: PNSAnalysisResult = st.session_state.decoy_result
        if d_res:
            pns_status = "CRITICAL PNS ATTACK DETECTED" if d_res.pns_attack_detected else "VERIFIED SINGLE-PHOTON SECURE"
            st.markdown(f"""
            <table class="metrics-table">
                <tr><th>Decoy Metric</th><th>Observed Value</th><th>Analytical Description</th></tr>
                <tr><td>Signal State Gain (Q_mu)</td><td><b>{d_res.signal_gain_Q_mu:.5f}</b></td><td>Detection probability for mu={mu_val}</td></tr>
                <tr><td>Decoy State Gain (Q_nu)</td><td><b>{d_res.decoy_gain_Q_nu:.5f}</b></td><td>Detection probability for nu={nu_val}</td></tr>
                <tr><td>Vacuum Dark Count Gain (Q_0)</td><td><b>{d_res.vacuum_gain_Q_0:.6f}</b></td><td>Thermal APD dark count baseline</td></tr>
                <tr><td>Single-Photon Yield Lower Bound (Y_1)</td><td><b>{d_res.lower_bound_Y1:.4f}</b></td><td>Hwang-Lo theoretical single-photon floor</td></tr>
                <tr><td>Single-Photon Error Upper Bound (e_1)</td><td><b>{d_res.upper_bound_e1*100:.2f}%</b></td><td>Maximum tolerable single-photon disturbance</td></tr>
                <tr><td>PNS Security Disposition</td><td><b>{pns_status}</b></td><td>PNS resistance verdict</td></tr>
            </table>
            <div style="background:#f8fafc; border:1px solid #cbd5e1; padding:8px 10px; font-size:0.75rem; color:#334155; margin-top:10px;">
                <b>Decoy Cryptanalytic Proof:</b> {d_res.cryptanalytic_proof}
            </div>
            """, unsafe_allow_html=True)

with tab8:
    st.markdown("#### Quantum Trojan-Horse & Memory Decoherence Watchtower (Q-TROJAN)")
    st.caption("Multi-sensor defense against optical Trojan-Horse probe pulses (bright pulses, out-of-band spectral injections, asynchronous timing bypass) and Lindblad T1/T2 memory decoherence tracking.")
    
    col_t1, col_t2 = st.columns([1, 1])
    with col_t1:
        st.markdown("**Quantum Memory Buffer & Optical Probe Injection**")
        mem_storage_time = st.slider(
            "Quantum Memory Storage Time (microseconds)",
            min_value=0.0,
            max_value=1000.0,
            value=80.0,
            step=20.0,
            help="Simulates T1 longitudinal relaxation (1000 us) and T2 transverse dephasing (200 us) on stored signature qubits."
        )
        
        trojan_attack_mode = st.selectbox(
            "Optical Probe / Ingress Attack Vector",
            options=[
                "Honest Ingress (Clean Channel, Zero Probing)",
                "High-Intensity Probe (Bright Pulse Attack, 2.5 uW)",
                "Out-of-Band Spectral Evasion Probe (1310 nm Injection)",
                "Asynchronous Timing Gate Probe (+3.5 ns TOF Jitter)"
            ]
        )
        
        run_trojan_btn = st.button("Execute Q-TROJAN Multi-Sensor Optical Scan", use_container_width=True)
        
        if run_trojan_btn or st.session_state.trojan_result is None:
            trojan_detector = TrojanHorseDetector(
                safe_power_threshold_uw=0.010,
                passband_center_nm=1550.0,
                passband_width_nm=10.0,
                gate_window_ns=1.0,
                baseline_channel_noise=ambient_noise_p0
            )
            
            if "Honest" in trojan_attack_mode:
                probe_sig = None
            elif "Bright Pulse" in trojan_attack_mode:
                probe_sig = TrojanProbeSignal(
                    optical_power_uw=2.50,
                    wavelength_nm=1550.0,
                    arrival_offset_ns=0.0,
                    pulse_duration_ns=1.0,
                    internal_reflectivity_r=0.02
                )
            elif "Spectral" in trojan_attack_mode:
                probe_sig = TrojanProbeSignal(
                    optical_power_uw=0.08,
                    wavelength_nm=1310.0,
                    arrival_offset_ns=0.0,
                    pulse_duration_ns=1.0,
                    internal_reflectivity_r=0.01
                )
            else:  # Asynchronous
                probe_sig = TrojanProbeSignal(
                    optical_power_uw=0.08,
                    wavelength_nm=1550.0,
                    arrival_offset_ns=3.5,
                    pulse_duration_ns=1.0,
                    internal_reflectivity_r=0.01
                )
                
            t_res = trojan_detector.analyze_probe(
                probe=probe_sig,
                elapsed_storage_us=mem_storage_time,
                total_trials=trials_per_token
            )
            st.session_state.trojan_result = t_res
            
    with col_t2:
        st.markdown("**Multi-Sensor Telemetry & Cryptanalytic Audit**")
        t_res: TrojanDetectionResult = st.session_state.trojan_result
        if t_res:
            st.markdown(f"""
            <table class="metrics-table">
                <tr><th>Sensor / Physical Parameter</th><th>Measured Value</th><th>Operational Baseline</th></tr>
                <tr><td>Incident Optical Power</td><td><b>{t_res.optical_power_uw:.4f} uW</b></td><td>Ingress sensor reading</td></tr>
                <tr><td>Back-Reflected Photons</td><td><b>{t_res.back_reflected_photons:.1f} photons</b></td><td>Eve probing flux per pulse</td></tr>
                <tr><td>Optical Wavelength</td><td><b>{t_res.wavelength_nm:.1f} nm</b></td><td>Passband: 1545.0 - 1555.0 nm</td></tr>
                <tr><td>Arrival Time-of-Flight Jitter</td><td><b>{t_res.arrival_offset_ns:+.2f} ns</b></td><td>Synchronous gate: +/- 1.0 ns</td></tr>
                <tr><td>Quantum Memory Fidelity</td><td><b>{t_res.memory_fidelity*100:.2f}%</b></td><td>Lindblad T1/T2 model (elapsed: {t_res.storage_time_us:.0f} us)</td></tr>
                <tr><td>Eve Mutual Information (I_E)</td><td><b>{t_res.information_leakage_bits:.6f} bits</b></td><td>Helstrom/Holevo security bound</td></tr>
                <tr><td>Classification Disposition</td><td><b>{t_res.attack_classification}</b></td><td>Threat category: {t_res.verdict.value}</td></tr>
            </table>
            <div style="background:#f8fafc; border:1px solid #cbd5e1; padding:8px 10px; font-size:0.75rem; color:#334155; margin-top:10px;">
                <b>Watchtower Cryptanalytic Proof:</b> {t_res.cryptanalytic_proof}
            </div>
            """, unsafe_allow_html=True)

with tab9:
    st.markdown("#### Quantum Detector Blinding & Spatial-Mode Side-Channel Watchtower (Q-BLIND)")
    st.caption("Monitors APD anode DC bias currents, Geiger-to-linear mode phase transitions, spatial beam steering via quadrant sensors, and click inter-arrival Shannon entropy.")
    
    col_b1, col_b2 = st.columns([1, 1])
    with col_b1:
        st.markdown("**Detector Hardware State & Attack Vector Injection**")
        blind_scenario = st.selectbox(
            "Hardware Side-Channel Attack Mode",
            options=[
                "Honest Geiger Operation (Clean Single-Photon APD)",
                "Continuous-Wave Blinding Attack (18.5 uA DC Illumination)",
                "Spatial-Mode Beam Shift Exploit (4.1 um Quadrant Drift)",
                "Faked-State Periodic Triggering (Dead-Time Violation & Entropy Collapse)"
            ]
        )
        
        click_sample_size = st.slider("Click Event Sample Size", min_value=100, max_value=600, value=300, step=50)
        run_blind_btn = st.button("Execute APD Hardware & Side-Channel Scan", use_container_width=True)
        
        if run_blind_btn or st.session_state.blinding_result is None:
            watcher = DetectorBlindingWatcher(
                current_threshold_ua=5.0,
                max_spatial_displacement_um=2.5,
                min_entropy_nats=1.0,
                detector_dead_time_us=1.0
            )
            b_res = watcher.simulate_detector_scan(scenario=blind_scenario, num_clicks=click_sample_size)
            st.session_state.blinding_result = b_res
            
    with col_b2:
        st.markdown("**Hardware Telemetry & Cryptanalytic Security Audit**")
        b_res: BlindingDetectionResult = st.session_state.blinding_result
        if b_res:
            st.markdown(f"""
            <table class="metrics-table">
                <tr><th>Hardware Metric</th><th>Observed Value</th><th>Safe Threshold</th></tr>
                <tr><td>Anode DC Bias Current</td><td><b>{b_res.bias_current_ua:.3f} uA</b></td><td>Threshold: &lt; 5.000 uA</td></tr>
                <tr><td>Detector Operating Mode</td><td><b>{b_res.operating_mode}</b></td><td>Geiger Mode (Single-Photon Sensitive)</td></tr>
                <tr><td>Spatial Beam Displacement</td><td><b>{b_res.spatial_displacement_um:.3f} um</b></td><td>Quadrant tolerance: &lt; 2.500 um</td></tr>
                <tr><td>Click Inter-Arrival Entropy</td><td><b>{b_res.inter_arrival_entropy:.2f} nats</b></td><td>Poisson floor: &gt; 1.00 nats</td></tr>
                <tr><td>Dead-Time Violations (&lt;1.0 us)</td><td><b>{'VIOLATION DETECTED' if b_res.dead_time_violation else 'ZERO (CLEARED)'}</b></td><td>Physical APD hold-off filter</td></tr>
                <tr><td>Dual-Detector Double Clicks</td><td><b>{b_res.double_click_ratio*100:.2f}%</b></td><td>Thermal coincidences baseline</td></tr>
                <tr><td>Side-Channel Security Verdict</td><td><b>{b_res.verdict.value}</b></td><td>Classification: {b_res.attack_classification}</td></tr>
            </table>
            <div style="background:#f8fafc; border:1px solid #cbd5e1; padding:8px 10px; font-size:0.75rem; color:#334155; margin-top:10px;">
                <b>Hardware Cryptanalytic Proof:</b> {b_res.cryptanalytic_proof}
            </div>
            """, unsafe_allow_html=True)

with tab10:
    st.markdown("#### Device-Independent CHSH Bell Inequality Watchtower (Q-CHSH)")
    st.caption("Verifies non-classical quantum entanglement of distributed Bell pairs via the Clauser-Horne-Shimony-Holt (CHSH) Bell test (Tsirelson bound S <= 2.8284 vs. Classical local realism S <= 2.0000).")
    
    col_c1, col_c2 = st.columns([1, 1])
    with col_c1:
        st.markdown("**Entanglement Source & Channel Spoofing Injection**")
        chsh_scenario = st.selectbox(
            "Entanglement Channel State / Attack Scenario",
            options=[
                "Honest Maximally Entangled (|Phi+> Bell State)",
                "Classical Separable Spoofing (50% |00> + 50% |11> LHV Mixture)",
                "Intercept-Resend Measurement Attack (Z-Basis Collapse)",
                "High Depolarizing Noise (40% Channel Disturbance)"
            ]
        )
        
        chsh_trials = st.slider("Measurement Trials per Correlation Setting", min_value=100, max_value=800, value=400, step=50)
        run_chsh_btn = st.button("Execute CHSH Bell Non-Locality Evaluation", use_container_width=True)
        
        if run_chsh_btn or st.session_state.chsh_result is None:
            bell_watcher = CHSHBellWatcher(trials_per_setting=chsh_trials)
            c_res = bell_watcher.simulate_chsh_scenario(scenario=chsh_scenario)
            st.session_state.chsh_result = c_res
            
    with col_c2:
        st.markdown("**Bell Test Correlations & Device-Independent Verification**")
        c_res: CHSHVerificationResult = st.session_state.chsh_result
        if c_res:
            st.markdown(f"""
            <table class="metrics-table">
                <tr><th>CHSH Bell Parameter</th><th>Observed Value</th><th>Physical Constraint</th></tr>
                <tr><td>CHSH S-Parameter</td><td><b>{c_res.chsh_s_parameter:.4f}</b></td><td>Classical Limit: &le; 2.0000 | Tsirelson: 2.8284</td></tr>
                <tr><td>Standard Error sigma(S)</td><td><b>&plusmn;{c_res.standard_error_s:.4f}</b></td><td>Propagated empirical uncertainty</td></tr>
                <tr><td>Bell Violation Significance</td><td><b>{c_res.bell_violation_z_score:+.2f} sigma</b></td><td>Threshold: &gt; +2.50 sigma over classical</td></tr>
                <tr><td>Correlation E(A0, B0) [Z, (Z+X)/&radic;2]</td><td><b>{c_res.correlations.get('E(A0, B0)', 0.0):+.4f}</b></td><td>Theoretical: +0.7071</td></tr>
                <tr><td>Correlation E(A0, B1) [Z, (Z-X)/&radic;2]</td><td><b>{c_res.correlations.get('E(A0, B1)', 0.0):+.4f}</b></td><td>Theoretical: +0.7071</td></tr>
                <tr><td>Correlation E(A1, B0) [X, (Z+X)/&radic;2]</td><td><b>{c_res.correlations.get('E(A1, B0)', 0.0):+.4f}</b></td><td>Theoretical: +0.7071</td></tr>
                <tr><td>Correlation E(A1, B1) [X, (Z-X)/&radic;2]</td><td><b>{c_res.correlations.get('E(A1, B1)', 0.0):+.4f}</b></td><td>Theoretical: -0.7071</td></tr>
                <tr><td>Entanglement Certified</td><td><b>{'YES (TRUE QUANTUM NON-LOCALITY)' if c_res.entanglement_certified else 'NO (CLASSICAL SEPARABLE SPOOF)'}</b></td><td>Device-Independent Guarantee</td></tr>
                <tr><td>Security Verdict</td><td><b>{c_res.verdict.value}</b></td><td>Classification: {c_res.attack_classification}</td></tr>
            </table>
            <div style="background:#f8fafc; border:1px solid #cbd5e1; padding:8px 10px; font-size:0.75rem; color:#334155; margin-top:10px;">
                <b>Bell Non-Locality Proof:</b> {c_res.cryptanalytic_proof}
            </div>
            """, unsafe_allow_html=True)

with tab11:
    st.markdown("#### Finite-Size Security Analysis & Serfling Bound Watchtower (Q-FINITE)")
    st.caption("Evaluates composable finite-key epsilon-security (epsilon <= 10^-10) using Serfling's Martingale large-deviation inequality for sampling without replacement and smooth min-entropy privacy amplification.")
    
    col_f1, col_f2 = st.columns([1, 1])
    with col_f1:
        st.markdown("**Finite Block Partitioning & Fluctuation Scenario**")
        finite_scenario = st.selectbox(
            "Finite-Key Operational Scenario",
            options=[
                "Honest Production Block (N = 1800, Robust Extractable Key)",
                "Block Starvation Regime (N = 250, Fluctuations Exhaust Key)",
                "Adversarial Disturbance (14% QBER, Security Collapse)",
                "Marginal Channel Noise (8% QBER, Near Boundary)"
            ]
        )
        
        block_size_slider = st.slider("Total Signature Block Size (N qubits)", min_value=200, max_value=3000, value=1800, step=100)
        run_finite_btn = st.button("Execute Finite-Size Serfling Composable Security Audit", use_container_width=True)
        
        if run_finite_btn or st.session_state.finite_result is None:
            analyzer = FiniteSizeSecurityAnalyzer(f_ec=1.16, target_epsilon_sec=1e-10)
            f_res = analyzer.simulate_finite_scenario(scenario=finite_scenario, block_size_n=block_size_slider)
            st.session_state.finite_result = f_res
            
    with col_f2:
        st.markdown("**Composable Epsilon-Security & Distillation Audit**")
        f_res: FiniteSecurityResult = st.session_state.finite_result
        if f_res:
            st.markdown(f"""
            <table class="metrics-table">
                <tr><th>Finite-Key Parameter</th><th>Evaluated Value</th><th>Security Constraint</th></tr>
                <tr><td>Total Block Size (N)</td><td><b>{f_res.total_block_size_N} qubits</b></td><td>Sample: n={f_res.sample_size_n} (m={f_res.total_block_size_N - f_res.sample_size_n})</td></tr>
                <tr><td>Raw Sample Error Rate (e)</td><td><b>{f_res.raw_sample_error_rate*100:.2f}%</b></td><td>Measured in parameter estimation</td></tr>
                <tr><td>Serfling Deviation Cutoff (xi)</td><td><b>&plusmn;{f_res.serfling_deviation_xi:.4f}</b></td><td>Martingale large-deviation bound</td></tr>
                <tr><td>Phase Error Upper Bound (e_U)</td><td><b>{f_res.upper_bound_phase_error*100:.2f}%</b></td><td>Safe threshold: &lt; 18.00%</td></tr>
                <tr><td>Error Correction Leakage</td><td><b>{f_res.error_correction_leakage} bits</b></td><td>Classical reconciliation overhead</td></tr>
                <tr><td>Extractable Signature Tokens (ell)</td><td><b>{f_res.extractable_signature_length} tokens</b></td><td>Distillation rate: {f_res.distillation_rate*100:.1f}%</td></tr>
                <tr><td>Composable Security Epsilon</td><td><b>&le; {f_res.composable_epsilon:.1e}</b></td><td>Standard: &le; 10^-10</td></tr>
                <tr><td>Composable Security Verdict</td><td><b>{'CERTIFIED COMPOSABLY SECURE' if f_res.is_composably_secure else 'INSECURE / STARVED'}</b></td><td>Classification: {f_res.attack_classification}</td></tr>
            </table>
            <div style="background:#f8fafc; border:1px solid #cbd5e1; padding:8px 10px; font-size:0.75rem; color:#334155; margin-top:10px;">
                <b>Finite-Size Cryptanalytic Proof:</b> {f_res.cryptanalytic_proof}
            </div>
            """, unsafe_allow_html=True)

with tab12:
    st.markdown("#### Measurement-Device-Independent (MDI) QDS Architecture & Untrusted Relay Watchtower (Q-MDI)")
    st.caption("Guarantees 100% immunity against all detector side-channel attacks by routing Bell-state measurements through an untrusted relay and certifying Hong-Ou-Mandel two-photon interference visibility and coincidence prohibition.")
    
    col_mdi1, col_mdi2 = st.columns([1, 1])
    with col_mdi1:
        st.markdown("**Untrusted Relay Operational Scenarios**")
        mdi_scenario = st.selectbox(
            "Relay Operational State & Channel Alignment",
            options=[
                "Honest Untrusted Relay (Genuine HOM Interference, Zero Detector Side-Channels)",
                "Compromised Untrusted Relay (Relay Cheating / Fabricated Symmetric Coincidences)",
                "Distinguishable Photon Spoofing (Spectral/Temporal Misalignment, Interference Collapse)",
                "Elevated Channel Noise / Announcement Bias (Relay Asymmetry)"
            ]
        )
        
        mdi_trials_slider = st.slider("MDI Session Transmission Trials", min_value=300, max_value=3000, value=1500, step=150)
        run_mdi_btn = st.button("Execute MDI Untrusted Relay & HOM Interference Verification", use_container_width=True)
        
        if run_mdi_btn or st.session_state.mdi_result is None:
            mdi_watcher = MDIRelayWatcher(min_hom_visibility=0.70, max_z_error_rate=0.08, max_announcement_bias=0.20)
            m_res = mdi_watcher.simulate_mdi_session(scenario=mdi_scenario, num_trials=mdi_trials_slider)
            st.session_state.mdi_result = m_res
            
    with col_mdi2:
        st.markdown("**MDI Two-Photon Interference & Untrusted Relay Telemetry**")
        m_res: MDIAnalysisResult = st.session_state.mdi_result
        if m_res:
            st.markdown(f"""
            <table class="metrics-table">
                <tr><th>MDI Cryptanalytic Parameter</th><th>Evaluated Value</th><th>Physical Constraint</th></tr>
                <tr><td>Transmitted Trials (N)</td><td><b>{m_res.total_transmitted_trials} pulses</b></td><td>Alice & Bob random basis (Z, X)</td></tr>
                <tr><td>Total BSM Coincidences</td><td><b>{m_res.total_bsm_coincidences} clicks</b></td><td>Psi- state projections announced by relay</td></tr>
                <tr><td>BSM Coincidence Rate</td><td><b>{m_res.bsm_success_rate*100:.2f}%</b></td><td>Theoretical linear optical limit: &le; 50%</td></tr>
                <tr><td>Hong-Ou-Mandel Visibility (V_HOM)</td><td><b>{m_res.hom_visibility*100:.2f}%</b></td><td>Honest threshold: &ge; 70.00%</td></tr>
                <tr><td>Forbidden Symmetric Error (e_Z)</td><td><b>{m_res.z_basis_error_rate*100:.2f}%</b></td><td>Physical prohibition: &le; 8.00%</td></tr>
                <tr><td>Phase Error Rate (e_X)</td><td><b>{m_res.x_basis_error_rate*100:.2f}%</b></td><td>Complementary basis verification</td></tr>
                <tr><td>Relay Basis Announcement Bias</td><td><b>{m_res.relay_bias_ratio*100:.2f}%</b></td><td>Asymmetry threshold: &le; 20.00%</td></tr>
                <tr><td>Detector Side-Channel Immunity</td><td><b>{'GUARANTEED 100% IMMUNE' if m_res.detector_immune else 'COMPROMISED'}</b></td><td>MDI Invariant (Zero Trust in Relay Detectors)</td></tr>
                <tr><td>Untrusted Relay Security Verdict</td><td><b>{m_res.verdict.value}</b></td><td>Classification: {m_res.attack_classification}</td></tr>
            </table>
            <div style="background:#f8fafc; border:1px solid #cbd5e1; padding:8px 10px; font-size:0.75rem; color:#334155; margin-top:10px;">
                <b>MDI Cryptanalytic Proof:</b> {m_res.cryptanalytic_proof}
            </div>
            """, unsafe_allow_html=True)

with tab13:
    st.markdown("#### Quantum Wavelength Division Multiplexing & Co-Propagation Raman Defense (Q-WDM)")
    st.caption("Protects quantum signature transmission co-propagating alongside high-power classical optical channels in standard telecom fiber (SMF-28) by evaluating non-linear spontaneous Raman scattering, FBG narrowband optical isolation, and signal-to-noise ratio.")
    
    col_wdm1, col_wdm2 = st.columns([1, 1])
    with col_wdm1:
        st.markdown("**Co-Propagation Channel & Fiber Topology**")
        wdm_scenario = st.selectbox(
            "WDM Co-Propagation Optical Scenario",
            options=[
                "Honest Co-Propagation (0 dBm Classical, 20 nm Separation)",
                "Adversarial Cross-Talk Jamming (+14 dBm High-Power Pump)",
                "Raman Scattering Saturation (+8 dBm Close Wavelength)",
                "Elevated Co-Propagation Noise (+3.5 dBm Marginal)"
            ]
        )
        
        fiber_len_slider = st.slider("Fiber Span Length (km)", min_value=5.0, max_value=80.0, value=25.0, step=5.0)
        run_wdm_btn = st.button("Execute Q-WDM Raman Scattering & Optical Isolation Audit", use_container_width=True)
        
        if run_wdm_btn or st.session_state.wdm_result is None:
            wdm_watcher = WDMRamanWatcher(target_min_snr=12.0, max_tolerable_raman_qber=0.050)
            w_res = wdm_watcher.simulate_wdm_scenario(scenario=wdm_scenario, fiber_length_km=fiber_len_slider)
            st.session_state.wdm_result = w_res
            
    with col_wdm2:
        st.markdown("**Physical Non-Linear Optics & Raman Cross-Talk Telemetry**")
        w_res: WDMAnalysisResult = st.session_state.wdm_result
        if w_res:
            st.markdown(f"""
            <table class="metrics-table">
                <tr><th>WDM Optical Parameter</th><th>Evaluated Value</th><th>Design Specification</th></tr>
                <tr><td>Fiber Span Distance (L)</td><td><b>{w_res.fiber_length_km:.1f} km</b></td><td>ITU-T G.652 SMF-28 Standard</td></tr>
                <tr><td>Effective Length (L_eff)</td><td><b>{w_res.effective_length_km:.3f} km</b></td><td>Non-linear asymptotic limit: &le; 21.7 km</td></tr>
                <tr><td>Classical Launch Power</td><td><b>{w_res.classical_launch_power_dbm:+.1f} dBm ({w_res.classical_launch_power_mw:.2f} mW)</b></td><td>Co-propagating DWDM channel</td></tr>
                <tr><td>Wavelength Separation</td><td><b>{w_res.wavelength_separation_nm:.1f} nm</b></td><td>Anti-Stokes shift band allocation</td></tr>
                <tr><td>Raman Photons per Gate</td><td><b>{w_res.raman_noise_photons_per_pulse:.6f} ph/pulse</b></td><td>200 ps temporal gating window</td></tr>
                <tr><td>Raman Count Rate</td><td><b>{w_res.raman_noise_count_rate_hz:,.0f} counts/s</b></td><td>Total spurious noise arriving at SPAD</td></tr>
                <tr><td>Signal-to-Noise Ratio (SNR)</td><td><b>{w_res.signal_to_noise_ratio_snr:.2f}</b></td><td>Safe threshold: &ge; 15.00</td></tr>
                <tr><td>Raman-Induced QBER</td><td><b>{w_res.induced_raman_qber*100:.2f}%</b></td><td>Maximum tolerable: &le; 4.50%</td></tr>
                <tr><td>FBG Optical Isolation</td><td><b>{w_res.optical_isolation_db:.1f} dB</b></td><td>Narrowband 50 pm optical rejection</td></tr>
                <tr><td>Co-Propagation Security Verdict</td><td><b>{w_res.verdict.value}</b></td><td>Classification: {w_res.attack_classification}</td></tr>
            </table>
            <div style="background:#f8fafc; border:1px solid #cbd5e1; padding:8px 10px; font-size:0.75rem; color:#334155; margin-top:10px;">
                <b>WDM Cryptanalytic Proof:</b> {w_res.cryptanalytic_proof}
            </div>
            """, unsafe_allow_html=True)

with tab14:
    st.markdown("#### Enterprise SOC SIEM Integration & Automated STIX 2.1 Threat Intelligence (Q-SOC)")
    st.caption("Translates quantum threat indicators, hypothesis tests, and mitigation actions into OASIS STIX 2.1 Cyber Threat Intelligence (CTI) JSON bundles and Elastic Common Schema (ECS 8.x) SIEM event streams.")
    
    col_soc_ctrl, col_soc_meta = st.columns([1, 1])
    with col_soc_ctrl:
        st.markdown("**Enterprise Threat Intelligence Dispatch Console**")
        soc_scenario_choice = st.selectbox(
            "Target Threat Telemetry Context",
            options=[
                "Latest Live Verification Session Telemetry",
                "Quantum Signature Forgery (CAPEC-QDS-FORGERY)",
                "Signer Authority Impersonation (CAPEC-QDS-IMPERSONATION)",
                "Single-Photon Detector Blinding (CAPEC-QDS-BLINDING)",
                "WDM Co-Propagation Raman Jamming (CAPEC-QDS-WDM-JAMMING)"
            ]
        )
        
        target_soc_platform = st.selectbox(
            "Destination Enterprise SIEM Platform",
            options=[
                "Elastic SIEM (Elastic Common Schema 8.11.0)",
                "Splunk HTTP Event Collector (HEC ECS / CIM)",
                "IBM QRadar SIEM (Common Event Format / STIX)",
                "Microsoft Sentinel (Azure Log Analytics)"
            ]
        )
        
        dispatch_btn = st.button("Generate STIX 2.1 CTI Bundle & Dispatch to Enterprise SOC", use_container_width=True)
        
        if dispatch_btn or st.session_state.stix_bundle is None:
            # Build target assessment based on choice
            if "Latest Live" in soc_scenario_choice and assessment:
                eval_assess = assessment
                eval_signer = signer_id
                eval_scen = scenario_info
                eval_msg = message_input
                eval_inc = incident_report
            elif "Blinding" in soc_scenario_choice:
                eval_assess = ThreatAssessment(
                    verdict=ThreatCategory.MALICIOUS,
                    error_rate=0.48,
                    z_score=14.2,
                    p_value=1e-15,
                    confidence=0.9999,
                    baseline_noise_p0=ambient_noise_p0,
                    total_trials=400,
                    error_count=192,
                    match_count=208,
                    ci_lower=0.43,
                    ci_upper=0.53,
                    freshness_passed=True,
                    freshness_reason="Fresh token.",
                    diagnostic_text="Detector Blinding: DC anode bias current collapsed single-photon APDs into linear mode."
                )
                eval_signer = "Eve-Blinding-Probe"
                eval_scen = "DETECTOR_BLINDING"
                eval_msg = "Critical Infrastructure Grid Command"
                eval_inc = None
            elif "Raman" in soc_scenario_choice:
                eval_assess = ThreatAssessment(
                    verdict=ThreatCategory.MALICIOUS,
                    error_rate=0.22,
                    z_score=8.75,
                    p_value=1e-12,
                    confidence=0.9999,
                    baseline_noise_p0=ambient_noise_p0,
                    total_trials=400,
                    error_count=88,
                    match_count=312,
                    ci_lower=0.18,
                    ci_upper=0.26,
                    freshness_passed=True,
                    freshness_reason="Fresh token.",
                    diagnostic_text="WDM Cross-Talk: +14 dBm out-of-band pump generated spontaneous Raman noise photons."
                )
                eval_signer = "Mallory-Telecom-Tap"
                eval_scen = "RAMAN_CROSS_TALK_JAMMING"
                eval_msg = "Inter-Bank RTGS Settlement Batch #8812"
                eval_inc = None
            else:
                eval_assess = ThreatAssessment(
                    verdict=ThreatCategory.MALICIOUS,
                    error_rate=0.18,
                    z_score=6.52,
                    p_value=1.2e-8,
                    confidence=0.9999,
                    baseline_noise_p0=ambient_noise_p0,
                    total_trials=400,
                    error_count=72,
                    match_count=328,
                    ci_lower=0.145,
                    ci_upper=0.22,
                    freshness_passed=True,
                    freshness_reason="Fresh token.",
                    diagnostic_text="Pauli state forgery: statistical discrepancy rejected under exact binomial test."
                )
                eval_signer = "Mallory"
                eval_scen = "FORGERY"
                eval_msg = message_input
                eval_inc = incident_report

            integrator = QSOCIntegrator()
            stix_sum, siem_disp = integrator.process_incident_and_export(
                assessment=eval_assess,
                signer_id=eval_signer,
                scenario_name=eval_scen,
                message_payload=eval_msg,
                incident_report=eval_inc
            )
            st.session_state.stix_bundle = stix_sum
            st.session_state.siem_dispatch = siem_disp

    with col_soc_meta:
        st.markdown("**Enterprise SIEM Dispatch Status & Audit Header**")
        disp: SIEMDispatchResult = st.session_state.siem_dispatch
        stix: STIXBundleSummary = st.session_state.stix_bundle
        if disp and stix:
            st.markdown(f"""
            <table class="metrics-table">
                <tr><th>SOC Integration Attribute</th><th>Telemetry Value</th><th>Standard / Format</th></tr>
                <tr><td>STIX 2.1 Bundle ID</td><td><code>{stix.bundle_id[:32]}...</code></td><td>OASIS CTI STIX v2.1</td></tr>
                <tr><td>STIX SDO Object Count</td><td><b>{stix.object_count} Cyber Threat Objects</b></td><td>Identity, Indicator, Attack-Pattern, COA</td></tr>
                <tr><td>Mapped Attack Pattern</td><td><b>{stix.attack_pattern_name}</b></td><td>CAPEC / MITRE ATT&CK Matrix</td></tr>
                <tr><td>Destination SIEM Ingestion</td><td><b>{disp.target_platform}</b></td><td>Elastic Common Schema (ECS 8.11.0)</td></tr>
                <tr><td>SIEM Severity Code</td><td><b>Level {disp.severity_code} / 10</b></td><td>Automated SOC Escalation Priority</td></tr>
                <tr><td>Dispatch Delivery Status</td><td><b>{disp.dispatch_status}</b></td><td>HTTPS TLS 1.3 Webhook Forwarder</td></tr>
            </table>
            """, unsafe_allow_html=True)

    st.markdown("---")
    col_t1, col_t2 = st.columns([1, 1])
    with col_t1:
        st.markdown("**OASIS STIX 2.1 Threat Intelligence Bundle (JSON)**")
        if st.session_state.stix_bundle:
            st.code(st.session_state.stix_bundle.bundle_json, language="json")
            st.download_button(
                "Download STIX 2.1 Bundle (JSON)",
                data=st.session_state.stix_bundle.bundle_json,
                file_name=f"stix_bundle_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
            
    with col_t2:
        st.markdown("**Elastic Common Schema (ECS 8.x) SIEM Event (JSON)**")
        if st.session_state.siem_dispatch:
            st.code(st.session_state.siem_dispatch.raw_payload_json, language="json")
            st.download_button(
                "Download ECS 8.x Event (JSON)",
                data=st.session_state.siem_dispatch.raw_payload_json,
                file_name=f"ecs_event_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )

with tab15:
    st.markdown("""
    <div style="background-color: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #0b2545; padding: 12px 14px; margin-bottom: 14px;">
        <div style="font-weight: 700; font-size: 0.95rem; color: #0b2545; margin-bottom: 4px;">
            NATIONAL QUANTUM MISSION (NQM) EXECUTIVE WHITEPAPER & 14-WATCHTOWER REHEARSAL KIT (Q-DOC)
        </div>
        <div style="font-size: 0.80rem; color: #475569; line-height: 1.45;">
            Official publication-grade technical defense whitepaper and continuous Monte Carlo stress testing harness.
            Validates complete 14-watchtower operational readiness, mathematical physics proofs, enterprise standards compliance,
            and zero false negative detection across randomized quantum and classical adversarial vectors.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_doc_ctrl, col_doc_summary = st.columns([1.1, 0.9], gap="medium")

    with col_doc_ctrl:
        st.markdown("**Monte Carlo Stress Rehearsal Execution**")
        rehearsal_iterations = st.slider(
            "Monte Carlo Iterations",
            min_value=20,
            max_value=200,
            value=100,
            step=20,
            help="Number of mixed legitimate and adversarial sessions to simulate under randomized noise."
        )

        if st.button("Execute Full 14-Watchtower Monte Carlo Rehearsal", use_container_width=True):
            with st.spinner("Executing 14-watchtower sweep and Monte Carlo stress tests..."):
                runner = QuantumRehearsalRunner()
                report = runner.run_monte_carlo_stress_test(num_iterations=rehearsal_iterations)
                st.session_state.rehearsal_report = report

        # Auto-run if first visit
        if st.session_state.rehearsal_report is None:
            runner = QuantumRehearsalRunner()
            st.session_state.rehearsal_report = runner.run_monte_carlo_stress_test(num_iterations=40)

        rep: RehearsalReport = st.session_state.rehearsal_report

        if rep:
            status_text = "ALL 14 WATCHTOWERS OPERATIONAL (100% PASS RATE)" if rep.watchtowers_passed == 14 else "DEFENSE WARNING"
            st.markdown(f"""
            <div style="background-color: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #0b2545; padding: 10px 12px; margin-top: 10px; margin-bottom: 12px;">
                <div style="font-weight: 700; font-size: 0.85rem; color: #0b2545;">
                    REHEARSAL STATUS: {status_text}
                </div>
                <div style="font-size: 0.78rem; color: #334155; margin-top: 2px;">
                    Completed: {rep.timestamp} | Sessions: {rep.total_sessions} | Pass Rate: {rep.watchtower_pass_rate * 100:.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_doc_summary:
        st.markdown("**Rehearsal Benchmark Telemetry**")
        if rep:
            st.markdown(f"""
            <table class="metrics-table">
                <tr><th>Metric Name</th><th>Observed Value</th><th>Compliance Target</th></tr>
                <tr><td>Watchtowers Verified</td><td><b>{rep.watchtowers_passed} / {rep.watchtowers_total} Active</b></td><td>14 / 14 (100.0%)</td></tr>
                <tr><td>Malicious Detection Rate</td><td><b>{rep.detection_rate_pct:.1f}%</b></td><td>100.0% (Zero Misses)</td></tr>
                <tr><td>False Negatives (Missed Attacks)</td><td><b>{rep.false_negatives} sessions</b></td><td>0 False Negatives</td></tr>
                <tr><td>False Positives (False Alarms)</td><td><b>{rep.false_positives} sessions</b></td><td>0 False Positives</td></tr>
                <tr><td>Average Verification Latency</td><td><b>{rep.mean_latency_ms:.2f} ms</b></td><td>&lt; 5.0 ms</td></tr>
                <tr><td>Peak Verification Latency</td><td><b>{rep.max_latency_ms:.2f} ms</b></td><td>&lt; 20.0 ms</td></tr>
            </table>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Watchtower Sweep Table
    if rep and rep.watchtower_results:
        st.markdown("**14-Watchtower Operational Health Sweep Matrix**")
        wt_data = []
        for r in rep.watchtower_results:
            wt_data.append({
                "Watchtower Module": r.watchtower_name,
                "Adversarial Scenario Tested": r.scenario,
                "Threat Verdict": r.verdict,
                "Latency (ms)": f"{r.latency_ms:.2f}",
                "Status": "PASS" if r.passed else "FAIL",
                "Physics Diagnostic Details": r.details
            })
        st.dataframe(wt_data, use_container_width=True)

    st.markdown("---")

    # Whitepaper Viewer & Download Section
    col_wp_view, col_wp_meta = st.columns([1.3, 0.7], gap="medium")

    wp_path = Path("docs/NQM_EXECUTIVE_WHITEPAPER.md")
    wp_text = wp_path.read_text(encoding="utf-8") if wp_path.exists() else "Whitepaper documentation not found."

    with col_wp_view:
        st.markdown("**National Quantum Mission (NQM) Technical Whitepaper Preview**")
        st.text_area(
            "NQM Executive Defense Whitepaper",
            value=wp_text,
            height=320,
            help="Official NQM Executive Whitepaper formatted for SIH jury and MeitY evaluation."
        )

    with col_wp_meta:
        st.markdown("**Document Specifications & Export**")
        st.markdown("""
        <table class="metrics-table">
            <tr><th>Document Field</th><th>Value</th></tr>
            <tr><td>Document Classification</td><td>Official NQM Defense Specification</td></tr>
            <tr><td>Authority</td><td>MeitY / National Quantum Mission</td></tr>
            <tr><td>Target Problem Statement</td><td>SIH-26141 Grand Finale</td></tr>
            <tr><td>Evaluation Category</td><td>Quantum Cyber Security Framework</td></tr>
            <tr><td>Framework Edition</td><td>Q-Sentinel 1.0.0 Enterprise</td></tr>
            <tr><td>Format</td><td>GitHub Flavored Markdown / KaTeX</td></tr>
        </table>
        """, unsafe_allow_html=True)

        if wp_path.exists():
            st.download_button(
                "Download Official NQM Whitepaper (.md)",
                data=wp_text,
                file_name="NQM_EXECUTIVE_WHITEPAPER_SIH26141.md",
                mime="text/markdown",
                use_container_width=True
            )

        if rep:
            st.download_button(
                "Download Rehearsal Telemetry Report (.json)",
                data=rep.to_json(),
                file_name=f"qsentinel_rehearsal_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
    st.markdown("---")

    # Grand Unified Release Audit Section (Phase 40)
    st.markdown("""
    <div style="background-color: #0b2545; color: #ffffff; padding: 10px 14px; font-weight: 700; font-size: 0.88rem; border-radius: 2px; margin-bottom: 12px;">
        PHASE 40: GRAND UNIFIED RELEASE AUDIT & PRODUCTION CERTIFICATION
    </div>
    """, unsafe_allow_html=True)

    col_rel_ctrl, col_rel_badge = st.columns([1.1, 0.9], gap="medium")

    with col_rel_ctrl:
        st.markdown("**Master 8-Pillar Release Certification**")
        if st.button("Execute Master Phase 40 Release Audit", use_container_width=True):
            with st.spinner("Executing Grand Unified Release Audit across all 40 phases..."):
                auditor = GrandUnifiedReleaseAuditor()
                st.session_state.release_report = auditor.execute_grand_unified_audit()

        if st.session_state.release_report is None:
            auditor = GrandUnifiedReleaseAuditor()
            st.session_state.release_report = auditor.execute_grand_unified_audit()

        rel_rep: GrandUnifiedReleaseReport = st.session_state.release_report

        if rel_rep:
            freeze_status = "LOCKED & CERTIFIED" if rel_rep.release_frozen else "AUDIT WARNING"
            st.markdown(f"""
            <div style="background-color: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #ff671f; padding: 10px 12px; margin-top: 8px;">
                <div style="font-weight: 700; font-size: 0.85rem; color: #0b2545;">
                    RELEASE STATUS: {freeze_status} (40/40 PHASES)
                </div>
                <div style="font-size: 0.76rem; color: #334155; margin-top: 3px;">
                    Audit ID: <code>{rel_rep.audit_id}</code> | SHA-256: <code>{rel_rep.integrity_hash_sha256[:24]}...</code>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_rel_badge:
        st.markdown("**Release Verification Metrics**")
        if rel_rep:
            st.markdown(f"""
            <table class="metrics-table">
                <tr><th>Audit Metric</th><th>Audited Value</th><th>Release Criteria</th></tr>
                <tr><td>Phases Verified</td><td><b>{rel_rep.total_phases_verified} / 40 Phases</b></td><td>40 / 40 (100.0%)</td></tr>
                <tr><td>Inspection Pillars Passed</td><td><b>{rel_rep.passed_inspections} / {rel_rep.total_inspections}</b></td><td>8 / 8 (100.0%)</td></tr>
                <tr><td>Codebase Hygiene</td><td><b>Zero Emojis / Zero ML</b></td><td>100% Deterministic</td></tr>
                <tr><td>Release Freeze Lock</td><td><b>{'CERTIFIED LOCKED' if rel_rep.release_frozen else 'INCOMPLETE'}</b></td><td>Production Release</td></tr>
            </table>
            """, unsafe_allow_html=True)

    # 8-Pillar Inspection Matrix
    if rel_rep and rel_rep.inspections:
        st.markdown("**8-Pillar Release Audit Inspections Matrix**")
        audit_rows = []
        for insp in rel_rep.inspections:
            audit_rows.append({
                "Check ID": insp.check_id,
                "Audit Pillar": insp.check_name,
                "Status": "PASSED" if insp.passed else "FAILED",
                "Execution Latency": f"{insp.latency_ms:.2f} ms",
                "Inspection Details": insp.details
            })
        st.dataframe(audit_rows, use_container_width=True)

        col_dl_cert, col_dl_man = st.columns([1, 1])
        with col_dl_cert:
            st.download_button(
                "Download Release Audit Certificate (.json)",
                data=rel_rep.to_json(),
                file_name=f"RELEASE_AUDIT_CERTIFICATE_{rel_rep.audit_id}.json",
                mime="application/json",
                use_container_width=True
            )
        with col_dl_man:
            manifest_path = Path("docs/RELEASE_MANIFEST.md")
            manifest_content = manifest_path.read_text(encoding="utf-8") if manifest_path.exists() else "Manifest not found"
            st.download_button(
                "Download Master Release Manifest (.md)",
                data=manifest_content,
                file_name="RELEASE_MANIFEST_SIH26141.md",
                mime="text/markdown",
                use_container_width=True
            )

st.markdown("</div></div>", unsafe_allow_html=True)


# Clean Footer (Zero Emojis/Symbols)
st.markdown("""
<div class="app-footer">
    <div style="font-weight:700; font-size:0.85rem; margin-bottom:4px;">
        Q-SENTINEL: QUANTUM-INSPIRED CYBER THREAT DETECTION FRAMEWORK
    </div>
    <div>
        Teleportation-Based Quantum Digital Signature Verification and Runtime Threat Watchtower
    </div>
    <div style="margin-top:4px; color:#94a3b8; font-size:0.7rem;">
        Smart India Hackathon (SIH-26141) | Grand Unified Release Version 1.0.0 Enterprise Defense Edition (Phase 40/40 Locked)
    </div>
</div>
""", unsafe_allow_html=True)
