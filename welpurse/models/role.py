from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from welpurse.models.base_model import BaseModel, Base


class Role(BaseModel, Base):
    __tablename__ = 'roles'
    name = Column(String(255), nullable=False)

    members = relationship('Member', secondary='memberroles', back_populates='roles')
