"""
Q-Sentinel: Grand Unified Release Audit Runner
Smart India Hackathon (SIH-26141) - Grand Finale Production Release

Executes the complete 8-pillar master release audit and confirms
cryptographic release freeze lock.
"""

import sys
from release_audit import GrandUnifiedReleaseAuditor


def main() -> None:
    """Entry point for grand unified release audit."""
    print("=" * 72)
    print("Q-SENTINEL: MASTER RELEASE AUDIT RUNNER")
    print("Smart India Hackathon (SIH-26141) - Grand Finale Verification")
    print("=" * 72)
    auditor = GrandUnifiedReleaseAuditor()
    report = auditor.execute_grand_unified_audit()
    sys.exit(0 if report.audit_pass_rate == 1.0 else 1)


if __name__ == "__main__":
    main()
