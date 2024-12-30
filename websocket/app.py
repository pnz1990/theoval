from flask import Flask, request, jsonify
from common.models import db, Message
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import os
from werkzeug.exceptions import BadRequest  
from services import (
    authenticate
)
import logging

logging.basicConfig(level=logging.DEBUG)

def create_app(test_config=None):
    """
    Creates and configures the Flask application.

    Args:
        test_config (dict, optional): Configuration for testing.

    Returns:
        Flask: Configured Flask application.
    """
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True, allow_headers=["Content-Type", "Authorization"], methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    
    if test_config:
        app.config.update(test_config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB', 'postgres')}"
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')
    
    db.init_app(app)  # Initialize SQLAlchemy with the app
    jwt = JWTManager(app)
    
    logging.basicConfig(level=logging.DEBUG)
    
    # Global error handler for BadRequest
    @app.errorhandler(BadRequest)
    def handle_bad_request(e):
        """
        Handles BadRequest exceptions globally.

        Args:
            e (BadRequest): The exception instance.

        Returns:
            Response: JSON response with error message and status code 400.
        """
        return jsonify({'message': e.description}), 400
    
    ### Route Definitions Start ###
    
    @app.route('/health')
    def health_check():
        """
        Health check endpoint to verify the application's status.

        Returns:
            Response: JSON response indicating health status.
        """
        return jsonify({'status': 'healthy'}), 200
        """
        Endpoint to create a new group.

        Requires JWT authentication.

        Returns:
            Response: JSON response with the created group's ID.
        """
        data = request.get_json()
        app.logger.debug('Create group data: %s', data)
        app.logger.debug('Type of max_profiles: %s', type(data.get('max_profiles')))
        new_group = create_group(data)
        return jsonify({'id': str(new_group.id)}), 201
    
    @app.route('/messages', methods=['POST'])
    @jwt_required()
    def create_message():
        """
        Endpoint to create a new message within a chat.

        Requires JWT authentication.

        Returns:
            Response: JSON response with the created message's ID.
        """
        data = request.get_json()
        app.logger.debug('Create message data: %s', data)
        new_message = Message(content=data['content'], chat_id=data['chat_id'], profile_id=data['profile_id'])
        db.session.add(new_message)
        db.session.commit()
        return jsonify({'id': str(new_message.id)}), 201

    @app.route('/chats/<chat_id>/messages', methods=['GET'])
    @jwt_required()
    def get_messages(chat_id):
        """
        Endpoint to retrieve all messages from a chat.

        Requires JWT authentication.

        Args:
            chat_id (str): ID of the chat.

        Returns:
            Response: JSON list of messages.
        """
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
