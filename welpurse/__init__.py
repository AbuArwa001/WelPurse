# welpurse/__init__.py
from flask import Flask
from flask_jwt_extended import JWTManager
from os import getenv
app = Flask(__name__)
jwt = JWTManager()

def create_app():
    app.config['SECRET_KEY'] = getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = getenv('JWT_SECRET_KEY')
    app.config['JWT_TOKEN_LOCATION'] = getenv('JWT_TOKEN_LOCATION')


    jwt.init_app(app)

    from welpurse.routes import app_routes
    app.register_blueprint(app_routes)

    return app

