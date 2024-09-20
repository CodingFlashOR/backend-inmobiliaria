from apps.users.infrastructure.repositories import UserRepository
from apps.users.infrastructure.serializers import (
    RegisterSearcherSerializer,
    SearcherReadOnlySerializer,
    SearcherSerializer,
)
from apps.users.infrastructure.schemas import (
    POSTSearcherSchema,
    GETSearcherSchema,
    PATCHearcherSchema,
)
from apps.users.applications import RegisterUser, UserDataManager
from apps.users.permissions import IsSearcher
from apps.authentication.jwt import JWTAuthentication
from apps.utils.views import MethodHTTPMapped, PermissionMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import GenericAPIView
from rest_framework import status


class SearcherAPIView(MethodHTTPMapped, PermissionMixin, GenericAPIView):
    """
    API view for managing operations for users with `searcher role`.

    It uses a mapping approach to determine the appropriate application logic,
    permissions, and serializers based on the HTTP method of the incoming request.
    """

    authentication_mapping = {
        "POST": [],
        "GET": [JWTAuthentication],
        "PATCH": [JWTAuthentication],
    }
    permission_mapping = {
        "POST": [AllowAny],
        "GET": [IsAuthenticated, IsSearcher],
        "PATCH": [IsAuthenticated, IsSearcher],
    }
    application_mapping = {
        "POST": RegisterUser,
        "GET": UserDataManager,
        "PATCH": UserDataManager,
    }
    serializer_mapping = {
        "POST": RegisterSearcherSerializer,
        "GET": SearcherReadOnlySerializer,
        "PATCH": SearcherSerializer,
    }

    @GETSearcherSchema
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Handle GET requests to obtain user information.

        This method returns the user account information associated with the request's
        access token, without revealing sensitive data, provided the user has
        permission to read their own information.
        """

        data_manager: UserDataManager = self.get_application_class(
            user_repository=UserRepository
        )
        user_role = data_manager.get(base_user=request.user)

        serializer_class = self.get_serializer_class()
        serializer: Serializer = serializer_class(
            instance=request.user, role_instance=user_role
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
            content_type="application/json",
        )

    @POSTSearcherSchema
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Handle POST requests for searcher user registration.

        This method allows you to register a new search user, waiting for a POST
        request with the registration data. A successful registration will consist of
        saving the user's information in the database, configuring the permissions for
        their role, and sending a message to the user's email with a link that will
        allow them to activate their account.
        """

        serializer_class = self.get_serializer_class()
        serializer: Serializer = serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(
                data={
                    "code": "invalid_request_data",
                    "detail": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
                content_type="application/json",
            )

        register: RegisterUser = self.get_application_class(
            user_repository=UserRepository
        )
        del serializer.validated_data["confirm_password"]
        register.searcher(data=serializer.validated_data, request=request)

        return Response(status=status.HTTP_201_CREATED)

    @PATCHearcherSchema
    def patch(self, request: Request, *args, **kwargs) -> Response:
        """
        Handle PATCH requests to update searcher user information.

        This method allows the user to update their own information, waiting for a
        PATCH request with the updated data. A successful update will consist of
        updating the user's information in the database and returning the updated
        information, provided the user has permission to update their own information.
        """

        serializer_class = self.get_serializer_class()
        serializer: Serializer = serializer_class(
            data=request.data, partial=True
        )

        if not serializer.is_valid():
            return Response(
                data={
                    "code": "invalid_request_data",
                    "detail": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
                content_type="application/json",
            )

        data_manager: UserDataManager = self.get_application_class(
            user_repository=UserRepository
        )
        searcher = data_manager.update(
            data=serializer.validated_data, base_user=request.user
        )
        data = SearcherReadOnlySerializer(
            instance=request.user, role_instance=searcher
        ).data

        return Response(
            data=data,
            status=status.HTTP_200_OK,
            content_type="application/json",
        )
