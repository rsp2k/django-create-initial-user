# 🐛 Troubleshooting Guide

## 🚨 Common Issues & Solutions

### Issue: Superuser Not Being Created

**Symptoms:**
- Login attempt redirects back to login page
- No warning message appears
- Normal authentication behavior

**Possible Causes & Solutions:**

#### 1. Backend Not Configured
```python
# ❌ Missing from settings.py
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# ✅ Correct configuration
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

if DEBUG:
    AUTHENTICATION_BACKENDS.insert(0,
        'create_initial_superuser.backends.CreateInitialSuperUserBackend'
    )
```

#### 2. DEBUG Mode Disabled
```python
# ❌ DEBUG is False
DEBUG = False

# ✅ Enable DEBUG for development
DEBUG = True
```

#### 3. Superuser Already Exists
```bash
# Check if superusers exist
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
print('Superusers:', User.objects.filter(is_superuser=True).count())
"

# Delete existing superusers if needed (CAREFUL!)
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.filter(is_superuser=True).delete()
print('Superusers deleted')
"
```

#### 4. Package Not Installed
```bash
# Check if package is installed
pip list | grep django-create-initial-user

# Install if missing
pip install django-create-initial-user
```

#### 5. App Not in INSTALLED_APPS
```python
# ❌ Missing from INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # ... other apps
]

# ✅ Add the app
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # ... other apps
    'create_initial_superuser',
]
```

---

### Issue: ImportError or Module Not Found

**Symptoms:**
```
ImportError: No module named 'create_initial_superuser'
ModuleNotFoundError: No module named 'create_initial_superuser.backends'
```

**Solutions:**

#### 1. Virtual Environment Issues
```bash
# Ensure you're in the correct virtual environment
which python
pip list | grep django-create-initial-user

# If not found, install in current environment
pip install django-create-initial-user
```

#### 2. Path Issues
```python
# Verify the import path is correct
from create_initial_superuser.backends import CreateInitialSuperUserBackend
```

#### 3. Django Project Setup
```bash
# Make sure you're in a Django project
python manage.py check

# Run from the correct directory
ls manage.py  # Should exist
```

---

### Issue: Authentication Still Asks for Existing User

**Symptoms:**
- Login form appears but only existing users can log in
- New credentials are rejected

**Solutions:**

#### 1. Backend Order
```python
# ❌ Wrong order - CreateInitialSuperUserBackend should be first
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'create_initial_superuser.backends.CreateInitialSuperUserBackend',
]

# ✅ Correct order
AUTHENTICATION_BACKENDS = [
    'create_initial_superuser.backends.CreateInitialSuperUserBackend',
    'django.contrib.auth.backends.ModelBackend',
]
```

#### 2. Multiple Backends Conflict
```python
# Check for conflicting backends
print(settings.AUTHENTICATION_BACKENDS)

# Ensure our backend is first
if DEBUG:
    backends = list(settings.AUTHENTICATION_BACKENDS)
    our_backend = 'create_initial_superuser.backends.CreateInitialSuperUserBackend'
    if our_backend in backends:
        backends.remove(our_backend)
    backends.insert(0, our_backend)
    settings.AUTHENTICATION_BACKENDS = backends
```

---

### Issue: Warnings Not Appearing

**Symptoms:**
- Superuser is created but no warning message
- Silent operation

**Solutions:**

#### 1. Logging Configuration
```python
# Add to settings.py for development
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'create_initial_superuser': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
```

#### 2. Warning Filters
```python
# Ensure warnings aren't being filtered
import warnings
warnings.simplefilter('always')
```

---

### Issue: Custom User Model Problems

**Symptoms:**
- Errors when creating superuser with custom user model
- Fields missing or incorrect

**Solutions:**

#### 1. Required Fields
```python
# Ensure your custom user model has required fields
class CustomUser(AbstractUser):
    # These fields are required for the backend
    username = models.CharField(max_length=150, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Optional: email field for auto-detection
    email = models.EmailField(blank=True)
```

#### 2. User Manager Issues
```python
# If using custom user manager, ensure it supports superuser creation
class CustomUserManager(BaseUserManager):
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)
```

---

### Issue: Docker/Container Problems

**Symptoms:**
- Works locally but not in Docker
- Environment variable issues

**Solutions:**

#### 1. Environment Variables
```dockerfile
# Dockerfile
ENV DEBUG=True
ENV DJANGO_SETTINGS_MODULE=myproject.settings

# Or in docker-compose.yml
environment:
  - DEBUG=1
  - ENABLE_INITIAL_SUPERUSER=1
```

#### 2. Package Installation
```dockerfile
# Ensure package is installed in container
RUN pip install django-create-initial-user

# Or copy requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt
```

---

## 🔍 Debug Mode

Enable detailed debugging:

```python
# settings.py - Add debug logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'create_initial_superuser': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.contrib.auth': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

## 🧪 Test Your Setup

Create a test script to verify everything works:

```python
# test_setup.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.conf import settings
from django.contrib.auth import get_user_model
from create_initial_superuser.backends import CreateInitialSuperUserBackend

# Test 1: Check settings
print("DEBUG:", settings.DEBUG)
print("AUTHENTICATION_BACKENDS:", settings.AUTHENTICATION_BACKENDS)

# Test 2: Check backend
backend = CreateInitialSuperUserBackend()
print("Backend created successfully")

# Test 3: Check user model
User = get_user_model()
superuser_count = User.objects.filter(is_superuser=True).count()
print(f"Existing superusers: {superuser_count}")

# Test 4: Test authentication (won't create user, just test the method)
print("Backend authenticate method available:", hasattr(backend, 'authenticate'))
```

## 📧 Still Need Help?

If you're still experiencing issues:

1. **Check our FAQ**: [FAQ.md](faq.md)
2. **Search existing issues**: [GitHub Issues](https://github.com/yourusername/django-create-initial-user/issues)
3. **Create a new issue**: Include:
   - Django version
   - Python version
   - Package version
   - Full error traceback
   - Minimal reproduction case
4. **Join our discussion**: [GitHub Discussions](https://github.com/yourusername/django-create-initial-user/discussions)

## 🐛 Bug Reports

When reporting bugs, please include:

```python
# System information
import sys
import django
import create_initial_superuser

print(f"Python: {sys.version}")
print(f"Django: {django.get_version()}")
print(f"Package: {create_initial_superuser.__version__}")
print(f"DEBUG: {settings.DEBUG}")
print(f"User Model: {settings.AUTH_USER_MODEL}")
```

This helps us diagnose issues much faster! 🚀
