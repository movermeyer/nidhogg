from flask import Blueprint
from common.utils import make_json

ajax_app = Blueprint('ajax_app', __name__)


@ajax_app.route('/tokens')
def tokens():
    data = [
        [1, 'Orhideous', 'orhideous@gmail.com', 'qwerty']
    ]
    return make_json(data)