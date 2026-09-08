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
from typing import List, Dict, Any, Optional
import pandas as pd
from security.detector import ThreatAssessment


class TelemetryStore:
    """
    Thread-safe SQLite datastore for security audit logs.
    """

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
            conn.commit()

    def log_verification(
        self,
        assessment: ThreatAssessment,
        signer_id: str,
        scenario: str,
        message: str,
        latency_ms: float = 0.0
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
            return cursor.lastrowid

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
            conn.commit()
