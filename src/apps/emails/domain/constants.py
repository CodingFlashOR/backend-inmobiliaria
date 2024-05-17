from enum import Enum
from datetime import timedelta


TOKEN_EXPIRATION = timedelta(minutes=30)
LOGIN_URL = "/login"


class SubjectsMail(Enum):
    """
    Enum that contains the subjects of the emails that the application sends.
    """

    ACCOUNT_ACTIVATION = "Activa tu cuenta"
