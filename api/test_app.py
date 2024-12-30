import pytest
from app import create_app
from common.models import db, User, Group, Profile, Chat, Message

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
        yield client
        with app.app_context():
            db.drop_all()

def authenticate_client(client, email, password):
    """
    Authenticates a client by registering and logging in to obtain a JWT token.

    Args:
        client: The test client.
        email (str): User's email.
        password (str): User's password.

    Returns:
        str: JWT token.
    """
    client.post('/register', json={'email': email, 'password': password})
    login_response = client.post('/login', json={'email': email, 'password': password})
    token = login_response.get_json().get('token')
    return token

def test_register(client):
    """
    Test user registration with valid credentials.
    """
    response = client.post('/register', json={'email': 'test@example.com', 'password': 'Password1'})
    assert response.status_code == 201

def test_register_weak_password(client):
    """
    Test user registration with a weak password.
    """
    response = client.post('/register', json={'email': 'test@example.com', 'password': 'weakpass'})
    assert response.status_code == 400

def test_login(client):
    """
    Test user login with valid credentials.
    """
    client.post('/register', json={'email': 'test@example.com', 'password': 'Password1'})
    response = client.post('/login', json={'email': 'test@example.com', 'password': 'Password1'})
    assert response.status_code == 200
    assert 'token' in response.get_json()

