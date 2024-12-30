from common.models import db, User, Group, Profile, Chat, Message
import uuid
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Message(db.Model):
    """
    Represents a message within a chat.

    Attributes:
        id (str): Primary key UUID.
        content (str): Content of the message.
        created_at (datetime): Timestamp of creation.
        chat_id (str): Foreign key to Chat.
        profile_id (str): Foreign key to Profile.
        chat (Chat): Associated chat.
        profile (Profile): Sender's profile.
    """
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    content = db.Column(db.String(1024), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    chat_id = db.Column(db.String(36), db.ForeignKey('chat.id'), nullable=False)
    profile_id = db.Column(db.String(36), db.ForeignKey('profile.id'), nullable=False)
    chat = db.relationship('Chat', backref=db.backref('messages', lazy=True))
    profile = db.relationship('Profile', backref=db.backref('messages', lazy=True))
