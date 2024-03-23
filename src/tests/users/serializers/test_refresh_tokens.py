import pytest

from apps.users.infrastructure.serializers import RefreshTokenSerializer
from tests.users.factory import JWTFactory


class TestSerializer:
    """
    A class to test the RefreshTokenSerializer.

    This class contains tests to validate the RefreshTokenSerializer. It tests
    various scenarios such as valid and invalid data.
    """

    serializer_class = RefreshTokenSerializer

    @pytest.mark.parametrize(
        "access, refresh",
        [(JWTFactory.access_exp(), JWTFactory.refresh())],
        ids=["Valid data"],
    )
    def test_serializer_valid(self, access, refresh) -> None:

        serializer = self.serializer_class(
            data={"access": access["token"], "refresh": refresh["token"]}
        )

        assert serializer.is_valid()
        assert serializer.initial_data["refresh"] == refresh["token"]
        assert serializer.initial_data["access"] == access["token"]
        assert (
            serializer.validated_data["refresh"]["token"] == refresh["token"]
        )
        assert (
            serializer.validated_data["refresh"]["payload"]
            == refresh["payload"]
        )
        assert serializer.validated_data["access"]["token"] == access["token"]
        assert (
            serializer.validated_data["access"]["payload"] == access["payload"]
        )

    @pytest.mark.parametrize(
        "access, refresh, error_message",
        [
            (
                JWTFactory.access_invalid(),
                JWTFactory.refresh(),
                "Token is invalid.",
            ),
            (
                JWTFactory.access_exp(),
                JWTFactory.refresh_invalid(),
                "Token is invalid.",
            ),
            (
                JWTFactory.access_exp(),
                JWTFactory.refresh_exp(),
                "Token is expired.",
            ),
            (
                JWTFactory.access(),
                JWTFactory.refresh(),
                "Token is not expired.",
            ),
        ],
        ids=[
            "access token invalid",
            "refresh token invalid",
            "refresh token expired",
            "access token not expired",
        ],
    )
    def test_serializer_invalid(self, access, refresh, error_message) -> None:

        serializer = self.serializer_class(
            data={"access": access["token"], "refresh": refresh["token"]}
        )

        assert not serializer.is_valid()
        assert serializer.validated_data == {}
        for _, value in serializer.errors.items():
            assert value[0] == error_message
