from sqlalchemy import Column, String, DECIMAL, Date, ForeignKey
from sqlalchemy.orm import relationship
from welpurse_v2.models.base_model import BaseModel, Base
from .associations import transaction_transaction_types


class WalletTransaction(BaseModel, Base):
    __tablename__ = "wallet_transactions"
    wallet_id = Column(String(60), ForeignKey("wallets.id"), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=True)
    transaction_type = Column(String(255), nullable=True)
    date_transaction = Column(Date, nullable=True)

    transaction_types = relationship(
        "TransactionType",
        secondary=transaction_transaction_types,
        back_populates="wallet_transactions",
    )


from welpurse_v2.models.transactiontype import TransactionType
