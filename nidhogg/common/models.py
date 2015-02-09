from sqlalchemy import Column, String, TIMESTAMP, func, ForeignKey, Integer
from sqlalchemy.orm import relationship, backref
from common.database import Base


class User(Base):
    """User model"""

    id = Column(Integer, primary_key=True)
    login = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))

    def __repr__(self):
        return '<{0}: [{1}] {2}>'.format(
            self.__class__.__name__,
            self.id,
            self.login
        )


class Token(Base):
    """Token model, used for authentication"""

    id = Column(Integer, primary_key=True)
    access = Column(String(32), nullable=True)
    client = Column(String(32), nullable=True)
    created = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.current_timestamp()
    )
    user = relationship(
        'User',
        uselist=False,
        backref=backref("token", uselist=False)
    )
    user_id = Column(ForeignKey(User.id))

    def __repr__(self):
        return '<{0}: [{1}] {2}>'.format(
            self.__class__.__name__,
            self.id,
            self.user_id
        )
