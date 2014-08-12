DEBUG = True
TESTING = False
SECRET_KEY = 'secret_key'

SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class DB:
    table = 'users'
    id = 'id'
    login = 'login'
    email = 'email'
    password = 'password'