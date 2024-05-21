from django.test import Client
from django.urls import reverse
from apps.users.models import User, UserRoles
from typing import Tuple, Dict
from faker import Faker
import pytest


fake = Faker("es_CO")


@pytest.fixture
def setUp() -> Tuple[Client, str]:
    return Client(), reverse(viewname="searcher_user")


@pytest.mark.django_db
class TestAPIViewPOSTMethod:
    """
    This class groups all test cases for the POST method of the `SearcherUserAPIView`.
    The view is responsible for managing the registration of new users with the
    `searcheruser` role.
    """

    @staticmethod
    def _assert_errors_nested_field(
        key: str, value: Dict, expected_errors: Dict[str, Dict]
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

    def test_request_valid(self, setUp: Tuple[Client, str]) -> None:
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

        # Simulating the request
        client, path = setUp
        response = client.post(
            path=path, data=data, content_type="application/json"
        )

        # Asserting that response data is correct
        assert response.status_code == 201

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
    def test_invalid_data(
        self,
        setUp: Tuple[Client, str],
        data: Dict[str, Dict],
        error_messages: Dict[str, Dict],
    ) -> None:
        # Simulating the request
        client, path = setUp
        response = client.post(
            path=path, data=data, content_type="application/json"
        )

        # Asserting that response data is correct
        assert response.status_code == 400
        assert response.data["code"] == "invalid_request_data"

        errors: Dict = response.data["detail"].copy()
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
    def test_base_data_used(
        self,
        setUp: Tuple[Client, str],
        data: Dict[str, Dict],
        error_messages: Dict[str, Dict],
    ) -> None:
        # Creating a user
        base_data = data["base_data"].copy()
        base_data.pop("confirm_password")
        _ = User.objects.create_user(
            base_data=base_data,
            profile_data=data["profile_data"],
            related_model_name=UserRoles.SEARCHER.value,
        )

        # Simulating the request
        client, path = setUp
        response = client.post(
            path=path, data=data, content_type="application/json"
        )

        # Asserting that response data is correct
        assert response.status_code == 400
        assert response.data["code"] == "invalid_request_data"

        self._assert_errors_nested_field(
            key="base_data",
            value=response.data["detail"]["base_data"],
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
    def test_profile_data_used(
        self,
        setUp: Tuple[Client, str],
        data: Dict[str, Dict],
        error_messages: Dict[str, Dict],
    ) -> None:
        # Creating a user
        base_data = data["base_data"].copy()
        base_data.pop("confirm_password")
        _ = User.objects.create_user(
            base_data=base_data,
            profile_data=data["profile_data"],
            related_model_name=UserRoles.SEARCHER.value,
        )

        # Simulating the request
        client, path = setUp
        response = client.post(
            path=path, data=data, content_type="application/json"
        )

        # Asserting that response data is correct
        assert response.status_code == 400
        assert response.data["code"] == "invalid_request_data"

        self._assert_errors_nested_field(
            key="profile_data",
            value=response.data["detail"]["profile_data"],
            expected_errors=error_messages,
        )
