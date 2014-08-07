#!/usr/bin/env python3
from flask import Flask


def create_app(config_filename):

    application = Flask(__name__)
    application.config.from_object(config_filename)

    from common.database import db
    db.init_app(application)

    from pages.views import pages_app
    from ajax.views import ajax_app
    from protocol.views import protocol_app

    application.register_blueprint(pages_app, url_prefix='/admin')
    application.register_blueprint(ajax_app, url_prefix='/ajax')
    application.register_blueprint(protocol_app)

    return application
