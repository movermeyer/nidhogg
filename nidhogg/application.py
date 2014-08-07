# !/usr/bin/env python3
from flask import Flask

from protocol.exceptions import YggdrasilError


def create_app(config_filename):
    application = Flask(__name__)
    application.config.from_object(config_filename)

    from common.database import db

    db.init_app(application)

    from pages.views import pages_app
    from ajax.views import ajax_app
    from protocol.views import protocol_app, error_handler

    application.register_blueprint(pages_app, url_prefix='/admin')
    application.register_blueprint(ajax_app, url_prefix='/ajax')
    application.register_blueprint(protocol_app)
    application.register_error_handler(YggdrasilError, error_handler)

    return application
