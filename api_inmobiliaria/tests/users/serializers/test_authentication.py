from apps.users.infrastructure.serializers import AuthenticationSerializer
from apps.constants import ERROR_MESSAGES


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

    def test_failed_execution(self) -> None:
        # Instantiating the serializer
        serializer = self.serializer_class(data={})

        # Asserting that the serializer is not valid and the errors are correct
        assert not serializer.is_valid()
        assert serializer.validated_data == {}

        serializer_errors_formated = {
            field: [str(error) for error in errors]
            for field, errors in serializer.errors.items()
        }

        assert (
            serializer_errors_formated["email"][0] == ERROR_MESSAGES["required"]
        )
        assert (
            serializer_errors_formated["password"][0]
            == ERROR_MESSAGES["required"]
        )
