from flask import Flask
from .celery_config import make_celery
from flask_jwt_extended import JWTManager
from os import getenv

jwt = JWTManager()
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = getenv('JWT_SECRET_KEY')
    app.config['JWT_TOKEN_LOCATION'] = eval(getenv('JWT_TOKEN_LOCATION'))
    app.config['CELERY_BROKER_URL'] = getenv('CELERY_BROKER_URL')
    app.config['CELERY_RESULT_BACKEND'] = getenv('CELERY_RESULT_BACKEND')
    app.config['JWT_COOKIE_SECURE'] = False
    # print(type(app.config['JWT_TOKEN_LOCATION']))
    jwt.init_app(app)

    from welpurse.routes import app_routes
    app.register_blueprint(app_routes)

    # Initialize Celery
    # celery = make_celery(app)
    # app.extensions['celery'] = celery
    # from welpurse.routes.example import example
    # app.register_blueprint(example)

    return app
