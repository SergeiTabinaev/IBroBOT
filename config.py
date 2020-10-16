
SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://postgres:initeb53@localhost/SmitShablon'


class Configuration(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URL
