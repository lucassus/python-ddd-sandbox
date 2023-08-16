from starlette import status
from starlette.testclient import TestClient


def test_create_project(create_project, client: TestClient):
    response = create_project(name="Project X")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Project X"


def test_list_projects(register_user, create_project, client: TestClient):
    # Given
    response = register_user("test@email.com")
    assert response.status_code == status.HTTP_200_OK

    user_id = response.json()["id"]

    response = create_project(name="Project A", user_id=user_id)
    assert response.status_code == status.HTTP_200_OK

    response = create_project(name="Project B", user_id=user_id)
    assert response.status_code == status.HTTP_200_OK

    # When
    response = client.get("/api/projects")

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["projects"]) == 3
