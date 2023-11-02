from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
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
        return f'<User id:{self.username}, first:{self.first_name}, surname:{self.surname}, handicap:{self.handicap_index}, email:{self.email}, password:{self.password}, admin:{self.is_admin}, subscriptions_relationship:{self.subscriptions}, chats_relationship:{self.chats}, events_relationship:{self.events}, messages_relationship:{self.messages}>'
    

class User_subscription(db.Model):
    subscription_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('club.club_id'), nullable=False)

    __table_args__ = (UniqueConstraint('user_id', 'club_id'),)

    # string representation
    def __repr__(self):
        return f'<Subscriptions id:{self.subscription_id}, user:{self.user_id}, club_id:{self.club_id}>'


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

    # string representation
    def __repr__(self):
        return f'<Club id:{self.club_id}, name:{self.club_name}, url:{self.club_url}, address:{self.club_address}, postcode:{self.club_postcode}, phone:{self.club_phone_number}, approved:{self.approved}, subscriptions_relationship:{self.subscriptions}, events_relationship:{self.events}>'

    
class Chat(db.Model):
    chat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), unique=True, nullable=False)

    messages = db.relationship('Message', backref='chat')
    event = db.relationship('Event', back_populates='chat', uselist=False)

    # string representation
    def __repr__(self):
        return f'<Chat id:{self.chat_id}, user:{self.user_id}, event_id:{self.event_id}, messages_relationship:{self.messages}, event_relationship:{self.event}>'


class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.chat_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    
    def timestamp_as_iso(self):
        return self.timestamp.isoformat()
    
    # string representation
    def __repr__(self):
        return f'<Message id:{self.message_id}, chat:{self.chat_id}, user:{self.user_id}, message:{self.message}, timestamp_stored:{self.timestamp}, timestamp_as_iso:({self.timestamp_as_iso()}, active:{self.active})>'


class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id_creator = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('club.club_id'), nullable=False)
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

    def datetime_as_iso(self):
        return self.planned_datetime.isoformat()
    
    # string representation
    def __repr__(self):
        return f'<Event id:{self.event_id}, user_creator:{self.user_id_creator}, club:{self.club_id}, event_name:{self.event_name}, description:{self.event_description}, planned_datetime_stored:{self.planned_datetime}, planned_datetime_iso:({self.datetime_as_iso()}), max_capacity:{self.max_capacity}, min_hc:{self.min_hc}, max_hc:{self.max_hc}, current_participants:{self.current_participants}, tee_time_booked:{self.tee_time_booked}, event_open:{self.event_open})>'