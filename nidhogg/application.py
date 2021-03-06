# !/usr/bin/env python3
import os

from flask import Flask
from common.exceptions import NidhoggError

from nidhogg.protocol.yggdrasil.views import YggdrasilView
from nidhogg.protocol.legacy.views import LegacyView
from nidhogg.api.views import ApiView


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
        '/auth/<method>',
        view_func=YggdrasilView.as_view('generic'),
    )
    application.add_url_rule(
        '/auth/legacy/<method>',
        view_func=LegacyView.as_view('legacy'),
    )
    application.add_url_rule(
        '/api/<method>',
        view_func=ApiView.as_view('api'),
    )
    application.register_error_handler(NidhoggError, NidhoggError.handler)

    return application
