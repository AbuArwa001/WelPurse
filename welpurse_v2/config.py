from os import getenv
from dotenv import load_dotenv

load_dotenv()
class Config:
    SECRET_KEY = getenv("SECRET_KEY")
    JWT_SECRET_KEY = getenv("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = eval(getenv("JWT_TOKEN_LOCATION"))
    CELERY_BROKER_URL = getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = getenv("CELERY_RESULT_BACKEND")
    JWT_COOKIE_SECURE = False
    