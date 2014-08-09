import configparser
from os.path import dirname, join
from importlib import import_module

from sqlalchemy.orm import relationship, backref

from settings import CURRENT_CMS
from common.database import db


config = configparser.ConfigParser()
config.read(join(dirname(__file__), 'cms.ini'))

cms_config = config[CURRENT_CMS]
hasher = import_module('common.hashers.' + CURRENT_CMS)


class User(db.Model):
    __tablename__ = cms_config['table']

    id = db.Column(cms_config['id'], db.Integer, primary_key=True)
    login = db.Column(cms_config['login'], db.String(255))
    email = db.Column(cms_config['email'], db.String(255))
    password = db.Column(cms_config['password'], db.String(255))

    def __repr__(self):
        return '<{0}: [{1}] {2}>'.format(self.__class__.__name__, self.id, self.login)

    def check_password(self, raw_password):
        return hasher.check_password(raw=raw_password, hash=self.password)

    def set_password(self, raw_password):
        self.password = hasher.make_password(raw=raw_password)


class Token(db.Model):
    __tablename__ = 'minecraft_tokens'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(36), nullable=True, unique=True)
    user = relationship('User', uselist=False, backref=backref("token", uselist=False))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
