"""
Q-Sentinel: Automated Final Submission Packaging Engine
Smart India Hackathon (SIH-26141) | Production Packaging Specification

Compiles all certified source code, test suites, documentation, and deployment
launchers into a cryptographically sealed submission archive:
dist/Q-SENTINEL_SIH26141_FINAL_SUBMISSION.zip
"""

import os
import zipfile
import hashlib
import time
from pathlib import Path


def create_submission_package(workspace_root: str = ".") -> str:
    root = Path(workspace_root).resolve()
    dist_dir = root / "dist"
    dist_dir.mkdir(parents=True, exist_ok=True)

    archive_name = "Q-SENTINEL_SIH26141_FINAL_SUBMISSION.zip"
    archive_path = dist_dir / archive_name

    included_dirs = ["quantum", "security", "analytics", "dashboard", "data", "docs", "tests"]
    included_files = [
        "app.py",
        "benchmark.py",
        "rehearsal.py",
        "release_audit.py",
        "verify_demo.py",
        "verify_release.py",
        "requirements.txt",
        "README.md",
        "Dockerfile",
        "docker-compose.yml",
        ".dockerignore",
        "run_qsentinel.bat",
        "run_tests.bat",
        "run_audit.bat",
        "run_qsentinel.sh",
        "package_submission.py"
    ]

    excluded_extensions = {".pyc", ".pyo", ".pyd"}
    excluded_dirs = {"__pycache__", ".pytest_cache", ".git", ".idea", ".vscode", "venv", ".venv"}

    file_count = 0
    total_bytes = 0

    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add root files
        for fn in included_files:
            fp = root / fn
            if fp.exists():
                zf.write(fp, arcname=f"qsentinel/{fn}")
                file_count += 1
                total_bytes += fp.stat().st_size

        # Add directories
        for d in included_dirs:
            dp = root / d
            if dp.exists():
                for p in dp.rglob("*"):
                    if p.is_dir():
                        continue
                    if p.suffix in excluded_extensions:
                        continue
                    if any(ex in p.parts for ex in excluded_dirs):
                        continue

                    rel_path = p.relative_to(root)
                    zf.write(p, arcname=f"qsentinel/{rel_path.as_posix()}")
                    file_count += 1
                    total_bytes += p.stat().st_size

    # Compute SHA-256 checksum of the package
    archive_bytes = archive_path.read_bytes()
    package_sha256 = hashlib.sha256(archive_bytes).hexdigest()
    checksum_path = dist_dir / f"{archive_name}.sha256"
    checksum_path.write_text(f"{package_sha256}  {archive_name}\n", encoding="utf-8")

    return package_sha256


if __name__ == "__main__":
    print("=" * 80)
    print("Q-SENTINEL: AUTOMATED SUBMISSION PACKAGING ENGINE (PHASE 41)")
    print("=" * 80)
    t0 = time.perf_counter()
    checksum = create_submission_package()
    elapsed = time.perf_counter() - t0

    print(f"[*] Package Target:      dist/Q-SENTINEL_SIH26141_FINAL_SUBMISSION.zip")
    print(f"[*] Cryptographic Hash:  {checksum}")
    print(f"[*] Checksum File:       dist/Q-SENTINEL_SIH26141_FINAL_SUBMISSION.zip.sha256")
    print(f"[*] Packaging Completed: in {elapsed:.2f} seconds")
    print("=" * 80)
    print("SUBMISSION PACKAGE CERTIFIED AND SEALED FOR SMART INDIA HACKATHON GRAND FINALE.")
    print("=" * 80)
