import pytest
from app import create_app
from app.extensions import db
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    RATELIMIT_ENABLED = False

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    client.post("/api/auth/register", json={
        "username": "tester",
        "email": "tester@example.com",
        "password": "secret123"
    })
    response = client.post("/api/auth/login", json={
        "email": "tester@example.com",
        "password": "secret123"
    })
    token = response.get_json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}
