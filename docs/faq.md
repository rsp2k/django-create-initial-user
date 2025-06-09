# ❓ Frequently Asked Questions

## 🤔 General Questions

### Q: What exactly does this package do?
**A:** Django Create Initial User automatically creates a superuser account on the first login attempt when no superuser accounts exist in your Django database. This eliminates the need to manually run `python manage.py createsuperuser` during development.

### Q: Is this safe to use?
**A:** Yes! The package is designed with security in mind:
- Only operates when `DEBUG=True` by default
- Uses Django's secure password hashing
- Provides transparent warnings when creating users
- No hardcoded credentials or backdoors

### Q: Does this modify my database schema?
**A:** No! This package doesn't add any new models, tables, or migrations. It works entirely through Django's existing authentication system.

---

## 🛠️ Installation & Setup

### Q: How do I install this package?
**A:** Use any Python package manager:

```bash
# pip
pip install django-create-initial-user

# uv (recommended)
uv add django-create-initial-user

# poetry
poetry add django-create-initial-user
```

### Q: Do I need to run migrations?
**A:** No migrations are required! Just add the package to `INSTALLED_APPS` and configure the authentication backend.

### Q: Can I use this with existing Django projects?
**A:** Absolutely! Add it to any Django project. If superusers already exist, the package won't interfere with normal authentication.

---

## 🔧 Configuration

### Q: What's the minimal configuration needed?
**A:** Just two steps in `settings.py`:

```python
# 1. Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ... your apps
    'create_initial_superuser',
]

# 2. Configure authentication backend
if DEBUG:
    AUTHENTICATION_BACKENDS = [
        'create_initial_superuser.backends.CreateInitialSuperUserBackend',
        'django.contrib.auth.backends.ModelBackend',
    ]
```

### Q: Can I use this with custom user models?
**A:** Yes! The package works with any user model that inherits from Django's `AbstractUser` or `AbstractBaseUser` and has the required fields (`username`, `is_staff`, `is_superuser`).

### Q: How do I disable this in production?
**A:** Simply remove the backend from `AUTHENTICATION_BACKENDS` or set `DEBUG=False`. The recommended approach is environment-based configuration:

```python
if DEBUG or os.getenv('ENABLE_INITIAL_SUPERUSER'):
    AUTHENTICATION_BACKENDS.insert(0,
        'create_initial_superuser.backends.CreateInitialSuperUserBackend'
    )
```

---

## 🚀 Usage

### Q: How do I create a superuser with this package?
**A:**
1. Navigate to your Django admin login page (`/admin/`)
2. Enter any username and password you want for your superuser
3. Click "Log in"
4. You'll be automatically logged in as the new superuser!

### Q: What happens after the first superuser is created?
**A:** The package detects that superusers exist and stops creating new ones. All subsequent authentication uses Django's standard authentication backend.

### Q: Can I create multiple superusers this way?
**A:** No. Once any superuser exists in the database, the package stops creating new ones. You'll need to use Django's normal user creation methods (`createsuperuser` command or admin interface).

### Q: What if I want to reset and create a new initial superuser?
**A:** Delete all existing superusers from your database:

```python
# In Django shell
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.filter(is_superuser=True).delete()
```

---

## 🔒 Security

### Q: Is this secure for production use?
**A:** The package is designed for development environments. While you *can* use it for initial production deployment, we recommend removing it from `AUTHENTICATION_BACKENDS` after creating your production superuser for maximum security.

### Q: How are passwords stored?
**A:** Passwords are hashed using Django's `make_password()` function, which provides the same security as Django's built-in user creation methods.

### Q: Does this create any security vulnerabilities?
**A:** No. The package doesn't bypass Django's security features or create backdoors. It simply automates the initial superuser creation process.

### Q: Why does it only work in DEBUG mode?
**A:** This prevents accidental superuser creation in production environments. You can override this behavior with environment variables if needed for deployment automation.

---

## 🐛 Troubleshooting

### Q: The superuser isn't being created. What's wrong?
**A:** Check these common issues:
1. Is `DEBUG=True`?
2. Is the backend in `AUTHENTICATION_BACKENDS`?
3. Do superusers already exist?
4. Is the package installed and in `INSTALLED_APPS`?

