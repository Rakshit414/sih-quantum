#!/usr/bin/env bash
# ==============================================================================
# Q-SENTINEL: Linux / macOS Application Launcher
# Smart India Hackathon (SIH-26141) | Grand Finale Evaluation Runner
# ==============================================================================

set -e

echo "=============================================================================="
echo "  Q-SENTINEL: QUANTUM-INSPIRED CYBER THREAT DETECTION FRAMEWORK"
echo "  Teleportation-Based Quantum Digital Signature Verification Watchtower"
echo "  Smart India Hackathon (SIH-26141) - Grand Finale Production Release"
echo "=============================================================================="
echo ""

if ! command -v python3 &> /dev/null; then
    echo "[ERROR] python3 could not be found. Please install Python 3.10+."
    exit 1
fi

echo "[*] Launching Q-Sentinel Streamlit Web Dashboard..."
echo "[*] Local URL: http://localhost:8501"
echo ""

python3 -m streamlit run app.py --server.port 8501 --server.headless false
