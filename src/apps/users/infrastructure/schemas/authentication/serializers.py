from drf_spectacular.utils import (
    extend_schema_serializer,
    OpenApiExample,
)
from apps.users.domain.constants import SearcherUser


AuthenticationSerializerSchema = extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="data_valid",
            summary="Valid credentials for a user.",
            description=f"Valid credentials for a user. The following validations will be applied:\n- **email:** This field is required and must not exceed {SearcherUser.EMAIL_MAX_LENGTH.value} characters and must follow standard email format.\n- **password:** This field is required and should be between {SearcherUser.PASSWORD_MIN_LENGTH.value} and {SearcherUser.PASSWORD_MAX_LENGTH.value} characters. It should not be a common password or contain only numbers.",
            value={
                "email": "user1@email.com",
                "password": "contraseña1234",
            },
            request_only=True,
        ),
    ],
)
