from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTestCase(TestCase):
    def setUp(self):
        self.email = "testuser@example.com"
        self.password = "testpassword"

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email=self.email,
            password=self.password
        )

        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        superuser = User.objects.create_superuser(
            email=self.email,
            password=self.password
        )

        self.assertEqual(superuser.email, self.email)
        self.assertTrue(superuser.check_password(self.password))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_user_without_email(self):
        User = get_user_model()

        with self.assertRaises(ValueError):
            User.objects.create_user(
                email=None,
                password=self.password
            )
