from apps.users.constants import RealEstateEntityProperties, BaseUserProperties
from apps.api_exceptions import DatabaseConnectionAPIError
from utils.messages import ERROR_MESSAGES
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
)


# Real estate entity and base user properties
EMAIL_MAX_LENGTH = BaseUserProperties.EMAIL_MAX_LENGTH.value
PASSWORD_MAX_LENGTH = BaseUserProperties.PASSWORD_MAX_LENGTH.value
PASSWORD_MIN_LENGTH = BaseUserProperties.PASSWORD_MIN_LENGTH.value
NAME_MAX_LENGTH = RealEstateEntityProperties.NAME_MAX_LENGTH.value
LINK_MAX_LENGTH = RealEstateEntityProperties.LINK_MAX_LENGTH.value
DEPARTMENT_MAX_LENGTH = RealEstateEntityProperties.DEPARTMENT_MAX_LENGTH.value
MUNICIPALITY_MAX_LENGTH = RealEstateEntityProperties.MUNICIPALITY_MAX_LENGTH.value
REGION_MAX_LENGTH = RealEstateEntityProperties.REGION_MAX_LENGTH.value
COORDINATE_MAX_LENGTH = RealEstateEntityProperties.COORDINATE_MAX_LENGTH.value
NIT_MAX_LENGTH = RealEstateEntityProperties.NIT_MAX_LENGTH.value
PHONE_NUMBER_MAX_LENGTH = RealEstateEntityProperties.PHONE_NUMBER_MAX_LENGTH.value
MAXIMUM_PHONE_NUMBERS = RealEstateEntityProperties.MAXIMUM_PHONE_NUMBERS.value
DESCRIPTION_MAX_LENGTH = RealEstateEntityProperties.DESCRIPTION_MAX_LENGTH.value


