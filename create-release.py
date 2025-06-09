#!/usr/bin/env python3
"""
🚀 Automated Release Script

This script helps you create a new release with automated version management,
changelog updates, and GitHub release creation.
"""

import re
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description, check=True):
    """Run a command and handle errors."""
    print(f"\n🔧 {description}")
    print(f"💻 Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, check=check, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Success!")
            return result.stdout.strip()
        else:
            print(f"❌ {description} - Failed!")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return None
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed!")
        print(f"Error: {e}")
        return None


def get_current_version():
    """Get the current version from pyproject.toml."""
    try:
        with open("pyproject.toml") as f:
            content = f.read()
            match = re.search(r'version = "([^"]+)"', content)
            if match:
                return match.group(1)
    except FileNotFoundError:
        print("❌ pyproject.toml not found")
        return None

    print("❌ Version not found in pyproject.toml")
    return None


def update_version(new_version):
    """Update version in pyproject.toml."""
    try:
        with open("pyproject.toml") as f:
            content = f.read()

        # Update version
        new_content = re.sub(
            r'version = "[^"]+"', f'version = "{new_version}"', content
        )

        with open("pyproject.toml", "w") as f:
            f.write(new_content)

        print(f"✅ Updated version to {new_version} in pyproject.toml")
        return True
    except Exception as e:
        print(f"❌ Failed to update version: {e}")
        return False


def suggest_next_version(current_version):
    """Suggest next version based on current version."""
    parts = current_version.split(".")
    if len(parts) != 3:
        return None

    major, minor, patch = map(int, parts)

    suggestions = {
        "patch": f"{major}.{minor}.{patch + 1}",
        "minor": f"{major}.{minor + 1}.0",
        "major": f"{major + 1}.0.0",
    }

    return suggestions


def update_changelog(version):
    """Update CHANGELOG.md with new version."""
    changelog_path = Path("CHANGELOG.md")

    if not changelog_path.exists():
        print("⚠️  CHANGELOG.md not found, skipping changelog update")
        return True

    try:
        with open(changelog_path) as f:
            content = f.read()

        # Check if version already exists
        if f"## [{version}]" in content:
            print(f"ℹ️  Version {version} already exists in CHANGELOG.md")
            return True

        # Find the insertion point (after # Changelog header)
        lines = content.split("\n")
        insert_index = None

        for i, line in enumerate(lines):
            if line.startswith("## [") and "Unreleased" not in line:
                insert_index = i
                break

        if insert_index is None:
            # Find after # Changelog header
            for i, line in enumerate(lines):
                if line.startswith("# Changelog"):
                    insert_index = i + 2
                    break

        if insert_index is None:
            print("⚠️  Could not find insertion point in CHANGELOG.md")
            return False

        # Insert new version entry
        from datetime import datetime

        today = datetime.now().strftime("%Y-%m-%d")

        new_entry = [
            f"## [{version}] - {today}",
            "",
            "### Added",
            "- New features and improvements",
            "",
            "### Changed",
            "- Updated dependencies and improvements",
            "",
            "### Fixed",
            "- Bug fixes and stability improvements",
            "",
        ]

        # Insert the new entry
        lines[insert_index:insert_index] = new_entry

        with open(changelog_path, "w") as f:
            f.write("\n".join(lines))

        print(f"✅ Added version {version} to CHANGELOG.md")
        print(f"💡 Please edit CHANGELOG.md to add specific changes")
        return True

    except Exception as e:
        print(f"❌ Failed to update CHANGELOG.md: {e}")
        return False


def check_git_status():
    """Check if git working directory is clean."""
    result = run_command(
        ["git", "status", "--porcelain"], "Checking git status", check=False
    )
    if result is None:
        return False

    if result:
        print("⚠️  You have uncommitted changes:")
        print(result)
        response = input("\n❓ Continue anyway? (y/N): ").lower()
        return response == "y"

    return True


def run_tests():
    """Run tests before release."""
    print("\n🧪 Running tests before release...")

    result = run_command(
        ["python", "dev-test.py"], "Running development tests", check=False
    )
    if result is None:
        response = input("\n❓ Tests failed. Continue anyway? (y/N): ").lower()
        return response == "y"

    return True


def create_git_commit_and_tag(version):
    """Create git commit and tag for the release."""
    # Add changed files
    run_command(
        ["git", "add", "pyproject.toml", "CHANGELOG.md"], "Adding changed files"
    )

    # Commit changes
    result = run_command(
        ["git", "commit", "-m", f"bump: version {version}"],
        f"Committing version {version}",
        check=False,
    )

    if result is None:
        print("ℹ️  No changes to commit")

    # Create tag
    run_command(["git", "tag", f"v{version}"], f"Creating tag v{version}")

    return True


def push_changes(version):
    """Push changes and tags to remote."""
    # Push commits
    run_command(["git", "push"], "Pushing commits")

    # Push tags
    run_command(["git", "push", "origin", f"v{version}"], f"Pushing tag v{version}")

    return True


def main():
    """Main release workflow."""
    print("🚀 Django Create Initial User - Automated Release")
    print("=" * 60)

    # Change to project directory
    Path(__file__).parent.resolve()

    # Check git status
    if not check_git_status():
        print("\n❌ Please commit your changes first")
        sys.exit(1)

    # Get current version
    current_version = get_current_version()
    if not current_version:
        sys.exit(1)

    print(f"\n📋 Current version: {current_version}")

    # Suggest next version
    suggestions = suggest_next_version(current_version)
    if suggestions:
        print(f"\n💡 Version suggestions:")
        print(f"   1. Patch: {suggestions['patch']} (bug fixes)")
        print(f"   2. Minor: {suggestions['minor']} (new features)")
        print(f"   3. Major: {suggestions['major']} (breaking changes)")
        print(f"   4. Custom version")

        while True:
            choice = input("\nChoose version type (1-4): ").strip()
            if choice == "1":
                new_version = suggestions["patch"]
                break
            elif choice == "2":
                new_version = suggestions["minor"]
                break
            elif choice == "3":
                new_version = suggestions["major"]
                break
            elif choice == "4":
                new_version = input("Enter custom version: ").strip()
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
    else:
        new_version = input("Enter new version: ").strip()

    if not new_version:
        print("❌ Version cannot be empty")
        sys.exit(1)

    print(f"\n🎯 New version: {new_version}")

    # Confirm release
    response = input(f"\n❓ Create release v{new_version}? (y/N): ").lower()
    if response != "y":
        print("👋 Release cancelled")
        sys.exit(0)

    # Run tests
    if not run_tests():
        print("\n❌ Release cancelled due to test failures")
        sys.exit(1)

    # Update version
    if not update_version(new_version):
        sys.exit(1)

    # Update changelog
    if not update_changelog(new_version):
        sys.exit(1)

    # Create commit and tag
    if not create_git_commit_and_tag(new_version):
        sys.exit(1)

    # Push changes
    print(f"\n🚀 Pushing release v{new_version}...")
    if not push_changes(new_version):
        sys.exit(1)

    print("\n" + "=" * 60)
    print("🎉 Release created successfully!")
    print(f"\n📋 What happens next:")
    print(f"   1. GitHub will automatically create a release")
    print(f"   2. Package will be built and published to PyPI")
    print(f"   3. You can monitor progress in GitHub Actions")
    print(f"\n🔗 Links:")
    print(
        f"   Release: https://github.com/rsp2k/django-create-initial-user/releases/tag/v{new_version}"
    )
    print(f"   Actions: https://github.com/rsp2k/django-create-initial-user/actions")
    print(f"   PyPI: https://pypi.org/project/django-create-initial-user/")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Release cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
