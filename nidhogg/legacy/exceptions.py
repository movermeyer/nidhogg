"""Exceptions for Legacy Auth protocol"""

from nidhogg.common.utils import Classproperty


class LegacyError(Exception):
    """Base exception class for Legacy Auth errors."""

    message = None

    def __new__(cls, *args, **kwargs):
        if cls is LegacyError:
            raise TypeError(
                "{} class may not be instantiated!"
                .format(cls.__name__)
            )
        return super().__new__(cls, *args, **kwargs)

    @Classproperty
    @classmethod
    def data(cls):
        """The text representation of the error.

        :rtype: str
        """
        return cls.message


class NoSuchMethod(LegacyError):
    message = "No such method"


class InvalidCredentials(LegacyError):
    message = "Invalid credentials. Invalid username or password."


class EmptyCredentials(LegacyError):
    """Raises when username/email/password was not submitted."""

    message = "Credentials can not be null."


class EmptyPayload(LegacyError):
    message = "Empty Data"


class BadPayload(LegacyError):
    message = "Bad Payload"
