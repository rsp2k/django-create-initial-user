#!/usr/bin/env python
"""Django test runner script for the django-create-initial-user project."""

import os
import subprocess
import sys
from pathlib import Path


def main():
    """Run the Django test suite."""
    # Change to the project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)

    # Set up environment
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")

    # Build the command - start with basic django test command
    cmd = ["python", "-m", "django", "test", "--settings=tests.settings"]

    # Add any arguments passed to this script
    if len(sys.argv) > 1:
        cmd.extend(sys.argv[1:])
    else:
        # Default to verbose level 2
        cmd.extend(["-v", "2"])

    print(f"Running command: {' '.join(cmd)}")
    print(f"Working directory: {project_dir}")
    print("-" * 50)

    # Run the tests
    result = subprocess.run(cmd, cwd=project_dir)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
