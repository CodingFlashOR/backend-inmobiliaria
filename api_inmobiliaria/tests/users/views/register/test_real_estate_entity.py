from apps.users.constants import RealEstateEntityProperties
from apps.api_exceptions import DatabaseConnectionAPIError
from utils.messages import ERROR_MESSAGES
from tests.factory import UserFactory
from tests.utils import fake
from rest_framework import status
from django.test import Client
from django.urls import reverse
from django.db import OperationalError
from unittest.mock import Mock, patch
from typing import Dict
import pytest


MAXIMUM_PHONE_NUMBERS = RealEstateEntityProperties.MAXIMUM_PHONE_NUMBERS.value


@pytest.mark.django_db
class TestRegisterRealEstateEntityAPIView:
    """
    This class encapsulates the tests for the view responsible for creating a
    user with the "real estate entity" role.
    """

    path = reverse(viewname="real_estate_entity")
    user_factory = UserFactory
    client = Client()

    def test_if_valid_data(self, setup_database) -> None:
        """
        This test is responsible for validating the expected behavior of the
        view when the request data is valid.
        """

        # Creating the user data to be used in the test
        _, _, data = self.user_factory.real_estate_entity(save=False)
        data["confirm_password"] = data["password"]

        # Simulating the request
        response = self.client.post(
            path=self.path, data=data, content_type="application/json"
        )

        # Asserting that response data is correct
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.parametrize(
        argnames="data, messages_expected",
        argvalues=[
            (
                {},
                {
                    "type_entity": [ERROR_MESSAGES["required"]],
                    "logo": [ERROR_MESSAGES["required"]],
                    "name": [ERROR_MESSAGES["required"]],
                    "description": [ERROR_MESSAGES["required"]],
                    "nit": [ERROR_MESSAGES["required"]],
                    "phone_numbers": [ERROR_MESSAGES["required"]],
                    "department": [ERROR_MESSAGES["required"]],
                    "municipality": [ERROR_MESSAGES["required"]],
                    "region": [ERROR_MESSAGES["required"]],
                    "coordinate": [ERROR_MESSAGES["required"]],
                    "documents": [ERROR_MESSAGES["required"]],
                    "email": [ERROR_MESSAGES["required"]],
                    "password": [ERROR_MESSAGES["required"]],
                },
            ),
            (
                {"documents": {}, "phone_numbers": []},
                {
                    "type_entity": [ERROR_MESSAGES["required"]],
                    "logo": [ERROR_MESSAGES["required"]],
                    "name": [ERROR_MESSAGES["required"]],
                    "description": [ERROR_MESSAGES["required"]],
                    "nit": [ERROR_MESSAGES["required"]],
                    "phone_numbers": [ERROR_MESSAGES["empty"]],
                    "department": [ERROR_MESSAGES["required"]],
                    "municipality": [ERROR_MESSAGES["required"]],
                    "region": [ERROR_MESSAGES["required"]],
                    "coordinate": [ERROR_MESSAGES["required"]],
                    "documents": [ERROR_MESSAGES["empty"]],
                    "email": [ERROR_MESSAGES["required"]],
                    "password": [ERROR_MESSAGES["required"]],
                },
            ),
            (
                {
                    "email": "useremail.com",
                    "type_entity": "Otra entidad",
                    "name": "Entity123",
                    "nit": "abcdefghij",
                    "phone_numbers": ["3111111111"],
                },
                {
                    "password": [ERROR_MESSAGES["required"]],
                    "logo": [ERROR_MESSAGES["required"]],
                    "description": [ERROR_MESSAGES["required"]],
                    "department": [ERROR_MESSAGES["required"]],
                    "municipality": [ERROR_MESSAGES["required"]],
                    "region": [ERROR_MESSAGES["required"]],
                    "coordinate": [ERROR_MESSAGES["required"]],
                    "email": [ERROR_MESSAGES["invalid"]],
                    "name": [ERROR_MESSAGES["invalid"]],
                    "nit": [ERROR_MESSAGES["invalid"]],
                    "phone_numbers": {"0": [ERROR_MESSAGES["invalid"]]},
                    "type_entity": [
                        ERROR_MESSAGES["invalid_choice"].format(
                            input="Otra entidad"
                        ),
                    ],
                },
            ),
            (
                {
                    "type_entity": "realestate",
                    "documents": {"other doc": fake.url()},
                },
                {
                    "logo": [ERROR_MESSAGES["required"]],
                    "name": [ERROR_MESSAGES["required"]],
                    "description": [ERROR_MESSAGES["required"]],
                    "nit": [ERROR_MESSAGES["required"]],
                    "phone_numbers": [ERROR_MESSAGES["required"]],
                    "department": [ERROR_MESSAGES["required"]],
                    "municipality": [ERROR_MESSAGES["required"]],
                    "region": [ERROR_MESSAGES["required"]],
                    "coordinate": [ERROR_MESSAGES["required"]],
                    "email": [ERROR_MESSAGES["required"]],
                    "password": [ERROR_MESSAGES["required"]],
                    "documents": [
                        ERROR_MESSAGES["document_invalid"].format(
                            doc_name="other doc"
                        )
                    ],
                },
            ),
            (
                {
                    "phone_numbers": [
                        "+573111111111",
                        "+573111111112",
                        "+573111111113",
                        "+573111111114",
                        "+573111111115",
                        "+573111111116",
                    ]
                },
                {
                    "type_entity": [ERROR_MESSAGES["required"]],
                    "logo": [ERROR_MESSAGES["required"]],
                    "name": [ERROR_MESSAGES["required"]],
                    "description": [ERROR_MESSAGES["required"]],
                    "nit": [ERROR_MESSAGES["required"]],
                    "department": [ERROR_MESSAGES["required"]],
                    "municipality": [ERROR_MESSAGES["required"]],
                    "region": [ERROR_MESSAGES["required"]],
                    "coordinate": [ERROR_MESSAGES["required"]],
                    "documents": [ERROR_MESSAGES["required"]],
                    "email": [ERROR_MESSAGES["required"]],
                    "password": [ERROR_MESSAGES["required"]],
                    "phone_numbers": [
                        ERROR_MESSAGES["max_length_list"].format(
                            max_length=MAXIMUM_PHONE_NUMBERS
                        )
                    ],
                },
            ),
        ],
        ids=[
            "empty_data",
            "empty_data_nested_fields",
            "invalid_data",
            "invalid_documents",
            "max_length_phone_numbers",
        ],
    )
    def test_if_invalid_data(
        self,
        data: Dict[str, Dict],
        messages_expected: Dict[str, Dict],
    ) -> None:
        """
        This test is responsible for validating the expected behavior of the
        view when the request data is invalid and does not exist in the database.
        """

        # Simulating the request
        response = self.client.post(
            path=self.path, data=data, content_type="application/json"
        )

        # Asserting that response data is correct
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["code"] == "invalid_request_data"

        errors_formatted = {}

        for field, errors in response.data["detail"].items():
            if isinstance(errors, dict):
                for field_nested, errors_nested in errors.items():
                    errors_formatted[field] = {}
                    errors_formatted[field][str(field_nested)] = [
                        str(error) for error in errors_nested
                    ]
            else:
                errors_formatted[field] = [str(error) for error in errors]

        for field, message in messages_expected.items():
            if isinstance(message, dict):
                for field_nested, message_nested in message.items():
                    assert errors_formatted[field][field_nested] == message_nested
            else:
                assert errors_formatted[field] == message

    def test_data_used(self) -> None:
        """
        This test is responsible for validating the expected behavior of the
        view when the request data is invalid and exists in the database.
        """

        # Creating the user
        _, _, data = self.user_factory.real_estate_entity(
            active=False, save=True, add_perm=False
        )
        messages_expected = {
            "name": [ERROR_MESSAGES["name_in_use"]],
            "nit": [ERROR_MESSAGES["nit_in_use"]],
            "phone_numbers": [
                ERROR_MESSAGES["phone_numbers_in_use"].format(
                    phone_number=data["phone_numbers"][0]
                ),
                ERROR_MESSAGES["phone_numbers_in_use"].format(
                    phone_number=data["phone_numbers"][1]
                ),
            ],
            "coordinate": [ERROR_MESSAGES["coordinate_in_use"]],
        }

        # Simulating the request
        response = self.client.post(
            path=self.path, data=data, content_type="application/json"
        )

        # Asserting that response data is correct
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["code"] == "invalid_request_data"

        errors_formatted = {
            field: [str(error) for error in errors]
            for field, errors in response.data["detail"].items()
        }

        for field, message in messages_expected.items():
            assert errors_formatted[field] == message

    @patch(target="apps.users.applications.register.Group")
    def test_if_conection_db_failed(self, model_group_mock: Mock) -> None:
        """
        This test is responsible for validating the expected behavior of the
        view when a DatabaseConnectionAPIError exception is raised.
        """

        # Mocking the methods
        get: Mock = model_group_mock.objects.get
        get.side_effect = OperationalError

        # Creating the user data to be used in the test
        _, _, data = self.user_factory.real_estate_entity(save=False)
        data["confirm_password"] = data["password"]

        # Simulating the request
        response = self.client.post(
            path=self.path, data=data, content_type="application/json"
        )

        # Asserting that response data is correct
        status_code_expected = DatabaseConnectionAPIError.status_code
        response_code_expected = DatabaseConnectionAPIError.default_code
        response_data_expected = DatabaseConnectionAPIError.default_detail

        assert response.status_code == status_code_expected
        assert response.data["code"] == response_code_expected
        assert response.data["detail"] == response_data_expected
