from rest_framework.serializers import Serializer
from rest_framework.request import Request
from rest_framework import generics, permissions
from apps.exceptions import NotAuthenticated, PermissionDenied
from typing import List, Callable


class MappedAPIView(generics.GenericAPIView):
    """
    A base view class that maps HTTP methods to specific application classes,
    authentication classes, permission classes, and serializers.

    The mappings allow different behavior for different HTTP methods in the same view.
    For example, you might want to use different serializers for GET and POST requests,
    or apply different permissions for different methods.
    """

    application_class = None
    application_mapping = {}
    authentication_mapping = {}
    permission_mapping = {}
    serializer_mapping = {}

    def get_authenticators(self):
        try:
            authentication_classes = self.authentication_mapping[
                self.request.method
            ]
        except AttributeError:
            authentication_classes = []

        return [auth() for auth in authentication_classes]

    def get_permissions(self) -> List[permissions.BasePermission]:
        permission_classes = self.permission_mapping[self.request.method]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self) -> Serializer:

        return self.serializer_mapping[self.request.method]

    def get_application_class(self) -> Callable:

        return self.application_mapping[self.request.method]

    def permission_denied(
        self, request: Request, message=None, code=None
    ) -> None:
        if request.authenticators and not request.successful_authenticator:
            raise NotAuthenticated(code=code, detail=message)
        raise PermissionDenied(code=code, detail=message)

    def check_permissions(self, request: Request) -> None:
        """
        Check if the request should be permitted.
        Raises an appropriate exception if the request is not permitted.
        """

        for permission in self.get_permissions():
            if not permission.has_permission(request=request, view=self):
                self.permission_denied(
                    request=request,
                    message=getattr(permission, "message", None),
                    code=getattr(permission, "code", None),
                )
