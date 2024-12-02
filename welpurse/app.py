from flask import Flask, session, redirect, url_for, flash

from welpurse.config import Config
# from .celery_config import make_celery
from flask_jwt_extended import JWTManager
# from os import getenv
from datetime import datetime
from .utils import refresh_token

# Add the filter to the app's Jinja2 environment

jwt = JWTManager()


def create_app(config_class=Config):
    app = Flask(__name__)

    @app.template_filter("parse_datetime")
    def parse_datetime(value, format="%a, %d %b %Y %H:%M:%S GMT"):
        return datetime.strptime(value, format)
    app.config.from_object(config_class)
    app.jinja_env.filters["parse_datetime"] = parse_datetime
    # print(type(app.config['JWT_TOKEN_LOCATION']))
    jwt.init_app(app)
    @app.before_request
    def refresh_token_on_activity():
        if "access_token" in session:
            # Attempt to refresh the token if it's close to expiring
            token_refreshed = refresh_token()
            if not token_refreshed:
                # Handle cases where refresh fails
                session.pop("access_token", None)
                session.pop("refresh_token", None)
                flash("Your session has expired. Please log in again.", "warning")
                return redirect(url_for("members.login"))

    from welpurse.main.route import main
    from welpurse.members.route import members
    from welpurse.contribute.route import contribute
    from welpurse.create_group.route import create_group
    from welpurse.success.route import success
    from welpurse.donation_req.route import donations
    from welpurse.events.route import events

    app.register_blueprint(main)
    app.register_blueprint(members)
    app.register_blueprint(create_group)
    app.register_blueprint(success)
    app.register_blueprint(donations)
    app.register_blueprint(events)

    # Initialize Celery
    # celery = make_celery(app)
    # app.extensions['celery'] = celery
    # from welpurse_v2.routes.example import example
    # app.register_blueprint(example)

    return app