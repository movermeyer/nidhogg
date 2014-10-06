from time import time

from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from nidhogg.common.utils import generate_token
from nidhogg.common.database import db
from nidhogg.common.models import User, Token
from nidhogg.legacy import exceptions as exc


class LegacyRequest:

    _result = None

    def __init__(self, raw_payload):
        self.validate(raw_payload)
        self.payload = raw_payload

    def validate(self, payload):
        try:
            assert isinstance(payload, dict)
        except AssertionError:
            raise exc.BadPayload

        try:
            assert len(payload)
        except AssertionError:
            raise exc.EmptyPayload

        try:
            assert all((isinstance(key, str) for key in payload.keys()))
            assert all((isinstance(value, str) for value in payload.values()))
        except AssertionError:
            raise exc.BadPayload

    @property
    def result(self):
        if isinstance(self._result, tuple):
            return ':'.join(self._result)
        else:
            return self._result

    def process(self):
        """Processes the request and returns the result.
        :rtype: str
        """

        raise NotImplementedError


class Authenticate(LegacyRequest):

    def validate(self, payload):
        super().validate(payload)
        try:
            assert all(
                (
                    bool(item) for item in
                    (payload.get(key) for key in ['user', 'password'])
                )
            )
        except AssertionError:
            raise exc.EmptyCredentials

    def process(self):
        username = self.payload.get('user')
        password = self.payload.get('password')

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

        token = user.token or Token()
        token.access = generate_token()
        token.client = generate_token()
        user.token = token

        db.session.commit()

        self._result = (
            str(int(time())),
            'deprecated',
            user.login,
            token.access,
            token.client
        )


class _Validate(LegacyRequest):
    def validate(self, payload):
        try:
            assert all(
                (
                    bool(item) for item in
                    (payload.get(key) for key in ['user', 'sessionId'])
                )
            )
        except AssertionError:
            raise exc.EmptyCredentials

    def process(self):
        session_id = self.payload.get("sessionId")
        username = self.payload.get('user')

        try:
            (
                Token.query
                .filter(
                    Token.access == session_id,
                    or_(User.login == username, User.email == username)
                )
                .join(User)
                .one()
            )
        except (NoResultFound, MultipleResultsFound):
            raise exc.BadPayload


class Check(_Validate):
    def process(self):
        super().process()
        self._result = "YES"


class Join(_Validate):
    def process(self):
        super().process()
        self._result = "OK"
