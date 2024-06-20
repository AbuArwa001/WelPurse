#!/usr/bin/python3

from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from hashlib import md5
from welpurse_v2.models.base_model import BaseModel, Base
from welpurse_v2.models.beneficiary import Beneficiary
from welpurse_v2.models.benefit import Benefit
from welpurse_v2.models.contribution import Contribution
from welpurse_v2.models.dependent import Dependent
from welpurse_v2.models.role import Role


# Association Tables
memberroles = Table(
    "memberroles",
    Base.metadata,
    Column(
        "member_id", String(60), ForeignKey("members.id"), primary_key=True
    ),
    Column("role_id", String(60), ForeignKey("roles.id"), primary_key=True),
)


class Member(BaseModel, Base):
    __tablename__ = "members"
    # id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))
    beneficiaries = relationship(
        "Beneficiary", back_populates="member", cascade="all, delete-orphan"
    )
    benefits = relationship(
        "Benefit", backref="member", cascade="all, delete-orphan"
    )
    contributions = relationship(
        "Contribution", backref="member", cascade="all, delete-orphan"
    )
    dependents = relationship(
        "Dependent", backref="member", cascade="all, delete-orphan"
    )
    roles = relationship(
        "Role", secondary="memberroles", back_populates="members"
    )
    welfares = relationship(
        "Welfare", secondary="welfaremembers", back_populates="members"
    )

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)


from welpurse_v2.models.welfare import Welfare
