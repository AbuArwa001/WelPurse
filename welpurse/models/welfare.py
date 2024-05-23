
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import relationship, backref
from welpurse.models.base_model import BaseModel, Base
from welpurse.models.event import Event
from welpurse.models.member import Member
from welpurse.models.wallet import Wallet

class Welfare(BaseModel, Base):
    __tablename__ = 'welfares'
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    events = relationship('Event', backref='welfare', cascade='all, delete-orphan')
    members = relationship('Member', secondary='welfaremembers', back_populates='welfares')
    wallet = relationship('Wallet', uselist=False, back_populates='welfare', cascade='all, delete-orphan')
