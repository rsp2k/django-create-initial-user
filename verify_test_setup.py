#!/usr/bin/env python
"""Verify the Django test setup is working correctly."""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"Command: {' '.join(cmd)}")
    print("=" * 60)

    result = subprocess.run(cmd, capture_output=False)

    if result.returncode == 0:
        print(f"✅ {description} - PASSED")
        return True
    else:
        print(f"❌ {description} - FAILED")
        return False


def main():
    """Run verification tests."""
    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)

    # Set environment
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")

    print("🚀 Verifying Django test setup for django-create-initial-user")
    print(f"Working directory: {project_dir}")

    tests_passed = 0
    total_tests = 0

    # Test 1: Check Django configuration
    total_tests += 1
    if run_command(
        ["python", "-m", "django", "check", "--settings=tests.settings"],
        "Django configuration",
    ):
        tests_passed += 1

    # Test 2: Run app config tests
    total_tests += 1
    if run_command(
        [
            "python",
            "-m",
            "django",
            "test",
            "tests.test_apps",
            "--settings=tests.settings",
            "-v",
            "2",
        ],
        "App configuration tests",
    ):
        tests_passed += 1

    # Test 3: Run backend tests
    total_tests += 1
    if run_command(
        [
            "python",
            "-m",
            "django",
            "test",
            "tests.test_backends",
            "--settings=tests.settings",
            "-v",
            "2",
        ],
        "Backend authentication tests",
    ):
        tests_passed += 1

    # Test 4: Run all tests
    total_tests += 1
    if run_command(
        ["python", "-m", "django", "test", "--settings=tests.settings", "-v", "2"],
        "Full test suite",
    ):
        tests_passed += 1

    # Test 5: Test coverage (if available)
    total_tests += 1
    if run_command(
        [
            "coverage",
            "run",
            "--source=create_initial_superuser",
            "-m",
            "django",
            "test",
            "--settings=tests.settings",
        ],
        "Coverage test",
    ):
        tests_passed += 1
        # Show coverage report
        subprocess.run(["coverage", "report", "-m"], capture_output=False)

    # Summary
    print(f"\n{'='*60}")
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    print(f"Tests passed: {tests_passed}/{total_tests}")

    if tests_passed == total_tests:
        print("🎉 All tests passed! Your Django test setup is working correctly.")
        print("\n📋 Available test commands:")
        print("  make test           - Run all tests")
        print("  make test-coverage  - Run tests with coverage")
        print("  make test-quick     - Run tests with minimal output")
        print("  make test-backends  - Run only backend tests")
        print("  python run_tests.py - Custom test runner script")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
