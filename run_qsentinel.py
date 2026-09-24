"""
Q-Sentinel: Cross-Platform Web Application Launcher
Smart India Hackathon (SIH-26141) - Grand Finale Production Release

Launches the Q-Sentinel Streamlit Web Dashboard deterministically
across Windows, Linux, and macOS without triggering executable
or script-blocking antivirus heuristics.
"""

import sys
import streamlit.web.cli as stcli


def main() -> None:
    """Entry point for Q-Sentinel web application."""
    print("=" * 72)
    print("Q-SENTINEL: QUANTUM-INSPIRED CYBER THREAT DETECTION FRAMEWORK")
    print("Teleportation-Based Quantum Digital Signature Watchtower")
    print("Smart India Hackathon (SIH-26141) - Grand Finale Release")
    print("=" * 72)
    print("[*] Launching Streamlit Web Dashboard at http://localhost:8501 ...")
    sys.argv = [
        "streamlit",
        "run",
        "app.py",
        "--server.port",
        "8501",
        "--server.headless",
        "false",
    ]
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
