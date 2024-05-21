from apps.users.infrastructure.serializers import UpdateTokenSerializer
from tests.users.factory import JWTFactory
from typing import Dict, List
import pytest


class TestSerializer:
    """
    A class to test the `UpdateTokenSerializer` class.
    """

    serializer_class = UpdateTokenSerializer

    def test_correct_execution(self) -> None:
        data = JWTFactory.access_and_refresh(
            exp_access=True, exp_refresh=False
        )
        # Instantiating the serializer
        serializer = self.serializer_class(data=data["tokens"])

        # Check if the serializer is valid
        assert serializer.is_valid()

        # Check if the serializer has the correct validated data
        for key, value in data["payloads"]["access"].items():
            assert serializer.validated_data["access"][key] == value
        for key, value in data["payloads"]["refresh"].items():
            assert serializer.validated_data["refresh"][key] == value

    @pytest.mark.parametrize(
        argnames="data, error_messages",
        argvalues=[
            (
                {},
                {
                    "refresh": ["This field is required."],
                    "access": ["This field is required."],
                },
            ),
            (
                {
                    "refresh": JWTFactory.refresh_invalid(),
                    "access": JWTFactory.access_invalid(),
                },
                {
                    "refresh": ["Token is invalid."],
                    "access": ["Token is invalid."],
                },
            ),
            (
                {
                    "refresh": JWTFactory.refresh(exp=True).get("token"),
                },
                {
                    "access": ["This field is required."],
                    "refresh": ["Token is expired."],
                },
            ),
            (
                {
                    "access": JWTFactory.access(exp=False).get("token"),
                },
                {
                    "refresh": ["This field is required."],
                    "access": ["Token is not expired."],
                },
            ),
        ],
        ids=[
            "empty_data",
            "tokens_invalid",
            "refresh_expired",
            "access_not_expired",
        ],
    )
    def test_failed_execution(
        self, data: Dict[str, str], error_messages: Dict[str, List]
    ) -> None:
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
