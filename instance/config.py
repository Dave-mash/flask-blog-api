"""
This module sets up all the necessary configurations for the app
"""

import os

class Config:
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
    DB_URL = 'postgres://kevllcnzjjheqj:618fdd2780ace3d3087294da0c8152dcc70b71243f61b4dd95773e35f3a24ea5@ec2-54-197-232-203.compute-1.amazonaws.com:5432/d5638sardlpet5'


app_config = {
    'development': Development,
    'testing': Testing,
    'production': Production
}