from rest_framework.exceptions import APIException
from rest_framework import status

from typing import Any, Dict, Optional, Union


class DetailDictMixin:
    """
    A mixin class that provides a method to build a detailed dictionary for the error.
    """

    default_detail: str
    default_code: str

    def __init__(
        self,
        detail: Union[Dict[str, Any], str, None] = None,
        code: Optional[str] = None,
    ) -> None:
        """
        Builds a detail dictionary for the error to give more information to API
        users.
        """

        detail_dict = {
            "detail": self.default_detail,
            "code": self.default_code,
        }
        if isinstance(detail, dict):
            detail_dict.update(detail)
        elif detail is not None:
            detail_dict["detail"] = detail
        if code is not None:
            detail_dict["code"] = code
        super().__init__(detail_dict)  # type: ignore


class DatabaseConnectionError(DetailDictMixin, APIException):
    """
    Exception raised when a connection to the database cannot be established.
    """

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Unable to establish a connection with the database. Please try again later."
    default_code = "database_connection_error"

    def __init__(self, detail: str | Dict[str, Any] = None) -> None:
        if isinstance(detail, dict):
            self.detail = {"detail": detail or self.default_detail}
        else:
            self.detail = detail or self.default_detail
        self.code = self.default_code
        super().__init__(detail=self.detail, code=self.code)


class UserNotFoundError(DetailDictMixin, APIException):
    """
    Exception raised when a user is not found.
    """

    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "User not found."
    default_code = "user_not_found"

    def __init__(self, detail: str | Dict[str, Any] = None) -> None:
        if isinstance(detail, dict):
            self.detail = {"detail": detail or self.default_detail}
        else:
            self.detail = detail or self.default_detail
        self.code = self.default_code
        super().__init__(detail=self.detail, code=self.code)


class UserInactiveError(DetailDictMixin, APIException):
    """
    Exception raised when a user is inactive.
    """

    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "User is inactive."
    default_code = "user_inactive"

    def __init__(
        self, detail: str | Dict[str, Any] = None, code: str = None
    ) -> None:
        if isinstance(detail, dict):
            self.detail = {"detail": detail or self.default_detail}
        else:
            self.detail = detail or self.default_detail
        self.code = code or self.default_code
        super().__init__(detail=self.detail, code=self.code)


class JWTNotFoundError(DetailDictMixin, APIException):
    """
    Exception raised when a token is not found.
    """

    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Token not found."
    default_code = "token_not_found"

    def __init__(self, detail: str | Dict[str, Any] = None, code: str = None):
        if isinstance(detail, dict):
            self.detail = {"detail": detail or self.default_detail}
        else:
            self.detail = detail or self.default_detail
        self.code = code or self.default_code
        super().__init__(detail=self.detail, code=self.code)


class JWTError(DetailDictMixin, APIException):
    """
    Exception raised when a token error occurs.
    """

    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Token error."
    default_code = "token_error"

    def __init__(self, detail: str | Dict[str, Any] = None, code: str = None):
        if isinstance(detail, dict):
            self.detail = {"detail": detail or self.default_detail}
        else:
            self.detail = detail or self.default_detail
        self.code = code or self.default_code
        super().__init__(detail=self.detail, code=self.code)


class NotAuthenticated(APIException, DetailDictMixin):
    """
    Exception raised when the user is not authenticated.
    """

    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Authentication credentials were not provided."
    default_code = "authentication_failed"

    def __init__(
        self, detail: str | Dict[str, Any] = None, code: str = None
    ) -> None:
        if isinstance(detail, dict):
            self.detail = {"detail": detail or self.default_detail}
        else:
            self.detail = detail or self.default_detail
        self.code = code or self.default_code
        super().__init__(detail=self.detail, code=self.code)
