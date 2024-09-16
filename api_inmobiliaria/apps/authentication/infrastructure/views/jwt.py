from apps.authentication.infrastructure.repositories import JWTRepository
from apps.authentication.infrastructure.serializers import (
    UpdateTokenSerializer,
    LoginSerializer,
)
from apps.authentication.infrastructure.schemas.jwt import (
    UpdateTokenSchema,
    LoginSchema,
    LogoutSchema,
)
from apps.authentication.applications import JWTLogout, JWTLogin, JWTUpdate
from apps.authentication.jwt import JWTAuthentication
from apps.users.infrastructure.repositories import UserRepository
from apps.utils.views import PermissionMixin
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status


class LoginAPIView(TokenObtainPairView):
    """
    API View for user authentication.

    This view handles the `POST` request to authenticate a user in the real estate
    management system.
    """

    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    application_class = JWTLogin

    @LoginSchema
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Handle POST requests for user authentication.

        This method allows for the authentication of a user, it expects a POST request
        with their credentials. Successful authentication will result in the creation
        of the user access token if their credentials are valid, their account is
        active, and they have the necessary permissions to perform this action.
        """

        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(
                data={
                    "code": "invalid_request_data",
                    "detail": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
                content_type="application/json",
            )

        access_token = self.application_class.authenticate_user(
            credentials=serializer.validated_data
        )

        return Response(
            data={"access_token": access_token},
            status=status.HTTP_200_OK,
            content_type="application/json",
        )


class UpdateTokenAPIView(GenericAPIView):
    """
    API View for refreshing user tokens. This view handles the request to
    refresh a user access token in the system.
    """

    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = UpdateTokenSerializer
    application_class = JWTUpdate

    @UpdateTokenSchema
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Handle POST requests for token refresh.

        This method allows updating the JSON Web Tokens of an authenticated user,
        waiting for a POST request with the access and update tokens. A successful
        refresh will consist of creating new access token to keep the user authenticated and
        invalidating the previous refresh token by adding it to the blacklist.
        """

        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(
                data={
                    "code": "invalid_request_data",
                    "detail": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
                content_type="application/json",
            )

        app = self.application_class(
            jwt_repository=JWTRepository,
            user_repository=UserRepository,
        )
        new_access_token = app.new_tokens(
            access_token=serializer.validated_data["access_token"]
        )

        return Response(
            data={"access_token": new_access_token},
            status=status.HTTP_200_OK,
            content_type="application/json",
        )


class LogoutAPIView(PermissionMixin, GenericAPIView):
    """
    API View for user logout. This view handles the request to logout a user
    from the system.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    application_class = JWTLogout

    @LogoutSchema
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Handles POST requests for user logout.

        This method allows to logout an authenticated user. Wait for a POST request
        with the update token. A successful logout will consist of invalidating the
        access token by adding them to the blacklist.
        """

        self.application_class.logout_user(access_token=request.auth)

        return Response(
            status=status.HTTP_200_OK,
            content_type="application/json",
        )
