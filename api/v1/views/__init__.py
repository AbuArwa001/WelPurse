#!/usr/bin/python3
""" Blueprint for API """
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.mpesa.mpesa import *
from api.v1.intasend.intasend import *
from api.v1.views.member import *
from api.v1.views.welfare import *
from api.v1.views.wallet import *
from api.v1.views.beneficiary import *
from api.v1.views.dependent import *
from api.v1.views.events import *
from api.v1.views.contrribution import *
from api.v1.views.benefits import *
from api.v1.views.role import *
from api.v1.views.transaction import *
from api.v1.views.transactiontype import *