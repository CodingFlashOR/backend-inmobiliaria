from rest_framework.serializers import Serializer


ERROR_MESSAGES = {
    # Length errors
    "max_length": "El valor ingresado no puede tener más de {max_length} caracteres.",
    "min_length": "El valor ingresado debe tener al menos {min_length} caracteres.",
    # Password errors
    "password_mismatch": "Las contraseñas no coinciden.",
    "password_common": "Esta contraseña es demasiado común.",
    "password_no_upper_lower": "La contraseña debe contener al menos una mayuscula o una minuscula.",
    # Invalid data
    "invalid": "El valor ingresado es inválido.",
    "invalid_choice": "{input} no es una elección válida.",
    # Required fields
    "required": "Este campo es requerido.",
    "blank": "Este campo no puede estar en blanco.",
    "null": "Este campo no puede ser nulo.",
    # Data in use
    "email_in_use": "Este correo electrónico ya está en uso.",
    "phone_in_use": "Este número de teléfono ya está en uso.",
    "address_in_use": "Esta dirección ya está en uso.",
}


class ErrorMessagesSerializer(Serializer):
    """
    A serializer class that provides custom error messages for fields.
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
