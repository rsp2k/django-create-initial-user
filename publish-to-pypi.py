#!/usr/bin/env python3
"""
🚀 PyPI Publishing Script

This script guides you through publishing your Django package to PyPI
with all the necessary checks and validations.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description, check=True):
    """Run a command and handle errors."""
    print(f"\n🔧 {description}")
    print(f"💻 Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, check=check, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Success!")
            return True
        else:
            print(f"❌ {description} - Failed!")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed with error: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {cmd[0]}")
        return False


def check_prerequisites():
    """Check if all prerequisites are met."""
    print("🔍 Checking prerequisites...")

    checks = [
        (["git", "status", "--porcelain"], "Checking for uncommitted changes"),
        (["uv", "--version"], "Checking uv installation"),
        (["python", "-m", "twine", "--version"], "Checking twine installation"),
    ]

    all_good = True

    for cmd, desc in checks:
        if not run_command(cmd, desc, check=False):
            all_good = False

    # Check for uncommitted changes
    result = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True
    )
    if result.stdout.strip():
        print("⚠️  You have uncommitted changes:")
        print(result.stdout)
        print("💡 Consider committing changes before publishing")

        response = input("\n❓ Continue anyway? (y/N): ").lower()
        if response != "y":
            return False

    return all_good


def run_tests():
    """Run the test suite."""
    print("\n🧪 Running test suite...")

    commands = [
        (["python", "dev-test.py"], "Running development test suite"),
        (["uv", "run", "pytest", "tests/", "-v"], "Running pytest"),
    ]

    for cmd, desc in commands:
        if not run_command(cmd, desc, check=False):
            response = input(f"\n❓ {desc} failed. Continue anyway? (y/N): ").lower()
            if response != "y":
                return False

    return True


def build_package():
    """Build the package."""
    print("\n📦 Building package...")

    # Clean previous builds
    run_command(
        ["rm", "-rf", "dist/", "build/"], "Cleaning previous builds", check=False
    )

    # Build package
    if not run_command(["uv", "build"], "Building package with uv"):
        return False

    # Check package
    if not run_command(
        ["python", "-m", "twine", "check", "dist/*"], "Checking package"
    ):
        return False

    return True


def get_version():
    """Get the current version from pyproject.toml."""
    try:
        with open("pyproject.toml") as f:
            for line in f:
                if line.startswith("version = "):
                    version = line.split("=")[1].strip().strip('"')
                    return version
    except FileNotFoundError:
        print("❌ pyproject.toml not found")
        return None

    print("❌ Version not found in pyproject.toml")
    return None


def confirm_publish(environment):
    """Confirm publication details."""
    version = get_version()
    if not version:
        return False

    print(f"\n📋 Publication Summary:")
    print(f"   Package: django-create-initial-user")
    print(f"   Version: {version}")
    print(f"   Environment: {environment}")

    if environment == "pypi":
        print(
            f"   🌍 URL: https://pypi.org/project/django-create-initial-user/{version}/"
        )
        print(f"\n⚠️  WARNING: This will publish to PRODUCTION PyPI!")
        print(f"           This action cannot be undone!")
    else:
        print(
            f"   🧪 URL: https://test.pypi.org/project/django-create-initial-user/{version}/"
        )
        print(f"   ℹ️  This is Test PyPI (safe for testing)")

    response = input(f"\n❓ Proceed with publication? (y/N): ").lower()
    return response == "y"


def publish_package(environment):
    """Publish the package."""
    print(f"\n🚀 Publishing to {environment.upper()}...")

    if environment == "testpypi":
        cmd = ["python", "-m", "twine", "upload", "--repository", "testpypi", "dist/*"]
        desc = "Uploading to Test PyPI"
    else:
        cmd = ["python", "-m", "twine", "upload", "dist/*"]
        desc = "Uploading to PyPI"

    return run_command(cmd, desc)


def main():
    """Main publishing workflow."""
    print("🚀 Django Create Initial User - PyPI Publishing Script")
    print("=" * 60)

    # Change to project directory
    os.chdir(Path(__file__).parent)

    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please fix issues and try again.")
        sys.exit(1)

    # Choose environment
    print("\n🎯 Choose publishing environment:")
    print("  1. Test PyPI (recommended for first-time)")
    print("  2. Production PyPI")

    while True:
        choice = input("\nEnter choice (1 or 2): ").strip()
        if choice == "1":
            environment = "testpypi"
            break
        elif choice == "2":
            environment = "pypi"
            break
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")

    # Run tests
    if not run_tests():
        print("\n❌ Tests failed. Please fix issues and try again.")
        sys.exit(1)

    # Build package
    if not build_package():
        print("\n❌ Package build failed. Please fix issues and try again.")
        sys.exit(1)

    # Confirm publication
    if not confirm_publish(environment):
        print("\n👋 Publication cancelled by user.")
        sys.exit(0)

    # Publish package
    if publish_package(environment):
        version = get_version()
        print("\n" + "=" * 60)
        print("🎉 Package published successfully!")

        if environment == "testpypi":
            print(f"\n🧪 Test PyPI URL:")
            print(
                f"   https://test.pypi.org/project/django-create-initial-user/{version}/"
            )
            print(f"\n💡 Test installation:")
            print(
                f"   pip install -i https://test.pypi.org/simple/ django-create-initial-user"
            )
            print(
                f"\n🚀 Ready for production? Run this script again and choose option 2."
            )
        else:
            print(f"\n🌍 PyPI URL:")
            print(f"   https://pypi.org/project/django-create-initial-user/{version}/")
            print(f"\n📦 Installation:")
            print(f"   pip install django-create-initial-user")
            print(f"\n🎊 Congratulations! Your package is now publicly available!")
    else:
        print("\n❌ Publication failed. Please check errors and try again.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Publication cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check the error and try again.")
        sys.exit(1)
