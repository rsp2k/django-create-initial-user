# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
Django Create Initial User is a Django authentication backend that automatically creates a superuser on first login when no superusers exist in the database. It's designed to simplify Django development setup.

## Key Components

### Main Backend Implementation
- `create_initial_superuser/backends.py`: Contains the `CreateInitialSuperUserBackend` class that handles automatic superuser creation
- The backend checks if DEBUG=True and no superusers exist, then creates one with the provided credentials
- Supports both username and email-based authentication

### Testing
- Tests are located in `tests/` directory
- Main test file: `tests/test_backends.py`
- Test settings: `tests/settings.py`

## Common Commands

### Running Tests
```bash
# Run all tests
python run_tests.py

# Run specific test module
python run_tests.py tests.test_backends -v 2

# Run with coverage
make test-coverage

# Quick test run
python quick_test.py
```

### Code Quality & Formatting
```bash
# Format code with black and isort
make format

# Run linting checks
make lint

# Run security checks
make security
```

### Building & Publishing
```bash
# Build distribution packages
make build

# Create a patch release
make release-patch

# Interactive release creation
python create-release.py

# Publish to PyPI (interactive)
python publish-to-pypi.py
```

### Development Setup
```bash
# Complete development environment setup
make dev-setup

# Install development dependencies
make install-dev

# Setup pre-commit hooks
make precommit-setup
```

## Architecture Notes

### Authentication Flow
1. User attempts to login through Django admin or authentication
2. `CreateInitialSuperUserBackend.authenticate()` is called
3. If DEBUG=True and no superusers exist, `_create_initial_superuser()` creates one
4. The method handles both username and email authentication
5. Password is properly hashed using Django's `make_password()`
6. A warning is issued when creating the initial superuser

### Key Design Decisions
- Only works when DEBUG=True by default (security feature)
- Automatically detects email-like usernames and sets the email field
- Falls back to Django's default ModelBackend when superusers exist
- Proper password hashing and security practices
- Compatible with custom user models

## Testing Strategy
- Tests verify behavior with and without existing superusers
- Tests cover DEBUG=True and DEBUG=False scenarios
- Tests verify email detection and setting
- Tests ensure proper password hashing
- Tests verify warning messages are issued
- Tests cover edge cases (empty credentials, None values)

## CI/CD Pipeline
- GitHub Actions workflows in `.github/workflows/`
- Test matrix covers Python 3.9-3.12 and Django 4.2-5.1
- Automated security checks, linting, and coverage reporting
- Build verification and package testing
