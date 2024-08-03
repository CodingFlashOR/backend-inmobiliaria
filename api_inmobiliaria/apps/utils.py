from apps.users.domain.typing import JSONWebToken, JWTPayload
from apps.constants import ERROR_MESSAGES
from settings.environments.base import SIMPLE_JWT
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework import serializers
from jwt import decode
from typing import Dict, Any


class ErrorMessagesSerializer(serializers.Serializer):
    """
    A serializer class that provides custom error messages for fields.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customized error messages
        msg = {
            "invalid": ERROR_MESSAGES["invalid"],
            "required": ERROR_MESSAGES["required"],
            "blank": ERROR_MESSAGES["blank"],
            "null": ERROR_MESSAGES["null"],
        }
        fields = list(self.fields.keys())
        for field_name in fields:
            self.fields[field_name].error_messages.update(msg)


def api_exception_handler(
    exc: APIException, context: Dict[str, Any]
) -> Response:
    """
    Custom exception handler that handles `TokenPermissionDenied` exception.

    Args:
    - exc (Exception) : The exception instance to be handled.
    - context (dict) : A dictionary containing the request object.
    """

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    if not isinstance(exc, APIException):
        raise exc
    response = exception_handler(exc, context)
    response.status_code = exc.status_code
    try:
        response.data["code"] = exc.detail["code"]
        response.data["detail"] = exc.detail["detail"]
    except TypeError:
        response.data["code"] = getattr(exc, "code", exc.default_code)
        response.data["detail"] = getattr(exc, "detail", exc.default_detail)

    return response


def decode_jwt(
    token: JSONWebToken, options: Dict[str, bool] = None
) -> JWTPayload:
    """
    Returns the token payload.
    """

    return decode(
        jwt=token,
        key=SIMPLE_JWT["SIGNING_KEY"],
        algorithms=[SIMPLE_JWT["ALGORITHM"]],
        options=options,
    )