POSTRealEstateEntitySchema = extend_schema(
    operation_id="create_real_estate_entity",
    tags=["Users"],
    responses={
        201: OpenApiResponse(
            description="**(CREATED)** User created successfully and message was sent."
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
                    name="invalid_data1",
                    summary="Invalid data",
                    description="These are the possible error messages for each field.",
                    value={
                        "code": "invalid_request_data",
                        "detail": {
                            "type_entity": [
                                ERROR_MESSAGES["required"],
                                ERROR_MESSAGES["blank"],
                                ERROR_MESSAGES["null"],
                                ERROR_MESSAGES["invalid"],
                                ERROR_MESSAGES["invalid_choice"].format(
                                    input="Broker"
                                ),
                            ],
                            "logo": [
                                ERROR_MESSAGES["required"],
                                ERROR_MESSAGES["blank"],
                                ERROR_MESSAGES["null"],
                                ERROR_MESSAGES["invalid_url"],
                                ERROR_MESSAGES["max_length"].format(
                                    max_length=LINK_MAX_LENGTH
                                ),
                            ],
                            "name": [
                                ERROR_MESSAGES["required"],
                                ERROR_MESSAGES["blank"],
                                ERROR_MESSAGES["null"],
                                ERROR_MESSAGES["invalid"],
                                ERROR_MESSAGES["name_in_use"],
                                ERROR_MESSAGES["max_length"].format(
                                    max_length=NAME_MAX_LENGTH
                                ),
                            ],
                            "description": [
                                ERROR_MESSAGES["required"],
                                ERROR_MESSAGES["blank"],
                                ERROR_MESSAGES["null"],
                                ERROR_MESSAGES["invalid"],
                                ERROR_MESSAGES["max_length"].format(
                                    max_length=DESCRIPTION_MAX_LENGTH
                                ),
                            ],
                            "nit": [
                                ERROR_MESSAGES["required"],
                                ERROR_MESSAGES["blank"],
                                ERROR_MESSAGES["null"],
                                ERROR_MESSAGES["invalid"],
                                ERROR_MESSAGES["nit_in_use"],
                                ERROR_MESSAGES["max_length"].format(
                                    max_length=NIT_MAX_LENGTH
                                ),
                                ERROR_MESSAGES["min_length"].format(
                                    min_length=NIT_MAX_LENGTH
                                ),
                            ],
                            "department": [
                                ERROR_MESSAGES["required"],
                                ERROR_MESSAGES["blank"],
                                ERROR_MESSAGES["null"],
                                ERROR_MESSAGES["invalid"],
                                ERROR_MESSAGES["max_length"].format(
                                    max_length=DEPARTMENT_MAX_LENGTH
                                ),
                            ],
                            "municipality": [
                                ERROR_MESSAGES["required"],
                                ERROR_MESSAGES["blank"],
                                ERROR_MESSAGES["null"],
                                ERROR_MESSAGES["invalid"],
                                ERROR_MESSAGES["max_length"].format(
                                    max_length=MUNICIPALITY_MAX_LENGTH
                                ),
                            ],
                            "region": [
                                ERROR_MESSAGES["required"],
                                ERROR_MESSAGES["blank"],
                                ERROR_MESSAGES["null"],
                                ERROR_MESSAGES["invalid"],
                                ERROR_MESSAGES["max_length"].format(
                                    max_length=REGION_MAX_LENGTH
                                ),
                            ],
                            "coordinate": [
                                ERROR_MESSAGES["required"],
                                ERROR_MESSAGES["blank"],
                                ERROR_MESSAGES["null"],
                                ERROR_MESSAGES["invalid"],
                                ERROR_MESSAGES["max_length"].format(
                                    max_length=COORDINATE_MAX_LENGTH
                                ),
                            ],
                            "email": [
                                ERROR_MESSAGES["required"],
                                ERROR_MESSAGES["blank"],
                                ERROR_MESSAGES["null"],
                                ERROR_MESSAGES["invalid"],
                                ERROR_MESSAGES["email_in_use"],
                                ERROR_MESSAGES["max_length"].format(
                                    max_length=EMAIL_MAX_LENGTH
                                ),
                            ],
                            "password": [
                                ERROR_MESSAGES["required"],
                                ERROR_MESSAGES["blank"],
                                ERROR_MESSAGES["null"],
                                ERROR_MESSAGES["invalid"],
                                ERROR_MESSAGES["max_length"].format(
                                    max_length=PASSWORD_MAX_LENGTH
                                ),
                                ERROR_MESSAGES["min_length"].format(
                                    min_length=PASSWORD_MIN_LENGTH
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
                OpenApiExample(
                    name="invalid_data2",
                    summary="Invalid phone numbers",
                    description="When a data type other than an array of elements is received, the possible error responses are shown in example 1. If an array is received but the validations for each element fail, the error responses for that case are shown in example 2.",
                    value={
                        "code": "invalid_request_data",
                        "detail": {
                            "phone_numbers (example 1)": [
                                ERROR_MESSAGES["required"],
                                ERROR_MESSAGES["blank"],
                                ERROR_MESSAGES["null"],
                                ERROR_MESSAGES["invalid"],
                                ERROR_MESSAGES["empty"],
                                ERROR_MESSAGES["not_a_list"].format(
                                    input_type="int"
                                ),
                                ERROR_MESSAGES["max_length_list"].format(
                                    max_length=MAXIMUM_PHONE_NUMBERS
                                ),
                            ],
                            "phone_numbers (example 2)": {
                                "0": [
                                    ERROR_MESSAGES["blank"],
                                    ERROR_MESSAGES["null"],
                                    ERROR_MESSAGES["invalid"],
                                    ERROR_MESSAGES["max_length"].format(
                                        max_length=PHONE_NUMBER_MAX_LENGTH
                                    ),
                                ],
                            },
                        },
                    },
                ),
                OpenApiExample(
                    name="invalid_data3",
                    summary="Invalid documents",
                    description="When a data type other than a dictionary or JSON is received, the possible error responses are shown in example 1. If a dictionary or JSON is received but validations for each element fail, the error responses for that case are shown in example 2.",
                    value={
                        "code": "invalid_request_data",
                        "detail": {
                            "documents (example 1)": [
                                ERROR_MESSAGES["required"],
                                ERROR_MESSAGES["blank"],
                                ERROR_MESSAGES["null"],
                                ERROR_MESSAGES["invalid"],
                                ERROR_MESSAGES["empty"],
                                ERROR_MESSAGES["not_a_dict"].format(
                                    input_type="int"
                                ),
                                ERROR_MESSAGES["document_invalid"].format(
                                    doc_name="Otro documento"
                                ),
                                "No se ha definido el tipo de entidad.",
                            ],
                            "documents (example 2)": {
                                "Cámara de Comercio": [
                                    ERROR_MESSAGES["blank"],
                                    ERROR_MESSAGES["null"],
                                    ERROR_MESSAGES["invalid_url"],
                                    ERROR_MESSAGES["max_length"].format(
                                        max_length=LINK_MAX_LENGTH
                                    ),
                                ],
                                "Certificado del Registro Único Tributario (RUT)": [
                                    ERROR_MESSAGES["blank"],
                                    ERROR_MESSAGES["null"],
                                    ERROR_MESSAGES["invalid_url"],
                                    ERROR_MESSAGES["max_length"].format(
                                        max_length=LINK_MAX_LENGTH
                                    ),
                                ],
                                "Licencias de construcción": [
                                    ERROR_MESSAGES["blank"],
                                    ERROR_MESSAGES["null"],
                                    ERROR_MESSAGES["invalid_url"],
                                    ERROR_MESSAGES["max_length"].format(
                                        max_length=LINK_MAX_LENGTH
                                    ),
                                ],
                            },
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
