import os

class DevelopmentConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-hotel-majda-2024')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hotel.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
