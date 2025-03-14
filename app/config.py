import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')



class DevelopmentConfig(Config):
    DEBUG = True    
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', "postgresql://juanantonioluera:tino@localhost:5432/flask_prod_db")
    print("DATABASE_URL", SQLALCHEMY_DATABASE_URI)


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL environment variable is not set in production!")
    print("Production DATABASE_URL:", SQLALCHEMY_DATABASE_URI)