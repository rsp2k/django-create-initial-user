# 🛡️ Security Guide

## 🎯 Security Philosophy

Django Create Initial User is designed with security as a top priority. This guide outlines our security measures and best practices for safe usage.

## 🔒 Built-in Security Features

### 1. DEBUG Mode Only
By default, the backend only operates when `DEBUG=True`:

```python
# In backends.py
if settings.DEBUG and not UserModel.objects.filter(is_superuser=True).exists():
    # Only creates superuser in debug mode
```

### 2. Proper Password Hashing
All passwords are hashed using Django's secure `make_password` function:

```python
hashed_password = make_password(password)
user = UserModel.objects.create(
    username=username,
    password=hashed_password,  # Never stored in plaintext
    is_staff=True,
    is_superuser=True,
)
```

### 3. Transparent Operation
Warning messages alert you when superusers are created:

```python
warnings.warn(
    f"django-create-initial-user: No superusers exist! "
    f"Creating initial superuser with username '{username}'",
    UserWarning
)
```

### 4. No Backdoors
- No hardcoded credentials
- No hidden authentication mechanisms
- No bypassing of Django's security features

## 🚨 Security Considerations

### Development vs Production

| Environment | Recommendation | Risk Level |
|-------------|---------------|------------|
| **Development** | ✅ Safe to use | 🟢 Low |
| **Testing** | ✅ Safe to use | 🟢 Low |
| **Staging** | ⚠️ Use with caution | 🟡 Medium |
| **Production** | ❌ Remove after initial setup | 🔴 High |

### Production Deployment Strategy

**Option 1: Remove After Initial Setup**
```python
# settings.py - Production
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # Remove CreateInitialSuperUserBackend in production
]
```

**Option 2: Environment-Based Control**
```python
# settings.py
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Only enable in development or initial deployment
if DEBUG or os.getenv('ENABLE_INITIAL_SUPERUSER'):
    AUTHENTICATION_BACKENDS.insert(0, 
        'create_initial_superuser.backends.CreateInitialSuperUserBackend'
    )
```

**Option 3: Management Command Alternative**
```python
# For production initial deployment, use management commands
from django.core.management import call_command
from django.contrib.auth import get_user_model

def create_initial_superuser():
    User = get_user_model()
    if not User.objects.filter(is_superuser=True).exists():
        call_command('createsuperuser', 
                    username='admin', 
                    email='admin@example.com',
                    interactive=False)
```

## 🔐 Security Best Practices

### 1. Use Strong Credentials
Even in development, use strong passwords:

```python
# Good
username: admin@company.com
password: MyStr0ng!P@ssw0rd2024

# Avoid
username: admin
password: admin
```

### 2. Monitor Superuser Creation
Set up logging to track when superusers are created:

```python
# settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'security_file': {
            'class': 'logging.FileHandler',
            'filename': 'security.log',
        },
    },
    'loggers': {
        'create_initial_superuser': {
            'handlers': ['security_file'],
            'level': 'WARNING',
        },
    },
}
```

### 3. Regular Security Audits
Periodically review your authentication backends:

```bash
# Check your settings
python manage.py diffsettings | grep AUTHENTICATION_BACKENDS

# Audit superusers
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
print('Superusers:', User.objects.filter(is_superuser=True).values_list('username', flat=True))
"
```

### 4. Container Security
For Docker deployments:

```dockerfile
# Dockerfile
# Don't include the package in production images
ARG ENVIRONMENT=production
RUN if [ "$ENVIRONMENT" = "development" ]; then \
        pip install django-create-initial-user; \
    fi
```

## 🚨 Security Warnings

### ⚠️ Do NOT Use If:
- You need hardcoded production credentials
- You're building a multi-tenant application
- You require complex user permissions setup
- You're in a high-security environment

### ✅ Safe to Use If:
- You're in active development
- You need rapid prototyping
- You're running automated tests
- You're doing initial deployment setup

## 🔍 Security Checklist

Before deploying to production:

- [ ] Remove `CreateInitialSuperUserBackend` from `AUTHENTICATION_BACKENDS`
- [ ] Verify no hardcoded credentials in your code
- [ ] Audit all superuser accounts
- [ ] Enable Django's security middleware
- [ ] Set up proper logging and monitoring
- [ ] Use HTTPS in production
- [ ] Enable CSRF protection
- [ ] Configure secure cookies

## 📊 Security Scanning

We regularly scan our codebase for vulnerabilities:

```bash
# Security scanning with bandit
bandit -r create_initial_superuser

# Dependency vulnerability check
safety check

# SAST scanning in CI/CD
# See .github/workflows/test.yml
```

## 🆘 Security Issues

If you discover a security vulnerability:

1. **DO NOT** open a public issue
2. Email us at: security@django-create-initial-user.com
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We take security seriously and will respond within 24 hours.

## 📚 Additional Resources

- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Guidelines](https://python.org/dev/security/)
- [Django Authentication Best Practices](https://docs.djangoproject.com/en/stable/topics/auth/)
