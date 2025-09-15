"""Configuration settings for HTTPilot."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    ENV = 'development'


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    ENV = 'production'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    def __init__(self):
        if not self.SECRET_KEY:
            raise ValueError("No SECRET_KEY set for production environment")


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    ENV = 'testing'


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}