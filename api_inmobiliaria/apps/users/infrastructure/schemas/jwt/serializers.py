from apps.users.constants import BaseUserProperties
from drf_spectacular.utils import (
    extend_schema_serializer,
    OpenApiExample,
)


AuthenticationSerializerSchema = extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="data_valid",
            summary="Valid data for the request.",
            description=f"Valid credentials for a user. The following validations will be applied:\n- **Email:** This field is required and must not exceed {BaseUserProperties.EMAIL_MAX_LENGTH.value} characters.\n- **Password:** This field is required and must not exceed {BaseUserProperties.PASSWORD_MAX_LENGTH.value} characters.\n\nRequest responses that include messages in Spanish indicate that these are messages intended for use on the frontend by the client.",
            value={
                "email": "user1@email.com",
                "password": "contraseña1234",
            },
            request_only=True,
        ),
    ],
)


UpdateTokenSerializerSchema = extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="data_valid",
            summary="Valid data for the request.",
            description=f"Valid data for the request. The following validations will be applied:\n- **Access token:** It is required, must be a valid token, must be expired and it should not exist on the blacklist.\n- **Refresh token:** It is required, must be a valid token, it must not be expired and it should not exist on the blacklist.",
            value={
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE1NjQ4MTAyLCJpYXQiOjE3MTU2NDA5MDIsImp0aSI6ImQ0YzEwYzEzMTgwODQ3YmNiNGU5NDMwMjFhYmQ3OGMyIiwidXNlcl91dWlkIjoiZDdiYTM0NzEtZWQzOS00NTQxLWFmOTktZWVmYzFjMWRlYmJkIiwicm9sZSI6IlNlYXJjaGVyVXNlciJ9.C5W1Q4XLBRXUbSUtKcESvudwo6-Ylg8u1fZZ4i79GWw",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTcyNzMwMiwiaWF0IjoxNzE1NjQwOTAyLCJqdGkiOiI0YjgwNjA2YTk3ODI0Y2U3YjZjNzIxZTBkYTE3YmUzMiIsInVzZXJfdXVpZCI6ImQ3YmEzNDcxLWVkMzktNDU0MS1hZjk5LWVlZmMxYzFkZWJiZCIsInJvbGUiOiJTZWFyY2hlclVzZXIifQ.JpRoGrk7GVDQmHrJnc1LelgzGMKmKvmXYKvAKQzhsWg",
            },
            request_only=True,
        ),
    ],
)


LogoutSerializerSchema = extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="data_valid",
            summary="Valid data for the request.",
            description=f"Valid data for the request. The following validations will be applied:\n- **Refresh token:** It is required, must be a valid token, it must not be expired and it should not exist on the blacklist.",
            value={
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTcyNzMwMiwiaWF0IjoxNzE1NjQwOTAyLCJqdGkiOiI0YjgwNjA2YTk3ODI0Y2U3YjZjNzIxZTBkYTE3YmUzMiIsInVzZXJfdXVpZCI6ImQ3YmEzNDcxLWVkMzktNDU0MS1hZjk5LWVlZmMxYzFkZWJiZCIsInJvbGUiOiJTZWFyY2hlclVzZXIifQ.JpRoGrk7GVDQmHrJnc1LelgzGMKmKvmXYKvAKQzhsWg",
            },
            request_only=True,
        ),
    ],
)
