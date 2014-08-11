DEBUG = True
TESTING = False
SECRET_KEY = 'qh\x98\xc4o\xc4]\x8f\x8d\x93\xa4\xec\xc5\xfd]\xf8\xb1c\x84\x86\xa7A\xcb\xc0'
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
