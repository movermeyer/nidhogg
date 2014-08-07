from flask import Blueprint

from protocol.utils import yggdrasil
from common.utils import json_response


protocol_app = Blueprint('protocol_app', __name__)


@protocol_app.route('/authenticate')
@yggdrasil
@json_response
def authenticate(payload):
    return


@protocol_app.route('/refresh')
@yggdrasil
@json_response
def refresh(payload):
    return


@protocol_app.route('/validate')
@yggdrasil
@json_response
def validate(payload):
    return


@protocol_app.route('/signout')
@yggdrasil
@json_response
def signout(payload):
    return


@protocol_app.route('/invalidate')
@yggdrasil
@json_response
def invalidate(payload):
    return


@json_response
def error_handler(exception):
    return exception.dictionary
