from settings import *

DEBUG = False
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}".format(
    **{
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
)
