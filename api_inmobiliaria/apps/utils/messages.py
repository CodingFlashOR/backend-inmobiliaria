from apps.emails.constants import LOGIN_URL, REGISTER_URL, HOME_URL
from enum import Enum


ERROR_MESSAGES = {
    # Length errors
    "max_length": "El valor ingresado no puede tener más de {max_length} caracteres.",
    "min_length": "El valor ingresado debe tener al menos {min_length} caracteres.",
    "max_length_list": "No puedes agregar o seleccionar más de {max_length} elementos.",
    "min_length_list": "Debes agregar o seleccionar al menos {min_length} elementos.",
    "empty": "Debes agregar o seleccionar al menos un elemento.",
    # Password errors
    "password_mismatch": "Las contraseñas no coinciden.",
    "password_common": "Esta contraseña es demasiado común.",
    "password_no_upper_lower": "La contraseña debe contener al menos una mayuscula o una minuscula.",
    # Invalid data
    "invalid": "El valor ingresado es inválido.",
    "invalid_choice": "{input} no es una elección válida.",
    "invalid_url": "Introduzca una URL válida.",
    "document_invalid": "El documento con el nombre ({doc_name}) no es válido.",
    "not_a_list": "Se esperaba una lista de elementos pero se obtuvo un dato de tipo ({input_type}).",
    "not_a_dict": "Se esperaba un diccionario o JSON de elementos pero se obtuvo un dato de tipo ({input_type}).",
    # Required fields
    "required": "Este campo es requerido.",
    "blank": "Este campo no puede estar en blanco.",
    "null": "Este campo no puede ser nulo.",
    # Data in use
    "email_in_use": "Este correo electrónico ya está en uso.",
    "phone_in_use": "Este número de teléfono ya está en uso.",
    "name_in_use": "Esta nombre ya está en uso.",
    "cc_in_use": "Este número de identificación ya está en uso.",
    "nit_in_use": "Este número de identificación tributaria ya está en uso.",
    "phone_numbers_in_use": "El número de teléfono {phone_number} ya está en uso.",
    "coordinate_in_use": "Ubicación en uso.",
}


class JWTErrorMessages(Enum):
    """
    Enum class for error messages related to JWT use cases. The errors that are in
    Spanish are messages that the user will see.
    """

    AUTHENTICATION_FAILED = "Correo o contraseña incorrecta."
    INACTIVE_ACCOUNT = "Tu cuenta está inactiva. Te recomendamos revisar la bandeja de entrada de tu correo electrónico para encontrar el mensaje que te enviamos al registrarte. Ese correo incluye las instrucciones para activar tu cuenta."
    LAST_TOKENS = (
        "The JWTs sent in the request do not match the user's last tokens."
    )
    TOKEN_NOT_FOUND = {
        "code": "jwt_not_found",
        "detail": "{token_type} token is not in the outstanding token list.",
    }
    USER_NOT_FOUND = {
        "code": "user_not_found",
        "detail": "The token user does not exist.",
    }
    INVALID_OR_EXPIRED = "{token_type} token is invalid or expired."
    BLACKLISTED = "{token_type} token is blacklisted."
    DIFFERENT_TOKEN = "The access token does not belong to the update token."
    USER_NOT_MATCH = "The user of the access token does not match the user of the refresh token."
    ACCESS_NOT_EXPIRED = "Access token is not expired."


class ActionLinkManagerErrors(Enum):
    """
    Error enumeration for the email communication module related to user account
    management.
    """

    DEFAULT = {
        "message": "Lo sentimos, se ha producido un error inesperado en nuestro sistema. No se ha podido completar tu solicitud en este momento. Por favor, inténtalo de nuevo más tarde. Si el problema persiste, puedes ponerte en contacto con nuestro equipo de soporte al cliente para obtener más ayuda. Disculpa las molestias y gracias por tu paciencia.",
        "redirect": {
            "action": "Ir al inicio",
            "url": HOME_URL,
        },
    }
    USER_NOT_FOUND = {
        "message": "Ha ocurrido un error y no hemos podido identificarte. Por favor, regístrate en nuestra plataforma para disfrutar de nuestros servicios.",
        "redirect": {
            "action": "Registrarse",
            "url": REGISTER_URL,
        },
    }
    TOKEN_EXPIRED = {
        "message": "El enlace ha expirado. Para tu seguridad, estos enlaces son válidos solo por un tiempo limitado. Por favor, solicita un nuevo enlace para {action}",
        "redirect": {
            "action": "Solicitar nuevo enlace",
        },
    }
    TOKEN_INVALID = {
        "message": "Lo sentimos, este enlace es de un solo uso y ya ha sido utilizado. Para acceder a nuestros servicios o realizar otras acciones, por favor inicia sesión en tu cuenta.",
        "redirect": {
            "action": "Iniciar sesión",
            "url": LOGIN_URL,
        },
    }


class ActivationErrors(Enum):
    """
    Enum class for error messages related to the use case in charge of sending the
    account activation message. The errors that are in English are messages that the
    user will see.
    """

    USER_NOT_FOUND = {
        "message": "Ha ocurrido un error y no hemos podido identificarte. Por favor, regístrate en nuestra plataforma y activa tu cuenta para que puedas disfrutar de nuestros servicios.",
        "redirect": {
            "action": "Registrarse",
            "url": REGISTER_URL,
        },
    }
    ACTIVE_ACCOUNT = {
        "message": "¡Parece que tu cuenta ya estaba activada! Inicia sesión cuando quieras y comienza a disfrutar de nuestros servicios.",
        "redirect": {
            "action": "Iniciar sesión",
            "url": LOGIN_URL,
        },
    }


class ErrorMessagesSerializer:
    """
    A serializer class that provides custom error messages in Spanish for the fields.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customized error messages
        msg = {
            "invalid": ERROR_MESSAGES["invalid"],
            "required": ERROR_MESSAGES["required"],
            "blank": ERROR_MESSAGES["blank"],
            "null": ERROR_MESSAGES["null"],
        }
        fields = list(self.fields.keys())
        for field_name in fields:
            self.fields[field_name].error_messages.update(msg)
