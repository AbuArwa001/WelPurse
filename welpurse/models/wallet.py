
from sqlalchemy import Column, String, Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship, backref
from welpurse.models.base_model import BaseModel, Base
from welpurse.models.transaction import WalletTransaction

class Wallet(BaseModel, Base):
    __tablename__ = 'wallets'
    welfare_id = Column(String(60), ForeignKey('welfares.id'), nullable=False, unique=True)
    balance = Column(DECIMAL(10, 2), nullable=True)

    welfare = relationship('Welfare', back_populates='wallet')
    transactions = relationship('WalletTransaction', backref='wallet', cascade='all, delete-orphan')
