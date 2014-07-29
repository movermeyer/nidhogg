from flask import Flask


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    from pages.views import pages_app
    from ajax.views import ajax_app

    app.register_blueprint(pages_app, url_prefix='/admin')
    app.register_blueprint(ajax_app, url_prefix='/ajax')

    return app
