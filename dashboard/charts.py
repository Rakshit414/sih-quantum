"""
Q-Sentinel: Plotly Interactive Visualization Engine
Clean Institutional Layout: Open Sans, Toronto, and Calibri Typography with Pure White Background
"""

from __future__ import annotations
import plotly.graph_objects as go
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
