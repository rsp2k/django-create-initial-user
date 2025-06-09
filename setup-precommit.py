#!/usr/bin/env python3
"""
🔧 Pre-commit Setup and Validation Script

This script sets up pre-commit hooks and runs an initial validation
to ensure everything is working correctly.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description, check=True, capture_output=True):
    """Run a shell command with nice output."""
    print(f"\n🔧 {description}")
    print(f"💻 Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            check=check,
            capture_output=capture_output,
            text=True,
            cwd=Path(__file__).parent,
        )

        if result.returncode == 0:
            print(f"✅ {description} - Success!")
            if not capture_output and result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ {description} - Failed!")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False

    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed!")
        print(f"Error: {e}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {cmd[0]}")
        return False


def check_virtual_environment():
    """Check if we're in a virtual environment."""
    in_venv = hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )

    if in_venv:
        print("✅ Virtual environment detected")
    else:
        print("⚠️  No virtual environment detected")
        print("💡 Consider running: uv venv && source .venv/bin/activate")

    return in_venv


def install_pre_commit():
    """Install and set up pre-commit."""
    commands = [
        (["pre-commit", "--version"], "Checking pre-commit installation"),
        (["pre-commit", "install"], "Installing pre-commit hooks"),
        (
            ["pre-commit", "install", "--hook-type", "commit-msg"],
            "Installing commit-msg hooks",
        ),
    ]

    all_success = True

    for cmd, desc in commands:
        if not run_command(cmd, desc):
            all_success = False

    return all_success


def run_pre_commit_checks():
    """Run pre-commit checks on all files."""
    print("\n🧪 Running pre-commit checks on all files...")
    print("📝 This may take a few minutes on first run...")

    return run_command(
        ["pre-commit", "run", "--all-files"],
        "Running all pre-commit hooks",
        check=False,  # Don't fail on hook failures
        capture_output=False,  # Show output in real-time
    )


def main():
    """Main setup function."""
    print("🚀 Django Create Initial User - Pre-commit Setup")
    print("=" * 60)

    # Change to project directory
    os.chdir(Path(__file__).parent)

    # Check virtual environment
    check_virtual_environment()

    # Install pre-commit
    if not install_pre_commit():
        print("\n❌ Failed to set up pre-commit hooks!")
        print("💡 Make sure pre-commit is installed: pip install pre-commit")
        sys.exit(1)

    # Run initial checks
    print("\n" + "=" * 60)
    print("🧪 Running initial pre-commit validation...")

    success = run_pre_commit_checks()

    print("\n" + "=" * 60)

    if success:
        print("🎉 Pre-commit setup completed successfully!")
        print("\n✨ Your repository now has automated code quality checks!")
        print("\n📋 What happens next:")
        print("  • Every commit will automatically run code formatting")
        print("  • Black will format your Python code")
        print("  • isort will organize your imports")
        print("  • flake8 will check for code quality issues")
        print("  • mypy will validate type hints")
        print("  • bandit will scan for security issues")
        print("\n🔧 Useful commands:")
        print("  pre-commit run --all-files    # Run all hooks manually")
        print("  pre-commit run black          # Run just Black")
        print("  pre-commit autoupdate         # Update hook versions")
    else:
        print("⚠️  Pre-commit setup completed with some issues.")
        print("\n🔧 Next steps:")
        print("  1. Fix any issues shown above")
        print("  2. Run: pre-commit run --all-files")
        print("  3. Commit your changes")

        print("\n💡 Common fixes:")
        print("  • Let Black and isort auto-fix formatting issues")
        print("  • Review and fix any flake8 warnings")
        print("  • Add missing type hints for mypy")

    print("\n🤝 Happy coding with automated quality checks! 🚀")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please report this issue on our GitHub repository.")
        sys.exit(1)
