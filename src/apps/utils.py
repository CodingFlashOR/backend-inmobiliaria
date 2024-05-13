from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework import serializers
from typing import Dict, Any


ERROR_MESSAGES = {
    # Length errors
    "max_length": "El valor ingresado no puede tener más de {max_length} caracteres.",
    "min_length": "El valor ingresado debe tener al menos {min_length} caracteres.",
    # Password errors
    "password_mismatch": "Las contraseñas no coinciden.",
    "password_common": "Esta contraseña es demasiado común.",
    "password_no_upper_lower": "La contraseña debe contener al menos una mayuscula o una minuscula.",
    # Invalid data
    "invalid": "El valor ingresado es inválido.",
    "invalid_choice": "{input} no es una elección válida.",
    # Data in use
    "email_in_use": "Este correo electrónico ya está en uso.",
    "name_in_use": "Este nombre ya está en uso.",
    "phone_in_use": "Este número de teléfono ya está en uso.",
    "address_in_use": "Esta dirección ya está en uso.",
}


class ErrorMessagesSerializer(serializers.Serializer):
    """
    A serializer class that provides custom error messages for fields.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customized error messages
        msg = {
            "invalid": "El valor ingresado es inválido.",
            "required": "Este campo es requerido.",
            "blank": "Este campo no puede estar en blanco.",
            "null": "Este campo no puede ser nulo.",
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
