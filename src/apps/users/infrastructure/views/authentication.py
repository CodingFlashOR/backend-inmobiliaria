from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from apps.users.infrastructure.serializers import AuthenticationSerializer
from apps.users.infrastructure.db import JWTRepository
from apps.users.applications import JWTUsesCases
from typing import Dict, Any, List


class AuthenticationAPIView(TokenObtainPairView):
    """
    API View for user authentication.

    This view handles the `POST` request to authenticate a user in the real estate
    management system.
    """

    authentication_classes = []
    permission_classes = []
    application_class = JWTUsesCases

    def _handle_valid_request(self, data: Dict[str, Any]) -> Response:
        tokens = self.application_class(
            jwt_class=self.get_serializer_class(),
            jwt_repository=JWTRepository,
        ).authenticate_user(credentials=data)

        return Response(
            data=tokens,
            status=status.HTTP_200_OK,
            content_type="application/json",
        )

    @staticmethod
    def _handle_invalid_request(errors: List[Dict[str, List]]) -> Response:

        return Response(
            data={
                "code": "invalid_request_data",
                "detail": errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
            content_type="application/json",
        )

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Handle POST requests for user authentication.

        This method allows authentication of a user. It waits for a POST request with
        your credentials, validates the information, and then returns a response with
        the authentication tokens if the data is valid or returns an error response
        if it is not.
        """

        serializer = AuthenticationSerializer(data=request.data)
        if serializer.is_valid():
            return self._handle_valid_request(data=serializer.validated_data)

        return self._handle_invalid_request(errors=serializer.errors)
