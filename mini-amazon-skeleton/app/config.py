import os
import secrets


class Config(object):
    SECRET_KEY = secrets.token_hex(16) #  os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@localhost/{}'\
        .format(os.environ.get('DB_USER'),
                os.environ.get('DB_PASSWORD'),
                os.environ.get('DB_NAME'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = 'cs516'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'cs516.miniamzon@gmail.com'
    MAIL_PASSWORD = 'cs516amazon'