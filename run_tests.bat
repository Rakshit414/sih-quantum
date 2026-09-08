@echo off
REM ============================================================================
REM Q-SENTINEL: One-Click Automated Regression Test Runner
REM Smart India Hackathon (SIH-26141) | Full Regression Verification
REM ============================================================================
title Q-Sentinel - Automated Test Suite
echo.
echo ============================================================================
echo   Q-SENTINEL: AUTOMATED TEST SUITE EXECUTION
echo   Verifying 100% Pass Rate Across All Quantum Physical Modules
echo ============================================================================
echo.
python -m pytest tests/ -v
echo.
echo ============================================================================
pause
