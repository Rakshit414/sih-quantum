@echo off
REM ============================================================================
REM Q-SENTINEL: One-Click Master Release Audit Runner
REM Smart India Hackathon (SIH-26141) | Grand Unified Release Verification
REM ============================================================================
title Q-Sentinel - Release Audit Runner
echo.
echo ============================================================================
echo   Q-SENTINEL: GRAND UNIFIED RELEASE AUDIT (8 AUDIT PILLARS)
echo   Verifying Production Freeze & Cryptographic Integrity Checksums
echo ============================================================================
echo.
python release_audit.py
echo.
echo ============================================================================
pause
