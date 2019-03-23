"""
This module sets up all the necessary configurations for the app
"""

import os

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY')


class Development(Config):
    """Configurations for Development."""
    ENV = "development"
    DEBUG = True
    TESTING = True
    DB_URL = os.getenv('FLASK_DATABASE_URI')


class Testing(Config):
    """Configurations for Testing, with a separate test database."""
    ENV = "testing"
    TESTING = True
    DEBUG = True
    DB_URL = os.getenv('TEST_DATABASE_URI')


class Production(Config):
    """Configurations for Production."""
    ENV = "production"
    DEBUG = False
    TESTING = False
    DB_URL = os.environ['FLASK_DATABASE_URI']
    SECRET_KEY = os.environ['SECRET_KEY']

app_config = {
    'development': Development,
    'testing': Testing,
    'production': Production
}