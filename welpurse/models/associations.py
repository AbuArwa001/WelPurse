from sqlalchemy import Column, String, ForeignKey, Table
from welpurse.models.base_model import Base

transaction_transaction_types = Table('transaction_transaction_types', Base.metadata,
    Column('transaction_id', String(60), ForeignKey('wallet_transactions.id'), primary_key=True),
    Column('type_id', String(60), ForeignKey('transactiontypes.id'), primary_key=True)
)
# Association Tables
memberroles = Table('memberroles', Base.metadata,
    Column('member_id', String(60), ForeignKey('members.id'), primary_key=True),
    Column('role_id', String(60), ForeignKey('roles.id'), primary_key=True)
)

welfaremembers = Table('welfaremembers', Base.metadata,
    Column('welfare_id', String(60), ForeignKey('welfares.id'), primary_key=True),
    Column('member_id', String(60), ForeignKey('members.id'), primary_key=True)
)