import pytest

from typing import Dict
from unittest.mock import Mock, patch

from apps.users.infrastructure.serializers import RegisterSerializer
from apps.exceptions import UserNotFoundError
from tests.users.factory import UserFactory


class TestSerializer:
    """
    A class to test the RegisterSerializer.

    This class contains tests to validate the RegisterSerializer. It tests various
    scenarios such as valid data, invalid data, and used email.
    """

    serializer_class = RegisterSerializer

    @pytest.mark.parametrize(
        "data",
        [
            {
                "email": "user@example.com",
                "password": "Aaa123456789",
                "confirm_password": "Aaa123456789",
            }
        ],
        ids=["valid data"],
    )
    @patch("apps.users.infrastructure.serializers.register.UserRepository")
    def test_serializer_valid(self, repository: Mock, data) -> None:

        # Mocking the methods
        get_user: Mock = repository.get_user

        # Setting the return values
        get_user.side_effect = UserNotFoundError

        serializer = self.serializer_class(data=data)

        assert serializer.is_valid()
        assert serializer.initial_data["email"] == data["email"]
        assert serializer.initial_data["password"] == data["password"]
        assert (
            serializer.initial_data["confirm_password"]
            == data["confirm_password"]
        )
        assert serializer.validated_data["email"] == data["email"]
        assert serializer.validated_data["password"] == data["password"]
        assert (
            serializer.validated_data["confirm_password"]
            == data["confirm_password"]
        )
        get_user.assert_called_once_with(email=data["email"])

    @pytest.mark.parametrize(
        "data, error_messages",
        [
            (
                {
                    "email": "user@example",
                    "password": "Aaad123456789",
                    "confirm_password": "Aaad123456789",
                },
                {"Correo electrónico inválido."},
            ),
            (
                {
                    "email": "user@example.com",
                    "password": "123456",
                    "confirm_password": "123456",
                },
                {"La contraseña debe tener al menos 8 caracteres."},
            ),
            (
                {},
                {
                    "Este campo es requerido.",
                    "Este campo es requerido.",
                    "Este campo es requerido.",
                },
            ),
            (
                {
                    "email": "user@example.com",
                    "password": "Aaa123456789",
                    "confirm_password": "Aaa12345678",
                },
                {"Las contraseñas no coinciden."},
            ),
            (
                {
                    "email": "user.com",
                    "password": "123456789",
                    "confirm_password": "12345678",
                },
                {
                    "La contraseña debe contener al menos una mayuscula y una minuscula.",
                    "Correo electrónico inválido.",
                },
            ),
        ],
        ids=[
            "email invalid",
            "password invalid",
            "missing all fields",
            "passwords not match",
            "all fields invalid",
        ],
    )
    @patch("apps.users.infrastructure.serializers.register.UserRepository")
    def test_serializer_invalid(
        self, repository: Mock, data, error_messages
    ) -> None:

        # Mocking the methods
        get_user: Mock = repository.get_user

        # Setting the return values
        get_user.side_effect = UserNotFoundError

        serializer = self.serializer_class(data=data)

        assert not serializer.is_valid()
        assert serializer.validated_data == {}
        error_password = set(serializer.errors.get("password", []))
        error_confirm_password = set(
            serializer.errors.get("non_field_errors", [])
        )
        error_email = set(serializer.errors.get("email", []))
        assert (
            error_password.union(error_email, error_confirm_password)
            == error_messages
        )

    @pytest.mark.parametrize(
        "data",
        [
            {
                "email": "user@example.com",
                "password": "Aaa123456789",
                "confirm_password": "Aaa123456789",
            }
        ],
        ids=["valid data"],
    )
    @patch("apps.users.infrastructure.serializers.register.UserRepository")
    def test_if_email_used(
        self, repository: Mock, data: Dict[str, str]
    ) -> None:

        user = UserFactory.build(email=data["email"])

        # Mocking the methods
        get_user: Mock = repository.get_user

        # Setting the return values
        get_user.return_value = user

        serializer = self.serializer_class(data=data)

        assert not serializer.is_valid()
        assert serializer.validated_data == {}
        assert (
            str(serializer.errors["email"][0])
            == "Este correo electrónico ya está en uso."
        )
        get_user.assert_called_once_with(email=data["email"])
