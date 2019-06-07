from flask import g, jsonify
from flask_login import current_user
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models import User
from app.api.errors import errorResponse

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return False
    g.current_user = user
    return user.verify_password_from_db(password)

@basic_auth.error_handler
def basicAuthError():
    return errorResponse(401)


@token_auth.verify_token
def verify_token(token):
    g.current_user = User.verify_auth_token(token)
    return g.current_user is not None

@token_auth.error_handler
def unauthorized_token():
    response = jsonify({'status': 401, 'error': 'unauthorized',
                        'message': 'please send your authentication token'})
    response.status_code = 401
    return response