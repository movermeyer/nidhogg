DEBUG = True
TESTING = False
SECRET_KEY = 'secret_key'

SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # SQLAlchemy connection URI


class DB:
    """Mapping to existing table with user data."""

    table = 'users'
    id = 'id'
    login = 'login'
    email = 'email'
    password = 'password'
