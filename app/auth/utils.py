from flask_jwt_extended import create_access_token, create_refresh_token

def create_tokens(user_id):
    identity = str(user_id)
    return create_access_token(identity=identity), create_refresh_token(identity=identity)
