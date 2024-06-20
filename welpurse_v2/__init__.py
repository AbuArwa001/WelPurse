from flask import Flask
from .celery_config import make_celery
from flask_jwt_extended import JWTManager
from os import getenv
from datetime import datetime

# Add the filter to the app's Jinja2 environment

jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    @app.template_filter("parse_datetime")
    def parse_datetime(value, format="%a, %d %b %Y %H:%M:%S GMT"):
        return datetime.strptime(value, format)

    app.config["SECRET_KEY"] = getenv("SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = getenv("JWT_SECRET_KEY")
    app.config["JWT_TOKEN_LOCATION"] = eval(getenv("JWT_TOKEN_LOCATION"))
    app.config["CELERY_BROKER_URL"] = getenv("CELERY_BROKER_URL")
    app.config["CELERY_RESULT_BACKEND"] = getenv("CELERY_RESULT_BACKEND")
    app.config["JWT_COOKIE_SECURE"] = False
    app.jinja_env.filters["parse_datetime"] = parse_datetime
    # print(type(app.config['JWT_TOKEN_LOCATION']))
    jwt.init_app(app)

    from welpurse_v2.routes import app_routes

    app.register_blueprint(app_routes)

    # Initialize Celery
    # celery = make_celery(app)
    # app.extensions['celery'] = celery
    # from welpurse_v2.routes.example import example
    # app.register_blueprint(example)

    return app
