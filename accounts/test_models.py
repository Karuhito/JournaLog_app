import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestCustomUser:
    def test_str_returns_username(self):
        user = User.objects.create_user(username="testuser", password="testpass123")

        assert str(user) == "testuser"

    def test_create_user_hashes_password(self):
        user = User.objects.create_user(username="testuser", password="testpass123")

        assert user.password != "testpass123"
        assert user.check_password("testpass123")
