from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from nidhogg.common.database import DBSession, Base
from nidhogg.resources import root_factory


def main(global_config, **settings):
    """
        Main entry point

        :return: Pyramid WSGI application
        :rtype: pyramid.router.Router
    """

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings, root_factory=root_factory)
    config.add_static_view('static', 'static', cache_max_age=3600)

    return config.make_wsgi_app()
