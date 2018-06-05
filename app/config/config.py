"""
    Object-based configuration. Use HerokuConfig in production, BaseConfig
    otherwise.
"""

import os

class BaseConfig(object):
    BCRYPT_LOG_ROUNDS = 10
    DEBUG = True
    SECRET_KEY = "AllYourBaseAreBelongToUs"
    SQLALCHEMY_DATABASE_URI = "sqlite:///sholdr.db"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class HerokuConfig(BaseConfig):
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_ECHO = False
