#!/usr/bin/env python3
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger

jwt = JWTManager()
cors = CORS()
swagger = Swagger()