import uuid
import json

from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from nidhogg.common.database import db
from nidhogg.common.models import User, Token
from nidhogg.protocol import exceptions as exc


class Request:
    """Base class for Yggdrasil request"""

    _result = None

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
        """Return result for request.
        :rtype: dict
        """
        return self._result

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

    @staticmethod
    def validate_credentials(payload):
        """Validates credentials format

        :type payload: dict
        :param payload: Dict containing username and password
        :raise exc.EmptyCredentials:
        :raise exc.InvalidCredentials:
        """

        username = payload.get("username")
        password = payload.get("password")

        try:
            assert username is not None and password is not None
        except AssertionError:
            raise exc.EmptyCredentials

        try:
            assert isinstance(username, str)
            assert isinstance(password, str)
        except AssertionError:
            raise exc.InvalidCredentials

    @staticmethod
    def get_user(username=None, password=None):
        """Get user object from database.

        :type username: str
        :param username: Username
        :type password: str
        :param password: Password
        :return: User instance
        :rtype: User
        :raise exc.InvalidCredentials:
        :raise exc.MigrationDone:
        """
        try:
            user = (
                User.query
                .options(joinedload('token'))
                .filter(or_(User.login == username, User.email == username))
                .one()
            )
        except (NoResultFound, MultipleResultsFound):
            raise exc.InvalidCredentials

        if not user.check_password(raw_password=password):
            raise exc.InvalidCredentials

        if username == user.login:
            raise exc.MigrationDone

        return user

    @staticmethod
    def validate_token_pair(payload):
        """Validates tokens format

        :type payload: dict
        :param payload: Dict containing accessToken and clientToken
        :raise exc.InvalidToken:
        """
        client_token = payload.get("clientToken")
        access_token = payload.get("accessToken")
        try:
            assert isinstance(client_token, str)
            assert isinstance(access_token, str)
            assert len(client_token)
            assert len(access_token)
        except AssertionError:
            raise exc.InvalidToken

    @staticmethod
    def get_token(client_token_value):
        """Fetches Token object by clientToken string

        :param client_token_value: clientToken value
        :type client_token_value: str
        :return: Token instance
        :rtype: Token
        :raise exc.InvalidToken:
        """
        try:
            token = (
                Token.query
                .filter(Token.client == client_token_value)
            ).one()
        except (NoResultFound, MultipleResultsFound):
            raise exc.InvalidToken
        else:
            return token


class Authenticate(Request):
    """Yggdrasil authentication request."""

    def validate(self, payload):
        super().validate(payload)
        self.validate_credentials(payload)

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

        user = self.get_user(
            username=self.payload.get("username"),
            password=self.payload.get("password")
        )
        token = user.token or Token()
        token.access = self._generate_token()
        token.client = self.payload.get("clientToken", self._generate_token())
        user.token = token

        db.session.commit()

        result = {"accessToken": token.access, "clientToken": token.client}

        if "agent" in self.payload:
            profile = {"id": token.client, "name": user.login}
            result["selectedProfile"] = profile
            result["availableProfiles"] = [profile]

        self._result = result


class Refresh(Request):
    """Yggdrasil refresh request."""

    def validate(self, payload):
        self.validate_token_pair(payload)

    def process(self):
        """Refreshes a valid accessToken.

        It can be uses to keep a user logged in between gaming sessions
        and is preferred over storing the user's password in a file.
        """

        token = self.get_token(self.payload.get("clientToken"))
        token.access = Request._generate_token()
        db.session.commit()

        self._result = {
            "accessToken": token.access,
            "clientToken": token.client
        }


class Validate(Request):
    """Yggdrasil validation request"""

    def validate(self, payload):
        try:
            access_token = payload.get("accessToken")
            assert isinstance(access_token, str)
            assert len(access_token)
        except AssertionError:
            raise exc.BadPayload

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
        try:
            (
                Token.query
                .filter(Token.access == self.payload.get("accessToken"))
            ).one()
        except (NoResultFound, MultipleResultsFound):
            raise exc.InvalidToken


class Signout(Request):
    """Yggdrasil sign out request"""

    def validate(self, payload):
        self.validate_credentials(payload)

    def process(self):
        """Invalidates accessTokens using an account's username and password."""
        user = self.get_user(
            username=self.payload.get("username"),
            password=self.payload.get("password")
        )
        db.session.delete(user.token)
        db.session.commit()


class Invalidate(Request):

    def validate(self, payload):
        self.validate_token_pair(payload)

    def process(self):
        """Invalidates accessTokens using a client/access token pair."""

        token = self.get_token(self.payload.get("clientToken"))
        db.session.delete(token)
        db.session.commit()
