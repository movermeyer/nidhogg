"""Hasher interface example"""


def check_password(raw=None, hashed=None):
    """«Checks» password."""
    return raw == hashed
