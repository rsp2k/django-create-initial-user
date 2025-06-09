"""Tests for Django app configuration."""

from django.apps import apps
from django.test import TestCase

from create_initial_superuser.apps import CreateInitialSuperuserConfig


class TestAppConfig(TestCase):
    """Test cases for the Django app configuration."""

    def test_app_config_exists(self):
        """Test that the app config is properly defined."""
        config = apps.get_app_config("create_initial_superuser")
        self.assertIsInstance(config, CreateInitialSuperuserConfig)

    def test_app_config_name(self):
        """Test that the app config has the correct name."""
        config = CreateInitialSuperuserConfig
        self.assertEqual(config.name, "create_initial_superuser")

    def test_app_config_verbose_name(self):
        """Test that the app config has a verbose name."""
        config = CreateInitialSuperuserConfig
        self.assertEqual(config.verbose_name, "Create Initial Superuser")

    def test_app_config_default_auto_field(self):
        """Test that the app config has the correct default auto field."""
        config = CreateInitialSuperuserConfig
        self.assertEqual(config.default_auto_field, "django.db.models.BigAutoField")

    def test_app_is_installed(self):
        """Test that the app is properly installed."""
        self.assertTrue(apps.is_installed("create_initial_superuser"))
