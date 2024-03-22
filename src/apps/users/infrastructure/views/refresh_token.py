from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.serializers import Serializer
from rest_framework import status, generics

from typing import Dict, Any

from apps.users.infrastructure.serializers import RefreshTokenSerializer
from apps.users.infrastructure.db import JWTRepository, UserRepository
from apps.users.applications import RefreshTokens


class RefreshTokenAPIView(generics.GenericAPIView):

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

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return self._handle_valid_request(
                token_data=serializer.validated_data
            )

        return self._handle_invalid_request(serializer=serializer)
