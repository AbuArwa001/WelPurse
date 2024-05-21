from flask import Blueprint


app_routes = Blueprint("app_routes", __name__)

from welpurse.routes.main_routes import *
from welpurse.routes.member_routes import *
from welpurse.routes.contribute import *
