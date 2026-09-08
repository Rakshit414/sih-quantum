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
    Renders a responsive, high-contrast schematic of the 3-qubit teleportation channel
    in a balanced 2x2 grid layout. All 4 stages have identical dimensions, visual weight,
    and distinct step indicators (1 -> 2 -> 3 -> 4) to ensure high visibility.
    """
    b1, b2 = bell_bits
    clean_recovered = recovered_label
    if clean_recovered.startswith("Teleported(") and clean_recovered.endswith(")"):
        clean_recovered = clean_recovered[len("Teleported("):-1]

    if attack_applied and attack_applied != "Clean transmission":
        status_banner = (
            f'<div style="background-color: #fef2f2; border: 1px solid #fca5a5; border-left: 4px solid #dc2626; '
            f'color: #991b1b; border-radius: 4px; padding: 10px 14px; font-size: 0.82rem; '
            f'margin-top: 14px; font-weight: 600; line-height: 1.4;">'
            f'<span style="font-weight: 800; color: #dc2626; text-transform: uppercase;">[ACTIVE CHANNEL ANOMALY]</span> '
            f'{attack_applied}'
            f'</div>'
        )
    else:
        status_banner = (
            f'<div style="background-color: #f0fdf4; border: 1px solid #86efac; border-left: 4px solid #16a34a; '
            f'color: #166534; border-radius: 4px; padding: 10px 14px; font-size: 0.82rem; '
            f'margin-top: 14px; font-weight: 600; line-height: 1.4;">'
            f'<span style="font-weight: 800; color: #16a34a; text-transform: uppercase;">[CHANNEL STATUS: VERIFIED]</span> '
            f'Clean Transmission (Quantum State Fidelity Verified: 100%)'
            f'</div>'
        )

    html = (
        f'<div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 16px; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); font-family: \'Open Sans\', \'Toronto\', \'Calibri\', sans-serif;">'
        f'<div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 8px; border-bottom: 1px solid #e2e8f0; padding-bottom: 10px; margin-bottom: 14px;">'
        f'<div>'
        f'<span style="font-weight: 800; color: #0b2545; font-size: 0.88rem; letter-spacing: 0.5px;">QUANTUM TELEPORTATION CHANNEL PIPELINE</span>'
        f'<div style="font-size: 0.72rem; color: #64748b; margin-top: 2px;">4-Stage Sequential Teleportation Verification Protocol</div>'
        f'</div>'
        f'<span style="background: #f8fafc; color: #334155; font-weight: 600; font-size: 0.74rem; padding: 4px 10px; border: 1px solid #cbd5e1; border-radius: 4px;">Shared Bell Pair: (|00&gt; + |11&gt;) / √2</span>'
        f'</div>'
        
        # Balanced 2x2 Grid Layout: Exactly 2 stages per row on desktop/tablet, equal width and height
        f'<div class="quantum-pipeline-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; width: 100%; box-sizing: border-box;">'
        
        # Stage 1: Signer Alice
        f'<div style="background: #f8fafc; border: 1px solid #cbd5e1; border-top: 3px solid #ff671f; border-radius: 6px; padding: 12px 14px; text-align: center; display: flex; flex-direction: column; justify-content: space-between; min-height: 125px; box-sizing: border-box; overflow: hidden;">'
        f'<div style="display: flex; justify-content: space-between; align-items: center; gap: 4px;">'
        f'<span style="font-size: 0.65rem; background: #fff7ed; color: #c2410c; font-weight: 700; padding: 2px 7px; border-radius: 3px; border: 1px solid #fed7aa; white-space: nowrap;">STEP 1 OF 4</span>'
        f'<span style="font-size: 0.65rem; color: #64748b; font-weight: 700; letter-spacing: 0.4px; white-space: nowrap;">ENCODE</span>'
        f'</div>'
        f'<div style="font-size: 0.75rem; color: #334155; font-weight: 700; text-transform: uppercase;">1. Signer ({signer_name})</div>'
        f'<div style="font-size: 1.35rem; font-weight: 800; color: #0b2545; margin: 4px 0; letter-spacing: 0.5px; font-family: monospace;">{input_state_label}</div>'
        f'<div style="font-size: 0.70rem; color: #64748b; white-space: nowrap;">Pauli Eigenstate |ψ&gt;</div>'
        f'</div>'
        
        # Stage 2: Bell Measurement
        f'<div style="background: #f8fafc; border: 1px solid #cbd5e1; border-top: 3px solid #0b2545; border-radius: 6px; padding: 12px 14px; text-align: center; display: flex; flex-direction: column; justify-content: space-between; min-height: 125px; box-sizing: border-box; overflow: hidden;">'
        f'<div style="display: flex; justify-content: space-between; align-items: center; gap: 4px;">'
        f'<span style="font-size: 0.65rem; background: #f1f5f9; color: #0b2545; font-weight: 700; padding: 2px 7px; border-radius: 3px; border: 1px solid #cbd5e1; white-space: nowrap;">STEP 2 OF 4</span>'
        f'<span style="font-size: 0.65rem; color: #64748b; font-weight: 700; letter-spacing: 0.4px; white-space: nowrap;">EPR BSM</span>'
        f'</div>'
        f'<div style="font-size: 0.75rem; color: #334155; font-weight: 700; text-transform: uppercase;">2. Bell Measurement</div>'
        f'<div style="font-size: 1.35rem; font-weight: 800; color: #0b2545; margin: 4px 0; letter-spacing: 0.5px; font-family: monospace;">({b1}, {b2})</div>'
        f'<div style="font-size: 0.70rem; color: #64748b; white-space: nowrap;">2 Classical Bits (m1, m2)</div>'
        f'</div>'
        
        # Stage 3: Pauli Correction
        f'<div style="background: #f8fafc; border: 1px solid #cbd5e1; border-top: 3px solid #3b82f6; border-radius: 6px; padding: 12px 14px; text-align: center; display: flex; flex-direction: column; justify-content: space-between; min-height: 125px; box-sizing: border-box; overflow: hidden;">'
        f'<div style="display: flex; justify-content: space-between; align-items: center; gap: 4px;">'
        f'<span style="font-size: 0.65rem; background: #eff6ff; color: #1d4ed8; font-weight: 700; padding: 2px 7px; border-radius: 3px; border: 1px solid #bfdbfe; white-space: nowrap;">STEP 3 OF 4</span>'
        f'<span style="font-size: 0.65rem; color: #64748b; font-weight: 700; letter-spacing: 0.4px; white-space: nowrap;">UNITARY</span>'
        f'</div>'
        f'<div style="font-size: 0.75rem; color: #334155; font-weight: 700; text-transform: uppercase;">3. Pauli Correction</div>'
        f'<div style="font-size: 1.35rem; font-weight: 800; color: #0b2545; margin: 4px 0; letter-spacing: 0.5px; font-family: monospace;">U = {correction_gate}</div>'
        f'<div style="font-size: 0.70rem; color: #64748b; white-space: nowrap;">Z^{b1} · X^{b2} Feed-Forward</div>'
        f'</div>'
        
        # Stage 4: Verifier Bob
        f'<div style="background: #f8fafc; border: 1px solid #cbd5e1; border-top: 3px solid #16a34a; border-radius: 6px; padding: 12px 14px; text-align: center; display: flex; flex-direction: column; justify-content: space-between; min-height: 125px; box-sizing: border-box; overflow: hidden;">'
        f'<div style="display: flex; justify-content: space-between; align-items: center; gap: 4px;">'
        f'<span style="font-size: 0.65rem; background: #f0fdf4; color: #15803d; font-weight: 700; padding: 2px 7px; border-radius: 3px; border: 1px solid #bbf7d0; white-space: nowrap;">STEP 4 OF 4</span>'
        f'<span style="font-size: 0.65rem; color: #64748b; font-weight: 700; letter-spacing: 0.4px; white-space: nowrap;">RECONSTRUCT</span>'
        f'</div>'
        f'<div style="font-size: 0.75rem; color: #334155; font-weight: 700; text-transform: uppercase;">4. Verifier ({verifier_name})</div>'
        f'<div style="font-size: 1.35rem; font-weight: 800; color: #0b2545; margin: 4px 0; letter-spacing: 0.5px; font-family: monospace;">{clean_recovered}</div>'
        f'<div style="font-size: 0.70rem; color: #64748b; white-space: nowrap;">Reconstructed State |ψ\'&gt;</div>'
        f'</div>'
        
        f'</div>'
        f'{status_banner}'
        f'</div>'
    )
    return html
