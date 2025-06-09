# Makefile for django-create-initial-user development

.PHONY: help install install-dev test test-all lint format security clean build publish-test publish docs dev-setup

# Default target
help:
	@echo "Available commands:"
	@echo "  install        Install package in production mode"
	@echo "  install-dev    Install package in development mode"
	@echo "  test          Run tests with Django test runner"
	@echo "  test-coverage Run tests with coverage reporting"
	@echo "  test-quick    Run tests with minimal output"
	@echo "  test-backends Run only backend tests"
	@echo "  test-all      Run tests with tox (all Python/Django versions)"
	@echo "  lint          Run all linting tools"
	@echo "  format        Format code with black and isort"
	@echo "  security      Run security checks"
	@echo "  precommit-install    Install pre-commit hooks"
	@echo "  precommit-run        Run pre-commit on all files"
	@echo "  precommit-update     Update pre-commit hook versions"
	@echo "  precommit-setup      Complete pre-commit setup with validation"
	@echo "  clean         Clean build artifacts"
	@echo "  build         Build distribution packages"
	@echo "  publish-test  Publish to Test PyPI"
	@echo "  publish       Publish to PyPI"
	@echo "  publish-interactive  Interactive publishing with validation"
	@echo "  release-interactive  Interactive release creation"
	@echo "  release-patch        Quick patch release"
	@echo "  docs          Build documentation"
	@echo "  dev-setup     Complete development environment setup"

# Installation
install:
	uv pip install .

install-dev:
	uv pip install -e ".[dev]"

# Testing
test:
	uv run python -m django test --settings=tests.settings -v 2

test-coverage:
	uv run coverage run --source='create_initial_superuser' -m django test --settings=tests.settings && coverage report -m && coverage html

test-quick:
	uv run python -m django test --settings=tests.settings -v 1

test-backends:
	uv run python -m django test tests.test_backends --settings=tests.settings -v 2

test-all:
	tox

# Code quality
lint:
	uv run flake8 create_initial_superuser tests
	uv run mypy create_initial_superuser
	uv run black --check .
	uv run isort --check-only .

format:
	uv run black .
	uv run isort .
	@echo "✅ Code formatted with Black and isort"

security:
	uv run bandit -r create_initial_superuser
	uv run safety check

# Pre-commit hooks
precommit-install:
	uv run pre-commit install
	uv run pre-commit install --hook-type commit-msg
	@echo "✅ Pre-commit hooks installed"

precommit-run:
	uv run pre-commit run --all-files

precommit-update:
	uv run pre-commit autoupdate
	@echo "✅ Pre-commit hooks updated"

precommit-setup:
	python setup-precommit.py

# Build and publish
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	uv build

publish-test: build
	python -m twine upload --repository testpypi dist/*

publish: build
	python -m twine upload dist/*

# Automated release workflows
release-interactive:
	python create-release.py

release-patch:
	@echo "🚀 Creating patch release..."
	@python -c "import subprocess, re; \
		content = open('pyproject.toml').read(); \
		version = re.search(r'version = \"([^\"]+)\"', content).group(1); \
		parts = version.split('.'); \
		new_version = f'{parts[0]}.{parts[1]}.{int(parts[2])+1}'; \
		print(f'Updating to {new_version}'); \
		new_content = re.sub(r'version = \"[^\"]+\"', f'version = \"{new_version}\"', content); \
		open('pyproject.toml', 'w').write(new_content); \
		subprocess.run(['git', 'add', 'pyproject.toml']); \
		subprocess.run(['git', 'commit', '-m', f'bump: version {new_version}']); \
		subprocess.run(['git', 'tag', f'v{new_version}']); \
		subprocess.run(['git', 'push']); \
		subprocess.run(['git', 'push', 'origin', f'v{new_version}'])"

# Interactive publishing
publish-interactive:
	python publish-to-pypi.py

# Documentation
docs:
	@echo "Documentation can be built with mkdocs (if configured)"
	@echo "Run: mkdocs serve"

# Development environment setup
dev-setup:
	@echo "🚀 Setting up development environment..."
	@if [ ! -d ".venv" ]; then \
		echo "📦 Creating virtual environment..."; \
		uv venv; \
	fi
	@echo "📦 Installing development dependencies..."
	uv pip install -e ".[dev]"
	@echo "🔧 Installing pre-commit hooks..."
	uv run pre-commit install
	uv run pre-commit install --hook-type commit-msg
	@echo "🧪 Running initial tests..."
	$(MAKE) test
	@echo "✅ Development environment ready!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Activate the virtual environment: source .venv/bin/activate"
	@echo "  2. Run tests: make test"
	@echo "  3. Run the full test suite: python dev-test.py"

# Quick development test
dev-test:
	python dev-test.py
