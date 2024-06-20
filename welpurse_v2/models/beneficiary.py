from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from welpurse_v2.models.base_model import BaseModel, Base


class Beneficiary(BaseModel, Base):
    __tablename__ = "beneficiaries"
    member_id = Column(String(60), ForeignKey("members.id"), nullable=False)
    dependent_id = Column(
        String(60), ForeignKey("dependents.id"), nullable=False
    )
    name = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False, default="inactive")
    relation = Column(String(255), nullable=True)
    member = relationship(
        "Member", back_populates="beneficiaries", cascade="all"
    )
