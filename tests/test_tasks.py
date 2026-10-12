def test_create_task(client, auth_headers):
    response = client.post("/api/tasks", headers=auth_headers, json={
        "title": "Complete Week 9",
        "description": "Build Flask REST API",
        "status": "pending",
        "priority": "high",
        "category": "learning",
        "due_date": "2026-12-31"
    })
    assert response.status_code == 201
    assert response.get_json()["data"]["task"]["title"] == "Complete Week 9"

def test_task_list(client, auth_headers):
    response = client.get("/api/tasks", headers=auth_headers)
    assert response.status_code == 200
    assert "pagination" in response.get_json()["data"]
