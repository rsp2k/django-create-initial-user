"""Tests for package structure and imports."""

import importlib
from django.test import TestCase

import create_initial_superuser


class TestPackageStructure(TestCase):
    """Test cases for package structure and imports."""

    def test_package_version(self):
        """Test that package has a version."""
        self.assertTrue(hasattr(create_initial_superuser, "__version__"))
        self.assertIsInstance(create_initial_superuser.__version__, str)

    def test_backend_import(self):
        """Test that the backend can be imported."""
        from create_initial_superuser.backends import CreateInitialSuperUserBackend

        self.assertTrue(callable(CreateInitialSuperUserBackend))

    def test_apps_import(self):
        """Test that the app config can be imported."""
        from create_initial_superuser.apps import CreateInitialSuperuserConfig

        self.assertTrue(callable(CreateInitialSuperuserConfig))

    def test_package_importable(self):
        """Test that the main package is importable."""
        module = importlib.import_module("create_initial_superuser")
        self.assertIsNotNone(module)

    def test_default_app_config(self):
        """Test that default_app_config is set."""
        self.assertTrue(hasattr(create_initial_superuser, "default_app_config"))
        self.assertEqual(
            create_initial_superuser.default_app_config,
            "create_initial_superuser.apps.CreateInitialSuperuserConfig",
        )

    def test_module_docstring(self):
        """Test that modules have docstrings."""
        self.assertIsNotNone(create_initial_superuser.__doc__)

        from create_initial_superuser import backends

        self.assertIsNotNone(backends.__doc__)

        from create_initial_superuser import apps

        self.assertIsNotNone(apps.__doc__)
