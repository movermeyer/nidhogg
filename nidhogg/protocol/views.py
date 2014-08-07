from flask import Blueprint

from protocol.utils import yggdrasil
from common.utils import json_response


protocol_app = Blueprint('protocol_app', __name__)


@protocol_app.route('/authenticate')
@yggdrasil
@json_response
def authenticate():
    return


@protocol_app.route('/refresh')
@yggdrasil
@json_response
def refresh():
    return


@protocol_app.route('/validate')
@yggdrasil
@json_response
def validate():
    return


@protocol_app.route('/signout')
@yggdrasil
@json_response
def signout():
    return


@protocol_app.route('/invalidate')
@yggdrasil
@json_response
def invalidate():
    return


@json_response
def error_handler(exception):
    return exception.dictionary
