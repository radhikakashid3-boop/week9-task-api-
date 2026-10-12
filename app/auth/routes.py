from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from ..extensions import db, limiter
from ..models import User
from ..utils.validators import validate_registration
from ..utils.responses import success_response, error_response
from .utils import create_tokens

class RegisterResource(Resource):
    @limiter.limit("10 per minute")
    def post(self):
        data = request.get_json(silent=True) or {}
        errors = validate_registration(data)
        if errors:
            return error_response("Validation failed", 400, errors)

        username = data["username"].strip()
        email = data["email"].strip().lower()

        if User.query.filter_by(username=username).first():
            return error_response("Username already exists", 409)
        if User.query.filter_by(email=email).first():
            return error_response("Email already exists", 409)

        user = User(username=username, email=email)
        user.set_password(data["password"])
        db.session.add(user)
        db.session.commit()

        access_token, refresh_token = create_tokens(user.id)
        return success_response({
            "message": "User registered successfully",
            "user": user.to_dict(),
            "access_token": access_token,
            "refresh_token": refresh_token
        }, status_code=201)

class LoginResource(Resource):
    @limiter.limit("10 per minute")
    def post(self):
        data = request.get_json(silent=True) or {}
        email = str(data.get("email", "")).strip().lower()
        password = str(data.get("password", ""))

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return error_response("Invalid email or password", 401)

        access_token, refresh_token = create_tokens(user.id)
        return success_response({
            "message": "Login successful",
            "user": user.to_dict(),
            "access_token": access_token,
            "refresh_token": refresh_token
        })

class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        user_id = get_jwt_identity()
        return success_response({
            "access_token": create_access_token(identity=user_id)
        })

class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        return success_response(message="Logout successful")

auth_ns = {
    "register": RegisterResource,
    "login": LoginResource,
    "refresh": RefreshResource,
    "logout": LogoutResource
}
