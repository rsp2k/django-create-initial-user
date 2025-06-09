"""Comprehensive tests for django-create-initial-user authentication backend."""

import warnings
from unittest.mock import Mock, patch

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.test import TestCase, override_settings

from create_initial_superuser.backends import CreateInitialSuperUserBackend


class TestCreateInitialSuperUserBackend(TestCase):
    """Test cases for CreateInitialSuperUserBackend."""

    def setUp(self):
        """Set up test fixtures."""
        self.backend = CreateInitialSuperUserBackend()
        self.UserModel = get_user_model()
        self.test_username = "testadmin"
        self.test_password = "testpass123"
        self.test_email = "admin@example.com"

    def tearDown(self):
        """Clean up after tests."""
        # Clear all users after each test
        self.UserModel.objects.all().delete()

    def test_create_initial_superuser_when_no_superusers_exist(self):
        """Test that superuser is created when none exist and DEBUG=True."""
        # Ensure no users exist
        self.assertEqual(self.UserModel.objects.count(), 0)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            user = self.backend.authenticate(
                request=None, username=self.test_username, password=self.test_password
            )

            # Check warning was issued
            self.assertEqual(len(w), 1)
            self.assertIn("No superusers exist", str(w[0].message))
            self.assertIn(self.test_username, str(w[0].message))

        # Verify user was created
        self.assertIsNotNone(user)
        self.assertEqual(user.username, self.test_username)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(check_password(self.test_password, user.password))

        # Verify user is in database
        self.assertEqual(self.UserModel.objects.count(), 1)
        db_user = self.UserModel.objects.get()
        self.assertEqual(db_user.username, self.test_username)
        self.assertTrue(db_user.is_superuser)

    def test_create_initial_superuser_with_email_username(self):
        """Test that email is set when username looks like an email."""
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")

            user = self.backend.authenticate(
                request=None, username=self.test_email, password=self.test_password
            )

        self.assertIsNotNone(user)
        self.assertEqual(user.username, self.test_email)
        self.assertEqual(user.email, self.test_email)

    def test_no_superuser_creation_when_superuser_exists(self):
        """Test that no superuser is created when one already exists."""
        # Create an existing superuser
        existing_user = self.UserModel.objects.create_user(
            username="existing_admin",
            password="existing_pass",
            is_superuser=True,
            is_staff=True,
        )

        initial_count = self.UserModel.objects.count()

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            user = self.backend.authenticate(
                request=None, username=self.test_username, password=self.test_password
            )

            # No warning should be issued
            self.assertEqual(len(w), 0)

        # Should fall back to normal authentication (which will fail for non-existent user)
        self.assertIsNone(user)

        # No new user should be created
        self.assertEqual(self.UserModel.objects.count(), initial_count)

    def test_normal_authentication_with_existing_user(self):
        """Test normal authentication when user exists and superuser exists."""
        # Create an existing superuser (to prevent initial creation)
        self.UserModel.objects.create_user(
            username="existing_admin",
            password="existing_pass",
            is_superuser=True,
            is_staff=True,
        )

        # Create a regular user to authenticate
        test_user = self.UserModel.objects.create_user(
            username=self.test_username, password=self.test_password
        )

        user = self.backend.authenticate(
            request=None, username=self.test_username, password=self.test_password
        )

        self.assertIsNotNone(user)
        self.assertEqual(user.id, test_user.id)
        self.assertEqual(user.username, self.test_username)

    @override_settings(DEBUG=False)
    def test_no_superuser_creation_when_debug_false(self):
        """Test that no superuser is created when DEBUG=False."""
        # Ensure no users exist
        self.assertEqual(self.UserModel.objects.count(), 0)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            user = self.backend.authenticate(
                request=None, username=self.test_username, password=self.test_password
            )

            # No warning should be issued
            self.assertEqual(len(w), 0)

        # Should fall back to normal authentication (which will fail)
        self.assertIsNone(user)

        # No user should be created
        self.assertEqual(self.UserModel.objects.count(), 0)

    def test_authentication_with_missing_username(self):
        """Test authentication fails gracefully with missing username."""
        user = self.backend.authenticate(
            request=None, username=None, password=self.test_password
        )
        self.assertIsNone(user)

    def test_authentication_with_missing_password(self):
        """Test authentication fails gracefully with missing password."""
        user = self.backend.authenticate(
            request=None, username=self.test_username, password=None
        )
        self.assertIsNone(user)

    def test_authentication_with_empty_credentials(self):
        """Test authentication fails gracefully with empty credentials."""
        user = self.backend.authenticate(request=None, username="", password="")
        self.assertIsNone(user)

    def test_superuser_creation_only_checks_is_superuser_true(self):
        """Test that only users with is_superuser=True prevent initial creation."""
        # Create a regular user (not superuser)
        self.UserModel.objects.create_user(
            username="regular_user", password="regular_pass", is_superuser=False
        )

        # Create a staff user (not superuser)
        self.UserModel.objects.create_user(
            username="staff_user",
            password="staff_pass",
            is_staff=True,
            is_superuser=False,
        )

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            user = self.backend.authenticate(
                request=None, username=self.test_username, password=self.test_password
            )

            # Warning should be issued because no superusers exist
            self.assertEqual(len(w), 1)

        # Superuser should be created
        self.assertIsNotNone(user)
        self.assertTrue(user.is_superuser)

    def test_multiple_authentication_attempts(self):
        """Test multiple authentication attempts behave correctly."""
        # First attempt should create superuser
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            user1 = self.backend.authenticate(
                request=None, username=self.test_username, password=self.test_password
            )

            self.assertEqual(len(w), 1)

        self.assertIsNotNone(user1)
        self.assertTrue(user1.is_superuser)

        # Second attempt should use normal authentication
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            user2 = self.backend.authenticate(
                request=None, username=self.test_username, password=self.test_password
            )

            self.assertEqual(len(w), 0)  # No warning for second attempt

        self.assertIsNotNone(user2)
        self.assertEqual(user1.id, user2.id)

    def test_request_parameter_handling(self):
        """Test that request parameter is handled correctly."""
        mock_request = Mock()

        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")

            user = self.backend.authenticate(
                request=mock_request,
                username=self.test_username,
                password=self.test_password,
            )

        self.assertIsNotNone(user)
        self.assertTrue(user.is_superuser)

    def test_kwargs_handling(self):
        """Test that additional kwargs are handled correctly."""
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")

            user = self.backend.authenticate(
                request=None,
                username=self.test_username,
                password=self.test_password,
                extra_param="test_value",
            )

        self.assertIsNotNone(user)
        self.assertTrue(user.is_superuser)

    @patch("create_initial_superuser.backends.get_user_model")
    def test_custom_user_model_compatibility(self, mock_get_user_model):
        """Test compatibility with custom user models."""
        # This test ensures the backend works with any user model
        mock_user_model = Mock()
        mock_user_model.objects.filter.return_value.exists.return_value = False
        mock_get_user_model.return_value = mock_user_model

        mock_user = Mock()
        mock_user_model.objects.create.return_value = mock_user

        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")

            with patch(
                "create_initial_superuser.backends.make_password"
            ) as mock_make_password:
                mock_make_password.return_value = "hashed_password"

                result = self.backend.authenticate(
                    request=None,
                    username=self.test_username,
                    password=self.test_password,
                )

        self.assertEqual(result, mock_user)
        mock_user_model.objects.create.assert_called_once()


