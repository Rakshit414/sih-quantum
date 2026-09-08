"""
Test Suite: Deployment, Pitch Deck, and Submission Packaging Verification
Phase 41 - Final Deployment, Pitch Deck & Distribution Packaging
Zero AI/ML Models. Deterministic verification of deployment artifacts.
"""

import os
import hashlib
from pathlib import Path
import pytest


def test_launchers_exist_and_valid():
    """Verify that all production Windows and Linux launcher scripts exist and contain proper commands."""
    workspace_root = Path(__file__).resolve().parent.parent

    launchers = {
        "run_qsentinel.bat": "streamlit run app.py",
        "run_tests.bat": "pytest",
        "run_audit.bat": "release_audit.py",
        "run_qsentinel.sh": "streamlit run app.py",
    }

    for filename, expected_cmd in launchers.items():
        file_path = workspace_root / filename
        assert file_path.exists(), f"Launcher script {filename} is missing."
        assert file_path.stat().st_size > 0, f"Launcher script {filename} is empty."
        content = file_path.read_text(encoding="utf-8")
        assert expected_cmd in content, f"Expected command '{expected_cmd}' not found in {filename}."


def test_docker_configuration_integrity():
    """Verify Docker containerization files, port exposure, security profile, and healthcheck."""
    workspace_root = Path(__file__).resolve().parent.parent

    dockerfile = workspace_root / "Dockerfile"
    docker_compose = workspace_root / "docker-compose.yml"
    dockerignore = workspace_root / ".dockerignore"

    assert dockerfile.exists(), "Dockerfile is missing."
    assert docker_compose.exists(), "docker-compose.yml is missing."
    assert dockerignore.exists(), ".dockerignore is missing."

    df_content = dockerfile.read_text(encoding="utf-8")
    assert "8501" in df_content, "Port 8501 not exposed in Dockerfile."
    assert "useradd" in df_content or "qsentinel" in df_content, "Non-root user not configured in Dockerfile."
    assert "HEALTHCHECK" in df_content, "Healthcheck instruction missing in Dockerfile."

    dc_content = docker_compose.read_text(encoding="utf-8")
    assert "8501:8501" in dc_content, "Port mapping 8501:8501 missing in docker-compose.yml."


def test_pitch_deck_structure():
    """Verify that the SIH Grand Finale pitch deck contains all 12 slides and required sections."""
    workspace_root = Path(__file__).resolve().parent.parent
    pitch_deck = workspace_root / "docs" / "SIH26141_FINAL_PITCH_DECK.md"

    assert pitch_deck.exists(), "Final pitch deck docs/SIH26141_FINAL_PITCH_DECK.md is missing."
    content = pitch_deck.read_text(encoding="utf-8")

    # Verify all 12 slides
    for slide_num in range(1, 13):
        assert f"## Slide {slide_num}:" in content, f"Slide {slide_num} is missing from pitch deck."

    # Verify key sections
    assert "30-Second Elevator Pitch" in content
    assert "1-Minute Executive Overview" in content
    assert "3-Minute Technical Architecture Walkthrough" in content
    assert "Judge Q&A & Objection Handling Matrix" in content


def test_packaging_engine_and_checksum():
    """Verify that the automated packaging engine creates valid zip file with matching SHA-256."""
    workspace_root = Path(__file__).resolve().parent.parent
    dist_dir = workspace_root / "dist"
    zip_path = dist_dir / "Q-SENTINEL_SIH26141_FINAL_SUBMISSION.zip"
    sha_path = dist_dir / "Q-SENTINEL_SIH26141_FINAL_SUBMISSION.zip.sha256"

    assert zip_path.exists(), "Distribution package zip is missing."
    assert sha_path.exists(), "Distribution package SHA-256 file is missing."

    recorded_sha = sha_path.read_text(encoding="utf-8").strip().split()[0]

    hasher = hashlib.sha256()
    with open(zip_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    actual_sha = hasher.hexdigest()

    assert recorded_sha == actual_sha, f"SHA-256 mismatch! Recorded: {recorded_sha}, Actual: {actual_sha}"
