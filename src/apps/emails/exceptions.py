from rest_framework.exceptions import APIException
from rest_framework import status
from apps.exceptions import DetailDictMixin
from typing import Any, Dict


class AccountActivationError(DetailDictMixin, APIException):
    """
    An exception that is raised when an error occurs during the account activation process.
    """

    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Error al activar la cuenta."
    default_code = "account_activation_error"

    def __init__(
        self, detail: str | Dict[str, Any] = None, code: str = None
    ) -> None:
        if isinstance(detail, dict):
            self.detail = {"detail": detail or self.default_detail}
        else:
            self.detail = detail or self.default_detail
        self.code = code or self.default_code
        super().__init__(detail=self.detail, code=self.code)


class SendingError(DetailDictMixin, APIException):
    """
    An exception that is raised when an error occurs during the process of sending
    an email.
    """

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = "Error al enviar el mensaje."
    default_code = "email_sending_error"

    def __init__(
        self, detail: str | Dict[str, Any] = None, code: str = None
    ) -> None:
        if isinstance(detail, dict):
            self.detail = {"detail": detail or self.default_detail}
        else:
            self.detail = detail or self.default_detail
        self.code = code or self.default_code
        super().__init__(detail=self.detail, code=self.code)
