from apps.api_exceptions import APIException
from apps.view_exceptions import ViewException
from rest_framework.response import Response
from rest_framework.views import set_rollback
from rest_framework.exceptions import NotFound
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import Http404
from typing import Dict, Any


def api_view_exception_handler(
    exc: Exception, context: Dict[str, Any]
) -> Response:
    """
    Custom exception handler to return a response with a detailed error message.

    Args:
    - exc: The exception instance to be handled.
    - context: A dictionary containing the request object.
    """

    if isinstance(exc, Http404):
        exc = NotFound(*(exc.args))
    elif isinstance(exc, APIException):
        headers = {}

        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header
        elif getattr(exc, "wait", None):
            headers["Retry-After"] = "%d" % exc.wait

        data = {"detail": exc.detail}
        data["code"] = exc.code
        set_rollback()

        return Response(data, status=exc.status_code, headers=headers)

    return None


def view_exception_handler(view_func) -> HttpResponse:
    """
    Decorator to handle exceptions raised in views.
    """

    def _wrapped_view_func(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Wrapper function to handle exceptions raised in views.
        """

        try:
            return view_func(request, *args, **kwargs)
        except Exception as exc:
            if not isinstance(exc, ViewException):
                raise exc

            return render(
                request=exc.request,
                template_name=exc.template_name,
                context=exc.context,
                status=exc.status_code,
            )

    return _wrapped_view_func
