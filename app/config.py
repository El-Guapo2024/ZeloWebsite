import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')


class DevelopmentConfig(Config):
    DEBUG = True    
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', "postgresql://juanantonioluera:tino@localhost:5432/flask_prod_db")


class ProductionConfig(Config):
    DEBUG = False
    # Use the base Config's DATABASE_URL
    # This ensures we use the exact URL provided in environment variables
    SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI