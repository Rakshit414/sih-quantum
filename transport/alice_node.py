"""
Q-Sentinel: Distributed Alice Node (QDS Signer)
Stage 22: Phase 43

Implements the physical signer node in the decoupled multi-process architecture:
- Generates message digests and maps bit sequences to Pauli eigenstates
- Distributes quantum signature states via teleportation protocol
- Transmits tokens and measurement trials sequentially over HTTP to Eve's channel relay

References:
- Bennett, C. H., et al. (1993). Teleporting an unknown quantum state via dual
  classical and Einstein-Podolsky-Rosen channels. Physical Review Letters, 70(13), 1895.
- Gottesman, D., & Chuang, I. (2001). Quantum digital signatures. arXiv:quant-ph/0105032.
"""

from __future__ import annotations
import json
import time
import urllib.request
import urllib.error
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional, Tuple

from security.signature import QDSKeyManager, QuantumDigitalSignature, distribute_signature_via_teleportation


@dataclass
class TransmissionPacket:
    """
    Individual network packet dispatched by Alice to the channel relay.
    """
    packet_id: str
    signer_id: str
    message: str
    token_index: int
    trial_index: int
    expected_basis: str
    expected_bit: int
    correction_bits: List[int]
    timestamp: float


class AliceSignerNode:
    """
    Physical QDS Signer node producing signed packets and transmitting
    sequentially over the network channel.
    """

    def __init__(self, signer_id: str = "Alice", private_seed: str = "alice_secret_seed_2026"):
        self.signer_id = signer_id
        self.key_mgr = QDSKeyManager(signer_id=signer_id, private_seed=private_seed)

    def prepare_session_packets(
        self,
        message: str,
        trials_per_token: int = 50
    ) -> Tuple[QuantumDigitalSignature, List[Dict[str, Any]]]:
        """
        Signs the message and converts all signature tokens into individual
        transmission packets ready for sequential channel transit.
        """
        signature = self.key_mgr.generate_signature(message)
        session = distribute_signature_via_teleportation(signature)
        
        packets: List[Dict[str, Any]] = []
        now = time.time()
        
        for t_idx, token in enumerate(signature.tokens):
            teleport_res = session.teleportation_results[t_idx]
            b1, b2 = teleport_res.bell_measurement_bits
            for trial_k in range(trials_per_token):
                pkt = TransmissionPacket(
                    packet_id=f"PKT-{t_idx:03d}-{trial_k:03d}",
                    signer_id=self.signer_id,
                    message=message,
                    token_index=t_idx,
                    trial_index=trial_k,
                    expected_basis=token.basis.name,
                    expected_bit=token.bit_value,
                    correction_bits=[b1, b2],
                    timestamp=now
                )
                packets.append(asdict(pkt))

        return signature, packets

    def transmit_session(
        self,
        message: str,
        relay_url: str = "http://127.0.0.1:8001/relay",
        trials_per_token: int = 50,
        inter_packet_delay_sec: float = 0.001
    ) -> Dict[str, Any]:
        """
        Executes sequential transmission of all trials over HTTP to the channel relay.
        """
        _, packets = self.prepare_session_packets(message, trials_per_token=trials_per_token)
        delivered_count = 0
        failed_count = 0

        for pkt in packets:
            data = json.dumps(pkt).encode("utf-8")
            req = urllib.request.Request(
                relay_url,
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            try:
                with urllib.request.urlopen(req, timeout=5.0) as resp:
                    if resp.status == 200:
                        delivered_count += 1
                    else:
                        failed_count += 1
            except Exception:
                failed_count += 1

            if inter_packet_delay_sec > 0:
                time.sleep(inter_packet_delay_sec)

        return {
            "status": "COMPLETED",
            "total_packets": len(packets),
            "delivered": delivered_count,
            "failed": failed_count
        }


if __name__ == "__main__":
    node = AliceSignerNode()
    res = node.transmit_session("PAYMENT_TX_APPROVED_1000000")
    print(f"Alice transmission summary: {res}")
