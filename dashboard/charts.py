"""
Q-Sentinel: Plotly Interactive Visualization Engine
Clean Institutional Layout: Open Sans, Toronto, and Calibri Typography with Pure White Background
"""

from __future__ import annotations
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from typing import List, Optional
from quantum.measure import MeasurementTrialResult


FONT_FAMILY = "'Open Sans', 'Toronto', 'Calibri', sans-serif"


def build_threat_gauge(
    z_score: float,
    z_suspicious: float = 2.0,
    z_malicious: float = 4.0
) -> go.Figure:
    """
    Renders an institutional gauge for the standardized z-score anomaly metric.
    Features generous top headroom to prevent title clipping, signed sigma formatting,
    and distinct pastel risk zones (Normal, Suspicious, Malicious).
    """
    max_range = max(10.0, float(z_score * 1.25))
    display_z = max(0.0, min(z_score, max_range))

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(display_z, 2),
        domain={'x': [0.05, 0.95], 'y': [0.05, 0.82]},
        title={
            'text': "<b>ANOMALY SCORE (z)</b><br><span style='font-size:0.75em;color:#64748b'>Statistical Z-Score (Deviations from Baseline)</span>",
            'font': {'size': 13, 'color': '#0b2545', 'family': FONT_FAMILY}
        },
        number={
            'font': {'family': FONT_FAMILY, 'color': '#0b2545', 'size': 32},
            'suffix': ' σ',
            'valueformat': '+.2f'
        },
        gauge={
            'axis': {'range': [0, max_range], 'tickwidth': 1, 'tickcolor': "#0b2545", 'tickfont': {'family': FONT_FAMILY}},
            'bar': {'color': "#0b2545", 'thickness': 0.38},
            'bgcolor': "#ffffff",
            'borderwidth': 1,
            'bordercolor': "#cbd5e1",
            'steps': [
                {'range': [0, z_suspicious], 'color': "#ecfdf5"},
                {'range': [z_suspicious, z_malicious], 'color': "#fef3c7"},
                {'range': [z_malicious, max_range], 'color': "#fee2e2"}
            ],
            'threshold': {
                'line': {'color': "#dc2626", 'width': 3},
                'thickness': 0.75,
                'value': z_malicious
            }
        }
    ))

    fig.update_layout(
        height=230,
        margin=dict(l=20, r=20, t=55, b=15, pad=4),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(family=FONT_FAMILY, color="#0f172a"),
        hoverlabel=dict(
            bgcolor="#ffffff",
            font_color="#0f172a",
            font_size=12,
            font_family=FONT_FAMILY,
            bordercolor="#cbd5e1"
        )
    )
    return fig


def build_outcome_distribution_chart(
    token_trials: List[MeasurementTrialResult],
    selected_token_idx: int = 0
) -> go.Figure:
    """
    Renders a grouped bar chart of expected Born rule probabilities vs empirical outcomes.
    Clean institutional styling with light, high-contrast hover tooltips.
    """
    if not token_trials or selected_token_idx >= len(token_trials):
        fig = go.Figure()
        fig.update_layout(
            title="No trial data available",
            font=dict(family=FONT_FAMILY, color="#0f172a"),
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff"
        )
        return fig

    trial = token_trials[selected_token_idx]
    
    categories = ["Valid Match (Eigenstate)", "Deviation Count"]
    theoretical_pcts = [trial.theoretical_match_prob * 100.0, trial.theoretical_error_prob * 100.0]
    observed_pcts = [(trial.n_match / trial.num_trials) * 100.0, (trial.n_error / trial.num_trials) * 100.0]

    fig = go.Figure(data=[
        go.Bar(
            name='Theoretical Probability (Born Rule)',
            x=categories,
            y=theoretical_pcts,
            marker=dict(color='#0b2545', line=dict(color='#0b2545', width=1)),
            text=[f"{v:.1f}%" for v in theoretical_pcts],
            textposition='auto',
            textfont=dict(family=FONT_FAMILY, color='#ffffff'),
            hovertemplate="<b>%{x}</b><br>Theoretical: %{y:.1f}%<extra></extra>"
        ),
        go.Bar(
            name='Observed Empirical Outcomes',
            x=categories,
            y=observed_pcts,
            marker=dict(color='#ff671f', line=dict(color='#e05512', width=1)),
            text=[f"{v:.1f}% (n={n})" for v, n in zip(observed_pcts, [trial.n_match, trial.n_error])],
            textposition='auto',
            textfont=dict(family=FONT_FAMILY, color='#ffffff'),
            hovertemplate="<b>%{x}</b><br>Observed: %{y:.1f}% (%{text})<extra></extra>"
        )
    ])

    fig.update_layout(
        title=dict(
            text=f"<b>Token #{selected_token_idx}: Quantum Measurement Statistics (N={trial.num_trials})</b>",
            font=dict(color="#0b2545", size=13, family=FONT_FAMILY),
            x=0.01,
            y=0.98,
            xanchor="left",
            yanchor="top"
        ),
        barmode='group',
        yaxis=dict(
            title=dict(text="Probability (%)", font=dict(color="#0f172a", family=FONT_FAMILY)),
            range=[0, 105],
            gridcolor="#f1f5f9",
            tickfont=dict(family=FONT_FAMILY, color="#0f172a")
        ),
        xaxis=dict(
            gridcolor="#f1f5f9",
            tickfont=dict(family=FONT_FAMILY, color="#0f172a")
        ),
        height=315,
        margin=dict(l=25, r=25, t=44, b=65),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.24,
            xanchor="center",
            x=0.5,
            font=dict(family=FONT_FAMILY, size=11, color="#0f172a"),
            bgcolor="rgba(248, 250, 252, 0.8)",
            bordercolor="#cbd5e1",
            borderwidth=1
        ),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(family=FONT_FAMILY, color="#0f172a"),
        hoverlabel=dict(
            bgcolor="#ffffff",
            font_color="#0f172a",
            font_size=12,
            font_family=FONT_FAMILY,
            bordercolor="#cbd5e1"
        )
    )
    return fig


