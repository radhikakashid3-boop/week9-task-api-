def test_profile(client, auth_headers):
    response = client.get("/api/users/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.get_json()["data"]["user"]["username"] == "tester"
