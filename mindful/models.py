
# from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy import Column, Integer, DateTime
from mindful import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Client(db.Model):
    __tablename__ = "clients"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=True)
    state = db.Column(db.String, nullable=True)
    zipcode = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    phone = db.Column(db.String, nullable=True)
    last_change_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Client('{self.first_name}','{self.last_name}','{self.email}', '{self.city}','{self.state}','{self.zipcode}')"

    def add_note(self, note_date):
        note = Note(note_date=datetime, last_change_date=datetime)
        db.session.add(note)
        db.session.commit()


class Note(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)
    note_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)
    last_change_date = db.Column(db.DateTime, nullable=False)


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String,)
    last_name = db.Column(db.String,)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    client = db.relationship('Client', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}','{self.email}')"
