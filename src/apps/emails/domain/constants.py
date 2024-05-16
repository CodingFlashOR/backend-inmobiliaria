from enum import Enum
from datetime import timedelta


TOKEN_EXPIRATION = timedelta(minutes=30)


class SubjectsMail(Enum):

    ACCOUNT_ACTIVATION = "Activate your account"
