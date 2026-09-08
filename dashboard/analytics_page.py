"""
Q-Sentinel: Quantum Graph Analytics & Deep Diagnostic Laboratory
Dedicated Interactive Telemetry Hub: Open Sans, Toronto, and Calibri Typography with Pure White Background
"""

from __future__ import annotations
import streamlit as st
import numpy as np
import pandas as pd
from typing import Optional

from quantum.measure import MeasurementTrialResult
from security.detector import ThreatAssessment
from security.signature import QuantumDigitalSignature
from quantum.tomography import QuantumStateTomography
from dashboard.charts import (
    build_outcome_distribution_chart,
    build_bloch_sphere_3d,
    build_density_matrix_heatmap,
    build_signature_token_matrix_chart,
    build_telemetry_trend_chart,
    build_phase_space_scatter
)


def render_quantum_graph_analytics_page(
    assessment: Optional[ThreatAssessment] = None,
    rx_sig: Optional[QuantumDigitalSignature] = None,
    legit_sig: Optional[QuantumDigitalSignature] = None,
    history_df: Optional[pd.DataFrame] = None
) -> None:
    """
    Renders the dedicated, highly navigatable Quantum Graph Analytics and Telemetry Lab.
    Provides 5 specialized sub-tabs with interactive token selection, 3D Bloch sphere rotation,
    density matrix tomography, multi-token signature fingerprinting, and phase space discrimination.
    """
    # Header & Quick Navigation Bar
    st.markdown("""
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-left:4px solid #0b2545; border-radius:6px; padding:16px 20px; margin-bottom:16px; box-shadow:0 1px 3px rgba(0,0,0,0.04);">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
            <div>
                <span style="font-weight:800; color:#0b2545; font-size:1.15rem; letter-spacing:0.5px;">QUANTUM GRAPH ANALYTICS & TELEMETRY LAB</span>
                <div style="color:#64748b; font-size:0.82rem; margin-top:3px;">
                    Interactive Physical Projections, 3D Bloch Spheres, Density Matrix Tomography, and Longitudinal Drift Telemetry
                </div>
            </div>
            <span style="background:#f8fafc; color:#334155; font-weight:700; font-size:0.75rem; padding:5px 12px; border:1px solid #cbd5e1; border-radius:4px;">
                Mode: Deep Physical Diagnostics
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Top return button
    col_ret1, col_ret2 = st.columns([1, 3])
    with col_ret1:
        if st.button("< RETURN TO LIVE COCKPIT", use_container_width=True, type="secondary"):
            st.session_state.active_view = "Live Watchtower Cockpit"
            st.rerun()

    if assessment is None or not assessment.token_trials:
        st.info("No active quantum verification telemetry is currently available. Please trigger a signature verification run in the Live Cockpit first.")
        return

    # Session State Token Tracker
    if "analytics_token_idx" not in st.session_state:
        st.session_state.analytics_token_idx = 0

    max_token_idx = len(assessment.token_trials) - 1
    selected_idx = min(st.session_state.analytics_token_idx, max_token_idx)

    # 5 Specialized Analytics Sub-Tabs
    tab_proj, tab_qst, tab_matrix, tab_trend, tab_phase = st.tabs([
        "1. Single-Token Born Rule Projections",
        "2. QST Tomography & 3D Bloch Sphere",
        "3. Multi-Token Signature Fingerprint",
        "4. Longitudinal Anomaly Telemetry",
        "5. Noise vs Attack Phase Space"
    ])

    # -------------------------------------------------------------
    # TAB 1: Single-Token Born Rule Projections
    # -------------------------------------------------------------
    with tab_proj:
        st.markdown("#### Projective Measurement Statistics & Empirical Born Rule Validation")
        st.caption("Inspects individual qubit measurement trials in the selected measurement basis against theoretical Born rule probabilities.")

        # Interactive Token Navigator Bar
        col_nav_prev, col_nav_select, col_nav_next = st.columns([1, 3, 1])
        with col_nav_prev:
            if st.button("< PREVIOUS TOKEN", use_container_width=True, disabled=(selected_idx <= 0)):
                st.session_state.analytics_token_idx = max(0, selected_idx - 1)
                st.rerun()

        with col_nav_select:
            token_options = list(range(len(assessment.token_trials)))
            def token_label_fmt(i: int) -> str:
                basis = rx_sig.tokens[i].basis.value if rx_sig and i < len(rx_sig.tokens) else "X"
                state = rx_sig.tokens[i].eigenstate.label if rx_sig and i < len(rx_sig.tokens) else "|+>"
                return f"Token #{i} (Basis: {basis}, State: {state})"

            chosen = st.selectbox(
                "Select Signature Token to Inspect:",
                options=token_options,
                index=selected_idx,
                format_func=token_label_fmt,
                key="analytics_token_select"
            )
            if chosen != selected_idx:
                st.session_state.analytics_token_idx = chosen
                st.rerun()

        with col_nav_next:
            if st.button("NEXT TOKEN >", use_container_width=True, disabled=(selected_idx >= max_token_idx)):
                st.session_state.analytics_token_idx = min(max_token_idx, selected_idx + 1)
                st.rerun()

        trial = assessment.token_trials[selected_idx]
        cur_tok = rx_sig.tokens[selected_idx] if rx_sig and selected_idx < len(rx_sig.tokens) else None

        # Token KPI Cards
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric("Prepared Eigenstate", cur_tok.eigenstate.label if cur_tok else "N/A")
        with col_m2:
            st.metric("Measurement Basis", cur_tok.basis.value if cur_tok else "N/A")
        with col_m3:
            obs_err = (trial.n_error / trial.num_trials) * 100.0
            st.metric("Observed Error Rate", f"{obs_err:.1f}%", delta=f"{obs_err - trial.theoretical_error_prob*100:+.1f}% vs baseline", delta_color="inverse")
        with col_m4:
            st.metric("Total Projective Trials", f"{trial.num_trials} Shots")

        # Projective Measurement Distribution Chart
        fig_dist = build_outcome_distribution_chart(assessment.token_trials, selected_idx)
        st.plotly_chart(fig_dist, use_container_width=True)

        st.markdown(f"""
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:6px; padding:12px 14px; font-size:0.8rem; color:#334155; line-height:1.5;">
            <b>Physical Validation:</b> Under the Born rule, projective measurement of state <code>{cur_tok.eigenstate.label if cur_tok else 'psi'}</code> 
            in basis <code>{cur_tok.basis.value if cur_tok else 'X'}</code> yields deterministic eigenstate alignment with theoretical fidelity 
            <code>{trial.theoretical_match_prob*100:.1f}%</code>. Observed empirical matches: <code>{trial.n_match}/{trial.num_trials}</code> shots.
        </div>
        """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # TAB 2: Quantum State Tomography (QST) & 3D Bloch Sphere
    # -------------------------------------------------------------
    with tab_qst:
        st.markdown("#### Quantum State Tomography (QST) & 3D Bloch Sphere Reconstruction")
        st.caption("Reconstructs the full 2x2 density matrix rho via Pauli Stokes projections (sigma_x, sigma_y, sigma_z) to distinguish thermal environmental noise from active eavesdropping.")

        chosen_token = rx_sig.tokens[selected_idx]
        expected_token = (legit_sig.tokens[selected_idx] if legit_sig and selected_idx < len(legit_sig.tokens) else chosen_token)

        qst_res = QuantumStateTomography.reconstruct_state(
            target_state=chosen_token.eigenstate,
            expected_state=expected_token.eigenstate,
            num_trials_per_basis=300
        )

        # Expected pure state Stokes vector
        theo_s1 = float(np.real(np.vdot(expected_token.eigenstate.vector, np.array([[0, 1], [1, 0]]) @ expected_token.eigenstate.vector)))
        theo_s2 = float(np.real(np.vdot(expected_token.eigenstate.vector, np.array([[0, -1j], [1j, 0]]) @ expected_token.eigenstate.vector)))
        theo_s3 = float(np.real(np.vdot(expected_token.eigenstate.vector, np.array([[1, 0], [0, -1]]) @ expected_token.eigenstate.vector)))

        col_bloch, col_matrix = st.columns([1.1, 0.9], gap="medium")

        with col_bloch:
            fig_bloch = build_bloch_sphere_3d(
                stokes_params=qst_res.stokes_parameters,
                expected_stokes=(theo_s1, theo_s2, theo_s3)
            )
            st.plotly_chart(fig_bloch, use_container_width=True)

        with col_matrix:
            st.markdown("##### Reconstructed 2x2 Density Matrix Components")
            fig_heat = build_density_matrix_heatmap(qst_res.density_matrix)
            st.plotly_chart(fig_heat, use_container_width=True)

        # Detailed Tomography Metric Table
        rho_00 = qst_res.density_matrix[0, 0].real
        rho_01 = qst_res.density_matrix[0, 1]
        rho_10 = qst_res.density_matrix[1, 0]
        rho_11 = qst_res.density_matrix[1, 1]

        st.markdown(f"""
        <table class="metrics-table" style="margin-top:10px;">
            <tr><th>Tomography Metric</th><th>Measured Value</th><th>Physical Significance</th></tr>
            <tr>
                <td>Reconstructed Density Matrix (rho)</td>
                <td><code>[[{rho_00:.3f}, {rho_01.real:.3f}{rho_01.imag:+.3f}j], [{rho_10.real:.3f}{rho_10.imag:+.3f}j, {rho_11:.3f}]]</code></td>
                <td>Hermitian, unit-trace positive semi-definite quantum state representation</td>
            </tr>
            <tr>
                <td>Quantum State Fidelity F(rho_exp, rho_rec)</td>
                <td><b>{qst_res.fidelity * 100:.2f}%</b></td>
                <td>Uhlmann transition overlap against authorized sender eigenstate</td>
            </tr>
            <tr>
                <td>State Purity gamma = Tr(rho^2)</td>
                <td><b>{qst_res.purity:.4f}</b> (Pure=1.00, Maximally Mixed=0.50)</td>
                <td>Discriminates coherent phase rotation from incoherent environmental decoherence</td>
            </tr>
            <tr>
                <td>Von Neumann Entropy S(rho)</td>
                <td><b>{qst_res.von_neumann_entropy:.4f} bits</b></td>
                <td>Information-theoretic quantum uncertainty / mixedness in channel</td>
            </tr>
            <tr>
                <td>Stokes Bloch Vector (S1, S2, S3)</td>
                <td>({qst_res.stokes_parameters[0]:+.2f}, {qst_res.stokes_parameters[1]:+.2f}, {qst_res.stokes_parameters[2]:+.2f})</td>
                <td>Coordinates on unit Bloch sphere: length r = {qst_res.bloch_vector_length:.4f}</td>
            </tr>
        </table>
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-left:4px solid #0b2545; padding:10px 14px; font-size:0.8rem; color:#334155; margin-top:10px; border-radius:4px;">
            <b>Tomographic Diagnostic Verdict:</b> {qst_res.diagnostic}
        </div>
        """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # TAB 3: Multi-Token Signature Fingerprint
    # -------------------------------------------------------------
    with tab_matrix:
        st.markdown("#### Full Signature Multi-Token Quantum Fingerprint Matrix")
        st.caption("Displays the comparative error profile across every single qubit token in the signature package. Instantly exposes which specific qubits were intercepted by an eavesdropper.")

        fig_matrix = build_signature_token_matrix_chart(assessment.token_trials, selected_idx)
        st.plotly_chart(fig_matrix, use_container_width=True)

        # Summary KPIs
        total_toks = len(assessment.token_trials)
        disturbed_toks = sum(1 for t in assessment.token_trials if (t.n_error / t.num_trials) > 0.15)
        clean_toks = total_toks - disturbed_toks

        col_tk1, col_tk2, col_tk3 = st.columns(3)
        with col_tk1:
            st.metric("Total Signature Tokens", total_toks)
        with col_tk2:
            st.metric("Clean Baseline Tokens", clean_toks, delta="Within normal noise bounds")
        with col_tk3:
            st.metric("Disturbed / Intercepted Tokens", disturbed_toks, delta=f"{disturbed_toks/total_toks*100:.1f}% compromised" if disturbed_toks > 0 else "0% clean", delta_color="inverse")

        st.markdown("""
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:6px; padding:12px 14px; font-size:0.8rem; color:#334155; margin-top:12px; line-height:1.5;">
            <b>Fingerprint Interpretation:</b> Under an intercept-resend forgery attack, Eve must guess between conjugate measurement bases (X, Y, Z). 
            When Eve guesses incorrectly (50% probability), she inevitably collapses the state, introducing an average 25% error rate on those specific qubits.
            The fingerprint chart directly reveals this selective collapse pattern across all transmission channels.
        </div>
        """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # TAB 4: Longitudinal Anomaly Stream & Statistical Drift
    # -------------------------------------------------------------
    with tab_trend:
        st.markdown("#### Longitudinal Anomaly Telemetry Stream & Moving Z-Score Trajectory")
        st.caption("Continuous time-series tracking of standardized Z-scores across all historical verification sessions.")

        if history_df is not None and not history_df.empty:
            fig_hist = build_telemetry_trend_chart(history_df)
            st.plotly_chart(fig_hist, use_container_width=True)

            col_tr1, col_tr2, col_tr3, col_tr4 = st.columns(4)
            with col_tr1:
                st.metric("Historical Verification Events", len(history_df))
            with col_tr2:
                mean_z = float(history_df["Z-Score"].mean())
                st.metric("Mean Anomaly Score", f"{mean_z:+.2f} sigma")
            with col_tr3:
                peak_z = float(history_df["Z-Score"].max())
                st.metric("Peak Threat Z-Score", f"{peak_z:+.2f} sigma")
            with col_tr4:
                mal_count = sum(1 for v in history_df.get("Verdict", []) if "Malicious" in str(v) or "REJECTED" in str(v))
                st.metric("Total Threat Blocks", mal_count)
        else:
            st.info("No historical verification telemetry has been logged yet in SQLite datastore.")

    # -------------------------------------------------------------
    # TAB 5: Noise vs Active Threat Phase Discrimination Plot
    # -------------------------------------------------------------
    with tab_phase:
        st.markdown("#### Noise vs Attack Phase Space Discrimination (Error Rate vs Z-Score)")
        st.caption("2D phase plane separating benign environmental decoherence from active quantum tampering.")

        fig_phase = build_phase_space_scatter(
            history_df=history_df if history_df is not None else pd.DataFrame(),
            current_error_rate=assessment.error_rate,
            current_z=assessment.z_score
        )
        st.plotly_chart(fig_phase, use_container_width=True)

        st.markdown("""
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:6px; padding:12px 14px; font-size:0.8rem; color:#334155; line-height:1.5;">
            <b>Phase Space Boundaries:</b>
            <ul style="margin-top:6px; margin-bottom:0; padding-left:20px;">
                <li><b>Green Region (Normal Noise):</b> Observed error rate below 6.0% with Z-score strictly under +2.00 sigma. High fidelity, zero false alarms.</li>
                <li><b>Amber Region (Suspicious Drift):</b> Z-score between +2.00 sigma and +4.00 sigma. Channel degradation or low-intensity probing.</li>
                <li><b>Red Region (Active Attack):</b> Z-score exceeding +4.00 sigma. Provable eavesdropping, forgery, or replay attack. Immediate deterministic quarantine.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
