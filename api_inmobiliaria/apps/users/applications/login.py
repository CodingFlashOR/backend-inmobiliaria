from apps.utils.messages import JWTErrorMessages
from apps.users.domain.constants import USER_ROLE_PERMISSIONS
from apps.users.models import User
from apps.api_exceptions import (
    PermissionDeniedAPIError,
    AuthenticationFailedAPIError,
)
from authentication.jwt import AccessToken, RefreshToken
from django.contrib.auth import authenticate
from typing import Dict


class JWTLogin:
    """
    This class encapsulates the use cases given to JSON Web Tokens in the system
    related to user authentication.
    """

    refresh_token_class = RefreshToken
    access_token_class = AccessToken

    @classmethod
    def authenticate_user(cls, credentials: Dict[str, str]) -> Dict[str, str]:
        """
        Authenticate a user with the given credentials and return access and refresh
        tokens.

        #### Parameters:
        - credentials: A dictionary containing the user's credentials.

        #### Raises:
        - AuthenticationFailedAPIError: If the credentials are invalid or the user is
        inactive.
        - PermissionDeniedAPIError: If the user does not have the required permissions.
        """

        user: User | None = authenticate(**credentials)

        if not user:
            raise AuthenticationFailedAPIError(
                detail=JWTErrorMessages.AUTHENTICATION_FAILED.value,
            )
        elif not user.is_active:
            raise AuthenticationFailedAPIError(
                detail=JWTErrorMessages.INACTIVE_ACCOUNT.value,
            )

        role_user = user.content_type.model

        if not user.has_perm(perm=USER_ROLE_PERMISSIONS[role_user]["jwt_auth"]):
            raise PermissionDeniedAPIError()

        refresh_token = cls.refresh_token_class(user=user)
        access_token = cls.access_token_class(
            user=user, refresh_token=refresh_token
        )

        return {
            "access_token": str(access_token),
            "refresh_token": str(refresh_token),
            "role_user": role_user,
        }
