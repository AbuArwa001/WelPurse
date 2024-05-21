# welpurse/__init__.py
from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)
jwt = JWTManager()

def create_app():
    app.config['SECRET_KEY'] = 'e94d628d5bc552207aa4c4b1f6e87cb1'
    app.config['JWT_SECRET_KEY'] = 'e94d628d5bc552207aa4c4b1f6e87cb1'
    app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']

    jwt.init_app(app)

    from welpurse.routes import app_routes
    app.register_blueprint(app_routes)

    return app

