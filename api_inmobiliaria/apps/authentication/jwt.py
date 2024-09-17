from apps.users.infrastructure.repositories import UserRepository
from apps.users.models import BaseUser
from apps.authentication.infrastructure.repositories import JWTRepository
from apps.authentication.constants import ACCESS_TOKEN_LIFETIME
from apps.authentication.typing import JWTPayload
from apps.utils.messages import JWTErrorMessages
from apps.api_exceptions import (
    AuthenticationFailedAPIError,
    ResourceNotFoundAPIError,
    JWTAPIError,
)
from rest_framework_simplejwt.tokens import Token as BaseToken
from rest_framework_simplejwt.authentication import (
    JWTAuthentication as BaseJWTuthentication,
)
from rest_framework_simplejwt.utils import get_md5_hash_password, aware_utcnow
from rest_framework_simplejwt.exceptions import TokenError, TokenBackendError
from rest_framework_simplejwt.settings import api_settings
from typing import Any, Dict


class Token(BaseToken):
    """
    A class which validates and wraps an existing JWT or can be used to build a new
    JWT.
    """

    _jwt_repository = JWTRepository

    def __init__(
        self,
        token: str = None,
        payload: JWTPayload = None,
        verify: bool = True,
        user: BaseUser = None,
    ) -> None:
        """
        !!!! IMPORTANT !!!! MUST raise a TokenError with a user-facing error
        message if the given token is invalid, expired, or otherwise not safe
        to use.
        """

        self.user = user
        self.payload = payload

        if self.token_type is None or self.lifetime is None:
            raise TokenError("Cannot create token with no type or lifetime")

        self.token = token
        self.current_time = aware_utcnow()

        # Set up token
        if not token and not payload:
            # New token.  Skip all the verification steps.
            self.payload = {api_settings.TOKEN_TYPE_CLAIM: self.token_type}

            # Set "exp" and "iat" claims with default value
            self.set_exp(from_time=self.current_time, lifetime=self.lifetime)
            self.set_iat(at_time=self.current_time)

            # Set "jti" claim
            self.set_jti()

        try:
            if not self.payload:
                # An encoded token was provided
                token_backend = self.get_token_backend()
                self.payload = token_backend.decode(token=token, verify=verify)
        except TokenBackendError:
            message = JWTErrorMessages.INVALID_OR_EXPIRED.value

            raise TokenError(message.format(token_type=self.token_type))

        if verify:
            self.verify()

    def save(self) -> None:
        """
        Saves the token to the outstanding token list.
        """

        self._jwt_repository.add_checklist(
            token=str(self), payload=self.payload, user=self.user
        )


class BlacklistMixin:
    """
    A mixin that provides blacklist functionality for a token.
    """

    payload: Dict[str, Any]
    token_type: str
    _jwt_repository: JWTRepository

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if not Token in cls.__bases__:
            raise TypeError(
                f"The {cls.__name__} class must inherit from Token. Make sure your view definition includes Token as a base class when using the BlacklistMixin class."
            )

    def check_blacklist(self) -> None:
        """
        Checks if this token is present in the token blacklist.
        """

        jti = self.payload[api_settings.JTI_CLAIM]

        if self._jwt_repository.exists_in_blacklist(jti=jti):
            message = JWTErrorMessages.BLACKLISTED.value

            raise TokenError(message.format(token_type=self.token_type))

    def blacklist(self) -> None:
        """
        Ensures this token is included in the outstanding token list and adds it to
        the blacklist.
        """

        jti = self.payload[api_settings.JTI_CLAIM]

        # Ensure outstanding token exists with given jti
        token = self._jwt_repository.get(jti=jti)

        if not token:
            message = JWTErrorMessages.TOKEN_NOT_FOUND.value

            raise ResourceNotFoundAPIError(
                code=message["code"],
                detail=message["detail"].format(token_type=self.token_type),
            )

        self._jwt_repository.add_blacklist(token=token)


class AccessToken(Token, BlacklistMixin):
    """
    AccessToken is a class that extends the base access token class to include
    blacklist functionality.
    """

    token_type = "access"
    lifetime = ACCESS_TOKEN_LIFETIME

    def __init__(
        self,
        user: BaseUser = None,
        token: Token = None,
        payload: JWTPayload = None,
        verify: bool = True,
    ) -> None:
        super().__init__(token=token, payload=payload, verify=verify, user=user)

        if not self.token and self.user:
            # Set the user_id and role claims
            user_id = getattr(self.user, api_settings.USER_ID_FIELD)

            if not isinstance(user_id, int):
                user_id = str(user_id)

            self[api_settings.USER_ID_CLAIM] = user_id
            self["user_role"] = self.user.content_type.model

            self.save()

    def verify(self, *args, **kwargs) -> None:
        self.check_blacklist()

        super().verify(*args, **kwargs)


class JWTAuthentication(BaseJWTuthentication):
    """
    JWTAuthentication is a class that handles JSON web token authentication.
    """

    _user_repository = UserRepository

    def get_validated_token(self, raw_token: bytes) -> Token:
        """
        Validates an encoded JSON web token and returns a validated token wrapper
        object.
        """

        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthToken(token=raw_token)
            except TokenError as e:
                raise JWTAPIError(detail=e.args[0])

    def get_user(self, validated_token: Token) -> BaseUser:
        """
        Attempts to find and return a user using the given validated token.
        """

        try:
            user_uuid = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise JWTAPIError(
                detail="Token contained no recognizable user identification"
            )

        base_user = self._user_repository.get_base_data(
            uuid=user_uuid, is_active=True
        )

        if not base_user:
            message = JWTErrorMessages.USER_NOT_FOUND.value

            raise ResourceNotFoundAPIError(
                code=message["code"], detail=message["detail"]
            )

        if not base_user.is_active:
            raise AuthenticationFailedAPIError(
                detail=JWTErrorMessages.INACTIVE_ACCOUNT.value
            )

        if api_settings.CHECK_REVOKE_TOKEN:
            if validated_token.get(
                api_settings.REVOKE_TOKEN_CLAIM
            ) != get_md5_hash_password(base_user.password):
                raise AuthenticationFailedAPIError(
                    detail="The user's password has been changed.",
                )

        return base_user
