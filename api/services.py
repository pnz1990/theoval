import logging
from models import db, Group, Profile, User, Chat, chat_participants  # Import necessary models
from werkzeug.exceptions import BadRequest
from uuid import UUID
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import request, jsonify
from werkzeug.exceptions import Unauthorized

def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            request.user_id = user_id
            return func(*args, **kwargs)
        except Exception:
            return jsonify({'message': 'Authorization token is missing or invalid'}), 401
    return wrapper

def validate_group_data(data):
    logging.debug(f"Validating group data: {data}")
    if 'name' not in data or not isinstance(data['name'], str):
        raise BadRequest('Invalid group name')
    if 'max_profiles' not in data or not isinstance(data['max_profiles'], int) or data['max_profiles'] <= 0:
        raise BadRequest('Invalid max_profiles')
    if 'picture' in data and not isinstance(data['picture'], str):
        raise BadRequest('Invalid picture URL')

def validate_profile_data(data, user_id=None):
    if 'name' not in data or not isinstance(data['name'], str):
        raise BadRequest('Invalid profile name')
    if 'bio' in data and not isinstance(data['bio'], str):
        raise BadRequest('Invalid bio')
    if 'picture' in data and not isinstance(data['picture'], str):
        raise BadRequest('Invalid picture URL')
    if 'group_id' not in data or not isinstance(data['group_id'], str):
        raise BadRequest('Invalid group_id')
    if user_id:
        # Check for existing profile by user in group
        existing_profile = Profile.query.filter_by(group_id=data['group_id'], user_id=user_id).first()
        if existing_profile:
            raise BadRequest('User already has a profile in this group')
    # Check for duplicate profile name in group regardless of user
    name_exists = Profile.query.filter_by(group_id=data['group_id'], name=data['name']).first()
    if name_exists:
        raise BadRequest('Profile name already exists in this group')

def is_strong_password(password):
    if len(password) < 8:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    return True

def create_group(data):
    validate_group_data(data)
    new_group = Group(name=data['name'], picture=data.get('picture'), max_profiles=data['max_profiles'])
    db.session.add(new_group)
    db.session.commit()
    # Create a "general" chat for the new group
    general_chat = Chat(name='general', group_id=new_group.id)
    db.session.add(general_chat)
    db.session.commit()
    return new_group

def update_group(group, data):
    validate_group_data(data)
    group.name = data['name']
    group.picture = data.get('picture')
    group.max_profiles = data['max_profiles']
    db.session.commit()
    return group

def create_profile(data, user_id):
    validate_profile_data(data, user_id)
    new_profile = Profile(name=data['name'], picture=data.get('picture'), bio=data.get('bio'), group_id=data['group_id'], user_id=user_id)
    db.session.add(new_profile)
    db.session.commit()
    # Add the new profile to the "general" chat of the group
    general_chat = Chat.query.filter_by(group_id=data['group_id'], name='general').first()
    if general_chat:
        general_chat.participants.append(new_profile)
        db.session.commit()
    return new_profile

def validate_chat_data(data, group_id=None):
    if 'name' not in data or not isinstance(data['name'], str):
        raise BadRequest('Invalid chat name')
    participant_ids = data.get('participant_ids', [])
    if not isinstance(participant_ids, list):
        raise BadRequest('participant_ids must be a list if provided')
    if group_id and participant_ids:
        profiles = Profile.query.filter(Profile.id.in_(participant_ids)).all()
        if len(profiles) != len(participant_ids):
            raise BadRequest('One or more profiles not found')
        if not all(profile.group_id == group_id for profile in profiles):
            raise BadRequest('All participants must belong to the same group')

def create_chat(data, group_id):
    validate_chat_data(data, group_id)
    profiles = Profile.query.filter(Profile.id.in_(data.get('participant_ids', []))).all()
    new_chat = Chat(name=data['name'], group_id=group_id)
    new_chat.participants = profiles
    db.session.add(new_chat)
    db.session.commit()
    return new_chat

def update_chat(chat, data):
    validate_chat_data(data, chat.group_id)
    profiles = Profile.query.filter(Profile.id.in_(data['participant_ids'])).all()
    chat.name = data['name']
    chat.participants = profiles
    db.session.commit()
    return chat

def get_user_info(user_id):
    user = User.query.get(user_id)
    if not user:
        raise BadRequest("User not found")
    
    # Retrieve profiles associated with the user
    profiles = Profile.query.filter_by(user_id=user_id).all()
    
    # Extract unique groups from the user's profiles
    groups = []
    group_ids = []
    for profile in profiles:
        group = Group.query.get(profile.group_id)
        if group:
            groups.append({
                'id': str(group.id),
                'name': group.name,
                'picture': group.picture,
                'max_profiles': group.max_profiles
            })
            group_ids.append(group.id)
    
    # Fetch chats associated with the user's groups
    chats = Chat.query.filter(Chat.group_id.in_(group_ids)).all()
    chats_data = [{
        'id': str(chat.id),
        'name': chat.name,
        'created_at': chat.created_at.isoformat(),
        'updated_at': chat.updated_at.isoformat(),
        'group_id': str(chat.group_id),
        'participant_ids': [str(profile.id) for profile in chat.participants]
    } for chat in chats]
    
    user_info = {
        'id': str(user.id),
        'email': user.email,
        'profiles': [{'id': str(p.id), 'name': p.name, 'group_id': str(p.group_id)} for p in profiles],
        'groups': groups,  # Only groups where the user has profiles
        'chats': chats_data  # Chats associated with the user's groups
    }
    
    return user_info
