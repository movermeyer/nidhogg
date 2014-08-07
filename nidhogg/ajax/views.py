from flask import Blueprint

from common.database import db
from common.models import User, Token
from common.utils import json_response


ajax_app = Blueprint('ajax_app', __name__)


@ajax_app.route('/tokens')
@json_response
def tokens():
    query = db.session.query(User.id, User.login, User.email, Token.value).outerjoin(Token)
    return [row._asdict() for row in query]
