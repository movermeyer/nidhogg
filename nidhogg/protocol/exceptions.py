from common.utils import json_response


@json_response
def error_handler(exception):
    return exception.dictionary

class Classproperty(property):
    """Property decorator for classes."""

    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


class YggdrasilError(Exception):
    """Base exception class for Yggdrasil-specific errors."""

    status_code = None
    error = None
    message = None
    cause = None

    def __new__(cls, *args, **kwargs):
        if cls is YggdrasilError:
            raise TypeError("{} class may not be instantiated!".format(cls.__name__))
        return super().__new__(cls, *args, **kwargs)

    @Classproperty
    @classmethod
    def dictionary(cls):
        """The dictionary representation of the error.

        :rtype: dict
        """
        result = {"error": cls.error, "errorMessage": cls.message}
        if cls.cause is not None:
            result["cause"] = cls.cause
        return result


class MethodNotAllowed(YggdrasilError):
    """Yggdrasil support only POST requests"""

    status_code = 405
    error = "Method Not Allowed"
    message = ("The method specified in the request is not allowed "
               "for the resource identified by the request URI")


class NotFound(YggdrasilError):
    """Use for nonexistent and incorrect endpoints."""

    status_code = 404
    error = "Not Found"
    message = "The server has not found anything matching the request URI"


class BadPayload(YggdrasilError):
    """Raises when payload is corrupted, or not **application/json** mimetype."""

    status_code = 400
    error = "Unsupported Media Type"
    message = ("The server is refusing to service the request "
               "because the entity of the request is in a format "
               "not supported by the requested resource for the requested method")


class AccessDenied(YggdrasilError):
    """Common class for auth errors."""

    status_code = 403
    error = "ForbiddenOperationException"


class MigrationDone(AccessDenied):
    """Use for migrated accounts."""

    message = "Invalid credentials. Account migrated, use e-mail as username."
    cause = "UserMigratedException"


class InvalidCredentials(AccessDenied):
    """Wrong username, email or password."""

    message = "Invalid credentials. Invalid username or password."


class InvalidToken(AccessDenied):
    """Raises when accessToken expired or not exists."""

    message = "Invalid token."


class BadRequest(YggdrasilError):
    """Common class for incorrect requests."""

    status_code = 400
    error = "IllegalArgumentException"


class MultipleProfiles(BadRequest):
    """Use if multiple profiles for account found.

    .. warning::
        Selecting profiles isn't implemented yet.

    .. note::
        Currently each account will only have one single profile,
        multiple profiles per account are however planned in the future.[1]

        If a user attempts to log into a valid Mojang account
        with no attached Minecraft license, the authentication will be successful,
        but the response will not contain a "selectedProfile" field,
        and the "availableProfiles" array will be empty.

        Some instances in the wild have been observed of Mojang returning
        a flat "null" for failed refresh attempts against legacy accounts.
        It's not clear what the actual error tied to the null response is
        and it is extremely rare, but implementations should be wary of
        null output from the response.

    .. [1] See http://wiki.vg/Authentication#Response
    """

    message = "Access token already has a profile assigned."


class EmptyCredentials(BadRequest):
    """Raises when username/email/password was not submitted."""

    message = "Credentials can not be null."
