from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from nidhogg.auth import exceptions as exc
from nidhogg.common.database import DBSession
from nidhogg.common.models import User, Token
from nidhogg.common.utils import generate_token


def get_user(username, password):
    """Get user object from database.

    :type username: str
    :param username: Username
    :type password: str
    :param password: Password
    :return: User instance
    :rtype: User
    :raise exc.InvalidCredentials: Raised when no User match provided credentials
    :raise exc.MigrationDone: Raised when user account not migrated yet
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


def authenticate_user(user, client_token):
    """Authenticates a given user.

    :param user: User
    :type user: User
    :param client_token: clientToken from request
    :type client_token: str
    :return: User's auth token
    :rtype: Token

    .. note::
        This will however also invalidate all previously acquired
        accessTokens for this user across all clients.
    """
    token = user.token or Token()
    token.access = generate_token()
    token.client = client_token
    user.token = token

    DBSession.commit()

    return token


def get_token(client_token):
    """Fetches Token object by clientToken string

    :param client_token: clientToken value
    :type client_token: str
    :return: Token instance
    :rtype: Token
    :raise exc.InvalidToken:
    """
    try:
        token = (
            Token.query
            .filter(Token.client == client_token)
        ).one()
    except (NoResultFound, MultipleResultsFound):
        raise exc.InvalidToken
    else:
        return token


def refresh_token(token):
    """Refreshes accessToken in given valid token.

    It can be uses to keep a user logged in between
    gaming sessions and is preferred over storing
    the user's password in a file.

    :param token: Valid token
    :type token: Token
    :return: Refreshed token
    :rtype: Token
    """
    token.access = generate_token()
    DBSession.commit()

    return token


def validate_token(access_token):
    """Checks if given token belongs to currently-active session.

    :param access_token: Given accessToken for validation
    :type access_token: str

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
        Token.query.filter(Token.access == access_token).one()
    except (NoResultFound, MultipleResultsFound):
        raise exc.InvalidToken


def invalidate_token(token):
    """Invalidate given token"""

    DBSession.delete(token)