See our [troubleshooting guide](troubleshooting.md) for detailed solutions.

### Q: I'm getting import errors. How do I fix this?
**A:** Ensure:
1. The package is installed: `pip list | grep django-create-initial-user`
2. You're in the correct virtual environment
3. The import path is correct: `create_initial_superuser.backends.CreateInitialSuperUserBackend`

### Q: Can I see debug information?
**A:** Enable debug logging in your settings:

```python
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'loggers': {
        'create_initial_superuser': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

---

## 🔄 Compatibility

### Q: Which Django versions are supported?
**A:** Django 3.2, 4.0, 4.1, 4.2, and 5.0 are officially supported and tested.

### Q: Which Python versions work?
**A:** Python 3.8, 3.9, 3.10, 3.11, and 3.12 are supported.

### Q: Does this work with Django REST Framework?
**A:** Yes! The package only affects Django's authentication system and doesn't interfere with DRF.

### Q: Can I use this with other authentication backends?
**A:** Absolutely! Just ensure `CreateInitialSuperUserBackend` is listed first in `AUTHENTICATION_BACKENDS`.

---

## 🐳 Docker & Deployment

### Q: How do I use this with Docker?
**A:** Set the appropriate environment variables:

```dockerfile
ENV DEBUG=True
ENV ENABLE_INITIAL_SUPERUSER=1
```

Or in docker-compose.yml:
```yaml
environment:
  - DEBUG=1
  - ENABLE_INITIAL_SUPERUSER=1
```

### Q: Can I use this in CI/CD pipelines?
**A:** Yes! It's perfect for automated testing where you need superuser access without manual intervention.

### Q: How do I handle this in staging environments?
**A:** Use environment variables to control when the backend is active:

```python
if os.getenv('ENABLE_INITIAL_SUPERUSER', '').lower() in ('true', '1', 'yes'):
    AUTHENTICATION_BACKENDS.insert(0,
        'create_initial_superuser.backends.CreateInitialSuperUserBackend'
    )
```

---

## 🤝 Contributing

### Q: How can I contribute to this project?
**A:** We welcome contributions! You can:
- Report bugs or request features via [GitHub Issues](https://github.com/yourusername/django-create-initial-user/issues)
- Submit pull requests with improvements
- Help improve documentation
- Share your success stories

### Q: How do I set up a development environment?
**A:**

```bash
git clone https://github.com/yourusername/django-create-initial-user.git
cd django-create-initial-user
make dev-setup
```

### Q: How do I run the tests?
**A:**

```bash
# Quick test
python dev-test.py

# Full test suite
make test

# All Python/Django versions
tox
```

---

## 📚 Advanced Usage

### Q: Can I customize the user creation process?
**A:** Yes! You can subclass the backend and override the `_create_initial_superuser` method:

```python
from create_initial_superuser.backends import CreateInitialSuperUserBackend

class CustomSuperUserBackend(CreateInitialSuperUserBackend):
    def _create_initial_superuser(self, UserModel, username, password):
        # Your custom logic here
        user = super()._create_initial_superuser(UserModel, username, password)
        # Additional customization
        user.first_name = "Admin"
        user.save()
        return user
```

### Q: How can I integrate this with my deployment scripts?
**A:** Use environment variables to control the backend:

```bash
# Enable for initial deployment
export ENABLE_INITIAL_SUPERUSER=1
python manage.py migrate
# First admin login will create superuser

# Disable for normal operation
unset ENABLE_INITIAL_SUPERUSER
```

### Q: Can I use this for automated testing?
**A:** Perfect for testing! It ensures your tests always have superuser access:

```python
# In your test settings
AUTHENTICATION_BACKENDS = [
    'create_initial_superuser.backends.CreateInitialSuperUserBackend',
    'django.contrib.auth.backends.ModelBackend',
]
```

---

## 🆘 Still Have Questions?

If your question isn't answered here:

1. Check our [troubleshooting guide](troubleshooting.md)
2. Search [existing issues](https://github.com/yourusername/django-create-initial-user/issues)
3. Join our [discussions](https://github.com/yourusername/django-create-initial-user/discussions)
4. Create a [new issue](https://github.com/yourusername/django-create-initial-user/issues/new)

We're here to help! 🚀
