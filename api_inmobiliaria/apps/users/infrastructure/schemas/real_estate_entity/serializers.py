from apps.users.constants import (
    RealEstateEntityProperties,
    BaseUserProperties,
    UserRoles,
)
from drf_spectacular.utils import (
    extend_schema_serializer,
    OpenApiExample,
)


# User roles
CONSTRUCTION_COMPANY = UserRoles.CONSTRUCTION_COMPANY.value

# Real estate entity and base user properties
EMAIL_MAX_LENGTH = BaseUserProperties.EMAIL_MAX_LENGTH.value
PASSWORD_MAX_LENGTH = BaseUserProperties.PASSWORD_MAX_LENGTH.value
PASSWORD_MIN_LENGTH = BaseUserProperties.PASSWORD_MIN_LENGTH.value
NAME_MAX_LENGTH = RealEstateEntityProperties.NAME_MAX_LENGTH.value
LINK_MAX_LENGTH = RealEstateEntityProperties.LINK_MAX_LENGTH.value
NIT_MAX_LENGTH = RealEstateEntityProperties.NIT_MAX_LENGTH.value
PHONE_NUMBER_MAX_LENGTH = RealEstateEntityProperties.PHONE_NUMBER_MAX_LENGTH.value
MAXIMUM_PHONE_NUMBERS = RealEstateEntityProperties.MAXIMUM_PHONE_NUMBERS.value
DESCRIPTION_MAX_LENGTH = RealEstateEntityProperties.DESCRIPTION_MAX_LENGTH.value


RegisterRealEstateEntitySchema = extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="data_valid",
            summary="Register a new user with role searcher.",
            description=f"A valid user registration data. The following validations will be applied:\n- **Name:** This field is required, must not exceed {NAME_MAX_LENGTH} characters and must contain only letters and spaces.\n- **Email:** This field is required and must not exceed {EMAIL_MAX_LENGTH} characters, must follow standard email format, and must not be in use.\n- **Password:** This field is required and should be between {PASSWORD_MIN_LENGTH} and {PASSWORD_MAX_LENGTH} characters. It should not be a common password or contain only numbers.\n- **Confirm password:** This field is required and should match the password field.\n- **Logo:** This field is required, it must have the structure of a valid link and cannot have more than {LINK_MAX_LENGTH} character.\n- **Description:** This field is required, it must be a text string in Markdown (MD) format and cannot have more than {DESCRIPTION_MAX_LENGTH} character.\n- **NIT:** This field is required and must be a numeric text string of exactly {NIT_MAX_LENGTH} characters.\n- **Phone numbers:** This field is required and must be an array where each element is a text string with the structure of a valid phone number. Each number must have a maximum of {PHONE_NUMBER_MAX_LENGTH} characters. The array cannot be empty, and must contain at least 1 element and at most {MAXIMUM_PHONE_NUMBERS} elements.\n- **Department:** This field is required and must be a valid Colombian department.\n- **Municipality:** This field is required and must be a valid Colombian municipality.\n- **Region:** This field is required and must be a valid Colombian region.\n- **Coordinate:** This field is required and must follow a valid coordinate structure.\n- **Documents:** This field is required and must be a dictionary or JSON in which each element is a key-value pair. The allowed keys when the entity is a real estate company are: Tax Registry Certificate (RUT) and Chamber of Commerce; and when the entity is a construction company, the allowed keys are: Tax Registry Certificate (RUT), Chamber of Commerce and Construction Licenses. Values ​​must be valid URLs with a maximum of {LINK_MAX_LENGTH} characters.ucture.\n\nRequest responses that include messages in Spanish indicate that these are messages intended for use on the frontend by the client.",
            value={
                "type_entity": CONSTRUCTION_COMPANY,
                "name": "Nombres de la entidad",
                "logo": "https://www.logo.com/",
                "email": "user1@email.com",
                "password": "contraseña1234",
                "confirm_password": "contraseña1234",
                "description": "Descripción de la entidad.",
                "nit": "1234567890",
                "phone_numbers": ["+57 3111111111", "+57 3222222222"],
                "department": "Antioquia",
                "municipality": "Medellín",
                "region": "Región Eje Cafetero - Antioquia",
                "coordinate": "6.244203,-75.581211",
                "documents": {
                    "Cámara de Comercio": "https://www.camaracomercio.com/",
                    "Certificado del Registro Único Tributario (RUT)": "https://www.rut.com/",
                    "Licencias de construcción": "https://www.licencias.com/",
                },
            },
            request_only=True,
        ),
    ],
)
