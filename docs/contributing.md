# 🤝 Contributing to Django Create Initial User

We're thrilled that you're interested in contributing! This guide will help you get started with contributing to our project.

## 🌟 Ways to Contribute

### 🐛 Report Bugs
- Use our [bug report template](.github/ISSUE_TEMPLATE/bug_report.md)
- Include detailed reproduction steps
- Provide your environment information

### ✨ Request Features  
- Use our [feature request template](.github/ISSUE_TEMPLATE/feature_request.md)
- Explain the use case and benefit
- Consider security implications

### 💻 Code Contributions
- Fix bugs or implement features
- Improve test coverage
- Optimize performance
- Enhance documentation

### 📚 Documentation
- Fix typos or unclear explanations
- Add usage examples
- Improve API documentation
- Translate documentation

## 🚀 Getting Started

### 1. Fork & Clone
```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/yourusername/django-create-initial-user.git
cd django-create-initial-user
```

### 2. Set Up Development Environment
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Or use our Makefile
make dev-setup
```

### 3. Install Pre-commit Hooks
```bash
# Option 1: Use our setup script (recommended)
python setup-precommit.py

# Option 2: Manual installation
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg

# Option 3: Use Makefile
make precommit-install
```

### 4. Run Tests
```bash
# Quick test
python dev-test.py

# Full test suite
make test

# Test specific modules
pytest tests/test_backends.py -v
```

## 🔧 Development Workflow

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Make Changes
- Write clean, readable code
- Follow existing code style
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes
```bash
# Format code
make format

# Run linting
make lint

# Run tests
make test

# Run security checks
make security
```

### 4. Commit & Push
```bash
git add .
git commit -m "feat: add awesome new feature"
git push origin feature/your-feature-name
```

### 5. Create Pull Request
- Use our [PR template](.github/pull_request_template.md)
- Link to related issues
- Describe your changes clearly

## 📝 Code Style

### Python Code Style
We use several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting  
- **flake8**: Linting
- **mypy**: Type checking

```bash
# Format code
black .
isort .

# Check style
flake8 create_initial_superuser tests
mypy create_initial_superuser
```

### Commit Message Style
We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new feature
fix: resolve bug in authentication
docs: update README with examples
test: add tests for edge cases
refactor: improve code structure
```

### Type Hints
All new code should include type hints:

```python
from typing import Optional
from django.contrib.auth.models import AbstractUser
from django.http import HttpRequest

def authenticate(
    self,
    request: Optional[HttpRequest],
    username: Optional[str] = None,
    password: Optional[str] = None,
    **kwargs
) -> Optional[AbstractUser]:
    # Implementation
```

## 🧪 Testing Guidelines

### Test Structure
```
tests/
├── __init__.py
├── settings.py          # Test Django settings
├── urls.py             # Test URL configuration  
├── test_backends.py    # Main backend tests
├── test_apps.py        # App configuration tests
└── test_imports.py     # Import and structure tests
```

### Writing Tests
- Use descriptive test names
- Test both happy path and edge cases
- Include security-related tests
- Test with different Django/Python versions

```python
def test_create_initial_superuser_when_no_superusers_exist(self):
    """Test that superuser is created when none exist and DEBUG=True."""
    # Arrange
    self.assertEqual(self.UserModel.objects.count(), 0)
    
    # Act
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        user = self.backend.authenticate(
            request=None,
            username=self.test_username,
            password=self.test_password
        )
    
    # Assert
    self.assertIsNotNone(user)
    self.assertTrue(user.is_superuser)
    self.assertEqual(len(w), 1)
```

### Test Coverage
We maintain 100% test coverage. New code must include tests:

```bash
# Run with coverage
pytest tests/ --cov=create_initial_superuser --cov-report=html
open htmlcov/index.html
```

## 🛡️ Security Considerations

### Security Review
All changes are reviewed for security implications:

- No hardcoded credentials
- Proper input validation
- Secure password handling
- DEBUG mode restrictions
- No information disclosure

### Security Testing
```bash
# Run security scans
bandit -r create_initial_superuser
safety check

# Test with DEBUG=False
DEBUG=False python -m pytest tests/
```

## 📚 Documentation Standards

### Code Documentation
- Use clear docstrings for all public methods
- Include type hints
- Add inline comments for complex logic

