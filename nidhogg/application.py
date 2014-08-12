# !/usr/bin/env python3
from flask import Flask

from protocol.exceptions import YggdrasilError, error_handler
from protocol.views import YggdrasilView
import os


def create_app():
    config = os.environ.setdefault(
        'NIDHOGG_SETTINGS_MODULE',
        'nidhogg.settings.base'
    )
    application = Flask(__name__)
    application.config.from_object(config)

    from common.database import db

    db.init_app(application)

    from pages.views import pages_app
    from ajax.views import ajax_app

    application.register_blueprint(pages_app, url_prefix='/admin')
    application.register_blueprint(ajax_app, url_prefix='/ajax')
    application.add_url_rule(
        '/<method>',
        view_func=YggdrasilView.as_view('generic'),
    )
    application.register_error_handler(YggdrasilError, error_handler)

    return application
