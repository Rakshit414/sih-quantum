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
    Renders an unembellished, clean schematic of the 3-qubit teleportation channel.
    """
    b1, b2 = bell_bits
    attack_badge = ""
    if attack_applied and attack_applied != "Clean transmission":
        attack_badge = (
            f'<div style="background-color: #ffffff; border: 1px solid #94a3b8; '
            f'color: #1e293b; border-radius: 2px; padding: 6px 10px; font-size: 0.8rem; '
            f'margin-top: 10px; font-weight: 600;">'
            f'Channel Anomaly: {attack_applied}'
            f'</div>'
        )

    html = (
        f'<div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 2px; padding: 14px; margin-bottom: 14px; box-shadow: 0 1px 2px rgba(0,0,0,0.03); font-family: \'Open Sans\', \'Toronto\', \'Calibri\', sans-serif;">'
        f'<div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; margin-bottom: 12px;">'
        f'<span style="font-weight: 700; color: #0b2545; font-size: 0.85rem; letter-spacing: 0.4px;">QUANTUM TELEPORTATION CHANNEL FLOW</span>'
        f'<span style="background: #ffffff; color: #475569; font-weight: 600; font-size: 0.72rem; padding: 3px 8px; border: 1px solid #cbd5e1; border-radius: 2px;">Shared Bell State: (|00&gt; + |11&gt;) / sqrt(2)</span>'
        f'</div>'
        f'<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; align-items: center; text-align: center;">'
        f'<div style="background: #ffffff; border: 1px solid #cbd5e1; border-top: 2px solid #0b2545; border-radius: 2px; padding: 10px 4px;">'
        f'<div style="font-size: 0.7rem; color: #475569; font-weight: 700;">1. SIGNER ({signer_name.upper()})</div>'
        f'<div style="font-size: 1.15rem; font-weight: 700; color: #0b2545; margin: 4px 0; font-family: \'Open Sans\', \'Toronto\', \'Calibri\', sans-serif;">{input_state_label}</div>'
        f'<div style="font-size: 0.65rem; color: #64748b;">Pauli Eigenstate</div>'
        f'</div>'
        f'<div style="background: #ffffff; border: 1px solid #cbd5e1; border-top: 2px solid #0b2545; border-radius: 2px; padding: 10px 4px;">'
        f'<div style="font-size: 0.7rem; color: #475569; font-weight: 700;">2. BELL MEASUREMENT</div>'
        f'<div style="font-size: 1.15rem; font-weight: 700; color: #0b2545; margin: 4px 0; font-family: \'Open Sans\', \'Toronto\', \'Calibri\', sans-serif;">({b1}, {b2})</div>'
        f'<div style="font-size: 0.65rem; color: #64748b;">2 Classical Bits</div>'
        f'</div>'
        f'<div style="background: #ffffff; border: 1px solid #cbd5e1; border-top: 2px solid #0b2545; border-radius: 2px; padding: 10px 4px;">'
        f'<div style="font-size: 0.7rem; color: #475569; font-weight: 700;">3. PAULI CORRECTION</div>'
        f'<div style="font-size: 1.15rem; font-weight: 700; color: #0b2545; margin: 4px 0; font-family: \'Open Sans\', \'Toronto\', \'Calibri\', sans-serif;">U = {correction_gate}</div>'
        f'<div style="font-size: 0.65rem; color: #64748b;">Z^{b1} X^{b2} Operator</div>'
        f'</div>'
        f'<div style="background: #ffffff; border: 1px solid #cbd5e1; border-top: 2px solid #0b2545; border-radius: 2px; padding: 10px 4px;">'
        f'<div style="font-size: 0.7rem; color: #475569; font-weight: 700;">4. VERIFIER ({verifier_name.upper()})</div>'
        f'<div style="font-size: 1.15rem; font-weight: 700; color: #0b2545; margin: 4px 0; font-family: \'Open Sans\', \'Toronto\', \'Calibri\', sans-serif;">{recovered_label}</div>'
        f'<div style="font-size: 0.65rem; color: #64748b;">Recovered State</div>'
        f'</div>'
        f'</div>'
        f'{attack_badge}'
        f'</div>'
    )
    return html
