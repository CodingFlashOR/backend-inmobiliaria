from typing import NewType


UserUUID = NewType("UserUUID", str)
UserUUID.__doc__ = """
    A unique identifier for a user. For example:

    123e4567-e89b-12d3-a456-426614174000
"""
