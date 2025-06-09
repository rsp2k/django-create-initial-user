#!/usr/bin/env python3
"""Development script to run tests locally."""

import os
import subprocess
import sys


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}")
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return False


def main():
    """Run the development test suite."""
    print("🚀 Django Create Initial User - Development Test Suite")

    # Change to project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)

    commands = [
        (
            ["uv", "pip", "install", "-e", ".[dev]"],
            "Installing development dependencies",
        ),
        (["uv", "run", "black", "--check", "."], "Checking code formatting with Black"),
        (
            ["uv", "run", "isort", "--check-only", "."],
            "Checking import sorting with isort",
        ),
        (
            ["uv", "run", "flake8", "create_initial_superuser", "tests"],
            "Running flake8 linting",
        ),
        (
            ["uv", "run", "mypy", "create_initial_superuser"],
            "Running mypy type checking",
        ),
        (
            ["uv", "run", "pytest", "tests/", "-v", "--cov=create_initial_superuser"],
            "Running test suite",
        ),
    ]

    failed_commands = []

    for cmd, description in commands:
        if not run_command(cmd, description):
            failed_commands.append(description)

    print("\n" + "=" * 60)
    if failed_commands:
        print("❌ Some checks failed:")
        for failed in failed_commands:
            print(f"  - {failed}")
        sys.exit(1)
    else:
        print("✅ All checks passed! Your code is ready for submission.")
        sys.exit(0)


if __name__ == "__main__":
    main()
