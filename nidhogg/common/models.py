import configparser
from settings import CURRENT_CMS
from os.path import dirname, join
from .database import db


config = configparser.ConfigParser()
config.read(join(dirname(__file__), 'cms.ini'))

cms_config = config[CURRENT_CMS]


class User(db.Model):
    __tablename__ = cms_config['table']

    id = db.Column(cms_config['id'], db.Integer, primary_key=True)
    login = db.Column(cms_config['login'], db.String(255))
    email = db.Column(cms_config['email'], db.String(255))
    password = db.Column(cms_config['password'], db.String(255))

    def __repr__(self):
        return '<{0}: [{1}] {2}>'.format(self.__class__.__name__, self.id, self.login)
