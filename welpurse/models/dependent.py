from sqlalchemy import Column, String, Integer, ForeignKey, Date
from welpurse.models.base_model import BaseModel, Base


class Dependent(BaseModel, Base):
    __tablename__ = "dependents"
    member_id = Column(String(60), ForeignKey("members.id"), nullable=False)
    name = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False, default="active")
    relation = Column(String(255), nullable=False)
    date_of_birth = Column(Date, nullable=True)
