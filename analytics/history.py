"""
Q-Sentinel: Telemetry Logging & Audit Datastore
Stage 6: Phase 20
Persists verification history, quantum metrics, and threat detection decisions
to an auditable SQLite database.
"""

from __future__ import annotations
import sqlite3
import os
import time
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import json
import hashlib
import pandas as pd
from security.detector import ThreatAssessment


def canonical_json(obj: Any) -> str:
    """
    Returns RFC 8785 style canonical JSON string with sorted keys and no whitespace.
    """
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


class TelemetryStore:
    """
    Thread-safe SQLite datastore for security audit logs with cryptographic hash chaining.
    """

    GENESIS_HASH: str = "0" * 64

    def __init__(self, db_path: str = "data/qsentinel.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path) or ".", exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS verification_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    iso_time TEXT,
                    signer_id TEXT,
                    scenario TEXT,
                    message TEXT,
                    total_trials INTEGER,
                    error_count INTEGER,
                    error_rate REAL,
                    z_score REAL,
                    p_value REAL,
                    confidence REAL,
                    verdict TEXT,
                    latency_ms REAL,
                    diagnostic TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_chain (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    iso_time TEXT,
                    prev_hash TEXT,
                    entry_hash TEXT,
                    payload_json TEXT
                )
            """)
            conn.commit()

    def log_verification(
        self,
        assessment: ThreatAssessment,
        signer_id: str,
        scenario: str,
        message: str,
        latency_ms: float = 0.0,
        record_chain: bool = True
    ) -> int:
        now = time.time()
        iso_str = datetime.fromtimestamp(now).strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO verification_history (
                    timestamp, iso_time, signer_id, scenario, message,
                    total_trials, error_count, error_rate, z_score,
                    p_value, confidence, verdict, latency_ms, diagnostic
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                now,
                iso_str,
                signer_id,
                scenario,
                message,
                assessment.total_trials,
                assessment.error_count,
                assessment.error_rate,
                assessment.z_score,
                assessment.p_value,
                assessment.confidence,
                assessment.verdict.value,
                latency_ms,
                assessment.diagnostic_text
            ))
            conn.commit()
            last_id = cursor.lastrowid

        if record_chain:
            audit_record = {
                "id": last_id,
                "signer_id": signer_id,
                "scenario": scenario,
                "message": message,
                "verdict": assessment.verdict.value,
                "total_trials": assessment.total_trials,
                "error_count": assessment.error_count,
                "error_rate": round(float(assessment.error_rate), 6),
                "z_score": round(float(assessment.z_score), 6),
                "p_value": round(float(assessment.p_value), 6),
                "confidence": round(float(assessment.confidence), 6),
                "latency_ms": round(float(latency_ms), 4),
                "diagnostic": assessment.diagnostic_text
            }
            self.append_chained(audit_record)

        return last_id

    def append_chained(self, record: Dict[str, Any]) -> str:
        """
        Appends an arbitrary event record to the tamper-evident SHA3-256 audit chain.
        Returns the computed entry_hash.
        """
        now = time.time()
        iso_str = datetime.fromtimestamp(now).strftime("%Y-%m-%d %H:%M:%S")
        payload_str = canonical_json(record)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT entry_hash FROM audit_chain ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            prev_hash = row[0] if row else self.GENESIS_HASH
            
            entry_hash = hashlib.sha3_256((payload_str + prev_hash).encode("utf-8")).hexdigest()
            
            cursor.execute("""
                INSERT INTO audit_chain (
                    timestamp, iso_time, prev_hash, entry_hash, payload_json
                ) VALUES (?, ?, ?, ?, ?)
            """, (now, iso_str, prev_hash, entry_hash, payload_str))
            conn.commit()
            return entry_hash

    def verify_chain(self) -> Tuple[bool, Optional[int], str]:
        """
        Verifies the cryptographic integrity of the entire audit chain.
        Returns: (is_valid, broken_at_id, reason)
        If valid: (True, None, "Chain intact")
        If corrupted or broken link: (False, broken_id, reason_str)
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, prev_hash, entry_hash, payload_json FROM audit_chain ORDER BY id ASC")
            rows = cursor.fetchall()
            
        if not rows:
            return True, None, "Chain intact (empty)"
            
        expected_prev = self.GENESIS_HASH
        for row in rows:
            row_id, prev_hash, entry_hash, payload_json = row
            
            # Check linkage to predecessor
            if prev_hash != expected_prev:
                return False, row_id, f"Broken link at id {row_id}: expected prev_hash {expected_prev}, got {prev_hash}"
                
            # Recompute SHA3-256
            recomputed = hashlib.sha3_256((payload_json + prev_hash).encode("utf-8")).hexdigest()
            if recomputed != entry_hash:
                return False, row_id, f"Hash mismatch at id {row_id}: computed {recomputed}, recorded {entry_hash}"
                
            expected_prev = entry_hash
            
        return True, None, "Chain intact"

    def get_audit_chain(self, limit: int = 50) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM audit_chain
                ORDER BY id DESC LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def get_latest_chain_hash(self) -> str:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT entry_hash FROM audit_chain ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            return row[0] if row else self.GENESIS_HASH

    def get_recent_runs(self, limit: int = 50) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM verification_history
                ORDER BY id DESC LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def get_dataframe(self, limit: int = 100) -> pd.DataFrame:
        runs = self.get_recent_runs(limit=limit)
        if not runs:
            return pd.DataFrame(columns=[
                "ID", "Time", "Signer", "Scenario", "Verdict",
                "Error Rate", "Z-Score", "p-value", "Latency (ms)"
            ])
        df = pd.DataFrame(runs)
        df = df[[
            "id", "iso_time", "signer_id", "scenario", "verdict",
            "error_rate", "z_score", "p_value", "latency_ms"
        ]]
        df.columns = [
            "ID", "Time", "Signer", "Scenario", "Verdict",
            "Error Rate", "Z-Score", "p-value", "Latency (ms)"
        ]
        return df

    def clear_history(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM verification_history")
            cursor.execute("DELETE FROM audit_chain")
            conn.commit()
