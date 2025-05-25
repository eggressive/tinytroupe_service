"""
Configuration management for TinyTroupe Service
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Get the path to the .env file relative to this config file
env_path = Path(__file__).parent.parent / '.env'

# Load environment variables from .env file
load_dotenv(env_path)

class Config:
    """Base configuration"""
    # TinyTroupe API configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
    AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION', '2023-05-15')
    
    # Database configuration
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///tinytroupe.db')
    
    # Financial API configuration
    YAHOO_FINANCE_API_KEY = os.getenv('YAHOO_FINANCE_API_KEY')
    ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
    
    # Application configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret_key')
    DEBUG = os.getenv('FLASK_DEBUG', 'False') == 'True'
    
    # Advisor configuration
    DEFAULT_ADVISORS = [
        {
            'id': 'warren_buffett',
            'name': 'Warren Buffett',
            'description': 'The most successful investor of modern times with a 20% annualized return over 55+ years.',
            'expertise': ['value investing', 'business analysis', 'capital allocation']
        },
        {
            'id': 'john_keynes',
            'name': 'John Maynard Keynes',
            'description': 'Revolutionary economist who was also an exceptional practical investor.',
            'expertise': ['macroeconomics', 'contrarian investing', 'market psychology']
        },
        {
            'id': 'benjamin_graham',
            'name': 'Benjamin Graham',
            'description': 'The "Father of Value Investing" whose books created the intellectual foundation for generations of investors.',
            'expertise': ['value investing', 'margin of safety', 'fundamental analysis']
        },
        {
            'id': 'albert_einstein',
            'name': 'Albert Einstein',
            'description': 'Renowned physicist with analytical thinking and pattern recognition abilities.',
            'expertise': ['pattern recognition', 'systems thinking', 'thought experiments']
        }
    ]

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DATABASE_URI = 'sqlite:///:memory:'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get the current configuration"""
    env = os.getenv('FLASK_ENV', 'default')
    return config.get(env, config['default'])
