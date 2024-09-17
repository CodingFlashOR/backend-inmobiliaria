from apps.users.constants import SearcherProperties, BaseUserProperties
from apps.api_exceptions import (
    DatabaseConnectionAPIError,
    NotAuthenticatedAPIError,
    PermissionDeniedAPIError,
    JWTAPIError,
)
from apps.utils.messages import ERROR_MESSAGES, JWTErrorMessages
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
)


POSTSearcherSchema = extend_schema(
    operation_id="create_searcher_user",
    tags=["Users"],
    responses={
        201: OpenApiResponse(
            description="**(CREATED)** User created correctly."
        ),
        400: OpenApiResponse(
            description="**(BAD_REQUEST)** The request data is invalid, error messages are returned for each field that did not pass validations.",
            response={
                "properties": {
                    "code": {"type": "string"},
                    "detail": {"type": "object"},
                }
            },
            examples=[
                OpenApiExample(
                    name="invalid_data",
                    summary="Invalid data",
                    description="These are the possible error messages for each field.",
                    value={
                        "code": "invalid_request_data",
                        "detail": {
                            "name": [
                                ERROR_MESSAGES["required"],
                                ERROR_MESSAGES["blank"],
                                ERROR_MESSAGES["null"],
                                ERROR_MESSAGES["invalid"],
                                ERROR_MESSAGES["max_length"].format(
                                    max_length=SearcherProperties.NAME_MAX_LENGTH.value,
                                ),
                            ],
                            "last_name": [
                                ERROR_MESSAGES["required"],
                                ERROR_MESSAGES["blank"],
                                ERROR_MESSAGES["null"],
                                ERROR_MESSAGES["invalid"],
                                ERROR_MESSAGES["max_length"].format(
                                    max_length=SearcherProperties.LAST_NAME_MAX_LENGTH.value,
                                ),
                            ],
                            "email": [
                                ERROR_MESSAGES["required"],
                                ERROR_MESSAGES["blank"],
                                ERROR_MESSAGES["null"],
                                ERROR_MESSAGES["invalid"],
                                ERROR_MESSAGES["max_length"].format(
                                    max_length=BaseUserProperties.EMAIL_MAX_LENGTH.value,
                                ),
                                ERROR_MESSAGES["email_in_use"],
                            ],
                            "password": [
                                ERROR_MESSAGES["required"],
                                ERROR_MESSAGES["blank"],
                                ERROR_MESSAGES["null"],
                                ERROR_MESSAGES["invalid"],
                                ERROR_MESSAGES["max_length"].format(
                                    max_length=BaseUserProperties.PASSWORD_MAX_LENGTH.value,
                                ),
                                ERROR_MESSAGES["min_length"].format(
                                    min_length=BaseUserProperties.PASSWORD_MIN_LENGTH.value,
                                ),
                            ],
                            "confirm_password": [
                                ERROR_MESSAGES["required"],
                                ERROR_MESSAGES["blank"],
                                ERROR_MESSAGES["null"],
                                ERROR_MESSAGES["password_no_upper_lower"],
                                ERROR_MESSAGES["password_common"],
                                ERROR_MESSAGES["password_mismatch"],
                            ],
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
                    description="The connection to the database could not be established.",
                    value={
                        "code": DatabaseConnectionAPIError.default_code,
                        "detail": DatabaseConnectionAPIError.default_detail,
                    },
                ),
            ],
        ),
    },
)


GETSearcherSchema = extend_schema(
    operation_id="get_searcher_user",
    tags=["Users"],
    responses={
        200: OpenApiResponse(
            description="**(OK)** The requested user information is returned.",
            response={
                "properties": {
                    "base_data": {"type": "object"},
                    "role_data": {"type": "object"},
                }
            },
            examples=[
                OpenApiExample(
                    name="response_ok",
                    summary="Get user data",
                    description="User information is displayed without showing sensitive data, it is possible that some of this data has a 'null' value.",
                    value={
                        "base_data": {
                            "email": "user@email.com",
                        },
                        "role_data": {
                            "name": "Nombre del usuario",
                            "last_name": "Apellido del usuario",
                            "cc": "1234567890",
                            "phone_number": "+573111111111",
                            "is_phone_verified": False,
                        },
                    },
                )
            ],
        ),
        401: OpenApiResponse(
            description="**(UNAUTHORIZED)** The user's JSON Web Token is not valid for logout.",
            response={
                "properties": {
                    "code": {"type": "string"},
                    "detail": {"type": "string"},
                }
            },
            examples=[
                OpenApiExample(
                    name="invalid_expired",
                    summary="Access token invalid or expired",
                    description="The access token sent in the request header is invalid or has expired.",
                    value={
                        "code": JWTAPIError.default_code,
                        "detail": JWTErrorMessages.INVALID_OR_EXPIRED.value.format(
                            token_type="access",
                        ),
                    },
                ),
                OpenApiExample(
                    name="token_blacklisted",
                    summary="Access token exists in the blacklist",
                    description="The access token sent in the request header exists in the blacklist.",
                    value={
                        "code": JWTAPIError.default_code,
                        "detail": JWTErrorMessages.BLACKLISTED.value.format(
                            token_type="access",
                        ),
                    },
                ),
                OpenApiExample(
                    name="access_token_not_provided",
                    summary="Access token not provided",
                    description="The access token was not provided in the request header.",
                    value={
                        "code": NotAuthenticatedAPIError.default_code,
                        "detail": NotAuthenticatedAPIError.default_detail,
                    },
                ),
            ],
        ),
        403: OpenApiResponse(
            description="**(FORBIDDEN)** The user does not have permission to access this resource.",
            response={
                "properties": {
                    "code": {"type": "string"},
                    "detail": {"type": "string"},
                }
            },
            examples=[
                OpenApiExample(
                    name="permission_denied",
                    summary="Permission denied",
                    description="This response is displayed when the user does not have permission to read your data or does not have the required role.",
                    value={
                        "code": PermissionDeniedAPIError.default_code,
                        "detail": PermissionDeniedAPIError.default_detail,
                    },
                ),
            ],
        ),
        404: OpenApiResponse(
            description="**(NOT_FOUND)** Some resources necessary for this process were not found in the database.",
            response={
                "properties": {
                    "code": {"type": "string"},
                    "detail": {"type": "string"},
                }
            },
            examples=[
                OpenApiExample(
                    name="user_not_found",
                    summary="User not found",
                    description="The user in the provided JSON Web Tokens does not exist in the database.",
                    value=JWTErrorMessages.USER_NOT_FOUND.value,
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
                    description="The connection to the database could not be established.",
                    value={
                        "code": DatabaseConnectionAPIError.default_code,
                        "detail": DatabaseConnectionAPIError.default_detail,
                    },
                ),
            ],
        ),
    },
)


PATCHearcherSchema = extend_schema(
    operation_id="update_searcher_user",
    tags=["Users"],
    responses={
        200: OpenApiResponse(
            description="**(OK)** Updated user information is returned.",
            response={
                "properties": {
                    "base_data": {"type": "object"},
                    "role_data": {"type": "object"},
                }
            },
            examples=[
                OpenApiExample(
                    name="response_ok",
                    summary="New user data",
                    description="User information is displayed without showing sensitive data, it is possible that some of this data has a 'null' value.",
                    value={
                        "base_data": {
                            "email": "user@email.com",
                        },
                        "role_data": {
                            "name": "Nombre del usuario",
                            "last_name": "Apellido del usuario",
                            "cc": "1234567890",
                            "phone_number": "+573111111111",
                            "is_phone_verified": False,
                        },
                    },
                )
            ],
        ),
        400: OpenApiResponse(
            description="**(BAD_REQUEST)** The request data is invalid, error messages are returned for each field that did not pass validations.",
            response={
                "properties": {
                    "code": {"type": "string"},
                    "detail": {"type": "object"},
                }
            },
            examples=[
                OpenApiExample(
                    name="invalid_data",
                    summary="Empty data",
                    description="At least one piece of user data is required to proceed with the update.",
                    value={
                        "code": "invalid_request_data",
                        "detail": {
                            "non_field_errors": [
                                "You must provide at least one field to update.",
                            ],
                        },
                    },
                ),
                OpenApiExample(
                    name="invalid_data",
                    summary="Invalid data",
                    description="These are the possible error messages for each field.",
                    value={
                        "code": "invalid_request_data",
                        "detail": {
                            "name": [
                                ERROR_MESSAGES["blank"],
                                ERROR_MESSAGES["null"],
                                ERROR_MESSAGES["invalid"],
                                ERROR_MESSAGES["max_length"].format(
                                    max_length=SearcherProperties.NAME_MAX_LENGTH.value,
                                ),
                            ],
                            "last_name": [
                                ERROR_MESSAGES["blank"],
                                ERROR_MESSAGES["null"],
                                ERROR_MESSAGES["invalid"],
                                ERROR_MESSAGES["max_length"].format(
                                    max_length=SearcherProperties.LAST_NAME_MAX_LENGTH.value,
                                ),
                            ],
                            "cc": [
                                ERROR_MESSAGES["blank"],
                                ERROR_MESSAGES["null"],
                                ERROR_MESSAGES["invalid"],
                                ERROR_MESSAGES["max_length"].format(
                                    max_length=SearcherProperties.CC_MAX_LENGTH.value,
                                ),
                                ERROR_MESSAGES["min_length"].format(
                                    min_length=SearcherProperties.CC_MIN_LENGTH.value,
                                ),
                                ERROR_MESSAGES["cc_in_use"],
                            ],
                            "phone_number": [
                                ERROR_MESSAGES["blank"],
                                ERROR_MESSAGES["null"],
                                ERROR_MESSAGES["invalid"],
                                ERROR_MESSAGES["max_length"].format(
                                    max_length=SearcherProperties.PHONE_NUMBER_MAX_LENGTH.value,
                                ),
                                ERROR_MESSAGES["phone_in_use"],
                            ],
                        },
                    },
                ),
            ],
        ),
        401: OpenApiResponse(
            description="**(UNAUTHORIZED)** The user's JSON Web Token is not valid for logout.",
            response={
                "properties": {
                    "code": {"type": "string"},
                    "detail": {"type": "string"},
                }
            },
            examples=[
                OpenApiExample(
                    name="invalid_expired",
                    summary="Access token invalid or expired",
                    description="The access token sent in the request header is invalid or has expired.",
                    value={
                        "code": JWTAPIError.default_code,
                        "detail": JWTErrorMessages.INVALID_OR_EXPIRED.value.format(
                            token_type="access",
                        ),
                    },
                ),
                OpenApiExample(
                    name="token_blacklisted",
                    summary="Access token exists in the blacklist",
                    description="The access token sent in the request header exists in the blacklist.",
                    value={
                        "code": JWTAPIError.default_code,
                        "detail": JWTErrorMessages.BLACKLISTED.value.format(
                            token_type="access",
                        ),
                    },
                ),
                OpenApiExample(
                    name="access_token_not_provided",
                    summary="Access token not provided",
                    description="The access token was not provided in the request header.",
                    value={
                        "code": NotAuthenticatedAPIError.default_code,
                        "detail": NotAuthenticatedAPIError.default_detail,
                    },
                ),
            ],
        ),
        403: OpenApiResponse(
            description="**(FORBIDDEN)** The user does not have permission to access this resource.",
            response={
                "properties": {
                    "code": {"type": "string"},
                    "detail": {"type": "string"},
                }
            },
            examples=[
                OpenApiExample(
                    name="permission_denied",
                    summary="Permission denied",
                    description="This response is displayed when the user does not have permission to read your data or does not have the required role.",
                    value={
                        "code": PermissionDeniedAPIError.default_code,
                        "detail": PermissionDeniedAPIError.default_detail,
                    },
                ),
            ],
        ),
        404: OpenApiResponse(
            description="**(NOT_FOUND)** Some resources necessary for this process were not found in the database.",
            response={
                "properties": {
                    "code": {"type": "string"},
                    "detail": {"type": "string"},
                }
            },
            examples=[
                OpenApiExample(
                    name="user_not_found",
                    summary="User not found",
                    description="The user in the provided JSON Web Tokens does not exist in the database.",
                    value=JWTErrorMessages.USER_NOT_FOUND.value,
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
                    description="The connection to the database could not be established.",
                    value={
                        "code": DatabaseConnectionAPIError.default_code,
                        "detail": DatabaseConnectionAPIError.default_detail,
                    },
                ),
            ],
        ),
    },
)
