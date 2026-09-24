"""
Q-Sentinel: Automated Test Suite Runner
Smart India Hackathon (SIH-26141) - Grand Finale Production Release

Executes complete regression test suite verifying 100% pass rate
across all quantum physical and cyber security watchtowers.
"""

import sys
import pytest


def main() -> None:
    """Entry point for automated test suite execution."""
    print("=" * 72)
    print("Q-SENTINEL: AUTOMATED TEST SUITE EXECUTION")
    print("Smart India Hackathon (SIH-26141) - Grand Finale Verification")
    print("=" * 72)
    ret_code = pytest.main(["tests/", "-v"])
    sys.exit(ret_code)


if __name__ == "__main__":
    main()
