"""Exceptions for Yggdrasil protocol"""


class NidhoggError(Exception):
    """Base exception class for Yggdrasil-specific errors."""

    error = None
    message = None
    cause = None

    @classmethod
    def get_info(cls):
        """The dictionary representation of the error.

        :rtype: dict[str,str]
        """
        result = {"error": cls.error, "errorMessage": cls.message}
        if cls.cause is not None:
            result["cause"] = cls.cause
        return result
