from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.serializers import Serializer
from rest_framework import status, generics

from typing import Dict, Any

from apps.users.infrastructure.serializers import RefreshTokenSerializer
from apps.users.infrastructure.db import JWTRepository, UserRepository
from apps.users.applications import RefreshTokens
from apps.users.schemas.refresh_tokens import ViewSchema


class RefreshTokenAPIView(generics.GenericAPIView):
    """
    API View for refreshing user tokens.

    This view handles the `POST` request to refresh a user's access and refresh tokens
    in the system.
    """

    authentication_classes = ()
    serializer_class = RefreshTokenSerializer
    application_class = RefreshTokens

    def _handle_valid_request(self, token_data: Dict[str, Any]) -> Response:

        tokens = self.application_class(
            jwt_class=TokenObtainPairSerializer,
            jwt_repository=JWTRepository,
            user_repository=UserRepository,
        ).refresh_tokens(
            access_data=token_data["access"],
            refresh_data=token_data["refresh"],
        )

        return Response(
            data=tokens,
            status=status.HTTP_200_OK,
            content_type="application/json",
        )

    def _handle_invalid_request(self, serializer: Serializer) -> Response:

        return Response(
            data={
                "code": "jwt_error",
                "detail": serializer.errors,
            },
            status=status.HTTP_401_UNAUTHORIZED,
            content_type="application/json",
        )

    @ViewSchema
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Handle POST requests for token refresh.

        This method allows refreshing of a user's tokens. It waits for a POST request
        with the access and refresh tokens, validates the information, and then
        returns a response with the new tokens if the data is valid or returns an
        error response if it is not.
        """

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return self._handle_valid_request(
                token_data=serializer.validated_data
            )

        return self._handle_invalid_request(serializer=serializer)
