#!/usr/bin/env python3
"""
🚀 Django Create Initial User - Quick Setup Script

This script helps you get started with django-create-initial-user quickly!
"""

import os
import subprocess
import sys
import textwrap
from pathlib import Path


def print_banner():
    """Print a fancy banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   🔐 Django Create Initial User - Quick Setup 🚀               ║
    ║                                                               ║
    ║   Welcome to effortless Django superuser creation!           ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def run_command(command, description, check=True):
    """Run a shell command with nice output."""
    print(f"\n🔧 {description}")
    print(f"💻 Running: {' '.join(command)}")
    
    try:
        result = subprocess.run(
            command, 
            check=check, 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ {description} - Success!")
            return True
        else:
            print(f"❌ {description} - Failed!")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed!")
        print(f"Error: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {command[0]}")
        return False


def check_python_version():
    """Check if Python version is supported."""
    version = sys.version_info
    print(f"\n🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required!")
        return False
    
    print("✅ Python version is supported!")
    return True


def detect_package_manager():
    """Detect available package managers."""
    managers = {}
    
    # Check for uv
    if run_command(['uv', '--version'], 'Checking for uv', check=False):
        managers['uv'] = 'uv'
    
    # Check for pip
    if run_command(['pip', '--version'], 'Checking for pip', check=False):
        managers['pip'] = 'pip'
    
    return managers


def install_package(manager):
    """Install the package using the specified manager."""
    if manager == 'uv':
        return run_command(
            ['uv', 'add', 'django-create-initial-user'],
            'Installing django-create-initial-user with uv'
        )
    elif manager == 'pip':
        return run_command(
            ['pip', 'install', 'django-create-initial-user'],
            'Installing django-create-initial-user with pip'
        )
    else:
        print("❌ No supported package manager found!")
        return False


def create_demo_project():
    """Create a demo Django project."""
    print("\n🎯 Would you like to create a demo Django project? (y/n): ", end="")
    response = input().lower().strip()
    
    if response not in ('y', 'yes'):
        return True
    
    project_name = "demo_django_project"
    
    # Install Django if not present
    run_command(['pip', 'install', 'django'], 'Installing Django')
    
    # Create Django project
    if run_command(
        ['django-admin', 'startproject', project_name],
        f'Creating Django project: {project_name}'
    ):
        return setup_demo_project(project_name)
    
    return False


def setup_demo_project(project_name):
    """Set up the demo project with our package."""
    settings_path = Path(project_name) / project_name / 'settings.py'
    
    if not settings_path.exists():
        print(f"❌ Settings file not found: {settings_path}")
        return False
    
    # Read current settings
    with open(settings_path, 'r') as f:
        settings_content = f.read()
    
    # Add our app to INSTALLED_APPS
    if "'create_initial_superuser'," not in settings_content:
        settings_content = settings_content.replace(
            "'django.contrib.staticfiles',",
            "'django.contrib.staticfiles',\n    'create_initial_superuser',"
        )
    
    # Add authentication backend configuration
    backend_config = '''

# Django Create Initial User Configuration
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

if DEBUG:
    AUTHENTICATION_BACKENDS.insert(0, 
        'create_initial_superuser.backends.CreateInitialSuperUserBackend'
    )
'''
    
    if 'CreateInitialSuperUserBackend' not in settings_content:
        settings_content += backend_config
    
    # Write updated settings
    with open(settings_path, 'w') as f:
        f.write(settings_content)
    
    print(f"✅ Configured {project_name} with django-create-initial-user!")
    
    # Run migrations
    os.chdir(project_name)
    run_command(['python', 'manage.py', 'migrate'], 'Running database migrations')
    
    print_demo_instructions(project_name)
    return True


def print_demo_instructions(project_name):
    """Print instructions for using the demo project."""
    instructions = f"""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                          🎉 Demo Ready!                         ║
    ╚══════════════════════════════════════════════════════════════════╝
    
    Your demo Django project is ready! Here's how to test it:
    
    1️⃣  Start the development server:
        cd {project_name}
        python manage.py runserver
    
    2️⃣  Open your browser and go to:
        http://localhost:8000/admin/
    
    3️⃣  Login with ANY credentials you want:
        Username: admin
        Password: mysecretpassword
        (Or use any username/password you prefer!)
    
    4️⃣  You'll be automatically logged in as a superuser! 🎊
    
    ✨ That's it! No need to run 'createsuperuser' ever again!
    
    📚 Next steps:
        - Check out the full documentation
        - Add this to your existing Django projects
        - Share your success story with us!
    
    🔗 Useful links:
        - GitHub: https://github.com/yourusername/django-create-initial-user
        - Documentation: https://docs.django-create-initial-user.com
        - Issues: https://github.com/yourusername/django-create-initial-user/issues
    """
    print(textwrap.dedent(instructions))


def print_manual_setup():
    """Print manual setup instructions."""
    instructions = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║                     📋 Manual Setup Guide                       ║
    ╚══════════════════════════════════════════════════════════════════╝
    
    To add django-create-initial-user to your existing Django project:
    
    1️⃣  Add to your INSTALLED_APPS in settings.py:
        INSTALLED_APPS = [
            # ... your existing apps
            'create_initial_superuser',
        ]
    
    2️⃣  Configure authentication backends in settings.py:
        AUTHENTICATION_BACKENDS = [
            'django.contrib.auth.backends.ModelBackend',
        ]
        
        if DEBUG:
            AUTHENTICATION_BACKENDS.insert(0, 
                'create_initial_superuser.backends.CreateInitialSuperUserBackend'
            )
    
    3️⃣  That's it! Now when you go to /admin/ and login with any
        credentials, a superuser will be created automatically!
    
    🔒 Security Note: 
        The backend only works when DEBUG=True by default.
        Remove it from AUTHENTICATION_BACKENDS in production!
    
    📚 For more details, check out our documentation:
        https://github.com/yourusername/django-create-initial-user
    """
    print(textwrap.dedent(instructions))


def main():
    """Main setup function."""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Detect package managers
    print("\n🔍 Detecting package managers...")
    managers = detect_package_manager()
    
    if not managers:
        print("❌ No supported package manager found!")
        print("Please install pip or uv first.")
        sys.exit(1)
    
    # Choose package manager
    if 'uv' in managers:
        manager = 'uv'
        print("✅ Using uv (recommended)")
    else:
        manager = 'pip'
        print("✅ Using pip")
    
    # Install package
    if not install_package(manager):
        print("❌ Failed to install django-create-initial-user")
        sys.exit(1)
    
    print("🎉 django-create-initial-user installed successfully!")
    
    # Offer to create demo project
    if not create_demo_project():
        print_manual_setup()
    
    print("\n🎊 Setup complete! Happy coding with Django! 🚀")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled by user. Come back anytime!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please report this issue on our GitHub repository.")
        sys.exit(1)
