from drf_spectacular.utils import (
    extend_schema_serializer,
    OpenApiExample,
)


AuthenticationSerializerSchema = extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="data_valid",
            summary="Valid data for the request.",
            description=f"Valid credentials for a user. The following validations will be applied:\n- **email:** This field is required.\n- **password:** This field is required.",
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
            description="Valid data for the request. The following validations will be applied:\n- **refresh:** must be a valid token and not expired.",
            value={
                "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTcyNzMwMiwiaWF0IjoxNzE1NjQwOTAyLCJqdGkiOiI0YjgwNjA2YTk3ODI0Y2U3YjZjNzIxZTBkYTE3YmUzMiIsInVzZXJfdXVpZCI6ImQ3YmEzNDcxLWVkMzktNDU0MS1hZjk5LWVlZmMxYzFkZWJiZCIsInJvbGUiOiJTZWFyY2hlclVzZXIifQ.JpRoGrk7GVDQmHrJnc1LelgzGMKmKvmXYKvAKQzhsWg"
            },
            request_only=True,
        ),
    ],
)
