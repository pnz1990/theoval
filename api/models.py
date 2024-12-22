from flask_sqlalchemy import SQLAlchemy
import uuid
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """
    Represents a user in the application.

    Attributes:
        id (str): Primary key UUID.
        email (str): Unique email address.
        password (str): Hashed password.
        profiles (List[Profile]): Associated profiles.
    """
    __tablename__ = 'appuser'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    profiles = db.relationship('Profile', backref='user', lazy=True)

    def __init__(self, email, password):
        """
        Initializes a new User instance.

        Args:
            email (str): User's email.
            password (str): User's password.
        """
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        """
        Sets the user's password by hashing it.

        Args:
            password (str): Plain text password.
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks if the provided password matches the stored hash.

        Args:
            password (str): Plain text password.

        Returns:
            bool: True if match, False otherwise.
        """
        return check_password_hash(self.password, password)

class Group(db.Model):
    """
    Represents a group within the application.

    Attributes:
        id (str): Primary key UUID.
        name (str): Name of the group.
        picture (str): URL to the group's picture.
        max_profiles (int): Maximum number of profiles allowed.
        profiles (List[Profile]): Associated profiles.
    """
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(80), nullable=False)
    picture = db.Column(db.String(1024), nullable=False)
    max_profiles = db.Column(db.Integer, nullable=False)
    profiles = db.relationship('Profile', backref='group', lazy=True)

class Profile(db.Model):
    """
    Represents a user's profile within a group.

    Attributes:
        id (str): Primary key UUID.
        name (str): Profile name.
        picture (str): URL to the profile's picture.
        bio (str): Biography of the profile.
        group_id (str): Foreign key to Group.
        user_id (str): Foreign key to User.
    """
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
    """
    Represents a chat within a group.

    Attributes:
        id (str): Primary key UUID.
        name (str): Name of the chat.
        created_at (datetime): Timestamp of creation.
        updated_at (datetime): Timestamp of last update.
        group_id (str): Foreign key to Group.
        participants (List[Profile]): Profiles participating in the chat.
        messages (List[Message]): Messages within the chat.
    """
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    group_id = db.Column(db.String(36), db.ForeignKey('group.id'), nullable=False)
    participants = db.relationship('Profile', secondary=chat_participants, lazy='subquery',
        backref=db.backref('chats', lazy=True))

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
