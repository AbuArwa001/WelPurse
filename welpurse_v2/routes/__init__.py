from flask import Blueprint


app_routes = Blueprint("app_routes", __name__)

from welpurse_v2.routes.main_routes import *
from welpurse_v2.routes.member_routes import *
from welpurse_v2.routes.contribute import *
from welpurse_v2.routes.creategroup import *
from welpurse_v2.routes.success import *
from welpurse_v2.routes.donation import *
from welpurse_v2.routes.events import *
