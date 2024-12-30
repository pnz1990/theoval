import pytest
from app import create_app
from common.models import db, User, Group, Profile, Chat, Message
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask import current_app

@pytest.fixture
def client():
    """
    Pytest fixture to create a test client for the Flask application.
    """
    test_config = {
        'TESTING': True,
        'FLASK_ENV': 'testing',  
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'JWT_SECRET_KEY': 'test_jwt_secret_key'
    }
    app = create_app(test_config)
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            
            # Create a test user
            user = User(email='user1@example.com', password='Password1')
            user.set_password('Password1')
            db.session.add(user)
            db.session.commit()
            
            # Generate JWT token for the user
            token = create_access_token(identity=user.id)
            
            # Create a test group
            group = Group(name='Test Group', picture='http://example.com/pic.jpg', max_profiles=5)
            db.session.add(group)
            db.session.commit()
            
            # Create a test profile with user_id
            profile = Profile(
                name='Profile 1', 
                picture='http://example.com/pic1.jpg', 
                bio='Bio 1', 
                group_id=group.id, 
                user_id=user.id
            )
            db.session.add(profile)
            db.session.commit()
            
            # Create a test chat
            chat = Chat(
                name='Test Chat',
                group_id=group.id
            )
            db.session.add(chat)
            db.session.commit()
            
            # Add participant to chat if necessary (depends on your actual model relationships)
            # This step is skipped as relationships are not defined in the stub
            
            yield client, token, group, profile, chat  # Yield within the app context
            
            db.drop_all()

def test_create_message(client):
    """
    Test creating a message within a chat.
    """
    client, token, group, profile, chat = client  # Unpack fixtures
    
    message_data = {
        'content': 'Hello, world!', 
        'chat_id': chat.id, 
        'profile_id': profile.id
    }
    response = client.post('/messages', json=message_data, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201, f"Message creation failed: {response.data}"
    assert 'id' in response.get_json(), "Message ID not returned"

def test_get_messages(client):
    """
    Test retrieving messages from a chat.
    """
    client, token, group, profile, chat = client  # Unpack fixtures
    
    # Create a message first
    message = Message(content='Hello, world!', chat_id=chat.id, profile_id=profile.id)
    with client.application.app_context():
        db.session.add(message)
        db.session.commit()
    
    response = client.get(f'/chats/{chat.id}/messages', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200, f"Fetching messages failed: {response.data}"
    messages = response.get_json()
    assert isinstance(messages, list), "Messages response is not a list"
    assert len(messages) > 0, "No messages returned"
    assert all('content' in message for message in messages), "Some messages lack 'content'"
    assert all('created_at' in message for message in messages), "Some messages lack 'created_at'"

