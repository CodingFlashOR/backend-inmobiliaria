from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, exceptions
from apps.users.infrastructure.serializers import SearcherUserSerializer
from apps.users.infrastructure.db import UserRepository
from apps.users.infrastructure.views.base import MappedAPIView
from apps.users.applications import SearcherUserUsesCases
from apps.exceptions import NotAuthenticated
from typing import Dict, Any, List


class SearcherUserAPIView(MappedAPIView):
    """
    API view for managing operations for users with `searcheruser roles`.

    It uses a mapping approach to determine the appropriate application logic,
    permissions, and serializers based on the HTTP method of the incoming request.
    """

    application_class = SearcherUserUsesCases(user_repository=UserRepository)
    application_mapping = {
        "POST": application_class.create_user,
    }
    authentication_mapping = {
        "POST": [],
    }
    permission_mapping = {
        "POST": [],
    }
    serializer_mapping = {
        "POST": SearcherUserSerializer,
    }

    def permission_denied(self, request: Request, message=None, code=None):
        if request.authenticators and not request.successful_authenticator:
            raise NotAuthenticated(code=code, detail=message)
        raise exceptions.PermissionDenied(code=code, detail=message)

    def _handle_valid_request(self, data: Dict[str, Any]) -> Response:
        application = self.get_application_class()
        application(data=data)

        return Response(status=status.HTTP_201_CREATED)

    @staticmethod
    def _handle_invalid_request(errors: List[Dict[str, Any]]) -> Response:

        return Response(
            data={
                "code": "invalid_request_data",
                "detail": errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
            content_type="application/json",
        )

    # @ShelterPostSchema
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Handle POST requests for searcheruser registration.

        This method allows the registration of a new searcheruser. It waits for a POST
        request with record data, validates the information, and then creates a new
        record if the data is valid or returns an error response if it is not.
        """

        serializer_class = self.get_serializer_class()
        serializer: Serializer = serializer_class(data=request.data)

        if serializer.is_valid():
            return self._handle_valid_request(data=serializer.validated_data)

        return self._handle_invalid_request(errors=serializer.errors)
