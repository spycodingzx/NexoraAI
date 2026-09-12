#!/usr/bin/env python3
"""
Test Runner Script

Run all specs with various options.
"""

import sys
import subprocess
from pathlib import Path


def nv_run_tests(args=None):
    """
    Run pytest with given arguments.

    Args:
        args: List of additional pytest arguments
    """
    cmd = ["pytest"]

    if args:
        cmd.extend(args)
    else:
        # Default: run all specs with coverage
        cmd.extend(
            [
                "-v",  # Verbose
                "--tb=short",  # Short traceback
                "--cov=core",  # Coverage for core directory
                "--cov-report=html",  # HTML coverage report
                "--cov-report=term",  # Terminal coverage report
            ]
        )

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=Path(__file__).parent.parent)
    return result.returncode


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Run specs")
    parser.add_argument("pytest_args", nargs="*", help="Additional pytest arguments")
    parser.add_argument("--unit", action="store_true", help="Run only unit specs")
    parser.add_argument("--integration", action="store_true", help="Run only integration specs")
    parser.add_argument("--fast", action="store_true", help="Run fast specs only (skip slow specs)")

    args = parser.parse_args()

    pytest_args = list(args.pytest_args)

    if args.unit:
        pytest_args.append("specs/unit")
    elif args.integration:
        pytest_args.append("specs/integration")

    if args.fast:
        pytest_args.extend(["-m", "not slow"])

    sys.exit(nv_run_tests(pytest_args))


if __name__ == "__main__":
    main()