def build_telemetry_trend_chart(history_df: pd.DataFrame) -> go.Figure:
    """
    Renders an audit trend chart of standardized z-scores.
    Clean institutional styling with light, high-contrast hover tooltips.
    """
    fig = go.Figure()

    if history_df.empty:
        fig.update_layout(
            title="No verification history available.",
            font=dict(family=FONT_FAMILY, color="#0f172a"),
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff"
        )
        return fig

    df_sorted = history_df.sort_values("ID", ascending=True).tail(30)

    fig.add_trace(go.Scatter(
        x=df_sorted["ID"],
        y=df_sorted["Z-Score"],
        mode="lines+markers",
        name="Z-Score",
        line=dict(color="#0b2545", width=2),
        marker=dict(size=8, color="#ff671f", line=dict(width=1.5, color="#0b2545")),
        text=[f"Run #{r['ID']} | {r['Scenario']}<br>Z-Score: {r['Z-Score']:.2f} σ<br>Verdict: {r['Verdict']}" for _, r in df_sorted.iterrows()],
        hovertemplate="<b>%{text}</b><extra></extra>"
    ))

    fig.add_hline(
        y=4.0,
        line_dash="dash",
        line_color="#dc2626",
        annotation_text="Critical Threat (z ≥ 4.0 σ)",
        annotation_position="top left",
        annotation_font=dict(family=FONT_FAMILY, color="#dc2626", size=10),
        annotation_bgcolor="rgba(255, 255, 255, 0.9)",
        annotation_bordercolor="#fca5a5",
        annotation_borderwidth=1
    )
    fig.add_hline(
        y=2.0,
        line_dash="dot",
        line_color="#d97706",
        annotation_text="Suspicious Drift (z ≥ 2.0 σ)",
        annotation_position="bottom left",
        annotation_font=dict(family=FONT_FAMILY, color="#b45309", size=10),
        annotation_bgcolor="rgba(255, 255, 255, 0.9)",
        annotation_bordercolor="#fde68a",
        annotation_borderwidth=1
    )

    fig.update_layout(
        title=dict(
            text="<b>Verification History: Anomaly Score Telemetry Stream (Past 30 Runs)</b>",
            font=dict(color="#0b2545", size=13, family=FONT_FAMILY),
            x=0.01,
            y=0.96,
            xanchor="left",
            yanchor="top"
        ),
        showlegend=False,
        xaxis=dict(
            title=dict(text="Verification Run ID", font=dict(color="#0f172a", family=FONT_FAMILY)),
            dtick=1,
            gridcolor="#f1f5f9",
            tickfont=dict(family=FONT_FAMILY, color="#0f172a")
        ),
        yaxis=dict(
            title=dict(text="Standardized Z-Score (σ)", font=dict(color="#0f172a", family=FONT_FAMILY)),
            gridcolor="#f1f5f9",
            tickfont=dict(family=FONT_FAMILY, color="#0f172a")
        ),
        height=260,
        margin=dict(l=20, r=20, t=35, b=20),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(family=FONT_FAMILY, color="#0f172a"),
        hoverlabel=dict(
            bgcolor="#ffffff",
            font_color="#0f172a",
            font_size=12,
            font_family=FONT_FAMILY,
            bordercolor="#cbd5e1"
        )
    )
    return fig


