@echo off
REM ============================================================================
REM Q-SENTINEL: One-Click Windows Application Launcher
REM Smart India Hackathon (SIH-26141) | Grand Finale Evaluation Runner
REM ============================================================================
title Q-Sentinel - Quantum Threat Detection System
echo.
echo ============================================================================
echo   Q-SENTINEL: QUANTUM-INSPIRED CYBER THREAT DETECTION FRAMEWORK
echo   Teleportation-Based Quantum Digital Signature Verification Watchtower
echo   Smart India Hackathon (SIH-26141) - Grand Finale Production Release
echo ============================================================================
echo.
echo [*] Checking Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in system PATH.
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

echo [*] Launching Q-Sentinel Streamlit Web Dashboard...
echo [*] Local URL: http://localhost:8501
echo.
python -m streamlit run app.py --server.port 8501 --server.headless false
pause
