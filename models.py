from flask_sqlalchemy import SQLAlchemy, UniqueConstraint
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    first_name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    handicap_index = db.Column(db.String(5))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    subscriptions = db.relationship('User_subscription', backref='user')
    chats = db.relationship('Chat', backref='user')
    events = db.relationship('Event', backref='user')
    messages = db.relationship('Message', backref='user')

    
    # string representation
    def __repr__(self):
        return f'<User {self.username}>'
    

class User_subscription(db.Model):
    subscription_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('club.club_id'), nullable=False)

    __table_args__ = (UniqueConstraint('user_id', 'club_id'),)


class Club(db.Model):
    club_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    club_name = db.Column(db.String(255), unique=True, nullable=False)
    club_url = db.Column(db.String(255), nullable=False)
    club_address = db.Column(db.String(255))
    club_postcode = db.Column(db.String(8))
    club_phone_number = db.Column(db.String(20))
    approved = db.Column(db.Boolean, default=False, nullable=False)

    subscriptions = db.relationship('User_subscription', backref='club')
    events = db.relationship('Event', backref='club')

    
class Chat(db.Model):
    chat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), unique=True, nullable=False)

    messages = db.relationship('Message', backref='chat')
    event = db.relationship('Event', back_populates='chat', uselist=False)


class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.chat_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    
    def timestamp_as_iso(self):
        return self.timestamp.isoformat()


class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id_creator = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    club_id = db.Column(db.Integer, db.ForgeignKey('club.club_id'), nullable=False)
    event_name = db.Column(db.String(100))
    event_description = db.Column(db.String(500))
    planned_datetime = db.Column(db.DateTime)
    max_capacity = db.Column(db.Integer, nullable=False)
    min_hc = db.Column(db.String(5))
    max_hc = db.Column(db.String(5))
    current_participants = db.Column(db.Integer, nullable=False)
    tee_time_booked = db.Column(db.Boolean, nullable=False)
    event_open = db.Column(db.Boolean, nullable=False)

    chat = db.relationship('Chat', back_populates='event', uselist=False, cascade='all, delete-orphan')

    def timestamp_as_iso(self):
        return self.timestamp.isoformat()
    

