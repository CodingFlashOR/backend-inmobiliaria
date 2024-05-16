from apps.users.infrastructure.serializers import UpdateTokenSerializer
from tests.users.factory import JWTFactory
from typing import Dict
import pytest


class TestSerializer:
    """
    A class to test the `UpdateTokenSerializer` class.
    """

    serializer_class = UpdateTokenSerializer

    def test_correct_execution(self) -> None:
        # Creating the token
        refresh = JWTFactory.refresh().get("token")

        # Instantiating the serializer
        serializer = self.serializer_class(data={"refresh": refresh})

        # Check if the serializer is valid
        assert serializer.is_valid()

        # Check if the serializer has the correct validated data
        assert serializer.validated_data["refresh"]["token"] == refresh

    @pytest.mark.parametrize(
        argnames="data, error_messages",
        argvalues=[
            (
                {},
                {"refresh": ["This field is required."]},
            ),
            (
                {"refresh": JWTFactory.refresh_invalid()},
                {"refresh": ["Token is invalid."]},
            ),
            (
                {"refresh": JWTFactory.refresh_exp().get("token")},
                {"refresh": ["Token is expired."]},
            ),
        ],
        ids=[
            "empty_data",
            "token_invalid",
            "token_expired",
        ],
    )
    def test_failed_execution(self, data: Dict, error_messages: Dict) -> None:
        # Instantiating the serializer
        serializer = self.serializer_class(data=data)

        # Check if the serializer is not valid
        assert not serializer.is_valid()
        assert serializer.validated_data == {}

        # Check if the serializer has the correct error messages
        serializer_errors_formated = {
            field: [str(error) for error in errors]
            for field, errors in serializer.errors.items()
        }

        for field, message in error_messages.items():
            assert serializer_errors_formated[field] == message
