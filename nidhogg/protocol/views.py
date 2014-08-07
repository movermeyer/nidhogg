from flask import Blueprint

protocol_app = Blueprint('protocol_app', __name__)


@protocol_app.route('/authenticate')
def authenticate():
    return

@protocol_app.route('/refresh')
def refresh():
    return

@protocol_app.route('/validate')
def validate():
    return

@protocol_app.route('/signout')
def signout():
    return

@protocol_app.route('/invalidate')
def invalidate():
    return
