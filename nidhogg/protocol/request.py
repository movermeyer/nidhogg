import uuid
import json

from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from common.database import db

from common.models import User, Token

from protocol import exceptions as exc


class Request:
    """Base class for Yggdrasil request"""

    __result = None

    def __init__(self, raw_payload):
        """
        :type raw_payload: bytes | str | dict
        :raise exceptions.BadPayload:
        """

        try:
            assert isinstance(raw_payload, (bytes, str))
            payload = raw_payload
            if isinstance(payload, bytes):
                payload = payload.decode()
            if isinstance(payload, str):
                payload = json.loads(payload)
        except (AssertionError, UnicodeError, ValueError):
            raise exc.BadPayload

        self.validate(payload)
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

    @staticmethod
    def _generate_token():
        """Generate random UUID token like Java's UUID.toString()

        :rtype: str
        """

        return uuid.uuid1().hex


class Authenticate(Request):
    """Yggdrasil authentication request."""

    def validate(self, payload):
        super().validate(payload)

        agent = payload.get("agent")
        if agent is not None:
            try:
                assert agent == {"name": "Minecraft", "version": 1}
            except AssertionError:
                raise exc.BadPayload

        client_token = payload.get("clientToken")
        if client_token is not None:
            try:
                assert isinstance(client_token, str)
                assert len(client_token)
            except AssertionError:
                raise exc.BadPayload

        try:
            assert all((payload.get("username"), payload.get("password")))
        except AssertionError:
            raise exc.EmptyCredentials

        try:
            assert isinstance(payload.get("password"), str)
            assert isinstance(payload.get("password"), str)
        except AssertionError:
            raise exc.InvalidCredentials

    def process(self):
        """Authenticates a user using his password.

        .. note::
            The clientToken should be a randomly generated identifier and must
            be identical for each request. In case it is omitted the server will
            generate a random token based on Java's UUID.toString() which should
            then be stored by the client.

            This will however also invalidate all previously acquired
            accessTokens for this user across all clients.
        """
        username = self.payload["username"]
        password = self.payload["password"]

        try:
            user = (
                User.query
                .filter(or_(User.login == username, User.email == username))
                .one()
            )
        except (NoResultFound, MultipleResultsFound):
            raise exc.InvalidCredentials

        if not user.check_password(raw_password=password):
            raise exc.InvalidCredentials

        if username == user.login:
            raise exc.MigrationDone

        token = Token()
        token.access = self._generate_token()
        token.client = self.payload.get("clientToken", self._generate_token())
        user.token = token

        db.session.commit()

        result = {"accessToken": token.access, "clientToken": token.client}

        if "agent" in self.payload:
            profile = {"id": token.client, "name": user.login}
            result["selectedProfile"] = profile
            result["availableProfiles"] = [profile]

        return result


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
