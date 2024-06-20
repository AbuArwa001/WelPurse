#!/usr/bin/python3
"""
Contains the class DBStorage
"""
import welpurse
from welpurse_v2.models.base_model import BaseModel, Base
from welpurse_v2.models.member import Member
from welpurse_v2.models.welfare import Welfare
from welpurse_v2.models.wallet import Wallet
from welpurse_v2.models.beneficiary import Beneficiary
from welpurse_v2.models.dependent import Dependent
from welpurse_v2.models.event import Event
from welpurse_v2.models.contribution import Contribution
from welpurse_v2.models.benefit import Benefit
from welpurse_v2.models.role import Role
from welpurse_v2.models.transaction import WalletTransaction
from welpurse_v2.models.transactiontype import TransactionType
from welpurse_v2.models.donation_request import DonationRequest
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

classes = {
    "Member": Member,
    "Welfare": Welfare,
    "Wallet": Wallet,
    "Beneficiary": Beneficiary,
    "Dependent": Dependent,
    "Event": Event,
    "Contribution": Contribution,
    "Benefit": Benefit,
    "Role": Role,
    "WalletTransaction": WalletTransaction,
    "TransactionType": TransactionType,
    "DonationRequest": DonationRequest,
}


class DBStorage:
    """interaacts with the MySQL database"""

    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        MYSQL_USER = getenv("MYSQL_USER")
        MYSQL_PWD = getenv("MYSQL_PWD")
        MYSQL_HOST = getenv("MYSQL_HOST")
        MYSQL_DB = getenv("MYSQL_DB")
        ENV = getenv("ENV")
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_DB
            )
        )

        if ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + "." + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        try:
            self.__session.commit()
        except SQLAlchemyError as e:
            self.__session.rollback()
            raise
        finally:
            self.__session.close()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = welpurse_v2.models.storage.all(cls)
        for value in all_cls.values():
            if value.id == id:
                return value

        return None

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(welpurse_v2.models.storage.all(clas).values())
        else:
            count = len(welpurse_v2.models.storage.all(cls).values())

        return count