def build_bloch_sphere_3d(
    stokes_params: Tuple[float, float, float],
    expected_stokes: Optional[Tuple[float, float, float]] = None
) -> go.Figure:
    """
    Renders an interactive 3D Bloch sphere representation of the reconstructed density matrix.
    Visualizes the Stokes vector (S1, S2, S3) inside or on the unit Bloch sphere.
    """
    s1, s2, s3 = stokes_params

    # Wireframe circles for sphere geometry
    phi = np.linspace(0, 2 * np.pi, 60)

    # Equator (z=0)
    eq_x = np.cos(phi)
    eq_y = np.sin(phi)
    eq_z = np.zeros_like(phi)

    # Prime meridian (y=0)
    mer_x = np.cos(phi)
    mer_y = np.zeros_like(phi)
    mer_z = np.sin(phi)

    # 90-deg meridian (x=0)
    mer90_x = np.zeros_like(phi)
    mer90_y = np.cos(phi)
    mer90_z = np.sin(phi)

    fig = go.Figure()

    # Wireframe traces
    wire_style = dict(color="#cbd5e1", width=1.5)
    fig.add_trace(go.Scatter3d(x=eq_x, y=eq_y, z=eq_z, mode="lines", line=wire_style, hoverinfo="none", showlegend=False))
    fig.add_trace(go.Scatter3d(x=mer_x, y=mer_y, z=mer_z, mode="lines", line=wire_style, hoverinfo="none", showlegend=False))
    fig.add_trace(go.Scatter3d(x=mer90_x, y=mer90_y, z=mer90_z, mode="lines", line=wire_style, hoverinfo="none", showlegend=False))

    # Principal Axes (X, Y, Z)
    axis_line = dict(color="#94a3b8", width=2)
    fig.add_trace(go.Scatter3d(x=[-1.15, 1.15], y=[0, 0], z=[0, 0], mode="lines+text", text=["|-x>", "|+x>"], textposition="middle center", line=axis_line, textfont=dict(family=FONT_FAMILY, size=11, color="#475569"), hoverinfo="none", showlegend=False))
    fig.add_trace(go.Scatter3d(x=[0, 0], y=[-1.15, 1.15], z=[0, 0], mode="lines+text", text=["|-y>", "|+y>"], textposition="middle center", line=axis_line, textfont=dict(family=FONT_FAMILY, size=11, color="#475569"), hoverinfo="none", showlegend=False))
    fig.add_trace(go.Scatter3d(x=[0, 0], y=[0, 0], z=[-1.15, 1.15], mode="lines+text", text=["|1>", "|0>"], textposition="middle center", line=axis_line, textfont=dict(family=FONT_FAMILY, size=11, color="#475569"), hoverinfo="none", showlegend=False))

    # Expected State Vector (if provided)
    if expected_stokes is not None:
        e1, e2, e3 = expected_stokes
        fig.add_trace(go.Scatter3d(
            x=[0, e1], y=[0, e2], z=[0, e3],
            mode="lines+markers",
            line=dict(color="#0b2545", width=4, dash="dash"),
            marker=dict(size=[0, 7], color="#0b2545"),
            name="Expected Eigenstate",
            hovertext=f"Expected State Vector: ({e1:.2f}, {e2:.2f}, {e3:.2f})",
            hoverinfo="text"
        ))

    # Reconstructed Stokes Vector
    vec_len = float(np.sqrt(s1**2 + s2**2 + s3**2))
    fig.add_trace(go.Scatter3d(
        x=[0, s1], y=[0, s2], z=[0, s3],
        mode="lines+markers",
        line=dict(color="#ff671f", width=6),
        marker=dict(size=[0, 9], color="#ff671f", symbol="diamond"),
        name="Tomographic State Vector",
        hovertext=f"Reconstructed Stokes Vector: ({s1:.2f}, {s2:.2f}, {s3:.2f})<br>Purity (r): {vec_len:.4f}",
        hoverinfo="text"
    ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[-1.25, 1.25], showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=""),
            yaxis=dict(range=[-1.25, 1.25], showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=""),
            zaxis=dict(range=[-1.25, 1.25], showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=""),
            camera=dict(eye=dict(x=1.4, y=1.4, z=1.1))
        ),
        title=dict(
            text="<b>3D Quantum State Bloch Sphere Projection</b>",
            font=dict(color="#0b2545", size=13, family=FONT_FAMILY),
            x=0.02, y=0.98, xanchor="left", yanchor="top"
        ),
        height=380,
        margin=dict(l=10, r=10, t=40, b=10),
        paper_bgcolor="#ffffff",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=0.05,
            xanchor="center",
            x=0.5,
            font=dict(family=FONT_FAMILY, size=11, color="#0f172a"),
            bgcolor="rgba(248, 250, 252, 0.9)",
            bordercolor="#cbd5e1",
            borderwidth=1
        )
    )
    return fig


