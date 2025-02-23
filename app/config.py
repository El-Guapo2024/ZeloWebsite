import os
class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig:
    DEBUG = True    
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', "postgresql://juanantonioluera:tino@localhost:5432/flask_prod_db")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY','prod')