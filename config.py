import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    DEBUG=False
    SECRET_KEY = os.environ.get('SECRET_KEY', '1234')   # , FALLBACK_SECRET_KEY


class DevelopmentConfig(Config):
    DEBUG=True

class ProductionConfig(Config):
    DEBUG=False