```python
def authenticate(
    self,
    request: Optional[HttpRequest],
    username: Optional[str] = None,
    password: Optional[str] = None,
    **kwargs
) -> Optional[AbstractUser]:
    """
    Authenticate user and create initial superuser if needed.
    
    Args:
        request: The HTTP request object
        username: Username for authentication
        password: Password for authentication
        **kwargs: Additional keyword arguments
        
    Returns:
        User object if authentication successful, None otherwise
    """
```

### README Updates
When adding features, update relevant documentation:
- README.md feature list
- Usage examples
- Configuration options
- Security considerations

## 🏗️ Architecture Guidelines

### Project Structure
```
create_initial_superuser/
├── __init__.py         # Package info and version
├── apps.py            # Django app configuration
└── backends.py        # Authentication backend implementation

tests/
├── __init__.py
├── settings.py        # Test Django settings
├── urls.py           # Test URLs
├── test_*.py         # Test modules

docs/
├── README.md         # Documentation index
├── quick-start.md    # Getting started guide
├── security.md       # Security documentation
├── troubleshooting.md # Common issues
├── faq.md           # Frequently asked questions
└── contributing.md   # This file
```

### Design Principles
1. **Security First**: Every feature must be secure by default
2. **Developer Experience**: Make Django development easier
3. **Minimal Dependencies**: Keep the package lightweight
4. **Django Standards**: Follow Django conventions and best practices
5. **Backward Compatibility**: Don't break existing installations

## 🚦 Release Process

### Versioning
We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist
- [ ] Update version in `pyproject.toml`
- [ ] Update `CHANGELOG.md`
- [ ] Run full test suite
- [ ] Update documentation
- [ ] Create GitHub release
- [ ] Publish to PyPI

## 🎯 Contribution Areas

### 🔥 High Priority
- Bug fixes
- Security improvements
- Performance optimizations
- Test coverage improvements
- Documentation enhancements

### 🌟 Feature Ideas
- Custom user field mapping
- Integration with external auth systems
- Advanced logging and monitoring
- Configuration validation
- Deployment automation helpers

### 📚 Documentation Needs
- More usage examples
- Video tutorials
- Blog post tutorials
- Integration guides
- Best practices documentation

## 💬 Communication

### GitHub Discussions
For questions, ideas, and general discussion:
- [Q&A](https://github.com/yourusername/django-create-initial-user/discussions/categories/q-a)
- [Ideas](https://github.com/yourusername/django-create-initial-user/discussions/categories/ideas)
- [Show and Tell](https://github.com/yourusername/django-create-initial-user/discussions/categories/show-and-tell)

### Issue Tracking
- Use GitHub Issues for bugs and feature requests
- Search existing issues before creating new ones
- Use appropriate labels and templates
- Provide detailed information

### Code Reviews
- All PRs require review before merging
- Be constructive and respectful
- Focus on code quality and security
- Suggest improvements clearly

## 🏆 Recognition

### Contributors
All contributors are recognized in:
- GitHub contributors page
- CONTRIBUTORS.md file
- Release notes
- Special thanks in major releases

### Types of Contributions
We value all types of contributions:
- 💻 Code contributions
- 📚 Documentation improvements
- 🐛 Bug reports
- 💡 Feature suggestions
- 🎨 Design improvements
- 📢 Community building
- 🔍 Code reviews
- 🧪 Testing
- 🌍 Translations

## 🤔 Questions?

### Getting Help
- Check our [FAQ](faq.md)
- Search [GitHub Issues](https://github.com/yourusername/django-create-initial-user/issues)
- Start a [Discussion](https://github.com/yourusername/django-create-initial-user/discussions)
- Ask in our community channels

### Mentorship
New to open source? We're here to help!
- Look for "good first issue" labels
- Ask questions in discussions
- Request code review guidance
- Join our contributor onboarding

## 📄 Legal

### License
By contributing to Django Create Initial User, you agree that your contributions will be licensed under the MIT License.

### Code of Conduct
We follow the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). Please read and follow it in all interactions.

### Attribution
Contributors retain copyright to their contributions while granting the project rights to use and distribute the code.

---

## 🎉 Thank You!

Thank you for considering contributing to Django Create Initial User! Your contributions help make Django development easier for everyone.

**Happy contributing! 🚀**

---

*For questions about this contributing guide, please [open an issue](https://github.com/yourusername/django-create-initial-user/issues/new) or start a [discussion](https://github.com/yourusername/django-create-initial-user/discussions).*
