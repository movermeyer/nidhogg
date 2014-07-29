from flask import Blueprint

from common.utils import make_json_response


ajax_app = Blueprint('ajax_app', __name__)


@ajax_app.route('/tokens')
def tokens():
    data = [
        {
            'id': 1,
            'login': 'Orhideous',
            'email': 'orhideous@gmail.com',
            'token': 'qwerty'
        },
    ]
    return make_json_response(data)