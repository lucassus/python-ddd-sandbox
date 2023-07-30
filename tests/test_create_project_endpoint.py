from starlette.testclient import TestClient


def test_create_project(register_user, create_project, client: TestClient):
    response = register_user(email="test@email.com")

    assert response.status_code == 200
    user_id = response.json()["id"]

    response = create_project(user_id, name="Project X")

    assert response.status_code == 200

    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Project X"
