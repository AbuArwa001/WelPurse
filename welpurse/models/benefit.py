
from sqlalchemy import Column, String, Date, Text, DECIMAL, ForeignKey
from hashlib import md5
from welpurse.models.base_model import BaseModel, Base

class Benefit(BaseModel, Base):
    __tablename__ = 'benefits'
    member_id = Column(String(60), ForeignKey('members.id'), nullable=False)
    description = Column(Text, nullable=True)
    amount = Column(DECIMAL(10, 2), nullable=True)
    date_received = Column(Date, nullable=True)
