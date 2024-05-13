from rest_framework.serializers import Serializer
from rest_framework import generics
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

    def get_permissions(self) -> List:
        permission_classes = self.permission_mapping[self.request.method]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self) -> Serializer:
        serializer = self.serializer_mapping[self.request.method]

        return serializer

    def get_application_class(self) -> Callable:
        application_class = self.application_mapping[self.request.method]

        return application_class
