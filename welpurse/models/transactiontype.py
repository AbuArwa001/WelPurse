from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from welpurse.models.base_model import BaseModel, Base

from .associations import transaction_transaction_types


class TransactionType(BaseModel, Base):
    __tablename__ = "transactiontypes"
    name = Column(String(255), nullable=False)

    wallet_transactions = relationship(
        "WalletTransaction",
        secondary=transaction_transaction_types,
        back_populates="transaction_types",
    )


from welpurse.models.transaction import WalletTransaction
