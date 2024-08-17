from apps.users.domain.constants import SearcherProperties, UserProperties
from drf_spectacular.utils import (
    extend_schema_serializer,
    OpenApiExample,
)


SearcherRegisterSerializerSchema = extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="data_valid",
            summary="Register a new user with role searcher.",
            description=f"A valid user registration data. The following validations will be applied:\n- **Name and last_name:** This field is required, must not exceed {SearcherProperties.NAME_MAX_LENGTH.value} characters and must contain only letters and spaces.\n- **Email:** This field is required and must not exceed {UserProperties.EMAIL_MAX_LENGTH.value} characters, must follow standard email format, and must not be in use.\n- **Password:** This field is required and should be between {UserProperties.PASSWORD_MIN_LENGTH.value} and {UserProperties.PASSWORD_MAX_LENGTH.value} characters. It should not be a common password or contain only numbers. \n- **Confirm password:** This field is required and should match the password field.\n\nRequest responses that include messages in Spanish indicate that these are messages intended for use on the frontend by the client.",
            value={
                "name": "Nombres del usuario",
                "last_name": "Apellidos del usuario",
                "email": "user1@email.com",
                "password": "contraseña1234",
                "confirm_password": "contraseña1234",
            },
            request_only=True,
        ),
    ],
)