def test_create_group(client):
    """
    Test creating a new group.
    """
    client.post('/register', json={'email': 'test@example.com', 'password': 'Password1'})
    login_response = client.post('/login', json={'email': 'test@example.com', 'password': 'Password1'})
    token = login_response.get_json().get('token')
    assert token is not None
    response = client.post('/groups', json={'name': 'Test Group', 'picture': 'http://example.com/pic.jpg', 'max_profiles': 5}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    assert 'id' in response.get_json()

def test_create_profile(client):
    """
    Test creating a new profile within a group.
    """
    client.post('/register', json={'email': 'test@example.com', 'password': 'Password1'})
    login_response = client.post('/login', json={'email': 'test@example.com', 'password': 'Password1'})
    token = login_response.get_json().get('token')
    assert token is not None
    group_response = client.post('/groups', json={'name': 'Test Group', 'picture': 'http://example.com/pic.jpg', 'max_profiles': 5}, headers={'Authorization': f'Bearer {token}'})
    group_id = group_response.get_json()['id']
    response = client.post('/profiles', json={'name': 'Test Profile', 'picture': 'http://example.com/pic.jpg', 'bio': 'Test bio', 'group_id': group_id}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    assert 'id' in response.get_json()

def test_create_duplicate_profile(client):
    """
    Test creating a duplicate profile within the same group.
    """
    client.post('/register', json={'email': 'test@example.com', 'password': 'Password1'})
    login_response = client.post('/login', json={'email': 'test@example.com', 'password': 'Password1'})
    token = login_response.get_json().get('token')
    assert token is not None
    group_response = client.post('/groups', json={'name': 'Test Group', 'picture': 'http://example.com/pic.jpg', 'max_profiles': 5}, headers={'Authorization': f'Bearer {token}'})
    group_id = group_response.get_json()['id']
    client.post('/profiles', json={'name': 'Test Profile', 'picture': 'http://example.com/pic.jpg', 'bio': 'Test bio', 'group_id': group_id}, headers={'Authorization': f'Bearer {token}'})
    response = client.post('/profiles', json={'name': 'Test Profile 2', 'picture': 'http://example.com/pic2.jpg', 'bio': 'Test bio 2', 'group_id': group_id}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 400

def test_create_group_invalid_data(client):
    """
    Test creating a group with invalid data types.
    """
    client.post('/register', json={'email': 'test@example.com', 'password': 'Password1'})
    login_response = client.post('/login', json={'email': 'test@example.com', 'password': 'Password1'})
    token = login_response.get_json().get('token')
    assert token is not None
    response = client.post('/groups', json={'name': 123, 'picture': 'http://example.com/pic.jpg', 'max_profiles': 'five'}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 400

def test_create_profile_invalid_data(client):
    """
    Test creating a profile with invalid data types.
    """
    client.post('/register', json={'email': 'test@example.com', 'password': 'Password1'})
    login_response = client.post('/login', json={'email': 'test@example.com', 'password': 'Password1'})
    token = login_response.get_json().get('token')
    assert token is not None
    group_response = client.post('/groups', json={'name': 'Test Group', 'picture': 'http://example.com/pic.jpg', 'max_profiles': 5}, headers={'Authorization': f'Bearer {token}'})
    group_id = group_response.get_json()['id']
    response = client.post('/profiles', json={'name': 123, 'picture': 'http://example.com/pic.jpg', 'bio': 456, 'group_id': group_id}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 400

def test_update_group_invalid_data(client):
    """
    Test updating a group with invalid data types.
    """
    client.post('/register', json={'email': 'test@example.com', 'password': 'Password1'})
    login_response = client.post('/login', json={'email': 'test@example.com', 'password': 'Password1'})
    token = login_response.get_json().get('token')
    assert token is not None
    group_response = client.post('/groups', json={'name': 'Test Group', 'picture': 'http://example.com/pic.jpg', 'max_profiles': 5}, headers={'Authorization': f'Bearer {token}'})
    group_id = group_response.get_json()['id']
    response = client.put(f'/groups/{group_id}', json={'name': 123, 'picture': 'http://example.com/pic.jpg', 'max_profiles': 'five'}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 400

def test_create_duplicate_profile_name(client):
    """
    Test creating profiles with duplicate names across different users.
    """
    # Register and login the first user
    client.post('/register', json={'email': 'user1@example.com', 'password': 'Password1'})
    login_response1 = client.post('/login', json={'email': 'user1@example.com', 'password': 'Password1'})
    token1 = login_response1.get_json().get('token')
    assert token1 is not None

    # Create a group with the first user
    group_response = client.post('/groups', json={
        'name': 'Test Group',
        'picture': 'http://example.com/pic.jpg',
        'max_profiles': 5
    }, headers={'Authorization': f'Bearer {token1}'})
    group_id = group_response.get_json()['id']

    client.post('/profiles', json={
        'name': 'Unique Profile',
        'picture': 'http://example.com/pic.jpg',
        'bio': 'First user bio',
        'group_id': group_id
    }, headers={'Authorization': f'Bearer {token1}'})

    client.post('/register', json={'email': 'user2@example.com', 'password': 'Password2'})
    login_response2 = client.post('/login', json={'email': 'user2@example.com', 'password': 'Password2'})
    token2 = login_response2.get_json().get('token')
    assert token2 is not None

    response = client.post('/profiles', json={
        'name': 'Unique Profile',  
        'picture': 'http://example.com/pic2.jpg',
        'bio': 'Second user bio',
        'group_id': group_id
    }, headers={'Authorization': f'Bearer {token2}'})

    assert response.status_code == 400

def test_create_chat(client):
    """
    Test creating a chat with valid participants.
    """
    client.post('/register', json={'email': 'user1@example.com', 'password': 'Password1'})
    login_response1 = client.post('/login', json={'email': 'user1@example.com', 'password': 'Password1'})
    token1 = login_response1.get_json().get('token')
    assert token1 is not None
    group_response = client.post('/groups', json={'name': 'Test Group', 'picture': 'http://example.com/pic.jpg', 'max_profiles': 5},
                               headers={'Authorization': f'Bearer {token1}'})
    group_id = group_response.get_json()['id']
    client.post('/register', json={'email': 'user2@example.com', 'password': 'Password2'})
    login_response2 = client.post('/login', json={'email': 'user2@example.com', 'password': 'Password2'})
    token2 = login_response2.get_json().get('token')
    assert token2 is not None
    profile1_response = client.post('/profiles', 
                          json={'name': 'Profile 1', 'picture': 'http://example.com/pic1.jpg', 'bio': 'Bio 1', 'group_id': group_id},
                          headers={'Authorization': f'Bearer {token1}'})
    profile2_response = client.post('/profiles', 
                          json={'name': 'Profile 2', 'picture': 'http://example.com/pic2.jpg', 'bio': 'Bio 2', 'group_id': group_id},
                          headers={'Authorization': f'Bearer {token2}'})
    profile1_id = profile1_response.get_json().get('id')
    profile2_id = profile2_response.get_json().get('id')
    assert profile1_id is not None
    assert profile2_id is not None
    # Create a chat with both profiles
    chat_data = {
        'name': 'Test Chat',
        'participant_ids': [profile1_id, profile2_id]
    }
    response = client.post(f'/groups/{group_id}/chats', json=chat_data, headers={'Authorization': f'Bearer {token1}'})
    assert response.status_code == 201
    assert 'id' in response.get_json()

def test_create_chat_no_participants(client):
    """
    Test creating a chat without specifying participants.
    """
    client.post('/register', json={'email': 'user1@example.com', 'password': 'Password1'})
    login_resp = client.post('/login', json={'email': 'user1@example.com', 'password': 'Password1'})
    token = login_resp.get_json().get('token')
    assert token

    group_resp = client.post('/groups', json={
        'name': 'NoParticipantsGroup',
        'picture': 'http://example.com/pic.jpg',
        'max_profiles': 5
    }, headers={'Authorization': f'Bearer {token}'})
    group_id = group_resp.get_json()['id']

    chat_data = {'name': 'Empty Chat'}
    response = client.post(f'/groups/{group_id}/chats', json=chat_data, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    assert 'id' in response.get_json()

def test_list_chats(client):
    """
    Test listing chats within a group.
    """
    client.post('/register', json={'email': 'user1@example.com', 'password': 'Password1'})
    login_response1 = client.post('/login', json={'email': 'user1@example.com', 'password': 'Password1'})
    token1 = login_response1.get_json().get('token')
    assert token1 is not None
    group_response = client.post('/groups', json={'name': 'Test Group', 'picture': 'http://example.com/pic.jpg', 'max_profiles': 5},
                               headers={'Authorization': f'Bearer {token1}'})
    group_id = group_response.get_json()['id']
    client.post('/register', json={'email': 'user2@example.com', 'password': 'Password2'})
    login_response2 = client.post('/login', json={'email': 'user2@example.com', 'password': 'Password2'})
    token2 = login_response2.get_json().get('token')
    assert token2 is not None
    profile1_response = client.post('/profiles', 
                          json={'name': 'Profile 1', 'picture': 'http://example.com/pic1.jpg', 'bio': 'Bio 1', 'group_id': group_id},
                          headers={'Authorization': f'Bearer {token1}'})
    profile2_response = client.post('/profiles', 
                          json={'name': 'Profile 2', 'picture': 'http://example.com/pic2.jpg', 'bio': 'Bio 2', 'group_id': group_id},
                          headers={'Authorization': f'Bearer {token2}'})
    profile1_id = profile1_response.get_json().get('id')
    profile2_id = profile2_response.get_json().get('id')
    assert profile1_id is not None
    assert profile2_id is not None
    chat_data = {
        'name': 'Test Chat',
        'participant_ids': [profile1_id, profile2_id]
    }
    client.post(f'/groups/{group_id}/chats', json=chat_data, headers={'Authorization': f'Bearer {token1}'})
    
    # List chats
    response = client.get(f'/groups/{group_id}/chats', headers={'Authorization': f'Bearer {token1}'})
    assert response.status_code == 200
    chats = response.get_json()
    assert len(chats) > 0
    assert all(isinstance(chat['name'], str) for chat in chats)
    assert all('created_at' in chat for chat in chats)
    assert all('updated_at' in chat for chat in chats)

def test_get_chat(client):
    """
    Test retrieving a specific chat by ID.
    """
    client.post('/register', json={'email': 'user1@example.com', 'password': 'Password1'})
    login_response1 = client.post('/login', json={'email': 'user1@example.com', 'password': 'Password1'})
    token1 = login_response1.get_json().get('token')
    assert token1 is not None
    group_response = client.post('/groups', json={'name': 'Test Group', 'picture': 'http://example.com/pic.jpg', 'max_profiles': 5},
                               headers={'Authorization': f'Bearer {token1}'})
    group_id = group_response.get_json()['id']
    client.post('/register', json={'email': 'user2@example.com', 'password': 'Password2'})
    login_response2 = client.post('/login', json={'email': 'user2@example.com', 'password': 'Password2'})
    token2 = login_response2.get_json().get('token')
    assert token2 is not None
    profile1_response = client.post('/profiles', 
                          json={'name': 'Profile 1', 'picture': 'http://example.com/pic1.jpg', 'bio': 'Bio 1', 'group_id': group_id},
                          headers={'Authorization': f'Bearer {token1}'})
    profile2_response = client.post('/profiles', 
                          json={'name': 'Profile 2', 'picture': 'http://example.com/pic2.jpg', 'bio': 'Bio 2', 'group_id': group_id},
                          headers={'Authorization': f'Bearer {token2}'})
    profile1_id = profile1_response.get_json().get('id')
    profile2_id = profile2_response.get_json().get('id')
    assert profile1_id is not None
    assert profile2_id is not None
    chat_data = {
        'name': 'Test Chat',
        'participant_ids': [profile1_id, profile2_id]
    }
    chat_response = client.post(f'/groups/{group_id}/chats', json=chat_data, headers={'Authorization': f'Bearer {token1}'})
    chat_id = chat_response.get_json().get('id')
    assert chat_id is not None
    response = client.get(f'/chats/{chat_id}', headers={'Authorization': f'Bearer {token1}'})
    assert response.status_code == 200
    chat = response.get_json()
    assert chat['name'] == 'Test Chat'
    assert len(chat['participant_ids']) == 2

def test_update_chat(client):
    """
    Test updating a chat's details and participants.
    """
    client.post('/register', json={'email': 'user1@example.com', 'password': 'Password1'})
    login_response1 = client.post('/login', json={'email': 'user1@example.com', 'password': 'Password1'})
    token1 = login_response1.get_json().get('token')
    assert token1 is not None
    group_response = client.post('/groups', json={'name': 'Test Group', 'picture': 'http://example.com/pic.jpg', 'max_profiles': 5},
                               headers={'Authorization': f'Bearer {token1}'})
    group_id = group_response.get_json()['id']
    client.post('/register', json={'email': 'user2@example.com', 'password': 'Password2'})
    login_response2 = client.post('/login', json={'email': 'user2@example.com', 'password': 'Password2'})
    token2 = login_response2.get_json().get('token')
    assert token2 is not None
    profile1_response = client.post('/profiles', 
                          json={'name': 'Profile 1', 'picture': 'http://example.com/pic1.jpg', 'bio': 'Bio 1', 'group_id': group_id},
                          headers={'Authorization': f'Bearer {token1}'})
    profile2_response = client.post('/profiles', 
                          json={'name': 'Profile 2', 'picture': 'http://example.com/pic2.jpg', 'bio': 'Bio 2', 'group_id': group_id},
                          headers={'Authorization': f'Bearer {token2}'})
    profile1_id = profile1_response.get_json().get('id')
    profile2_id = profile2_response.get_json().get('id')
    assert profile1_id is not None
    assert profile2_id is not None
    chat_data = {
        'name': 'Test Chat',
        'participant_ids': [profile1_id, profile2_id]
    }
    chat_response = client.post(f'/groups/{group_id}/chats', json=chat_data, headers={'Authorization': f'Bearer {token1}'})
    chat_id = chat_response.get_json().get('id')
    assert chat_id is not None
    update_data = {
        'name': 'Updated Chat',
        'participant_ids': [profile1_id]  
    }
    response = client.put(f'/chats/{chat_id}', json=update_data, headers={'Authorization': f'Bearer {token1}'})
    assert response.status_code == 200
    get_response = client.get(f'/chats/{chat_id}', headers={'Authorization': f'Bearer {token1}'})
    updated_chat = get_response.get_json()
    assert updated_chat['name'] == 'Updated Chat'
    assert len(updated_chat['participant_ids']) == 1

def test_create_chat_invalid_participants(client):
    """
    Test creating a chat with invalid participant IDs.
    """
    client.post('/register', json={'email': 'test@example.com', 'password': 'Password1'})
    login_response = client.post('/login', json={'email': 'test@example.com', 'password': 'Password1'})
    token = login_response.get_json().get('token')
    assert token is not None
    group_response = client.post('/groups', json={'name': 'Test Group', 'picture': 'http://example.com/pic.jpg', 'max_profiles': 5},
                               headers={'Authorization': f'Bearer {token}'})
    group_id = group_response.get_json()['id']
    chat_data = {
        'name': 'Test Chat',
        'participant_ids': ['not-a-valid-uuid']
    }
    response = client.post(f'/groups/{group_id}/chats', json=chat_data, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 400
    response_data = response.get_json()

def test_create_group_creates_general_chat(client):
    """
    Test that creating a group automatically creates a 'general' chat.
    """
    client.post('/register', json={'email': 'test@example.com', 'password': 'Password1'})
    login_response = client.post('/login', json={'email': 'test@example.com', 'password': 'Password1'})
    token = login_response.get_json().get('token')
    assert token is not None
    response = client.post('/groups', json={'name': 'Test Group', 'picture': 'http://example.com/pic.jpg', 'max_profiles': 5}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    group_id = response.get_json()['id']
    chats_response = client.get(f'/groups/{group_id}/chats', headers={'Authorization': f'Bearer {token}'})
    assert chats_response.status_code == 200
    chats = chats_response.get_json()
    assert len(chats) == 1
    assert chats[0]['name'] == 'general'

def test_create_profile_adds_to_general_chat(client):
    """
    Test that creating a profile adds it to the 'general' chat.
    """
    client.post('/register', json={'email': 'test@example.com', 'password': 'Password1'})
    login_response = client.post('/login', json={'email': 'test@example.com', 'password': 'Password1'})
    token = login_response.get_json().get('token')
    assert token is not None
    group_response = client.post('/groups', json={'name': 'Test Group', 'picture': 'http://example.com/pic.jpg', 'max_profiles': 5}, headers={'Authorization': f'Bearer {token}'})
    group_id = group_response.get_json()['id']
    profile_response = client.post('/profiles', json={'name': 'Test Profile', 'picture': 'http://example.com/pic.jpg', 'bio': 'Test bio', 'group_id': group_id}, headers={'Authorization': f'Bearer {token}'})
    assert profile_response.status_code == 201
    profile_id = profile_response.get_json()['id']
    chats_response = client.get(f'/groups/{group_id}/chats', headers={'Authorization': f'Bearer {token}'})
    assert chats_response.status_code == 200
    chats = chats_response.get_json()
    general_chat = next(chat for chat in chats if chat['name'] == 'general')
    assert profile_id in general_chat['participant_ids']

def test_create_message(client):
    """
    Test creating a message within a chat.
    """
    client.post('/register', json={'email': 'user1@example.com', 'password': 'Password1'})
    login_response1 = client.post('/login', json={'email': 'user1@example.com', 'password': 'Password1'})
    token1 = login_response1.get_json().get('token')
    assert token1 is not None

    group_response = client.post('/groups', json={'name': 'Test Group', 'picture': 'http://example.com/pic.jpg', 'max_profiles': 5}, headers={'Authorization': f'Bearer {token1}'})
    group_id = group_response.get_json()['id']

    profile_response = client.post('/profiles', json={'name': 'Profile 1', 'picture': 'http://example.com/pic1.jpg', 'bio': 'Bio 1', 'group_id': group_id}, headers={'Authorization': f'Bearer {token1}'})
    profile_id = profile_response.get_json().get('id')
    assert profile_id is not None

    chat_response = client.post(f'/groups/{group_id}/chats', json={'name': 'Test Chat', 'participant_ids': [profile_id]}, headers={'Authorization': f'Bearer {token1}'})
    chat_id = chat_response.get_json().get('id')
    assert chat_id is not None

    message_data = {'content': 'Hello, world!', 'chat_id': chat_id, 'profile_id': profile_id}
    response = client.post('/messages', json=message_data, headers={'Authorization': f'Bearer {token1}'})
    assert response.status_code == 201
    assert 'id' in response.get_json()

def test_get_messages(client):
    """
    Test retrieving messages from a chat.
    """
    client.post('/register', json={'email': 'user1@example.com', 'password': 'Password1'})
    login_response1 = client.post('/login', json={'email': 'user1@example.com', 'password': 'Password1'})
    token1 = login_response1.get_json().get('token')
    assert token1 is not None

    group_response = client.post('/groups', json={'name': 'Test Group', 'picture': 'http://example.com/pic.jpg', 'max_profiles': 5}, headers={'Authorization': f'Bearer {token1}'})
    group_id = group_response.get_json()['id']

    profile_response = client.post('/profiles', json={'name': 'Profile 1', 'picture': 'http://example.com/pic1.jpg', 'bio': 'Bio 1', 'group_id': group_id}, headers={'Authorization': f'Bearer {token1}'})
    profile_id = profile_response.get_json().get('id')
    assert profile_id is not None

    chat_response = client.post(f'/groups/{group_id}/chats', json={'name': 'Test Chat', 'participant_ids': [profile_id]}, headers={'Authorization': f'Bearer {token1}'})
    chat_id = chat_response.get_json().get('id')
    assert chat_id is not None

    message_data = {'content': 'Hello, world!', 'chat_id': chat_id, 'profile_id': profile_id}
    client.post('/messages', json=message_data, headers={'Authorization': f'Bearer {token1}'})

    response = client.get(f'/chats/{chat_id}/messages', headers={'Authorization': f'Bearer {token1}'})
    assert response.status_code == 200
    messages = response.get_json()
    assert len(messages) > 0
    assert all('content' in message for message in messages)
    assert all('created_at' in message for message in messages)

def test_get_user_info(client):
    """
    Test retrieving user information.
    """
    token = authenticate_client(client, 'user@example.com', 'Password1')
    # Create group
    group_resp = client.post('/groups', json={'name': 'Test Group', 'picture': 'http://example.com/pic.jpg', 'max_profiles': 5},
                             headers={'Authorization': f'Bearer {token}'})
    group_id = group_resp.get_json()['id']
    # Create profile
    profile_resp = client.post('/profiles', json={'name': 'Test Profile', 'picture': 'http://example.com/pic.jpg', 'bio': 'Test bio', 'group_id': group_id},
                                headers={'Authorization': f'Bearer {token}'})
    profile_id = profile_resp.get_json()['id']
    # Create chat
    chat_resp = client.post('/groups/{}/chats'.format(group_id), json={'name': 'Test Chat', 'participant_ids': [profile_id]},
                            headers={'Authorization': f'Bearer {token}'})
    chat_id = chat_resp.get_json()['id']
    # Create message
    message_resp = client.post('/messages', json={'content': 'Hello', 'chat_id': chat_id, 'profile_id': profile_id},
                               headers={'Authorization': f'Bearer {token}'})
    assert message_resp.status_code == 201

    # Get user info
    response = client.get('/users/me', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'profiles' in data
    assert 'groups' in data
    assert 'chats' in data
    assert len(data['profiles']) == 1
    assert len(data['groups']) == 1
    assert len(data['chats']) == 2  

def test_get_user_info_unauthorized(client):
    """
    Test retrieving user information without authorization.
    """
    response = client.get('/users/me')
    assert response.status_code == 401

def test_get_user_info_no_profiles(client):
    """
    Test retrieving user information when the user has no profiles.
    """
    token = authenticate_client(client, 'user2@example.com', 'Password2')
    response = client.get('/users/me', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'profiles' in data
    assert 'groups' in data
    assert 'chats' in data
    assert len(data['profiles']) == 0
    assert len(data['groups']) == 0
    assert len(data['chats']) == 0

def test_get_user_info_multiple_profiles(client):
    """
    Test retrieving user information when the user has multiple profiles.
    """
    token = authenticate_client(client, 'multiuser@example.com', 'Password1')
    group1_resp = client.post('/groups', json={'name': 'Group One', 'picture': 'http://example.com/pic1.jpg', 'max_profiles': 5},
                              headers={'Authorization': f'Bearer {token}'})
    group1_id = group1_resp.get_json()['id']
    group2_resp = client.post('/groups', json={'name': 'Group Two', 'picture': 'http://example.com/pic2.jpg', 'max_profiles': 5},
                              headers={'Authorization': f'Bearer {token}'})
    group2_id = group2_resp.get_json()['id']
    profile1_resp = client.post('/profiles', json={'name': 'Profile One', 'picture': 'http://example.com/pic1.jpg', 'bio': 'Bio One', 'group_id': group1_id},
                                 headers={'Authorization': f'Bearer {token}'})
    profile2_resp = client.post('/profiles', json={'name': 'Profile Two', 'picture': 'http://example.com/pic2.jpg', 'bio': 'Bio Two', 'group_id': group2_id},
                                 headers={'Authorization': f'Bearer {token}'})
    profile1_id = profile1_resp.get_json()['id']
    profile2_id = profile2_resp.get_json()['id']
    chat1_resp = client.post('/groups/{}/chats'.format(group1_id), json={'name': 'Chat One', 'participant_ids': [profile1_id]},
                             headers={'Authorization': f'Bearer {token}'})
    chat2_resp = client.post('/groups/{}/chats'.format(group2_id), json={'name': 'Chat Two', 'participant_ids': [profile2_id]},
                             headers={'Authorization': f'Bearer {token}'})
    chat1_id = chat1_resp.get_json()['id']
    chat2_id = chat2_resp.get_json()['id']
    response = client.get('/users/me', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['profiles']) == 2
    assert len(data['groups']) == 2
    assert len(data['chats']) == 4
