from sqlalchemy import Column, String, Enum, ForeignKey, DECIMAL, Date
from sqlalchemy.orm import relationship, backref
from hashlib import md5
from welpurse.models.base_model import BaseModel, Base

class Contribution(BaseModel, Base):
    __tablename__ = 'contributions'
    member_id = Column(String(60), ForeignKey('members.id'), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=True)
    date_contributed = Column(Date, nullable=True)
    contribution_type = Column(Enum('monthly', 'event'), nullable=False)
    event_id = Column(String(60), ForeignKey('events.id'), nullable=True)
