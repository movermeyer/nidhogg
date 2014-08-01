from settings import *

DEBUG = False
TESTING = True

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}".format(
    **{
        'NAME': 'test',
        'USER': 'frontend',
        'PASSWORD': 'twilight',
        'HOST': 'localhost',
        'PORT': '3306',
    }
)