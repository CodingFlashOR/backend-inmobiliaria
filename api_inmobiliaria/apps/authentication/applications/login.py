from apps.authentication.typing import JSONWebToken
from apps.authentication.jwt import AccessToken
from apps.users.constants import USER_ROLE_PERMISSIONS
from apps.users.models import BaseUser
from apps.api_exceptions import (
    PermissionDeniedAPIError,
    AuthenticationFailedAPIError,
)
from utils.messages import JWTErrorMessages
from django.contrib.auth import authenticate
from typing import Dict


class JWTLogin:
    """
    Use case for login in with JSON Web Token.
    """

    _access_token_class = AccessToken

    @classmethod
    def authenticate_user(cls, credentials: Dict[str, str]) -> JSONWebToken:
        """
        Authenticate a user with the given credentials and return access token.

        #### Parameters:
        - credentials: A dictionary containing the user's credentials.

        #### Raises:
        - AuthenticationFailedAPIError: If the credentials are invalid or the user is
        inactive.
        - PermissionDeniedAPIError: If the user does not have the required permissions.
        """

        base_user: BaseUser | None = authenticate(**credentials)

        if not base_user:
            raise AuthenticationFailedAPIError(
                detail=JWTErrorMessages.AUTHENTICATION_FAILED.value,
            )
        elif not base_user.is_active:
            raise AuthenticationFailedAPIError(
                detail=JWTErrorMessages.INACTIVE_ACCOUNT.value,
            )

        user_role = base_user.content_type.model

        if not base_user.has_perm(
            perm=USER_ROLE_PERMISSIONS[user_role]["model_level"]["jwt_auth"]
        ):
            raise PermissionDeniedAPIError()

        return str(cls._access_token_class(user=base_user))
