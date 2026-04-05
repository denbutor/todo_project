from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_task():
    response = client.post("/tasks", json={"title": "Test task", "description": "Test desc"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test task"
    assert "id" in data


def test_get_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_task():
    create_res = client.post("/tasks", json={"title": "Old title"})
    task_id = create_res.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={"title": "New title", "completed": True})
    assert response.status_code == 200
    assert response.json()["title"] == "New title"
    assert response.json()["completed"] is True


def test_delete_task():
    create_res = client.post("/tasks", json={"title": "To delete"})
    task_id = create_res.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200

    get_res = client.get("/tasks")
    assert not any(t["id"] == task_id for t in get_res.json())


def test_update_nonexistent_task():
    response = client.put("/tasks/999", json={"title": "Ghost"})
    assert response.status_code == 404