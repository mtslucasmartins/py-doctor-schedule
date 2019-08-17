import os 
import datetime as dt

# Application
SECRET_KEY = os.urandom(24)
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = os.environ.get('PORT', 5000)

DEV_DATABASE = 'postgres://jzhmhjsctmarpn:bd2133f05cd0655ecb5d59da2bea46c6470391d98978f352fade1f8cbd0565ef@ec2-75-101-147-226.compute-1.amazonaws.com:5432/dk0hsvd2jciu'

# Database
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', DEV_DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

# JWT
JWT_SECRET_KEY = os.urandom(24)
JWT_EXPIRATION_DELTA = dt.timedelta(seconds=3600) # a datetime.timedelta indicating how long tokens are valid for.
JWT_ACCESS_TOKEN_EXPIRES = dt.timedelta(seconds=3600)
JWT_REFRESH_TOKEN_EXPIRES = dt.timedelta(days=30)

# RESTful
BUNDLE_ERRORS = True