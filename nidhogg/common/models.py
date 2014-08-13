import os
from importlib import import_module

from sqlalchemy.orm import relationship, backref

from nidhogg.common.database import db


hasher_name = os.environ.setdefault(
    'NIDHOGG_HASHER_MODULE',
    'nidhogg.common.hashers.generic'
)
config_name = os.environ.setdefault(
    'NIDHOGG_SETTINGS_MODULE',
    'nidhogg.settings.base'
)

hasher = import_module(hasher_name)
config = import_module(config_name)


class User(db.Model):
    """User model for mapping to existing table"""

    __tablename__ = config.DB.table

    id = db.Column(config.DB.id, db.Integer, primary_key=True)
    login = db.Column(config.DB.login, db.String(255))
    email = db.Column(config.DB.email, db.String(255))
    password = db.Column(config.DB.password, db.String(255))

    def __repr__(self):
        return '<{0}: [{1}] {2}>'.format(
            self.__class__.__name__,
            self.id,
            self.login
        )

    def check_password(self, raw_password):
        return hasher.check_password(raw=raw_password, hash=self.password)

    def set_password(self, raw_password):
        self.password = hasher.make_password(raw=raw_password)


class Token(db.Model):
    """Token model, used for authentication"""

    __tablename__ = 'minecraft_tokens'

    id = db.Column(db.Integer, primary_key=True)
    access = db.Column(db.String(32), nullable=True)
    client = db.Column(db.String(32), nullable=True)
    created = db.Column(
        db.TIMESTAMP,
        server_default=db.func.now(),
        onupdate=db.func.current_timestamp()
    )
    user = relationship(
        'User',
        uselist=False,
        backref=backref("token", uselist=False)
    )
    user_id = db.Column(db.ForeignKey(User.id))

    def __repr__(self):
        return '<{0}: [{1}] {2}>'.format(
            self.__class__.__name__,
            self.id,
            self.user_id
        )
