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

    def test_request_valid(self, setUp: Tuple[Client, str]) -> None:
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
                    "password": fake.password(length=21, special_chars=True),
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
    def test_invalid_data(
        self, setUp: Tuple[Client, str], data: Dict, error_messages: Dict
    ) -> None:
        # Simulating the request
        client, path = setUp
        response = client.post(
            path=path, data=data, content_type="application/json"
        )

        # Asserting that response data is correct
        assert response.status_code == 400
        assert response.data["code"] == "invalid_request_data"

        response_data_error: Dict = response.data["detail"].copy()
        profile_data_errors: Dict = response_data_error.get(
            "profile_data", None
        )

        # If there are errors in data_profile, we assert them separately
        if isinstance(profile_data_errors, dict):
            self._assert_errors_nested_field(
                key="profile_data",
                value=profile_data_errors,
                expected_errors=error_messages,
            )

            # Remove profile data errors from serializer errors and error_messages
            # We do not want to create problems with the other assertions.
            response_data_error.pop("profile_data")
            error_messages.pop("profile_data")

        # Asserting that response data is correct
        response_data_error_formated = {
            field: [str(error) for error in errors]
            for field, errors in response_data_error.items()
        }

        for field, message in error_messages.items():
            assert response_data_error_formated[field] == message

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
    def test_user_data_used(
        self,
        setUp: Tuple[Client, str],
        data: Dict,
        user_data_in_use: str,
        error_messages: Dict,
    ) -> None:
        # Creating a user
        User.objects.create_user(
            full_name=data["full_name"],
            email=data["email"],
            password=data["password"],
            related_model_name=UserRoles.SEARCHER.value,
            related_data=data["profile_data"],
        )

        # Simulating the request
        client, path = setUp
        response = client.post(
            path=path, data=data, content_type="application/json"
        )

        # Asserting that response data is correct
        assert response.status_code == 400
        assert response.data["code"] == "invalid_request_data"

        response_data_errors = {
            field: [str(error) for error in errors]
            for field, errors in response.data["detail"].items()
        }

        assert (
            response_data_errors[user_data_in_use]
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
    def test_profile_data_used(
        self,
        setUp: Tuple[Client, str],
        data: Dict,
        error_messages: Dict,
    ) -> None:
        # Creating a user
        User.objects.create_user(
            full_name=data["full_name"],
            email=data["email"],
            password=data["password"],
            related_model_name=UserRoles.SEARCHER.value,
            related_data=data["profile_data"],
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
