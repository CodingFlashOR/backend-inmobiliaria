from apps.users.constants import UserRoles
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.generics import GenericAPIView


# User roles
REAL_ESTATE_ENTITY = UserRoles.REAL_ESTATE_ENTITY.value
SEARCHER = UserRoles.SEARCHER.value


class IsSearcher(BasePermission):
    """
    Permission class that checks if the user has the searcher role.
    """

    def has_permission(self, request: Request, view: GenericAPIView) -> bool:
        return request.user.content_type.model == SEARCHER


class IsRealEstateEntity(BasePermission):
    """
    Permission class that checks if the user has the real estate entity role.
    """

    def has_permission(self, request: Request, view: GenericAPIView) -> bool:
        return request.user.content_type.model == REAL_ESTATE_ENTITY
