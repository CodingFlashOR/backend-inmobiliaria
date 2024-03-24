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
            description="**(OK)** New user tokens.",
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
                    "detail": {
                        "type": "object",
                        "properties": {
                            "access": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "refresh": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                        },
                    },
                }
            },
            examples=[
                OpenApiExample(
                    name="invalid_data1",
                    summary="Access token not expired",
                    value={
                        "code": "invalid_request_data",
                        "detail": {
                            "access": ["Token is not expired."],
                        },
                    },
                ),
                OpenApiExample(
                    name="invalid_data2",
                    summary="Refresh token expired",
                    value={
                        "code": "invalid_request_data",
                        "detail": {
                            "refresh": ["Token is expired."],
                        },
                    },
                ),
                OpenApiExample(
                    name="invalid_data3",
                    summary="Invalid tokens",
                    value={
                        "code": "invalid_request_data",
                        "detail": {
                            "access": ["Token is invalid."],
                            "refresh": ["Token is invalid."],
                        },
                    },
                ),
                OpenApiExample(
                    name="invalid_data4",
                    summary="Invalid request data",
                    value={
                        "code": "invalid_request_data",
                        "detail": {
                            "access": [
                                "This field is required.",
                                "This field may not be blank.",
                                "This field may not be null.",
                            ],
                            "refresh": [
                                "This field is required.",
                                "This field may not be blank.",
                                "This field may not be null.",
                            ],
                        },
                    },
                ),
            ],
        ),
        401: OpenApiResponse(
            description="**(UNAUTHORIZED)** Tokens cannot be refreshed, this is due to one of the following reasons.\n- The user of the tokens was not found.\n- The tokens do not match the user's last tokens.\n- The tokens were not found.",
            response={
                "properties": {
                    "code": {"type": "string"},
                    "detail": {"type": "string or object"},
                }
            },
            examples=[
                OpenApiExample(
                    name="user_not_found",
                    summary="The user of the tokens was not found",
                    value={
                        "code": "user_not_found",
                        "detail": "User 2a6b453b-fa2b-4318-9c35-b0e96e894b63 not found.",
                    },
                ),
                OpenApiExample(
                    name="token_not_found",
                    summary="The tokens were not foun",
                    value={
                        "code": "token_not_found",
                        "detail": "Tokens do not exist.",
                    },
                ),
                OpenApiExample(
                    name="token_error",
                    summary="The tokens do not match the user's last tokens",
                    value={
                        "code": "token_error",
                        "detail": {
                            "message": "The token does not match the user's last tokens.",
                            "token_type": "Access",
                            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxMTEzMzU2MiwiaWF0IjoxNzExMDQ3MTYyLCJqdGkiOiI2ZTRmNTdkMGJjNTc0NWY0OWMzODg4YjQ2YTM1OTJjNSIsInVzZXJfaWQiOiIyYTZiNDUzYi1mYTJiLTQzMTgtOWMzNS1iMGU5NmU4OTRiNjMifQ.81pQ3WftFZs5O50vGqwY2a6yPkXArQK6WKyrwus3s6A",
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
            summary="JWT for user",
            description="Valid data for the request. The following validations will be applied:\n- **Access token:** must be a valid token and expired.\n- **Refresh token:** must be a valid token and not expired.",
            value={
                "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA2Mjk2MzI3LCJpYXQiOjE3MDYyODkxMjcsImp0aSI6IjQ0Zjg3MDdjZTdhOTQ0Y2RhYWRlNzlhMDg1OThiY2NkIiwidXNlcl9pZCI6IjUwNTI5MjBjLWE3ZDYtNDM4ZS1iZmQwLWVhNTUyMTM4ODM2YyJ9.-FPGYs1m-SDZDs3FJ3wlnqESVhcIg8oYAgKOFBD6Qic",
                "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwNjM3NTUyNywiaWF0IjoxNzA2Mjg5MTI3LCJqdGkiOiI3NzE5OGZmM2JkYWQ0MTk5YTExNjcwZGMwMzdmNTM0YyIsInVzZXJfaWQiOiI1MDUyOTIwYy1hN2Q2LTQzOGUtYmZkMC1lYTU1MjEzODgzNmMifQ.dfHpJRflOA1M2BmraxcW401EJvrTqU6HfbVmHHRkF2U",
            },
            request_only=True,
        ),
    ],
)
