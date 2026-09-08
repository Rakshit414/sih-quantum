"""
Q-Sentinel: Quantum Teleportation Channel Schematic Visualizer
Clean English Pipeline Diagram with Open Sans, Toronto, and Calibri Typography
"""

from typing import Tuple, Optional


def render_teleportation_pipeline_html(
    input_state_label: str = "|+>",
    bell_bits: Tuple[int, int] = (0, 0),
    correction_gate: str = "I",
    recovered_label: str = "|+>",
    status_color: str = "#0b2545",
    attack_applied: Optional[str] = None,
    signer_name: str = "ALICE",
    verifier_name: str = "BOB"
) -> str:
    """
    Renders a responsive, high-contrast schematic of the 3-qubit teleportation channel.
    Designed to prevent text clipping, overlapping, or dark-box hover anomalies.
    """
    b1, b2 = bell_bits
    attack_badge = ""
    if attack_applied and attack_applied != "Clean transmission":
        attack_badge = (
            f'<div style="background-color: #fef2f2; border: 1px solid #f87171; border-left: 4px solid #dc2626; '
            f'color: #991b1b; border-radius: 4px; padding: 8px 12px; font-size: 0.82rem; '
            f'margin-top: 12px; font-weight: 600; line-height: 1.4;">'
            f'⚠️ <b>Active Channel Anomaly:</b> {attack_applied}'
            f'</div>'
        )
    else:
        attack_badge = (
            f'<div style="background-color: #f0fdf4; border: 1px solid #86efac; border-left: 4px solid #16a34a; '
            f'color: #166534; border-radius: 4px; padding: 8px 12px; font-size: 0.82rem; '
            f'margin-top: 12px; font-weight: 600; line-height: 1.4;">'
            f'✓ <b>Channel Status:</b> Clean Transmission (Quantum State Fidelity Verified: 100%)'
            f'</div>'
        )

    html = (
        f'<div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 16px; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); font-family: \'Open Sans\', \'Toronto\', \'Calibri\', sans-serif;">'
        f'<div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 8px; border-bottom: 1px solid #e2e8f0; padding-bottom: 10px; margin-bottom: 14px;">'
        f'<span style="font-weight: 800; color: #0b2545; font-size: 0.88rem; letter-spacing: 0.5px;">QUANTUM TELEPORTATION CHANNEL FLOW</span>'
        f'<span style="background: #f8fafc; color: #334155; font-weight: 600; font-size: 0.74rem; padding: 4px 10px; border: 1px solid #cbd5e1; border-radius: 4px;">Shared Bell Pair: (|00&gt; + |11&gt;) / √2</span>'
        f'</div>'
        f'<div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: space-between; align-items: stretch;">'
        
        # Stage 1: Signer
        f'<div style="flex: 1 1 140px; min-width: 130px; background: #f8fafc; border: 1px solid #cbd5e1; border-top: 3px solid #ff671f; border-radius: 4px; padding: 12px 8px; text-align: center;">'
        f'<div style="font-size: 0.72rem; color: #475569; font-weight: 700; text-transform: uppercase; letter-spacing: 0.3px;">1. Signer ({signer_name})</div>'
        f'<div style="font-size: 1.25rem; font-weight: 800; color: #0b2545; margin: 6px 0;">{input_state_label}</div>'
        f'<div style="font-size: 0.68rem; color: #64748b;">Pauli Eigenstate |ψ&gt;</div>'
        f'</div>'
        
        # Stage 2: Bell Measurement
        f'<div style="flex: 1 1 140px; min-width: 130px; background: #f8fafc; border: 1px solid #cbd5e1; border-top: 3px solid #0b2545; border-radius: 4px; padding: 12px 8px; text-align: center;">'
        f'<div style="font-size: 0.72rem; color: #475569; font-weight: 700; text-transform: uppercase; letter-spacing: 0.3px;">2. Bell Measurement</div>'
        f'<div style="font-size: 1.25rem; font-weight: 800; color: #0b2545; margin: 6px 0;">({b1}, {b2})</div>'
        f'<div style="font-size: 0.68rem; color: #64748b;">2 Classical Bits (m1, m2)</div>'
        f'</div>'
        
        # Stage 3: Pauli Correction
        f'<div style="flex: 1 1 140px; min-width: 130px; background: #f8fafc; border: 1px solid #cbd5e1; border-top: 3px solid #0b2545; border-radius: 4px; padding: 12px 8px; text-align: center;">'
        f'<div style="font-size: 0.72rem; color: #475569; font-weight: 700; text-transform: uppercase; letter-spacing: 0.3px;">3. Pauli Correction</div>'
        f'<div style="font-size: 1.25rem; font-weight: 800; color: #0b2545; margin: 6px 0;">U = {correction_gate}</div>'
        f'<div style="font-size: 0.68rem; color: #64748b;">Z^{b1} · X^{b2} Unitary</div>'
        f'</div>'
        
        # Stage 4: Verifier
        f'<div style="flex: 1 1 140px; min-width: 130px; background: #f8fafc; border: 1px solid #cbd5e1; border-top: 3px solid #16a34a; border-radius: 4px; padding: 12px 8px; text-align: center;">'
        f'<div style="font-size: 0.72rem; color: #475569; font-weight: 700; text-transform: uppercase; letter-spacing: 0.3px;">4. Verifier ({verifier_name})</div>'
        f'<div style="font-size: 1.25rem; font-weight: 800; color: #0b2545; margin: 6px 0;">{recovered_label}</div>'
        f'<div style="font-size: 0.68rem; color: #64748b;">Reconstructed State</div>'
        f'</div>'
        
        f'</div>'
        f'{attack_badge}'
        f'</div>'
    )
    return html
