"""This module declares the app configuration.

The classes include:

BaseConfig:
    Has all the configurations shared by all the environments.

"""
import os

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    """Base configuration."""

    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ["SECRET_KEY"]
    db_conn_string = 'sqlite:///./butterfly.db'
    SQLALCHEMY_DATABASE_URI = db_conn_string
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development confuguration."""

    DEBUG = True
    TESTING = False
    

class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING = True
    SECRET_KEY = 'secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'

class ProductionConfig(BaseConfig):
    """Production configuration."""

    TESTING = False


Config = {
    "development": DevelopmentConfig,
    "test": TestingConfig,
    "production": ProductionConfig,
    "staging": ProductionConfig,
}
