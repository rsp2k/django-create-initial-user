# Makefile for django-create-initial-user development

.PHONY: help install install-dev test test-all lint format security clean build publish-test publish docs dev-setup

# Default target
help:
	@echo "Available commands:"
	@echo "  install        Install package in production mode"
	@echo "  install-dev    Install package in development mode"
	@echo "  test          Run tests with pytest"
	@echo "  test-all      Run tests with tox (all Python/Django versions)"
	@echo "  lint          Run all linting tools"
	@echo "  format        Format code with black and isort"
	@echo "  security      Run security checks"
	@echo "  clean         Clean build artifacts"
	@echo "  build         Build distribution packages"
	@echo "  publish-test  Publish to Test PyPI"
	@echo "  publish       Publish to PyPI"
	@echo "  docs          Build documentation"
	@echo "  dev-setup     Complete development environment setup"

# Installation
install:
	uv pip install .

install-dev:
	uv pip install -e ".[dev]"

# Testing
test:
	uv run pytest tests/ -v --cov=create_initial_superuser --cov-report=term-missing

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

security:
	uv run bandit -r create_initial_superuser
	uv run safety check

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
	uv run twine upload --repository testpypi dist/*

publish: build
	uv run twine upload dist/*

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
