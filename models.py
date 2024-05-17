from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

db = SQLAlchemy()


def get_uuid():
    return uuid4().hex


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(11), primary_key=True, unique=True, default=get_uuid)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(80), nullable=False)


class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.String(11), primary_key=True, unique=True, default=get_uuid)
    title = db.Column(db.String(150), nullable=False)
    director = db.Column(db.String(100))
    photo = db.Column(db.String(100))
    summary = db.Column(db.Text)


from datetime import datetime

class Screening(db.Model):
    __tablename__ = "screening"
    id = db.Column(db.String(11), primary_key=True, unique=True, default=get_uuid)
    movie_id = db.Column(db.String(11), db.ForeignKey('movies.id'), nullable=False)
    start_time = db.Column(db.String(16), nullable=False)
    end_time = db.Column(db.String(16), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

class Ticket(db.Model):
    __tablename__ = "tickets"
    id = db.Column(db.String(11), primary_key=True, unique=True, default=get_uuid)
    session_id = db.Column(db.String(11), db.ForeignKey('screening.id'), nullable=False)  # Updated foreign key reference
    user_id = db.Column(db.String(11), db.ForeignKey('users.id'), nullable=False)
    seat_number = db.Column(db.Integer, nullable=False)
