# Quick Start Guide

## 🚀 Get Started in 2 Minutes

### Step 1: Install the Package

Choose your preferred package manager:

=== "uv (Recommended)"
    ```bash
    uv add django-create-initial-user
    ```

=== "pip"
    ```bash
    pip install django-create-initial-user
    ```

=== "poetry"
    ```bash
    poetry add django-create-initial-user
    ```

### Step 2: Configure Django

Add to your `settings.py`:

```python
# Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ... your existing apps
    'create_initial_superuser',
]

# Configure authentication backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Enable for development only
if DEBUG:
    AUTHENTICATION_BACKENDS.insert(0, 
        'create_initial_superuser.backends.CreateInitialSuperUserBackend'
    )
```

### Step 3: Run Your Project

```bash
python manage.py migrate
python manage.py runserver
```

### Step 4: Create Your Superuser

1. Navigate to `http://localhost:8000/admin/`
2. Enter any username and password you want
3. Click "Log in"
4. 🎉 You're now logged in as a superuser!

## ✅ That's It!

You've successfully set up automatic superuser creation. The next time you start a fresh Django project, you can skip the `createsuperuser` command entirely.

## 🔄 What Happens Next?

- **First login**: Creates superuser with your credentials
- **Subsequent logins**: Uses normal Django authentication
- **Production**: Remove from `AUTHENTICATION_BACKENDS` for security

## 🆘 Need Help?

- Check the [troubleshooting guide](troubleshooting.md)
- Review [security considerations](security.md)
- Browse our [FAQ](faq.md)
