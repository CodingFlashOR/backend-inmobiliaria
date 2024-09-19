from apps.users.constants import UserRoles
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.generics import GenericAPIView


class IsSearcher(BasePermission):
    """
    Permission class that checks if the user has the searcher role.
    """

    def has_permission(self, request: Request, view: GenericAPIView) -> bool:
        return request.user.content_type.model == UserRoles.SEARCHER.value
