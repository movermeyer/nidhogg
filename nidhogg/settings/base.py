DEBUG = True
TESTING = False
SECRET_KEY = 'secret_key'
CURRENT_CMS = 'generic'
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}".format(
    **{
        'NAME': 'test',
        'USER': 'frontend',
        'PASSWORD': 'twilight',
        'HOST': 'localhost',
        'PORT': '3306',
    }
)