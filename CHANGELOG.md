# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- Fixed email-only authentication where username is empty/null but email is provided in kwargs
- Backend now properly uses email as username when username is not provided

## [1.2.3] - 2025-06-09

### Added
- New features and improvements

### Changed
- Updated dependencies and improvements

### Fixed
- Bug fixes and stability improvements

## [1.2.2] - 2025-06-09

### Added
- New features and improvements

### Changed
- Updated dependencies and improvements

### Fixed
- Bug fixes and stability improvements

## [1.2.1] - 2025-06-09

### Added
- New features and improvements

### Changed
- Updated dependencies and improvements

### Fixed
- Bug fixes and stability improvements

## [1.2.0] - 2025-06-09

### Added
- New features and improvements

### Changed
- Updated dependencies and improvements

### Fixed
- Bug fixes and stability improvements

## [1.0.0] - 2025-06-09

### Added
- Initial release of django-create-initial-user
- `CreateInitialSuperUserBackend` authentication backend
- Automatic superuser creation on first login when no superusers exist
- Support for Django 3.2+ and Python 3.8+
- Comprehensive test suite with pytest and Django TestCase
- Type hints and mypy support
- GitHub Actions CI/CD pipeline
- Security considerations and DEBUG-only operation by default

### Features
- Creates superuser automatically when no superusers exist in database
- Warns when creating initial superuser for transparency
- Falls back to standard Django authentication for existing users
- Sets email field when username looks like an email address
- Only operates when `DEBUG=True` for security
- Comprehensive error handling and edge case coverage

### Security
- Passwords are properly hashed using Django's `make_password`
- Only creates users when `DEBUG=True` by default
- Includes security warnings and best practices in documentation
