import os

loginEmail = os.environ.get('LOGIN_EMAIL')
loginPassword = os.environ.get('LOGIN_PASSWORD')

SQLALCHEMY_DATABASE_URI = os.environ.get('JAWSDB_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_SECRET_KEY = 'dfsh3289349yhoelqwru9g'

MAILGUN_KEY = os.environ.get("MAILGUN_KEY")
MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
MAIL_SERVER = 'smtp.mailgun.org'
MAIL_PORT = 587
MAIL_USERNAME = os.environ.get("EMAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("EMAIL_PASS")