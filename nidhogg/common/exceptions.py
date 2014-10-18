"""Exceptions for Yggdrasil protocol"""
from nidhogg.common.json import json_response
from nidhogg.common.utils import Classproperty


class NidhoggError(Exception):
    """Base exception class for Yggdrasil-specific errors."""

    error = None
    message = None
    cause = None

    @Classproperty
    @classmethod
    def data(cls):
        """The dictionary representation of the error.

        :rtype: dict
        """
        result = {"error": cls.error, "errorMessage": cls.message}
        if cls.cause is not None:
            result["cause"] = cls.cause
        return result

    @staticmethod
    @json_response
    def handler(exception):
        """Helper function for proper exception handling in Flask"""
        return exception.data
