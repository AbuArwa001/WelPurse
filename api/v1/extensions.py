#!/usr/bin/env python3


from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger
from flask_login import LoginManager


login_manager = LoginManager()

@login_manager.user_loader
def load_user(member_id):
    from welpurse.models.member import Member
    return Member.query.get(int(member_id))

jwt = JWTManager()
cors = CORS()
swagger = Swagger()