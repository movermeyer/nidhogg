# !/usr/bin/env python3
from flask import Flask

from nidhogg.protocol.exceptions import YggdrasilError, error_handler
from nidhogg.protocol.views import YggdrasilView
import os


def create_app():
    """Flask application factory

    :rtype: Flask
    """

    config = os.environ.setdefault(
        'NIDHOGG_SETTINGS_MODULE',
        'nidhogg.settings.base'
    )
    application = Flask(__name__)
    application.config.from_object(config)

    from nidhogg.common.database import db

    db.init_app(application)

    application.add_url_rule(
        '/<method>',
        view_func=YggdrasilView.as_view('generic'),
    )
    application.register_error_handler(YggdrasilError, error_handler)

    return application
