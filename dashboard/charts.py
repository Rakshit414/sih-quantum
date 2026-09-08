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
    Uses clean slate and navy tones with zero bright text highlights.
    """
    max_range = max(10.0, float(z_score * 1.25))
    display_z = max(0.0, min(z_score, max_range))

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(display_z, 2),
        domain={'x': [0, 1], 'y': [0, 1]},
        title={
            'text': "<b>ANOMALY SCORE (z)</b><br><span style='font-size:0.75em;color:#64748b'>Standard Normal Deviations</span>",
            'font': {'size': 14, 'color': '#0b2545', 'family': FONT_FAMILY}
        },
        number={'font': {'family': FONT_FAMILY, 'color': '#0b2545', 'size': 32}},
        gauge={
            'axis': {'range': [0, max_range], 'tickwidth': 1, 'tickcolor': "#0b2545", 'tickfont': {'family': FONT_FAMILY}},
            'bar': {'color': "#0b2545", 'thickness': 0.35},
            'bgcolor': "#ffffff",
            'borderwidth': 1,
            'bordercolor': "#cbd5e1",
            'steps': [
                {'range': [0, z_suspicious], 'color': "#f8fafc"},
                {'range': [z_suspicious, z_malicious], 'color': "#f1f5f9"},
                {'range': [z_malicious, max_range], 'color': "#e2e8f0"}
            ],
            'threshold': {
                'line': {'color': "#475569", 'width': 2},
                'thickness': 0.75,
                'value': z_malicious
            }
        }
    ))

    fig.update_layout(
        height=240,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(family=FONT_FAMILY)
    )
    return fig


def build_outcome_distribution_chart(
    token_trials: List[MeasurementTrialResult],
    selected_token_idx: int = 0
) -> go.Figure:
    """
    Renders a grouped bar chart of expected Born rule probabilities vs empirical outcomes.
    Clean institutional styling with no saturated highlights.
    """
    if not token_trials or selected_token_idx >= len(token_trials):
        fig = go.Figure()
        fig.update_layout(title="No trial data available", font=dict(family=FONT_FAMILY))
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
            marker_color='#0b2545',
            text=[f"{v:.1f}%" for v in theoretical_pcts],
            textposition='auto',
            textfont=dict(family=FONT_FAMILY)
        ),
        go.Bar(
            name='Observed Empirical Outcomes',
            x=categories,
            y=observed_pcts,
            marker_color='#64748b',
            text=[f"{v:.1f}% (n={n})" for v, n in zip(observed_pcts, [trial.n_match, trial.n_error])],
            textposition='auto',
            textfont=dict(family=FONT_FAMILY)
        )
    ])

    fig.update_layout(
        title=dict(
            text=f"<b>Token #{selected_token_idx}: Quantum Measurement Statistics (N={trial.num_trials})</b>",
            font=dict(color="#0b2545", size=13, family=FONT_FAMILY)
        ),
        barmode='group',
        yaxis=dict(title="Probability (%)", range=[0, 105], gridcolor="#f1f5f9", tickfont=dict(family=FONT_FAMILY)),
        xaxis=dict(gridcolor="#f1f5f9", tickfont=dict(family=FONT_FAMILY)),
        height=270,
        margin=dict(l=20, r=20, t=45, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(family=FONT_FAMILY)),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(family=FONT_FAMILY)
    )
    return fig


def build_telemetry_trend_chart(history_df: pd.DataFrame) -> go.Figure:
    """
    Renders an audit trend chart of standardized z-scores.
    Clean institutional styling.
    """
    fig = go.Figure()

    if history_df.empty:
        fig.update_layout(title="No verification history available.", font=dict(family=FONT_FAMILY))
        return fig

    df_sorted = history_df.sort_values("ID", ascending=True).tail(30)

    fig.add_trace(go.Scatter(
        x=df_sorted["ID"],
        y=df_sorted["Z-Score"],
        mode="lines+markers",
        name="Z-Score",
        line=dict(color="#0b2545", width=2),
        marker=dict(size=7, color="#0b2545", line=dict(width=1, color="#0b2545")),
        text=[f"Run #{r['ID']} ({r['Scenario']}): z={r['Z-Score']:.2f}" for _, r in df_sorted.iterrows()],
        hoverinfo="text"
    ))

    fig.add_hline(y=4.0, line_dash="dash", line_color="#64748b", annotation_text="Threshold z=4.0 (Critical)", annotation_position="top right", annotation_font=dict(family=FONT_FAMILY))
    fig.add_hline(y=2.0, line_dash="dot", line_color="#94a3b8", annotation_text="Threshold z=2.0 (Suspicious)", annotation_position="top right", annotation_font=dict(family=FONT_FAMILY))

    fig.update_layout(
        title=dict(
            text="<b>Verification History: Anomaly Score Telemetry Stream</b>",
            font=dict(color="#0b2545", size=13, family=FONT_FAMILY)
        ),
        xaxis=dict(title="Verification Run ID", dtick=1, gridcolor="#f1f5f9", tickfont=dict(family=FONT_FAMILY)),
        yaxis=dict(title="Standardized Z-Score", gridcolor="#f1f5f9", tickfont=dict(family=FONT_FAMILY)),
        height=250,
        margin=dict(l=20, r=20, t=35, b=20),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(family=FONT_FAMILY)
    )
    return fig
