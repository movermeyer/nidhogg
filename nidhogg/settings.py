
# flask core settings
DEBUG = True
TESTING = False
SECRET_KEY = 'qh\x98\xc4o\xc4]\x8f\x8d\x93\xa4\xec\xc5\xfd]\xf8\xb1c\x84\x86\xa7A\xcb\xc0'
PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 30

# flask mail settings
MAIL_DEFAULT_SENDER = 'noreply@yourmail.com'

# project settings
PROJECT_PASSWORD_HASH_METHOD = 'pbkdf2:sha1'
PROJECT_SITE_NAME = 'Flask Example'
PROJECT_SITE_URL = 'http://127.0.0.1:5000/'
PROJECT_SIGNUP_TOKEN_MAX_AGE = 60 * 60 * 24 * 7
PROJECT_RECOVER_PASSWORD_TOKEN_MAX_AGE = 60 * 60 * 24 * 7
