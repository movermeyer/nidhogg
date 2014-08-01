from flask import Blueprint

from common.database import db
from common.models import User, Token
from common.utils import make_json_response


ajax_app = Blueprint('ajax_app', __name__)


@ajax_app.route('/tokens')
def tokens():
    query = db.session.query(User.id, User.login, User.email, Token.value).outerjoin(Token)
    return make_json_response([row._asdict() for row in query])
