
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from welpurse.models.base_model import BaseModel, Base


class Beneficiary(BaseModel, Base):
    __tablename__ = 'beneficiaries'
    member_id = Column(String(60), ForeignKey('members.id'), nullable=False)
    name = Column(String(255), nullable=False)
    relation = Column(String(255), nullable=True)
    member = relationship("Member", back_populates="beneficiaries", cascade='all')