from event_app import db
from sqlalchemy.orm import backref
from flask_login import UserMixin

rsvps = db.Table('rsvps',
  db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
  db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
)

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  email = db.Column(db.String(255), nullable=False, unique=True)
  password = db.Column(db.String(255), nullable=False)
  events = db.relationship('Event', back_populates='owner')
  rsvps = db.relationship('Event', secondary=rsvps)

class Event(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(255), nullable=False)
  desc = db.Column(db.Text, nullable=False)
  imgUrl = db.Column(db.Text, nullable=False)
  date = db.Column(db.String(255), nullable=False)
  location = db.Column(db.Text, nullable=False)
  owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  owner = db.relationship('User', back_populates='events')
  rsvps = db.relationship('User', secondary=rsvps)
