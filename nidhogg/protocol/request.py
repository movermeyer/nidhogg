from json import loads

from protocol import exceptions as exc


class Request:
    """Base class for Yggdrasil request"""

    is_valid = False
    __result = None

    def __init__(self, raw_payload):
        """
        :type raw_payload: bytes
        :param raw_payload: Raw payload bytes
        :raise exceptions.BadPayload:
        """

        try:
            payload = raw_payload.decode()
            payload = loads(payload)
        except (UnicodeError, ValueError):
            raise exc.BadPayload

        if self.validate(payload):
            self.is_valid = True
            self.payload = payload

    @property
    def result(self):
        """If necessary, processes the request and returns the result.
        :rtype: dict
        """

        if self.__result is None:
            self.__result = self.process()
        return self.__result

    def validate(self, payload):
        """Perform initial payload validation.

        :type payload: dict
        :param payload: Payload dictionary
        :raise exceptions.BadPayload:
        :rtype: bool
        """

        if not isinstance(payload, dict):
            raise exc.BadPayload

    def process(self):
        """Processes the request and returns the result.
        :rtype: dict
        """

        raise NotImplementedError


class Authenticate(Request):
    """Yggdrasil authentication request."""

    def validate(self, payload):
        super().validate(payload)

        try:
            agent = payload.get("agent", None)
            assert agent == {"name": "Minecraft", "version": 1}
            client_token = payload.get("clientToken", None)
            if client_token is not None:
                assert isinstance(client_token, str)
        except AssertionError:
            raise exc.BadPayload

        try:
            username = payload.get("username", None)
            password = payload.get("password", None)
            assert all((username, password))
            assert isinstance(username, str) and isinstance(password, str)
        except AssertionError:
            raise exc.EmptyCredentials

    def process(self):
        """Authenticates a user using his password."""

    """The clientToken should be a randomly generated identifier
    and must be identical for each request. In case it is omitted the server
    will generate a random token based on Java's UUID.toString() which should
    then be stored by the client.

    This will however also invalidate all previously acquired accessTokens
    for this user across all clients."""


class Refresh(Request):
    """Yggdrasil refresh request."""

    def process(self):
        """Refreshes a valid accessToken.

        It can be uses to keep a user logged in between gaming sessions
        and is preferred over storing the user's password in a file.
        """


class Validate(Request):
    def process(self):
        """Checks if an accessToken is a valid session token with a
        currently-active session.

        .. note:
            This method will not respond successfully to all currently-logged-in
            sessions, just the most recently-logged-in for each user.

            It is intended to be used by servers to validate that a user should
            be connecting (and reject users who have logged in elsewhere since
            starting Minecraft), NOT to auth that a particular session token is
            valid for authentication purposes.

            To authenticate a user by session token, use the refresh verb and
            catch resulting errors.
        """


class Signout(Request):
    def process(self):
        """Invalidates accessTokens using an account's username and password."""


class Invalidate(Request):
    def process(self):
        """Invalidates accessTokens using a client/access token pair."""
