from todos.entrypoints.api.dependencies import get_uow
from todos.test_utils.factories import build_project
from todos.test_utils.fake_unit_of_work import FakeUnitOfWork


def test_projects_endpoint_returns_list_of_projects(client):
    # Given
    fake_uow = FakeUnitOfWork(
        projects=[
            build_project(id=1, name="Project One"),
            build_project(id=2, name="Project Two"),
        ]
    )
    client.app.dependency_overrides[get_uow] = lambda: fake_uow

    # When
    response = client.get("/projects")

    # Then
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Project One"},
        {"id": 2, "name": "Project Two"},
    ]


def test_project_endpoint_returns_the_project(client):
    # Given
    fake_uow = FakeUnitOfWork(
        projects=[
            build_project(id=1, name="Project One"),
        ]
    )
    client.app.dependency_overrides[get_uow] = lambda: fake_uow

    # When
    response = client.get("/projects/1")

    # Then
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Project One"}


def test_project_endpoint_responds_with_404_if_project_cannot_be_found(client):
    # Given
    fake_uow = FakeUnitOfWork(projects=[])
    client.app.dependency_overrides[get_uow] = lambda: fake_uow

    # When
    response = client.get("/projects/1")

    # Then
    assert response.status_code == 404
