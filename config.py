import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "your_secret_key")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "your_jwt_secret_key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///contacts.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
