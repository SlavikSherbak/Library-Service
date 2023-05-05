from django.test import TestCase

import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(email="test@example.com", password="testpass")
    assert user.email == "test@example.com"
    assert user.username is None
    assert user.check_password("testpass")


@pytest.mark.django_db
def test_create_user_without_email():
    with pytest.raises(TypeError):
        user = User.objects.create_user(password="testpass")


@pytest.mark.django_db
def test_create_super_user():
    user = User.objects.create_superuser(email="admin@example.com", password="testpass")
    assert user.email == "admin@example.com"
    assert user.username is None
    assert user.check_password("testpass")
    assert user.is_staff
    assert user.is_superuser


@pytest.mark.django_db
def test_create_user_with_duplicate_email():
    User.objects.create_user(email="test@example.com", password="testpass")
    with pytest.raises(ValidationError):
        User.objects.create_user(email="test@example.com", password="testpass2")
