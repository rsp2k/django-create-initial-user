#!/usr/bin/env python
"""Quick test to verify Django test setup."""

import os
import subprocess
import sys
from pathlib import Path


def main():
    """Run a quick test."""
    project_dir = Path(__file__).parent
    os.chdir(project_dir)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")

    print("🧪 Running quick Django test verification...")

    # Run a single simple test
    cmd = [
        "python",
        "-m",
        "django",
        "test",
        "tests.test_apps.AppConfigTests.test_app_config",
        "--settings=tests.settings",
        "-v",
        "2",
    ]

    print(f"Command: {' '.join(cmd)}")
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("✅ Django test setup is working!")
        print("\nTo run all tests: make test")
        print("To run with coverage: make test-coverage")
    else:
        print("❌ Test failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
