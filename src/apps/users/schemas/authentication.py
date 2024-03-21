from drf_spectacular.utils import (
    extend_schema_serializer,
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
)


ViewSchema = extend_schema(
    tags=["Users"],
    responses={
        200: OpenApiResponse(
            description="**(OK)** Authenticated user.",
            response={
                "properties": {
                    "access": {"type": "string"},
                    "refresh": {"type": "string"},
                }
            },
            examples=[
                OpenApiExample(
                    name="response_ok",
                    summary="Valid request",
                    value={
                        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzExMDU0MzYyLCJpYXQiOjE3MTEwNDcxNjIsImp0aSI6IjY0MTE2YzgyYjhmMDQzOWJhNTJkZGZmMzgyNzQ2ZTIwIiwidXNlcl9pZCI6IjJhNmI0NTNiLWZhMmItNDMxOC05YzM1LWIwZTk2ZTg5NGI2MyJ9.gfhWpy5rYY6P3Xrg0usS6j1KhEvF1HqWMiU7AaFkp9A",
                        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxMTEzMzU2MiwiaWF0IjoxNzExMDQ3MTYyLCJqdGkiOiI2ZTRmNTdkMGJjNTc0NWY0OWMzODg4YjQ2YTM1OTJjNSIsInVzZXJfaWQiOiIyYTZiNDUzYi1mYTJiLTQzMTgtOWMzNS1iMGU5NmU4OTRiNjMifQ.81pQ3WftFZs5O50vGqwY2a6yPkXArQK6WKyrwus3s6A",
                    },
                ),
            ],
        ),
        400: OpenApiResponse(
            description="**(BAD_REQUEST)** The request data are invalid, error message(s) are returned for each field that did not pass the validations.",
            response={
                "properties": {
                    "code": {"type": "string"},
                    "detail": {"type": "object"},
                }
            },
            examples=[
                OpenApiExample(
                    name="email_invalid",
                    summary="Invalid request data",
                    value={
                        "code": "invalid_request_data",
                        "detail": {
                            "email": ["Correo electrónico inválido."],
                            "password": [
                                "La contraseña debe tener al menos 8 caracteres."
                            ],
                        },
                    },
                ),
                OpenApiExample(
                    name="data_invalid",
                    summary="Invalid request",
                    value={
                        "code": "invalid_request_data",
                        "detail": {
                            "email": [
                                "Este campo es requerido.",
                                "Este campo no puede estar en blanco.",
                                "Este campo no puede ser nulo.",
                            ],
                            "password": [
                                "Este campo es requerido.",
                                "Este campo no puede estar en blanco.",
                                "Este campo no puede ser nulo.",
                            ],
                        },
                    },
                ),
            ],
        ),
        401: OpenApiResponse(
            description="**(UNAUTHORIZED)** The user you are trying to authenticate is not authorized, this is due to some of the following reasons.\n- Invalid credentials.\n- The user's account has not been activated.",
            response={
                "properties": {
                    "code": {"type": "string"},
                    "detail": {"type": "string"},
                }
            },
            examples=[
                OpenApiExample(
                    name="authentication_failed",
                    summary="Credentials invalid",
                    value={
                        "code": "authentication_failed",
                        "detail": "Correo o contraseña inválida.",
                    },
                ),
                OpenApiExample(
                    name="user_inactive",
                    summary="User inactive",
                    value={
                        "code": "authentication_failed",
                        "detail": "Cuenta del usuario inactiva.",
                    },
                ),
            ],
        ),
        500: OpenApiResponse(
            description="**(INTERNAL_SERVER_ERROR)** An unexpected error occurred.",
            response={
                "properties": {
                    "detail": {
                        "type": "string",
                    },
                    "code": {
                        "type": "string",
                    },
                }
            },
            examples=[
                OpenApiExample(
                    name="database_connection_error",
                    summary="Database connection error",
                    value={
                        "code": "database_connection_error",
                        "detail": "Unable to establish a connection with the database. Please try again later.",
                    },
                ),
            ],
        ),
    },
)


SerializerSchema = extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="data_valid",
            summary="User authentication",
            description="Valid credentials for a user. The following validations will be applied:\n- **Email:** Must be in a valid email format and no longer than 90 characters.\n- **Password:** Must be at least 8 characters and not more than 20 characters.",
            value={
                "email": "user1@example.com",
                "password": "Aaa123456789",
            },
            request_only=True,
        ),
    ],
)
