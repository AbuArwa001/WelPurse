#!/usr/bin/env python3
"welpurse app"
from flask import Flask, render_template
import os
import uuid
from welpurse.routes import app_routes
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '1545d4c68638f11975345058719b854f'
app.config['JWT_SECRET_KEY'] = '1545d4c68638f11975345058719b854f'  # Replace with your actual secret key
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']  # Specify where to look for the token

jwt = JWTManager(app)
app.register_blueprint(app_routes)



def css(css_file):
    return render_template(f'{css_file}.css.jinja'), 200, {'Content-Type': 'text/css'}


