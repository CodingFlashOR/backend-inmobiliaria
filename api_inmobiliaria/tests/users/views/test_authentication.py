from apps.users.models import User, UserRoles
from apps.exceptions import DatabaseConnectionError
from django.test import Client
from django.urls import reverse
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
            "base_data": {
                "email": "user1@email.com",
                "password": "contraseña1234",
            },
            "profile_data": {
                "full_name": "Nombre Apellido",
                "address": "Residencia 1",
                "phone_number": "+57 3123574898",
            },
        }
        email = data["base_data"]["email"]
        password = data["base_data"]["password"]
        user = User.objects.create_user(
            base_data=data["base_data"],
            profile_data=data["profile_data"],
            related_model_name=UserRoles.SEARCHER.value,
        )
        user.is_active = True
        user.save()

        # Simulating the request
        client, path = setUp
        response = client.post(
            path=path,
            data={"email": email, "password": password},
            content_type="application/json",
        )

        # Asserting that response data is correct
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    def test_if_credentials_invalid(self, setUp: Tuple[Client, str]) -> None:
        # Simulating the request
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
            "base_data": {
                "email": "user1@email.com",
                "password": "contraseña1234",
            },
            "profile_data": {
                "full_name": "Nombre Apellido",
                "address": "Residencia 1",
                "phone_number": "+57 3123574898",
            },
        }
        email = data["base_data"]["email"]
        password = data["base_data"]["password"]
        _ = User.objects.create_user(
            base_data=data["base_data"],
            profile_data=data["profile_data"],
            related_model_name=UserRoles.SEARCHER.value,
        )

        # Simulating the request
        client, path = setUp
        response = client.post(
            path=path,
            data={"email": email, "password": password},
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

        # Simulating the request
        client, path = setUp
        response = client.post(
            path=path,
            data={"email": "user1@emial.com", "password": "contraseña1234"},
            content_type="application/json",
        )
        print(response.data)
        # Asserting that response data is correct
        assert response.status_code == 500
        assert "database_connection_error" in response.data["code"]
        assert (
            "Unable to establish a connection with the database. Please try again later."
            in response.data["detail"]
        )
