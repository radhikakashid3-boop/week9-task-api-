def test_register(client):
    response = client.post("/api/auth/register", json={
        "username": "john",
        "email": "john@example.com",
        "password": "secret123"
    })
    assert response.status_code == 201
    assert response.get_json()["status"] == "success"

def test_login(client):
    client.post("/api/auth/register", json={
        "username": "john",
        "email": "john@example.com",
        "password": "secret123"
    })
    response = client.post("/api/auth/login", json={
        "email": "john@example.com",
        "password": "secret123"
    })
    assert response.status_code == 200
    assert "access_token" in response.get_json()["data"]
