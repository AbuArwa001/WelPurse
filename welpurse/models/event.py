from sqlalchemy import Column, String, Integer, ForeignKey, Date, Text
from welpurse.models.base_model import BaseModel, Base

class Event(BaseModel, Base):
    __tablename__ = 'events'
    welfare_id = Column(String(60), ForeignKey('welfares.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    event_date = Column(Date, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)