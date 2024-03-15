from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import generics, status

from typing import Dict, Any

from apps.users.infrastructure.serializers import RegisterSerializer
from apps.users.infrastructure.db import UserRepository
from apps.users.applications import Registration
from apps.users.schemas.register import ViewSchema


class RegisterAPIView(generics.GenericAPIView):
    """
    API View for registering a new user.

    This view handles the `POST` request to create a new user in the real estate
    management system.
    """

    authentication_classes = ()
    serializer_class = RegisterSerializer
    application_class = Registration

    def _handle_valid_request(self, data: Dict[str, Any]) -> Response:
        self.application_class(user_repository=UserRepository).create_user(
            data=data
        )

        return Response(status=status.HTTP_201_CREATED)

    def _handle_invalid_request(self, serializer: Serializer) -> Response:

        return Response(
            data={
                "code": "invalid_request_data",
                "detail": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
            content_type="application/json",
        )

    @ViewSchema
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Handle POST requests for user registration.

        This method allows the registration of a new user. It waits for a POST
        request with a user's registration data, validates the information, and then
        creates a new user if the data is valid or returns an error response if it is
        not.
        """

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return self._handle_valid_request(data=serializer.validated_data)

        return self._handle_invalid_request(serializer=serializer)
