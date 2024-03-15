from drf_spectacular.utils import (
    extend_schema_serializer,
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
)


ViewSchema = extend_schema(
    tags=["Users"],
    responses={
        201: OpenApiResponse(
            description="**(CREATED)** User created correctly."
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
                    name="passwords_not_match",
                    summary="Passwords do not match",
                    value={
                        "code": "invalid_request_data",
                        "detail": {
                            "non_field_errors": [
                                "Las contraseñas no coinciden."
                            ]
                        },
                    },
                ),
                OpenApiExample(
                    name="email_already_use",
                    summary="Email already in use",
                    value={
                        "code": "invalid_request_data",
                        "detail": {
                            "email": [
                                "Este correo electrónico ya está en uso."
                            ]
                        },
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
            summary="Register a new user",
            description="A valid user registration data. The following validations will be applied:\n- **Email:** Must be in a valid email format, no longer than 90 characters and not in use.\n- **Password:** Must be at least 8 characters, not more than 20 characters, and not a common or simple password.\n- **Confirm Password:** Must match the password.",
            value={
                "email": "user1@example.com",
                "password": "Aaa123456789",
                "confirm_password": "Aaa123456789",
            },
            request_only=True,
        ),
    ],
)
