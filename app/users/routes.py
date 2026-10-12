from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import User
from ..extensions import db
from ..utils.responses import success_response, error_response

class ProfileResource(Resource):
    @jwt_required()
    def get(self):
        user = db.session.get(User, int(get_jwt_identity()))
        if not user:
            return error_response("User not found", 404)
        return success_response({"user": user.to_dict()})

user_ns = {"profile": ProfileResource}
