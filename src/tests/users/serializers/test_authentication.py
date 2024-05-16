from apps.users.infrastructure.serializers import AuthenticationSerializer
from apps.users.domain.constants import SearcherUser
from apps.constants import ERROR_MESSAGES
from faker import Faker
from typing import Dict
import pytest


fake = Faker("es_CO")


class TestSerializer:
    """
    A class to test the `AuthenticationSerializer` class.
    """

    serializer_class = AuthenticationSerializer

    def test_correct_execution(self) -> None:
        data = {
            "email": "user1@email.com",
            "password": "contraseña1234",
        }

        # Instantiating the serializer
        serializer = self.serializer_class(data=data)

        # Asserting that the serializer is valid and the data is correct
        assert serializer.is_valid()

        for field, value in data.items():
            assert serializer.validated_data[field] == value

    @pytest.mark.parametrize(
        argnames="data, error_messages",
        argvalues=[
            (
                {},
                {
                    "email": [ERROR_MESSAGES["required"]],
                    "password": [ERROR_MESSAGES["required"]],
                },
            ),
            (
                {
                    "email": "useremail.com",
                    "password": "contraseña1234",
                },
                {
                    "email": [ERROR_MESSAGES["invalid"]],
                },
            ),
            (
                {
                    "email": f"user{fake.random_number(digits=41)}@email.com",
                    "password": fake.bothify(text=f"{'?#' * 11}"),
                },
                {
                    "email": [
                        ERROR_MESSAGES["max_length"].format(
                            max_length=SearcherUser.EMAIL_MAX_LENGTH.value
                        ),
                    ],
                    "password": [
                        ERROR_MESSAGES["max_length"].format(
                            max_length=SearcherUser.PASSWORD_MAX_LENGTH.value
                        ),
                    ],
                },
            ),
            (
                {
                    "email": "user1@email.com",
                    "password": fake.bothify(text=f"{'?#' * 3}"),
                },
                {
                    "password": [
                        ERROR_MESSAGES["min_length"].format(
                            min_length=SearcherUser.PASSWORD_MIN_LENGTH.value
                        ),
                    ],
                },
            ),
        ],
        ids=[
            "empty_data",
            "invalid_data",
            "max_length_data",
            "min_length_data",
        ],
    )
    def test_failed_execution(self, data: Dict, error_messages: Dict) -> None:
        # Instantiating the serializer
        serializer = self.serializer_class(data=data)

        # Asserting that the serializer is not valid and the errors are correct
        assert not serializer.is_valid()
        assert serializer.validated_data == {}

        serializer_errors_formated = {
            field: [str(error) for error in errors]
            for field, errors in serializer.errors.items()
        }

        for field, message in error_messages.items():
            assert serializer_errors_formated[field] == message
