from flask_sqlalchemy import SQLAlchemy
import uuid
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'appuser'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    profiles = db.relationship('Profile', backref='user', lazy=True)

    def __init__(self, email, password):
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Group(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(80), nullable=False)
    picture = db.Column(db.String(1024), nullable=False)
    max_profiles = db.Column(db.Integer, nullable=False)
    profiles = db.relationship('Profile', backref='group', lazy=True)

class Profile(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(80), nullable=False)
    picture = db.Column(db.String(1024), nullable=False)
    bio = db.Column(db.String(1024), nullable=False)
    group_id = db.Column(db.String(36), db.ForeignKey('group.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('appuser.id'), nullable=False)

chat_participants = db.Table('chat_participants',
    db.Column('chat_id', db.String(36), db.ForeignKey('chat.id'), primary_key=True),
    db.Column('profile_id', db.String(36), db.ForeignKey('profile.id'), primary_key=True)
)

class Chat(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    group_id = db.Column(db.String(36), db.ForeignKey('group.id'), nullable=False)
    participants = db.relationship('Profile', secondary=chat_participants, lazy='subquery',
        backref=db.backref('chats', lazy=True))

class Message(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    content = db.Column(db.String(1024), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    chat_id = db.Column(db.String(36), db.ForeignKey('chat.id'), nullable=False)
    profile_id = db.Column(db.String(36), db.ForeignKey('profile.id'), nullable=False)
    chat = db.relationship('Chat', backref=db.backref('messages', lazy=True))
    profile = db.relationship('Profile', backref=db.backref('messages', lazy=True))
