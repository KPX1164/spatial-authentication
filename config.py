import os

SECRET_KEY = os.urandom(32)

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'mysql://root:password@127.0.0.1:3306/spatial-authentication'

SQLAlCHEMY_TRACK_MODIFICATIONS = False
JSON_SORT_KEYS = False
CORS_HEADERS = 'Content-Type'

MAX_CONTENT_LENGTH = 16*1024*1024

SQLAlCHEMY_POOL_SIZE = 30
SQLAlCHEMY_POOL_TIMEOUT = 300