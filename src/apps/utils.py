from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException

from typing import Dict, Any


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
