from django.test import Client
from django.urls import reverse
from apps.users.models import User, UserRoles
from apps.exceptions import DatabaseConnectionError
from unittest.mock import Mock, patch
from typing import Tuple
import pytest


@pytest.fixture
def setUp() -> Tuple[Client, str]:
    return Client(), reverse(viewname="authenticate_user")


@pytest.mark.django_db
class TestAPIViewPOSTMethod:

    def test_request_valid(self, setUp: Tuple[Client, str]) -> None:
        # Creating a user
        data = {
            "full_name": "Nombre Apellido",
            "email": "user1@email.com",
            "password": "contraseña1234",
            "confirm_password": "contraseña1234",
            "profile_data": {
                "address": "Residencia 1",
                "phone_number": "+57 3123574898",
            },
        }
        user = User.objects.create_user(
            full_name=data["full_name"],
            email=data["email"],
            password=data["password"],
            related_model_name=UserRoles.SEARCHER.value,
            related_data=data["profile_data"],
        )
        user.is_active = True
        user.save()

        client, path = setUp
        response = client.post(
            path=path,
            data={"email": data["email"], "password": data["password"]},
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    def test_if_credentials_invalid(self, setUp: Tuple[Client, str]) -> None:
        client, path = setUp
        response = client.post(
            path=path,
            data={"email": "user1@emial.com", "password": "contraseña1234"},
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == 401
        assert "authentication_failed" in response.data["code"]
        assert "Credenciales inválidas." in response.data["detail"]

    def test_if_inactive_user_account(self, setUp: Tuple[Client, str]) -> None:
        # Creating a user
        data = {
            "full_name": "Nombre Apellido",
            "email": "user1@email.com",
            "password": "contraseña1234",
            "confirm_password": "contraseña1234",
            "profile_data": {
                "address": "Residencia 1",
                "phone_number": "+57 3123574898",
            },
        }
        user = User.objects.create_user(
            full_name=data["full_name"],
            email=data["email"],
            password=data["password"],
            related_model_name=UserRoles.SEARCHER.value,
            related_data=data["profile_data"],
        )

        client, path = setUp
        response = client.post(
            path=path,
            data={"email": data["email"], "password": data["password"]},
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == 401
        assert "authentication_failed" in response.data["code"]
        assert "Cuenta del usuario inactiva." in response.data["detail"]

    @patch("apps.users.backend.UserRepository")
    def test_exception_raised_db(
        self, repository: Mock, setUp: Tuple[Client, str]
    ) -> None:
        # Mocking the methods
        get: Mock = repository.get

        # Setting the return values
        get.side_effect = DatabaseConnectionError

        client, path = setUp
        response = client.post(
            path=path,
            data={"email": "user1@emial.com", "password": "contraseña1234"},
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == 500
        assert "database_connection_error" in response.data["code"]
        assert (
            "Unable to establish a connection with the database. Please try again later."
            in response.data["detail"]
        )
