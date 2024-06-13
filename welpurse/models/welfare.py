from sqlalchemy import Column, String, Integer, Text, Boolean, JSON
from sqlalchemy.orm import relationship, backref
from welpurse.models.base_model import BaseModel, Base
from welpurse.models.event import Event
from welpurse.models.member import Member
from welpurse.models.wallet import Wallet
from welpurse.models.donation_request import DonationRequest


class Welfare(BaseModel, Base):
    __tablename__ = "welfares"
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    purpose = Column(Text, nullable=True)
    min_contribution = Column(Integer, nullable=True)
    eligibility_requirements = Column(Text, nullable=True)
    membership_approval = Column(String(255), nullable=True)
    contribution_frequency = Column(String(50), nullable=True)
    contribution_modes = Column(Text, nullable=True)
    special_events = Column(Boolean, nullable=True)
    administrator = Column(String(255), nullable=True)
    treasurer = Column(String(255), nullable=True)
    secretary = Column(String(255), nullable=True)
    youth_rep = Column(String(255), nullable=True)
    chairperson = Column(String(255), nullable=True)
    vice_chairperson = Column(String(255), nullable=True)
    role_descriptions = Column(JSON, nullable=True)
    group_visibility = Column(String(50), nullable=True)
    searchable = Column(Boolean, nullable=True)
    preferred_communication_channel = Column(String(50), nullable=True)
    notification_preferences = Column(Text, nullable=True)
    events = relationship(
        "Event", backref="welfare", cascade="all, delete-orphan"
    )
    members = relationship(
        "Member", secondary="welfaremembers", back_populates="welfares"
    )
    wallet = relationship(
        "Wallet",
        uselist=False,
        back_populates="welfare",
        cascade="all, delete-orphan",
    )
    requests = relationship(
        "DonationRequest",
        back_populates="welfare",
        cascade="all, delete-orphan",
    )
