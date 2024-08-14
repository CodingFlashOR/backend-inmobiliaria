from uuid import UUID


def is_valid_uuid(value: str) -> bool:
    """
    Validates if the provided string is a valid UUID.
    """

    try:
        UUID(value)

        return True
    except ValueError:
        return False
