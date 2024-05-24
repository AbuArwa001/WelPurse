
from sqlalchemy import Column, String, Integer, ForeignKey, DECIMAL, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship, backref
from welpurse.models.base_model import BaseModel, Base
from welpurse.models.transaction import WalletTransaction

class Wallet(BaseModel, Base):
    __tablename__ = 'wallets'
    welfare_id = Column(String(60), ForeignKey('welfares.id'), nullable=False, unique=True)
    available_balance = Column(DECIMAL(10, 2), nullable=True)
    can_disburse = Column(Boolean, nullable=True)
    currency = Column(String(10), nullable=True)
    current_balance = Column(DECIMAL(10, 2), nullable=True)
    label = Column(String(255), nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
    wallet_id = Column(String(10), nullable=True)
    wallet_type = Column(String(20), nullable=True)

    welfare = relationship('Welfare', back_populates='wallet')
    transactions = relationship('WalletTransaction', backref='wallet', cascade='all, delete-orphan')
