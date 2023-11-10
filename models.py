from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from datetime import datetime, timezone
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    first_name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    handicap_index = db.Column(db.String(5))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    subscriptions = db.relationship('User_subscription', backref='user', cascade='all, delete-orphan')
    chats = db.relationship('Chat', backref='user', cascade='none')
    events_created = db.relationship('Event', backref='user', cascade='none')
    messages = db.relationship('Message', backref='user', cascade='none')

    # function used by flask login
    def get_id(self):
        return str(self.user_id)
    
    # string representation
    def __repr__(self):
        return f'<User user_id:{self.user_id}, username:{self.username} first_name:{self.first_name}, surname:{self.surname}, handicap_index:{self.handicap_index}, email:{self.email}, password:{self.password}, is_admin:{self.is_admin}, subscriptions_relationship:{self.subscriptions}, chats_relationship:{self.chats}, events_relationship:{self.events_created}, messages_relationship:{self.messages}>'
    

class User_subscription(db.Model):
    subscription_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('club.club_id'), nullable=False)

    __table_args__ = (UniqueConstraint('user_id', 'club_id'),)

    # string representation
    def __repr__(self):
        return f'<User_subscriptions subscription_id:{self.subscription_id}, user_id:{self.user_id}, club_id:{self.club_id}>'


class Club(db.Model):
    club_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    club_name = db.Column(db.String(255), unique=True, nullable=False)
    club_url = db.Column(db.String(255), nullable=False)
    club_address = db.Column(db.String(255))
    club_postcode = db.Column(db.String(8), nullable=False)
    club_phone_number = db.Column(db.String(20))
    approved = db.Column(db.Boolean, default=False, nullable=False)

    subscriptions = db.relationship('User_subscription', backref='club', cascade='all, delete, delete-orphan')
    events = db.relationship('Event', backref='club', cascade='none')

    # string representation
    def __repr__(self):
        return f'<Club club_id:{self.club_id}, club_name:{self.club_name}, club_url:{self.club_url}, club_address:{self.club_address}, club_postcode:{self.club_postcode}, club_phone_number:{self.club_phone_number}, approved:{self.approved}, subscriptions_relationship:{self.subscriptions}, events_relationship:{self.events}>'

    
class Chat(db.Model):
    chat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)

    messages = db.relationship('Message', backref='chat', cascade='all, delete-orphan')
    event = db.relationship('Event', back_populates='chat', uselist=False, cascade='all, delete-orphan', single_parent=True)

    # string representation
    def __repr__(self):
        return f'<Chat chat_id:{self.chat_id}, user_id:{self.user_id}, event_id:{self.event_id}, active:{self.active}, messages_relationship:{self.messages}, event_relationship:{self.event}>'


class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.chat_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    # string representation
    def __repr__(self):
        return f'<Message message_id:{self.message_id}, chat_id:{self.chat_id}, user_id:{self.user_id}, message:{self.message}, timestamp (in local time):{self.timestamp})>'


class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id_creator = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('club.club_id'))
    event_name = db.Column(db.String(100))
    event_description = db.Column(db.String(500))
    planned_datetime = db.Column(db.DateTime, nullable=False)  # must be provided as date object
    max_capacity = db.Column(db.Integer, nullable=False)
    min_hc = db.Column(db.String(5))
    max_hc = db.Column(db.String(5))
    current_participants = db.Column(db.Integer, nullable=False)
    tee_time_booked = db.Column(db.Boolean, nullable=False)
    event_open = db.Column(db.Boolean, nullable=False)

    chat = db.relationship('Chat', back_populates='event', uselist=False, cascade='all, delete-orphan')
    
    # string representation
    def __repr__(self):
        return f'<Event event_id:{self.event_id}, user_id_creator:{self.user_id_creator}, club_id:{self.club_id}, event_name:{self.event_name}, event_description:{self.event_description}, planned_datetime (in local time):{self.planned_datetime}, max_capacity:{self.max_capacity}, min_hc:{self.min_hc}, max_hc:{self.max_hc}, current_participants:{self.current_participants}, tee_time_booked:{self.tee_time_booked}, event_open:{self.event_open})>'
    