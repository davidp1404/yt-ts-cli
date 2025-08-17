#!/usr/bin/env python3
"""
Test runner for yt-ts-cli.

This script runs the test suite using UV with the necessary dependencies.
Supports both unit tests (fast, no network) and integration tests (slow, real URLs).
"""

import subprocess
import sys
import argparse
from pathlib import Path


def run_tests(test_type="unit", verbose=False):
    """Run the test suite."""
    project_root = Path(__file__).parent
    
    if test_type == "unit":
        print("🧪 Running yt-ts-cli UNIT tests (fast, no network calls)...")
        test_files = ["tests/test_simple.py"]
        markers = []
    elif test_type == "integration":
        print("🌐 Running yt-ts-cli INTEGRATION tests (slow, real YouTube URLs)...")
        test_files = ["tests/test_integration.py"]
        markers = ["-m", "integration"]
    elif test_type == "all":
        print("🧪🌐 Running ALL yt-ts-cli tests (unit + integration)...")
        test_files = ["tests/"]  # Now safe to use tests/ since broken files are removed
        markers = []
    else:
        print(f"❌ Unknown test type: {test_type}")
        return 1
    
    print("=" * 60)
    
    # Build command
    cmd = [
        "uv", "run", 
        "--with", "pytest", 
        "--with", "pytest-mock",
        "pytest"
    ] + test_files + markers
    
    if verbose:
        cmd.append("-v")
    else:
        cmd.append("-v")  # Always verbose for now
    
    # Add warnings for integration tests
    if test_type in ["integration", "all"]:
        print("⚠️  Integration tests make real network calls to YouTube")
        print("⚠️  They may be slow and can fail due to network issues")
        print("⚠️  Video availability may change over time")
        print("-" * 60)
    
    try:
        result = subprocess.run(cmd, cwd=project_root, check=True)
        
        if test_type == "unit":
            print("\n✅ All unit tests passed!")
        elif test_type == "integration":
            print("\n✅ All integration tests passed!")
        else:
            print("\n✅ All tests passed!")
        
        return 0
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code {e.returncode}")
        return e.returncode
    except FileNotFoundError:
        print("❌ UV not found. Please install UV first:")
        print("   curl -LsSf https://astral.sh/uv/install.sh | sh")
        return 1


def main():
    parser = argparse.ArgumentParser(description="Run yt-ts-cli tests")
    parser.add_argument(
        "test_type", 
        nargs="?", 
        default="unit",
        choices=["unit", "integration", "all"],
        help="Type of tests to run (default: unit)"
    )
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    return run_tests(args.test_type, args.verbose)


if __name__ == "__main__":
    sys.exit(main())