class TestBackendIntegration(TestCase):
    """Integration tests for the authentication backend."""

    def setUp(self):
        """Set up test fixtures."""
        self.UserModel = get_user_model()

    def tearDown(self):
        """Clean up after tests."""
        self.UserModel.objects.all().delete()

    def test_backend_in_authentication_backends_setting(self):
        """Test that the backend is properly configured in settings."""
        self.assertIn(
            "create_initial_superuser.backends.CreateInitialSuperUserBackend",
            settings.AUTHENTICATION_BACKENDS,
        )

    def test_django_authenticate_function_integration(self):
        """Test integration with Django's authenticate function."""
        from django.contrib.auth import authenticate

        # Ensure no users exist
        self.assertEqual(self.UserModel.objects.count(), 0)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            user = authenticate(username="integration_test", password="test_password")

            self.assertEqual(len(w), 1)

        self.assertIsNotNone(user)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.username, "integration_test")


@pytest.mark.django_db
class TestBackendWithPytest:
    """Pytest-style tests for additional coverage."""

    def test_password_hashing_security(self):
        """Test that passwords are properly hashed."""
        backend = CreateInitialSuperUserBackend()
        UserModel = get_user_model()

        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")

            user = backend.authenticate(
                request=None, username="security_test", password="plaintext_password"
            )

        # Password should be hashed, not stored in plaintext
        assert user.password != "plaintext_password"
        assert user.password.startswith(("pbkdf2_sha256$", "bcrypt$", "argon2$"))
        assert check_password("plaintext_password", user.password)

    def test_warning_message_format(self):
        """Test the format of warning messages."""
        backend = CreateInitialSuperUserBackend()
        username = "warning_test_user"

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            backend.authenticate(
                request=None, username=username, password="test_password"
            )

        assert len(w) == 1
        warning_message = str(w[0].message)
        assert "django-create-initial-user" in warning_message
        assert "No superusers exist" in warning_message
        assert username in warning_message
        assert w[0].category == UserWarning
