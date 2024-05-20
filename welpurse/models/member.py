#!/usr/bin/python3

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from hashlib import md5
from welpurse.models.base_model import BaseModel, Base

class Member(BaseModel, Base):
    __tablename__ = 'members'
    # id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)


# class Contribution(db.Model):
#     __tablename__ = 'contributions'
#     contributnId = db.Column(db.Integer, primary_key=True)
#     memberId = db.Column(db.Integer, db.ForeignKey('members.memberId'))
#     amount = db.Column(db.Numeric(10, 2))
#     dateContributed = db.Column(db.Date)


