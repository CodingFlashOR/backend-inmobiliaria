from apps.users.infrastructure.repositories import UserRepository
from apps.users.infrastructure.serializers import RealEstateEntitySerializer
from apps.users.applications import RegisterUser
from apps.utils.views import MethodHTTPMapped, PermissionMixin
from rest_framework.permissions import AllowAny
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import GenericAPIView
from rest_framework import status


class RealEstateEntityAPIView(
    MethodHTTPMapped, PermissionMixin, GenericAPIView
):
    """
    API view for managing operations for users with `real estate entity role`.

    It uses a mapping approach to determine the appropriate application logic,
    permissions, and serializers based on the HTTP method of the incoming request.
    """

    authentication_mapping = {"POST": []}
    permission_mapping = {"POST": [AllowAny]}
    application_mapping = {"POST": RegisterUser}
    serializer_mapping = {"POST": RealEstateEntitySerializer}

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Handle POST requests for real estate entity registration.

        This method allows you to register a new construction or real estate company
        while waiting for a POST request with the registration data. A successful
        registration will consist of saving the user's information in the database,
        configuring the permissions for their role and sending a message to the user's
        email with a link that will allow them to activate their account.
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
        register.real_estate_entity(
            data=serializer.validated_data, request=request
        )

        return Response(status=status.HTTP_201_CREATED)
