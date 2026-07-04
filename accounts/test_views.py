import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.mark.django_db
class TestSignupView:
    def test_get_signup_page(self, client):
        response = client.get(reverse("accounts:signup"))

        assert response.status_code == 200

    def test_signup_creates_user_and_logs_in(self, client):
        response = client.post(
            reverse("accounts:signup"),
            {
                "username": "newuser",
                "password1": "supersecret123",
                "password2": "supersecret123",
            },
        )

        assert response.status_code == 302
        assert User.objects.filter(username="newuser").exists()
        assert response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
class TestLoginView:
    def test_login_succeeds_with_valid_credentials(self, client):
        User.objects.create_user(username="testuser", password="testpass123")

        response = client.post(
            reverse("accounts:login"),
            {"username": "testuser", "password": "testpass123"},
        )

        assert response.status_code == 302
        assert response.wsgi_request.user.is_authenticated

    def test_login_fails_with_invalid_credentials(self, client):
        User.objects.create_user(username="testuser", password="testpass123")

        response = client.post(
            reverse("accounts:login"),
            {"username": "testuser", "password": "wrongpass"},
        )

        assert response.status_code == 200
        assert not response.context["user"].is_authenticated
