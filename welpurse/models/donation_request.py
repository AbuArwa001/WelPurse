#!/usr/bin/python3

from sqlalchemy import Column, String, ForeignKey, DateTime, DECIMAL,Text
from sqlalchemy.orm import relationship, backref
from hashlib import md5
from welpurse.models.base_model import BaseModel, Base
from welpurse.models.member import Member
from datetime import datetime


class DonationRequest(BaseModel, Base):
    __tablename__ = 'donation_requests'
    id = Column(String(60), primary_key=True, nullable=False)
    reason = Column(Text, nullable=False)
    amount_requested = Column(DECIMAL(10, 2), nullable=False)
    member_id = Column(String(60), ForeignKey('members.id'), nullable=False)
    welfare_id = Column(String(60), ForeignKey('welfares.id'), nullable=False)
    status = Column(String(50), nullable=False, default='pending')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    member = relationship('Member', backref='donation_requests')
    welfare = relationship('Welfare', back_populates='requests')
