import logging
from werkzeug.exceptions import BadRequest
from uuid import UUID
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import request, jsonify
from werkzeug.exceptions import Unauthorized

def authenticate(func):
    """
    Decorator to authenticate routes using JWT.

    Args:
        func (callable): The route function to decorate.

    Returns:
        callable: The decorated function.
    """
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
