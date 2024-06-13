from sqlalchemy import Column, String, DateTime, ForeignKey, DECIMAL, Text
from welpurse.models.base_model import BaseModel, Base
from datetime import datetime


class Event(BaseModel, Base):
    __tablename__ = "events"
    welfare_id = Column(String(60), ForeignKey("welfares.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    event_date = Column(DateTime, nullable=True)
    status = Column(String(50), nullable=False)
    start_date = Column(DateTime, nullable=True, default=datetime.utcnow())
    end_date = Column(DateTime, nullable=True)
    target_amount = Column(DECIMAL(10, 2), nullable=False)
