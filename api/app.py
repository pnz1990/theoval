from flask import Flask, request, jsonify
from models import db, Group, Profile, User, Chat, Message
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import os
from werkzeug.exceptions import BadRequest  
from services import (
    validate_group_data, validate_profile_data, is_strong_password,
    create_group, update_group, create_profile,
    validate_chat_data, create_chat, update_chat
)
import logging

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True, allow_headers=["Content-Type", "Authorization"], methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    
    if test_config:
        app.config.update(test_config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB', 'postgres')}"
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')
    
    db.init_app(app)
    jwt = JWTManager(app)
    
    logging.basicConfig(level=logging.DEBUG)
    
    # @app.before_request
    # def log_request_info():
    #     # app.logger.debug('Headers: %s', request.headers)
    #     # app.logger.debug('Body: %s', request.get_data())
    #     return request
    
    # Global error handler for BadRequest
    @app.errorhandler(BadRequest)
    def handle_bad_request(e):
        return jsonify({'message': e.description}), 400
    
    ### Route Definitions Start ###
    
    @app.route('/health')
    def health_check():
        return jsonify({'status': 'healthy'}), 200
    
    @app.route('/groups', methods=['POST'])
    @jwt_required()
    def create_group_route():
        data = request.get_json()
        app.logger.debug('Create group data: %s', data)
        app.logger.debug('Type of max_profiles: %s', type(data.get('max_profiles')))
        new_group = create_group(data)
        return jsonify({'id': str(new_group.id)}), 201
    
    @app.route('/groups', methods=['GET'])
    @jwt_required()
    def get_groups():
        app.logger.debug('Fetching all groups')
        groups = Group.query.all()
        return jsonify([{'id': group.id, 'name': group.name, 'picture': group.picture, 'max_profiles': group.max_profiles} for group in groups])
    
    @app.route('/groups/<group_id>', methods=['GET'])
    @jwt_required()
    def get_group(group_id):
        app.logger.debug('Fetching group with id: %s', group_id)
        group = Group.query.get_or_404(group_id)
        return jsonify({'id': group.id, 'name': group.name, 'picture': group.picture, 'max_profiles': group.max_profiles})
    
    @app.route('/groups/<group_id>', methods=['PUT'])
    @jwt_required()
    def update_group_route(group_id):
        data = request.get_json()
        app.logger.debug('Update group data: %s', data)
        group = Group.query.get_or_404(group_id)
        updated_group = update_group(group, data)
        return jsonify({'id': updated_group.id})
    
    @app.route('/groups/<group_id>', methods=['DELETE'])
    @jwt_required()
    def delete_group(group_id):
        app.logger.debug('Deleting group with id: %s', group_id)
        group = Group.query.get_or_404(group_id)
        db.session.delete(group)
        db.session.commit()
        return '', 204
    
    @app.route('/profiles/check', methods=['POST'])
    @jwt_required()
    def check_profile():
        data = request.get_json()
        app.logger.debug('Check profile data: %s', data)
        user_id = get_jwt_identity()
        existing_profile = Profile.query.filter_by(group_id=data['group_id'], user_id=user_id).first()
        if existing_profile:
            return jsonify({'message': 'User already has a profile in this group'}), 400
        return jsonify({'message': 'No existing profile in this group'}), 200
    
    @app.route('/profiles', methods=['POST'])
    @jwt_required()
    def create_profile_route():
        data = request.get_json()
        app.logger.debug('Create profile data: %s', data)
        user_id = get_jwt_identity()
        try:
            new_profile = create_profile(data, user_id)
            return jsonify({
                'id': str(new_profile.id),
                'name': new_profile.name,
                'picture': new_profile.picture,
                'bio': new_profile.bio,
                'group_id': str(new_profile.group_id)
            }), 201
        except BadRequest as e:
            return jsonify({'message': str(e)}), 400
    
    @app.route('/profiles', methods=['GET'])
    @jwt_required()
    def get_profiles():
        app.logger.debug('Fetching all profiles')
        profiles = Profile.query.all()
        return jsonify([{'id': profile.id, 'name': profile.name, 'picture': profile.picture, 'bio': profile.bio, 'group_id': profile.group_id} for profile in profiles])
    
    @app.route('/profiles/<profile_id>', methods=['GET'])
    @jwt_required()
    def get_profile(profile_id):
        app.logger.debug('Fetching profile with id: %s', profile_id)
        profile = Profile.query.get_or_404(profile_id)
        return jsonify({'id': profile.id, 'name': profile.name, 'picture': profile.picture, 'bio': profile.bio, 'group_id': profile.group_id})
    
    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        app.logger.debug('Register data: %s', data)
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'User already exists'}), 400
        if not is_strong_password(data['password']):
            return jsonify({'message': 'Password must be at least 8 characters long and include an uppercase letter, a lowercase letter, and a number'}), 400
        new_user = User(email=data['email'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        app.logger.debug('Login data: %s', data)
        user = User.query.filter_by(email=data['email']).first()
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=str(user.id))
            return jsonify({'token': access_token}), 200
        return jsonify({'message': 'Invalid credentials'}), 401
    
    @app.route('/protected', methods=['GET'])
    @jwt_required()
    def protected():
        current_user_id = get_jwt_identity()
        app.logger.debug('Protected route accessed by user: %s', current_user_id)
        return jsonify({'message': f'Hello user {current_user_id}'}), 200
    
    @app.route('/groups/<group_id>/chats', methods=['POST'])
    @jwt_required()
    def create_chat_route(group_id):
        data = request.get_json()
        app.logger.debug('Create chat data: %s', data)
        try:
            new_chat = create_chat(data, group_id)
            user_id = get_jwt_identity()
            if user_id:
                profile = Profile.query.filter_by(user_id=user_id, group_id=group_id).first()
                if profile and profile not in new_chat.participants:
                    new_chat.participants.append(profile)
            db.session.commit()
            return jsonify({'id': str(new_chat.id)}), 201
        except BadRequest as e:
            return jsonify({'message': str(e)}), 400
    
    @app.route('/groups/<group_id>/chats', methods=['GET'])
    @jwt_required()
    def list_chats(group_id):
        app.logger.debug('Listing chats for group: %s', group_id)
        profile_id = request.args.get('profile_id')
        if profile_id:
            chats = Chat.query.filter(Chat.group_id == group_id, Chat.participants.any(id=profile_id)).all()
        else:
            chats = Chat.query.filter_by(group_id=group_id).all()
        return jsonify([{
            'id': chat.id,
            'name': chat.name,
            'created_at': chat.created_at.isoformat(),
            'updated_at': chat.updated_at.isoformat(),
            'participant_ids': [str(p.id) for p in chat.participants]
        } for chat in chats])
    
    @app.route('/chats/<chat_id>', methods=['GET'])
    @jwt_required()
    def get_chat(chat_id):
        app.logger.debug('Fetching chat with id: %s', chat_id)
        chat = Chat.query.get_or_404(chat_id)
        return jsonify({
            'id': chat.id,
            'name': chat.name,
            'created_at': chat.created_at.isoformat(),
            'updated_at': chat.updated_at.isoformat(),
            'group_id': chat.group_id,
            'participant_ids': [str(p.id) for p in chat.participants]
        })
    
    @app.route('/chats/<chat_id>', methods=['PUT'])
    @jwt_required()
    def update_chat_route(chat_id):
        data = request.get_json()
        app.logger.debug('Update chat data: %s', data)
        chat = Chat.query.get_or_404(chat_id)
        updated_chat = update_chat(chat, data)
        return jsonify({'id': updated_chat.id})
    
    @app.route('/messages', methods=['POST'])
    @jwt_required()
    def create_message():
        data = request.get_json()
        app.logger.debug('Create message data: %s', data)
        new_message = Message(content=data['content'], chat_id=data['chat_id'], profile_id=data['profile_id'])
        db.session.add(new_message)
        db.session.commit()
        return jsonify({'id': str(new_message.id)}), 201

    @app.route('/chats/<chat_id>/messages', methods=['GET'])
    @jwt_required()
    def get_messages(chat_id):
        app.logger.debug('Fetching messages for chat: %s', chat_id)
        messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.created_at).all()
        return jsonify([{
            'id': message.id,
            'content': message.content,
            'created_at': message.created_at.isoformat(),
            'chat_id': message.chat_id,
            'profile_id': message.profile_id
        } for message in messages])
    
    ### Route Definitions End ###
    
    return app  # Ensure the app is returned

# Assign the Flask application to a global variable for Gunicorn
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
