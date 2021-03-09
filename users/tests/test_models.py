import pytest

from ..models import User

pytestmark = pytest.mark.django_db


def test_create_user():
    user = User.objects.create_user(
        username="starwars", email="star@wars.com", password="senha@123"
    )

    assert user.username == "starwars"
    assert user.email == "star@wars.com"
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser


def test_create_superuser():
    user = User.objects.create_superuser(
        username="admin_star", email="adminstar@wars.com", password="senha@123"
    )

    assert user.username == "admin_star"
    assert user.email == "adminstar@wars.com"
    assert user.is_active
    assert user.is_staff
    assert user.is_superuser
