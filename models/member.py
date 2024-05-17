from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/yourdatabase'
db = SQLAlchemy(app)
api = Api(app)

class Member(db.Model):
    __tablename__ = 'members'
    memberId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))

class Contribution(db.Model):
    __tablename__ = 'contributions'
    contributnId = db.Column(db.Integer, primary_key=True)
    memberId = db.Column(db.Integer, db.ForeignKey('members.memberId'))
    amount = db.Column(db.Numeric(10, 2))
    dateContributed = db.Column(db.Date)


db.create_all()
