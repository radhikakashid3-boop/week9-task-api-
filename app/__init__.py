from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS

from config import Config
from .extensions import db, jwt, limiter

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    CORS(app)
    Migrate(app, db)
    api = Api(app)

    from .auth.routes import auth_ns
    from .tasks.routes import task_ns
    from .users.routes import user_ns

    api.add_resource(auth_ns["register"], "/api/auth/register")
    api.add_resource(auth_ns["login"], "/api/auth/login")
    api.add_resource(auth_ns["refresh"], "/api/auth/refresh")
    api.add_resource(auth_ns["logout"], "/api/auth/logout")

    api.add_resource(task_ns["list"], "/api/tasks")
    api.add_resource(task_ns["single"], "/api/tasks/<int:task_id>")
    api.add_resource(task_ns["search"], "/api/tasks/search")

    api.add_resource(user_ns["profile"], "/api/users/me")

    with app.app_context():
        db.create_all()

    return app
