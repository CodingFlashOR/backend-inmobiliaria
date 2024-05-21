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
    def _assert_errors_nested_field(
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
            "base_data": {
                "email": "user1@email.com",
                "password": "contraseña1234",
                "confirm_password": "contraseña1234",
            },
            "profile_data": {
                "full_name": "Nombre Apellido",
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

        base_data = data.pop("base_data")
        profile_data = data.pop("profile_data")

        for field, value in base_data.items():
            assert serializer.validated_data["base_data"][field] == value

        for field, value in profile_data.items():
            assert serializer.validated_data["profile_data"][field] == value

    @pytest.mark.parametrize(
        argnames="data, error_messages",
        argvalues=[
            (
                {},
                {
                    "base_data": ["Este campo es requerido."],
                    "profile_data": ["Este campo es requerido."],
                },
            ),
            (
                {
                    "base_data": {
                        "full_name": "Nombre Apellido",
                        "email": "user1@email.com",
                        "password": "contraseña1234",
                        "confirm_password": "contraseña1234",
                    },
                    "profile_data": {},
                },
                {
                    "profile_data": {
                        "full_name": ["Este campo es requerido."],
                        "address": ["Este campo es requerido."],
                        "phone_number": ["Este campo es requerido."],
                    },
                },
            ),
            (
                {
                    "base_data": {},
                    "profile_data": {
                        "full_name": "Nombre Apellido",
                        "address": "Residencia 1",
                        "phone_number": "+57 3123574898",
                    },
                },
                {
                    "base_data": {
                        "email": ["Este campo es requerido."],
                        "password": ["Este campo es requerido."],
                        "confirm_password": ["Este campo es requerido."],
                    },
                },
            ),
            (
                {
                    "base_data": {
                        "email": "useremail.com",
                        "password": "contraseña1234",
                        "confirm_password": "contraseña1234",
                    },
                    "profile_data": {
                        "full_name": "User123",
                        "address": "Residencia 1",
                        "phone_number": "3123574898",
                    },
                },
                {
                    "base_data": {
                        "email": ["El valor ingresado es inválido."],
                    },
                    "profile_data": {
                        "full_name": ["El valor ingresado es inválido."],
                        "phone_number": ["El valor ingresado es inválido."],
                    },
                },
            ),
            (
                {
                    "base_data": {
                        "email": f"user{fake.random_number(digits=41)}@email.com",
                        "password": fake.password(
                            length=21, special_chars=True
                        ),
                    },
                    "profile_data": {
                        "full_name": fake.bothify(text=f"{'?' * 41}"),
                        "address": fake.bothify(text=f"{'?' * 91}"),
                    },
                },
                {
                    "base_data": {
                        "email": [
                            "El valor ingresado no puede tener más de 40 caracteres."
                        ],
                        "password": [
                            "El valor ingresado no puede tener más de 20 caracteres."
                        ],
                        "confirm_password": ["Este campo es requerido."],
                    },
                    "profile_data": {
                        "full_name": [
                            "El valor ingresado no puede tener más de 40 caracteres."
                        ],
                        "address": [
                            "El valor ingresado no puede tener más de 90 caracteres."
                        ],
                        "phone_number": ["Este campo es requerido."],
                    },
                },
            ),
            (
                {
                    "base_data": {
                        "email": "user1@email.com",
                        "password": "contraseña1234",
                        "confirm_password": "contraseña5678",
                    },
                    "profile_data": {
                        "full_name": "Nombre Apellido",
                        "address": "Residencia 1",
                        "phone_number": "+57 3123574898",
                    },
                },
                {
                    "base_data": {
                        "confirm_password": ["Las contraseñas no coinciden."],
                    }
                },
            ),
            (
                {
                    "base_data": {
                        "email": "user1@email.com",
                        "password": f"{fake.random_number(digits=10)}",
                    },
                    "profile_data": {
                        "full_name": "Nombre Apellido",
                        "address": "Residencia 1",
                        "phone_number": "+57 3123574898",
                    },
                },
                {
                    "base_data": {
                        "password": [
                            "La contraseña debe contener al menos una mayuscula o una minuscula."
                        ],
                        "confirm_password": ["Este campo es requerido."],
                    }
                },
            ),
        ],
        ids=[
            "empty_data",
            "empty_profile_data",
            "empty_base_data",
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
        data: Dict[str, Dict],
        error_messages: Dict[str, Dict],
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

        errors = serializer.errors.copy()
        base_data_errors: Dict = errors.pop(key="base_data", default=None)
        profile_data_errors: Dict = errors.pop(
            key="profile_data", default=None
        )

        if isinstance(base_data_errors, dict):
            self._assert_errors_nested_field(
                key="base_data",
                value=base_data_errors,
                expected_errors=error_messages,
            )
        elif isinstance(profile_data_errors, dict):
            self._assert_errors_nested_field(
                key="profile_data",
                value=profile_data_errors,
                expected_errors=error_messages,
            )

    @pytest.mark.parametrize(
        argnames="data, error_messages",
        argvalues=[
            (
                {
                    "base_data": {
                        "email": "user1@email.com",
                        "password": "contraseña1234",
                        "confirm_password": "contraseña1234",
                    },
                    "profile_data": {
                        "full_name": "Nombre Apellido",
                        "address": "Residencia 1",
                        "phone_number": "+57 3123574898",
                    },
                },
                {
                    "base_data": {
                        "email": ["Este correo electrónico ya está en uso."],
                    }
                },
            ),
        ],
        ids=["email_in_use"],
    )
    @patch(
        "apps.users.infrastructure.serializers.searcher_user.UserRepository"
    )
    @patch("apps.users.infrastructure.serializers.base.UserRepository")
    def test_base_data_used(
        self,
        repository_base: Mock,
        repository_searcher_user: Mock,
        queryset: Mock,
        data: Dict[str, Dict],
        error_messages: Dict[str, Dict],
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

        self._assert_errors_nested_field(
            key="base_data",
            value=serializer.errors["base_data"],
            expected_errors=error_messages,
        )

    @pytest.mark.parametrize(
        argnames="data, error_messages",
        argvalues=[
            (
                {
                    "base_data": {
                        "email": "user1@email.com",
                        "password": "contraseña1234",
                        "confirm_password": "contraseña1234",
                    },
                    "profile_data": {
                        "full_name": "Nombre Apellido",
                        "address": "Residencia 1",
                        "phone_number": "+57 3123574898",
                    },
                },
                {
                    "profile_data": {
                        "full_name": ["Este nombre ya está en uso."],
                    },
                },
            ),
            (
                {
                    "base_data": {
                        "email": "user1@email.com",
                        "password": "contraseña1234",
                        "confirm_password": "contraseña1234",
                    },
                    "profile_data": {
                        "full_name": "Nombre Apellido",
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
                    "base_data": {
                        "email": "user1@email.com",
                        "password": "contraseña1234",
                        "confirm_password": "contraseña1234",
                    },
                    "profile_data": {
                        "full_name": "Nombre Apellido",
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
        ids=["full_name_in_use", "address_in_use", "phone_number_in_use"],
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
        data: Dict[str, Dict],
        error_messages: Dict[str, Dict],
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

        self._assert_errors_nested_field(
            key="profile_data",
            value=serializer.errors["profile_data"],
            expected_errors=error_messages,
        )
