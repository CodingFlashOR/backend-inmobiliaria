import pytest

from apps.users.infrastructure.serializers import AuthenticationSerializer


class TestSerializer:
    """
    A class to test the `AuthenticationSerializer`.

    This class contains tests to validate the AuthenticationSerializer. It tests
    various scenarios such as valid and invalid data.
    """

    serializer_class = AuthenticationSerializer

    @pytest.mark.parametrize(
        "data",
        [
            {
                "email": "user@example.com",
                "password": "Aaa123456789",
            }
        ],
        ids=["valid data"],
    )
    def test_serializer_valid(self, data) -> None:

        serializer = self.serializer_class(data=data)

        assert serializer.is_valid()
        assert serializer.initial_data["email"] == data["email"]
        assert serializer.initial_data["password"] == data["password"]
        assert serializer.validated_data["email"] == data["email"]
        assert serializer.validated_data["password"] == data["password"]

    @pytest.mark.parametrize(
        "data, error_message",
        [
            (
                {"email": "user@example", "password": "password123456"},
                {"Correo electrónico inválido."},
            ),
            (
                {"email": "user.com", "password": "password123456"},
                {"Correo electrónico inválido."},
            ),
            (
                {"email": "@user", "password": "password123456"},
                {"Correo electrónico inválido."},
            ),
            (
                {"email": "user@example.com", "password": "123456"},
                {"La contraseña debe tener al menos 8 caracteres."},
            ),
            ({}, {"This field is required.", "This field is required."}),
            (
                {"email": "user.com", "password": "123456"},
                {
                    "La contraseña debe tener al menos 8 caracteres.",
                    "Correo electrónico inválido.",
                },
            ),
        ],
        ids=[
            "email invalid",
            "email invalid",
            "email invalid",
            "password invalid",
            "missing email-password",
            "email-password invalid",
        ],
    )
    def test_serializer_invalid(self, data, error_message) -> None:

        serializer = self.serializer_class(data=data)

        assert not serializer.is_valid()
        assert serializer.validated_data == {}
        error_password = set(serializer.errors.get("password", []))
        error_email = set(serializer.errors.get("email", []))
        assert error_password.union(error_email) == error_message
