# api/v1/app.py
from flask import Flask, make_response, jsonify
from dotenv import load_dotenv, dotenv_values

load_dotenv()
from os import getenv
from .config import Config
from .extensions import cors, swagger, jwt
from .views import app_views
from .auth import auth_blueprint


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/v2/*": {"origins": "*"}})
    swagger.init_app(app)

    app.register_blueprint(app_views)
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({"error": "Not found"}), 404)

    return app
