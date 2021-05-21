import os


class Config:
    DEBUG = True
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv("SECRET_KEY")
    JSON_AS_ASCII = False
