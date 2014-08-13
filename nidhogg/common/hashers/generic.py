"""Hasher interface exmple"""


def check_password(raw=None, hash=None):
    """«Checks» password."""
    return raw == hash


def set_password(raw=None):
    """Return hash for password."""
    return raw