def build_density_matrix_heatmap(density_matrix: np.ndarray) -> go.Figure:
    """
    Renders heatmaps for the real and imaginary components of the 2x2 density matrix rho.
    """
    re_rho = np.real(density_matrix)
    im_rho = np.imag(density_matrix)

    labels = ["|0>", "|1>"]

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=["<b>Real Component Re(rho)</b>", "<b>Imaginary Component Im(rho)</b>"],
        horizontal_spacing=0.18
    )

    re_text = [[f"{re_rho[i, j]:+.3f}" for j in range(2)] for i in range(2)]
    im_text = [[f"{im_rho[i, j]:+.3f}" for j in range(2)] for i in range(2)]

    fig.add_trace(
        go.Heatmap(
            z=re_rho, x=labels, y=labels,
            text=re_text, texttemplate="%{text}",
            textfont=dict(family=FONT_FAMILY, size=14, color="#0b2545"),
            colorscale=[[0, "#eff6ff"], [0.5, "#93c5fd"], [1, "#1d4ed8"]],
            showscale=False,
            zmin=-0.5, zmax=1.0,
            hoverongaps=False
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Heatmap(
            z=im_rho, x=labels, y=labels,
            text=im_text, texttemplate="%{text}",
            textfont=dict(family=FONT_FAMILY, size=14, color="#0b2545"),
            colorscale=[[0, "#fff7ed"], [0.5, "#fdba74"], [1, "#ea580c"]],
            showscale=False,
            zmin=-0.5, zmax=0.5,
            hoverongaps=False
        ),
        row=1, col=2
    )

    fig.update_layout(
        height=260,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(family=FONT_FAMILY, color="#0f172a")
    )
    for annotation in fig['layout']['annotations']:
        annotation['font'] = dict(family=FONT_FAMILY, size=12, color="#0b2545")

    return fig


def build_signature_token_matrix_chart(
    token_trials: List[MeasurementTrialResult],
    selected_idx: int = 0
) -> go.Figure:
    """
    Renders a comparative error rate and basis distribution chart across all tokens in the signature.
    Highlights tokens that experienced high error rates (>15%) indicative of quantum disturbance.
    """
    if not token_trials:
        fig = go.Figure()
        fig.update_layout(title="No token trial data", paper_bgcolor="#ffffff")
        return fig

    token_ids = [f"#{i}" for i in range(len(token_trials))]
    error_rates = [(t.n_error / t.num_trials) * 100.0 for t in token_trials]
    colors = []
    for i, err in enumerate(error_rates):
        if i == selected_idx:
            colors.append("#ff671f")  # Saffron for selected token
        elif err > 15.0:
            colors.append("#dc2626")  # Red for disturbed token
        elif err > 5.0:
            colors.append("#d97706")  # Amber for mild drift
        else:
            colors.append("#0b2545")  # Navy for clean baseline

    fig = go.Figure(data=[
        go.Bar(
            x=token_ids,
            y=error_rates,
            marker=dict(color=colors, line=dict(color="#0f172a", width=1)),
            text=[f"{e:.1f}%" for e in error_rates],
            textposition="auto",
            textfont=dict(family=FONT_FAMILY, size=10, color="#ffffff"),
            hovertemplate="<b>Token %{x}</b><br>Observed Error Rate: %{y:.2f}%<extra></extra>"
        )
    ])

    fig.add_hline(
        y=2.78,
        line_dash="dot",
        line_color="#16a34a",
        annotation_text="Baseline Noise (p0 = 2.8%)",
        annotation_position="top left",
        annotation_font=dict(family=FONT_FAMILY, color="#16a34a", size=10),
        annotation_bgcolor="rgba(255, 255, 255, 0.9)",
        annotation_bordercolor="#bbf7d0",
        annotation_borderwidth=1
    )

    fig.add_hline(
        y=15.0,
        line_dash="dash",
        line_color="#dc2626",
        annotation_text="Tampering Cutoff (15%)",
        annotation_position="top left",
        annotation_font=dict(family=FONT_FAMILY, color="#dc2626", size=10),
        annotation_bgcolor="rgba(255, 255, 255, 0.9)",
        annotation_bordercolor="#fca5a5",
        annotation_borderwidth=1
    )

    fig.update_layout(
        title=dict(
            text="<b>Multi-Token Quantum Signature Fingerprint (Token-by-Token Error Distribution)</b>",
            font=dict(color="#0b2545", size=13, family=FONT_FAMILY),
            x=0.01, y=0.98, xanchor="left", yanchor="top"
        ),
        xaxis=dict(title=dict(text="Signature Token Index", font=dict(family=FONT_FAMILY)), gridcolor="#f1f5f9"),
        yaxis=dict(title=dict(text="Observed Error Rate (%)", font=dict(family=FONT_FAMILY)), range=[0, max(30.0, max(error_rates) * 1.25)], gridcolor="#f1f5f9"),
        height=280,
        margin=dict(l=25, r=25, t=44, b=25),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(family=FONT_FAMILY, color="#0f172a")
    )
    return fig


def build_phase_space_scatter(
    history_df: pd.DataFrame,
    current_error_rate: float = 0.0278,
    current_z: float = 0.0
) -> go.Figure:
    """
    Renders a 2D phase space diagram of Error Rate (e) vs Standardized Z-Score (z).
    Demonstrates zero-failure quantum discrimination between environmental noise and malicious tampering.
    """
    fig = go.Figure()

    # Normal Baseline Region (Green)
    fig.add_shape(
        type="rect", x0=0, x1=0.06, y0=-2.0, y1=2.0,
        fillcolor="rgba(240, 253, 244, 0.7)", line=dict(color="#86efac", width=1),
        layer="below"
    )

    # Suspicious Drift Region (Amber)
    fig.add_shape(
        type="rect", x0=0, x1=0.15, y0=2.0, y1=4.0,
        fillcolor="rgba(254, 243, 199, 0.5)", line=dict(color="#fde68a", width=1),
        layer="below"
    )

    # Critical Threat Region (Red)
    fig.add_shape(
        type="rect", x0=0, x1=0.60, y0=4.0, y1=25.0,
        fillcolor="rgba(254, 226, 226, 0.4)", line=dict(color="#fca5a5", width=1),
        layer="below"
    )

    if not history_df.empty and "Z-Score" in history_df.columns:
        err_col = [current_error_rate for _ in range(len(history_df))]
        fig.add_trace(go.Scatter(
            x=err_col,
            y=history_df["Z-Score"],
            mode="markers",
            marker=dict(size=7, color="#64748b", symbol="circle", opacity=0.6),
            name="Historical Runs",
            hovertext=[f"Run #{r['ID']} | {r.get('Verdict', 'N/A')}<br>z: {r['Z-Score']:.2f} sigma" for _, r in history_df.iterrows()],
            hoverinfo="text"
        ))

    # Current Verification Run (Highlighted Star/Diamond)
    curr_color = "#16a34a" if current_z < 2.0 else ("#d97706" if current_z < 4.0 else "#dc2626")
    fig.add_trace(go.Scatter(
        x=[current_error_rate],
        y=[current_z],
        mode="markers+text",
        marker=dict(size=14, color=curr_color, symbol="diamond", line=dict(color="#0b2545", width=2)),
        text=["CURRENT EVENT"],
        textposition="top center",
        textfont=dict(family=FONT_FAMILY, size=11, color=curr_color),
        name="Active Event",
        hovertext=f"Active Event: e={current_error_rate*100:.2f}%, z={current_z:+.2f} sigma",
        hoverinfo="text"
    ))

    fig.update_layout(
        title=dict(
            text="<b>Noise vs Attack Phase Space Discrimination (e vs z-score)</b>",
            font=dict(color="#0b2545", size=13, family=FONT_FAMILY),
            x=0.01, y=0.98, xanchor="left", yanchor="top"
        ),
        xaxis=dict(title=dict(text="Observed Quantum Error Rate (e_hat)", font=dict(family=FONT_FAMILY)), tickformat=".1%", range=[0, 0.40], gridcolor="#f1f5f9"),
        yaxis=dict(title=dict(text="Standardized Anomaly Score (z)", font=dict(family=FONT_FAMILY)), range=[-1, max(15.0, current_z * 1.25)], gridcolor="#f1f5f9"),
        height=320,
        margin=dict(l=25, r=25, t=44, b=30),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(family=FONT_FAMILY, color="#0f172a"),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            xanchor="center",
            x=0.5,
            font=dict(family=FONT_FAMILY, size=11),
            bgcolor="rgba(248, 250, 252, 0.8)",
            bordercolor="#cbd5e1",
            borderwidth=1
        )
    )
    return fig
