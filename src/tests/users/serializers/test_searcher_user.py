from apps.users.infrastructure.serializers import SearcherUserSerializer
from apps.users.models import User, SearcherUser
from tests.utils import get_empty_queryset
from unittest.mock import Mock, patch
from typing import Dict
from faker import Faker
import pytest


fake = Faker("es_CO")


class TestSerializer:
    """
    A class to test the `SearcherUserSerializer` class.
    """

    serializer_class = SearcherUserSerializer

    @staticmethod
    def assert_errors_nested_field(
        key: str, value: Dict, expected_errors: Dict
    ) -> None:
        """
        This method asserts the errors of a nested field in the serializer.

        #### Parameters:
        - key: The key of the nested field.
        - value: The errors of the nested field.
        - expected_errors: The expected errors of the nested field.
        """

        profile_data_errors_formatted = {
            field: [str(error) for error in errors]
            for field, errors in value.items()
        }

        for field, message in expected_errors[key].items():
            assert profile_data_errors_formatted[field] == message

    @patch(
        "apps.users.infrastructure.serializers.searcher_user.UserRepository"
    )
    @patch("apps.users.infrastructure.serializers.base.UserRepository")
    def test_correct_execution(
        self, repository_base: Mock, repository_searcher_user: Mock
    ) -> None:
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

        # Mocking the methods
        get: Mock = repository_base.get
        get_profile_data: Mock = repository_searcher_user.get_profile_data

        # Setting the return values
        get.return_value = get_empty_queryset(model=User)
        get_profile_data.return_value = get_empty_queryset(model=SearcherUser)

        # Instantiating the serializer
        serializer = self.serializer_class(data=data)

        # Asserting the serializer is valid and the data is correct
        assert serializer.is_valid()

        profile_data = data.pop("profile_data")

        for field, value in data.items():
            assert serializer.validated_data[field] == value

        for field, value in profile_data.items():
            assert serializer.validated_data["profile_data"][field] == value

    @pytest.mark.parametrize(
        argnames="data, error_messages",
        argvalues=[
            (
                {},
                {
                    "full_name": ["Este campo es requerido."],
                    "email": ["Este campo es requerido."],
                    "password": ["Este campo es requerido."],
                    "confirm_password": ["Este campo es requerido."],
                    "profile_data": ["Este campo es requerido."],
                },
            ),
            (
                {
                    "full_name": "Nombre Apellido",
                    "email": "user1@email.com",
                    "password": "contraseña1234",
                    "confirm_password": "contraseña1234",
                    "profile_data": {},
                },
                {
                    "profile_data": {
                        "address": ["Este campo es requerido."],
                        "phone_number": ["Este campo es requerido."],
                    },
                },
            ),
            (
                {
                    "full_name": "User123",
                    "email": "useremail.com",
                    "password": "contraseña1234",
                    "confirm_password": "contraseña1234",
                    "profile_data": {
                        "address": "Residencia 1",
                        "phone_number": "3123574898",
                    },
                },
                {
                    "full_name": ["El valor ingresado es inválido."],
                    "email": ["El valor ingresado es inválido."],
                    "profile_data": {
                        "phone_number": ["El valor ingresado es inválido."],
                    },
                },
            ),
            (
                {
                    "full_name": fake.bothify(text=f"{'?' * 41}"),
                    "email": f"user{fake.random_number(digits=41)}@email.com",
                    "password": fake.bothify(text=f"{'?#' * 21}"),
                    "profile_data": {
                        "address": fake.bothify(text=f"{'?' * 91}"),
                    },
                },
                {
                    "full_name": [
                        "El valor ingresado no puede tener más de 40 caracteres."
                    ],
                    "email": [
                        "El valor ingresado no puede tener más de 40 caracteres."
                    ],
                    "password": [
                        "El valor ingresado no puede tener más de 20 caracteres."
                    ],
                    "confirm_password": ["Este campo es requerido."],
                    "profile_data": {
                        "address": [
                            "El valor ingresado no puede tener más de 90 caracteres."
                        ],
                        "phone_number": ["Este campo es requerido."],
                    },
                },
            ),
            (
                {
                    "full_name": "Nombre Apellido",
                    "email": "user1@email.com",
                    "password": "contraseña1234",
                    "confirm_password": "contraseña5678",
                    "profile_data": {
                        "address": "Residencia 1",
                        "phone_number": "+57 3123574898",
                    },
                },
                {
                    "confirm_password": ["Las contraseñas no coinciden."],
                },
            ),
            (
                {
                    "full_name": "Nombre Apellido",
                    "email": "user1@email.com",
                    "password": f"{fake.random_number(digits=10)}",
                    "profile_data": {
                        "address": "Residencia 1",
                        "phone_number": "+57 3123574898",
                    },
                },
                {
                    "password": [
                        "La contraseña debe contener al menos una mayuscula o una minuscula."
                    ],
                    "confirm_password": ["Este campo es requerido."],
                },
            ),
        ],
        ids=[
            "empty_data",
            "empty_profile_data",
            "invalid_data",
            "max_length_data",
            "passwords_not_match",
            "password_no_upper_lower",
        ],
    )
    @patch(
        "apps.users.infrastructure.serializers.searcher_user.UserRepository"
    )
    @patch("apps.users.infrastructure.serializers.base.UserRepository")
    def test_failed_execution(
        self,
        repository_base: Mock,
        repository_searcher_user: Mock,
        data: Dict,
        error_messages: Dict,
    ) -> None:
        # Mocking the methods
        get: Mock = repository_base.get
        get_profile_data: Mock = repository_searcher_user.get_profile_data

        # Setting the return values
        get.return_value = get_empty_queryset(model=User)
        get_profile_data.return_value = get_empty_queryset(model=SearcherUser)

        # Instantiating the serializer
        serializer = self.serializer_class(data=data)

        # Asserting the serializer is not valid and the data is correct
        assert not serializer.is_valid()
        assert serializer.validated_data == {}

        serializer_errors = serializer.errors.copy()
        profile_data_errors: Dict = serializer_errors.get("profile_data", None)

        if isinstance(profile_data_errors, dict):
            # If there are errors in data_profile, we assert them separately
            self.assert_errors_nested_field(
                key="profile_data",
                value=profile_data_errors,
                expected_errors=error_messages,
            )

            # Remove profile data errors from serializer errors and error_messages
            # We do not want to create problems with the other assertions.
            serializer_errors.pop("profile_data")
            error_messages.pop("profile_data")

        serializer_errors_formated = {
            field: [str(error) for error in errors]
            for field, errors in serializer_errors.items()
        }

        for field, message in error_messages.items():
            assert serializer_errors_formated[field] == message

    @pytest.mark.parametrize(
        argnames="data, user_data_in_use, error_messages",
        argvalues=[
            (
                {
                    "full_name": "Nombre Apellido",
                    "email": "user1@email.com",
                    "password": "contraseña1234",
                    "confirm_password": "contraseña1234",
                    "profile_data": {
                        "address": "Residencia 1",
                        "phone_number": "+57 3123574898",
                    },
                },
                "full_name",
                {
                    "full_name": ["Este nombre ya está en uso."],
                },
            ),
            (
                {
                    "full_name": "Nombre Apellido",
                    "email": "user1@email.com",
                    "password": "contraseña1234",
                    "confirm_password": "contraseña1234",
                    "profile_data": {
                        "address": "Residencia 1",
                        "phone_number": "+57 3123574898",
                    },
                },
                "email",
                {
                    "email": ["Este correo electrónico ya está en uso."],
                },
            ),
        ],
        ids=["full_name_in_use", "email_in_use"],
    )
    @patch(
        "apps.users.infrastructure.serializers.searcher_user.UserRepository"
    )
    @patch("apps.users.infrastructure.serializers.base.UserRepository")
    def test_user_data_used(
        self,
        repository_base: Mock,
        repository_searcher_user: Mock,
        queryset: Mock,
        data: Dict,
        user_data_in_use: str,
        error_messages: Dict,
    ) -> None:
        # Mocking the methods
        get: Mock = repository_base.get
        get_profile_data: Mock = repository_searcher_user.get_profile_data
        user: Mock = queryset.first

        # Setting the return values
        get.return_value = queryset
        user.return_value = User
        get_profile_data.return_value = get_empty_queryset(model=SearcherUser)

        # Instantiating the serializer
        serializer = self.serializer_class(data=data)

        # Asserting the serializer is not valid and the data is correct
        assert not serializer.is_valid()
        assert serializer.validated_data == {}

        serializer_errors_formated = {
            field: [str(error) for error in errors]
            for field, errors in serializer.errors.items()
        }

        assert (
            serializer_errors_formated[user_data_in_use]
            == error_messages[user_data_in_use]
        )

    @pytest.mark.parametrize(
        argnames="data, error_messages",
        argvalues=[
            (
                {
                    "full_name": "Nombre Apellido",
                    "email": "user1@email.com",
                    "password": "contraseña1234",
                    "confirm_password": "contraseña1234",
                    "profile_data": {
                        "address": "Residencia 1",
                        "phone_number": "+57 3123574898",
                    },
                },
                {
                    "profile_data": {
                        "address": ["Esta dirección ya está en uso."],
                    },
                },
            ),
            (
                {
                    "full_name": "Nombre Apellido",
                    "email": "user1@email.com",
                    "password": "contraseña1234",
                    "confirm_password": "contraseña1234",
                    "profile_data": {
                        "address": "Residencia 1",
                        "phone_number": "+57 3123574898",
                    },
                },
                {
                    "profile_data": {
                        "phone_number": [
                            "Este número de teléfono ya está en uso."
                        ],
                    },
                },
            ),
        ],
        ids=["address_in_use", "phone_number_in_use"],
    )
    @patch(
        "apps.users.infrastructure.serializers.searcher_user.UserRepository"
    )
    @patch("apps.users.infrastructure.serializers.base.UserRepository")
    def test_profile_data_used(
        self,
        repository_base: Mock,
        repository_searcher_user: Mock,
        queryset: Mock,
        data: Dict,
        error_messages: Dict,
    ) -> None:
        # Mocking the methods
        get: Mock = repository_base.get
        get_profile_data: Mock = repository_searcher_user.get_profile_data
        user: Mock = queryset.first

        # Setting the return values
        get.return_value = get_empty_queryset(model=User)
        get_profile_data.return_value = queryset
        user.return_value = SearcherUser

        # Instantiating the serializer
        serializer = self.serializer_class(data=data)

        # Asserting the serializer is not valid and the data is correct
        assert not serializer.is_valid()
        assert serializer.validated_data == {}

        self.assert_errors_nested_field(
            key="profile_data",
            value=serializer.errors["profile_data"],
            expected_errors=error_messages,
        )
