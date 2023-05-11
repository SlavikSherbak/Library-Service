from rest_framework.test import APITestCase
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from .models import User

from user.serializers import UserSerializer


class UserTests(APITestCase):
    def setUp(self):
        self.register_url = reverse("user:create")
        self.login_url = reverse("user:token_obtain_pair")
        self.me_url = reverse("user:manage")
        self.user_data = {
            "email": "test@example.com",
            "password": "testpass123",
            "first_name": "John",
            "last_name": "Doe",
        }

    def test_register_user(self):
        response = self.client.post(self.register_url, data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(
            get_user_model().objects.first().email, self.user_data["email"]
        )

    def test_login_user(self):
        # Create a user
        get_user_model().objects.create_user(**self.user_data)
        # Login the user and get access and refresh tokens
        response = self.client.post(self.login_url, data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        access_token = response.data["access"]
        refresh_token = response.data["refresh"]
        # Set Authorization header to use access token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        # Access protected view
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user_data["email"])
        # Refresh access token
        response = self.client.post(
            reverse("user:token_refresh"), data={"refresh": refresh_token}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_access_token = response.data["access"]
        # Set Authorization header to use new access token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {new_access_token}")
        # Access protected view again
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user_data["email"])


class UserSerializerTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="password123"
        )
        self.serializer_data = {
            "email": "newuser@example.com",
            "password": "newpassword123",
        }
        self.serializer = UserSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {"id", "email", "is_staff"})

    def test_email_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["email"], self.user.email)

    def test_password_write_only(self):
        data = self.serializer_data
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertNotIn("password", serializer.validated_data)
        self.assertNotIn("password", serializer.data)

    def test_password_min_length_validation(self):
        data = {"email": "newuser@example.com", "password": "1234"}
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_create_user(self):
        serializer = UserSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertTrue(user.pk)
        self.assertEqual(user.email, self.serializer_data["email"])
        self.assertTrue(user.check_password(self.serializer_data["password"]))

    def test_update_user(self):
        updated_data = {"email": "updated@example.com", "password": "newpassword123"}
        serializer = UserSerializer(instance=self.user, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()
        self.assertEqual(updated_user.pk, self.user.pk)
        self.assertEqual(updated_user.email, updated_data["email"])
        self.assertTrue(updated_user.check_password(updated_data["password"]))


class UserAdminTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com", password="password123"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="test@example.com",
            password="password123",
            first_name="John",
            last_name="Doe",
        )
        self.change_user_url = reverse("admin:users_user_change", args=[self.user.id])
        self.user_data = {
            "email": "newemail@example.com",
            "first_name": "Jane",
            "last_name": "Doe",
            "is_active": True,
            "is_staff": False,
            "is_superuser": False,
        }

    def test_user_change_page(self):
        """Test that the user edit page works"""
        response = self.client.get(self.change_user_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.user.email)
        self.assertContains(response, self.user.first_name)
        self.assertContains(response, self.user.last_name)

    def test_user_change_page_updates_user(self):
        """Test that the user edit page updates a user"""
        response = self.client.post(self.change_user_url, self.user_data)

        self.assertRedirects(response, reverse("admin:users_user_changelist"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, self.user_data["email"])
        self.assertEqual(self.user.first_name, self.user_data["first_name"])
        self.assertEqual(self.user.last_name, self.user_data["last_name"])
        self.assertEqual(self.user.is_active, self.user_data["is_active"])
        self.assertEqual(self.user.is_staff, self.user_data["is_staff"])
        self.assertEqual(self.user.is_superuser, self.user_data["is_superuser"])

    def test_user_change_page_password_hashed(self):
        """Test that the user edit page updates a user's password hashed"""
        password = "newpassword123"
        response = self.client.post(
            self.change_user_url,
            {**self.user_data, "password": password, "password_confirmation": password},
        )

        self.assertRedirects(response, reverse("admin:users_user_changelist"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(password))

    def test_user_add_page(self):
        """Test that the user add page works"""
        add_user_url = reverse("admin:users_user_add")
        response = self.client.get(add_user_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_add_page_creates_user(self):
        """Test that the user add page creates a user"""
        add_user_url = reverse("admin:users_user_add")
        response = self.client.post(add_user_url, self.user_data)

        self.assertRedirects(response, reverse("admin:users_user_changelist"))
        self.assertEqual(User.objects.count(), 2)
        new_user = User.objects.get(email=self.user_data["email"])
        self.assertTrue(new_user.check_password("password123"))
