from django.test import Client
from django.urls import reverse
import pytest

from typing import Tuple

from apps.users.models import User
from tests.users.factory import UserFactory


@pytest.fixture
def setUp() -> Tuple[Client, str]:
    return Client(), reverse(viewname="register_user")


@pytest.mark.django_db
class TestAPIView:
    """
    This class groups all the test cases for the register API view. This view is
    responsible for registering a new user in the real estate management system.
    """

    @pytest.mark.parametrize(
        "data",
        [
            {
                "email": "user@example.com",
                "password": "Aaa123456789",
                "confirm_password": "Aaa123456789",
            }
        ],
        ids=["valid data"],
    )
    def test_request_valid(self, setUp: Tuple[Client, str], data) -> None:

        client, path = setUp

        assert not User.objects.filter(email=data["email"]).exists()

        response = client.post(path=path, data=data)

        assert response.status_code == 201
        assert User.objects.filter(email=data["email"]).exists()

    @pytest.mark.parametrize(
        "data",
        [
            {
                "email": "user.com",
                "password": "Aaa123456789",
                "confirm_password": "Aaa123456789",
            }
        ],
        ids=["email invalid"],
    )
    def test_request_invalid(self, setUp: Tuple[Client, str], data) -> None:

        client, path = setUp

        assert not User.objects.filter(email=data["email"]).exists()

        response = client.post(path=path, data=data)

        assert response.status_code == 400
        assert not User.objects.filter(email=data["email"]).exists()
        assert response.data["code"] == "invalid_request_data"
        assert (
            str(response.data["detail"]["email"][0])
            == "Correo electrónico inválido."
        )

    @pytest.mark.parametrize(
        "data",
        [
            {
                "email": "user@example.com",
                "password": "Aaa123456789",
                "confirm_password": "Aaa123456789",
            }
        ],
        ids=["valid data"],
    )
    def test_if_email_used(self, setUp: Tuple[Client, str], data) -> None:

        client, path = setUp

        UserFactory.create(email=data["email"], password=data["password"])

        response = client.post(path=path, data=data)

        assert response.status_code == 400
        assert response.data["code"] == "invalid_request_data"
        assert (
            str(response.data["detail"]["email"][0])
            == "Este correo electrónico ya está en uso."
        )
