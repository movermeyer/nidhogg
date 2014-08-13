"""AJAX-related views"""

from flask import Blueprint

from nidhogg.common.database import db
from nidhogg.common.models import User, Token
from nidhogg.common.utils import json_response


ajax_app = Blueprint('ajax_app', __name__)


@ajax_app.route('/tokens')
@json_response
def tokens():
    """Return all registered users and their tokens."""
    query = db.session.query(
        User.id,
        User.login,
        User.email,
        Token.created
    ).outerjoin(Token)
    return [row._asdict() for row in query]
