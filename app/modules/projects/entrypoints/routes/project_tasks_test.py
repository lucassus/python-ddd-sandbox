from unittest.mock import Mock

from starlette.testclient import TestClient

from app.modules.projects.application.queries.task_queries import ListTasksQuery
from app.modules.projects.application.tasks_service import TasksService
from app.modules.projects.domain.project import ProjectID
from app.modules.projects.domain.task import TaskNumber
from app.modules.projects.entrypoints.containers import Container


def test_task_create_endpoint(container: Container, client: TestClient):
    # Given
    mock_tasks_service = Mock(spec=TasksService)
    mock_tasks_service.create_task.return_value = TaskNumber(1)

    # When
    with container.tasks_service.override(mock_tasks_service):
        response = client.post(
            "/projects/123/tasks",
            json={"name": "Some task"},
            follow_redirects=False,
        )

    # Then
    assert response.status_code == 303
    assert response.headers["Location"] == "/api/projects/123/tasks/1"
    mock_tasks_service.create_task.assert_called_once_with(project_id=ProjectID(123), name="Some task")


def test_task_endpoint_returns_404_when_project_not_found(container: Container, client: TestClient):
    # Given
    get_project_query_mock = Mock(return_value=None)

    # When
    with container.get_project_query.override(get_project_query_mock):
        response = client.get("/projects/1/tasks/1")

    # Then
    assert response.status_code == 404


def test_task_endpoint_returns_404_when_task_not_found(container: Container, client: TestClient):
    # Given
    get_project_query_mock = Mock(return_value=Mock(id=1))
    get_task_query_mock = Mock(return_value=None)

    # When
    with (
        container.get_project_query.override(get_project_query_mock),
        container.get_task_query.override(get_task_query_mock),
    ):
        response = client.get("/projects/1/tasks/1")

    # Then
    assert response.status_code == 404


def test_task_list_endpoint(container: Container, client: TestClient):
    # Given
    class ListTasksQueryMock(ListTasksQuery):
        def __call__(self, project_id: ProjectID) -> ListTasksQuery.Result:
            return ListTasksQuery.Result(
                tasks=[
                    ListTasksQuery.Result.Task(
                        number=TaskNumber(1),
                        name="Some task",
                        completed_at=None,
                    ),
                ]
            )

    list_tasks_query_mock = Mock(wraps=ListTasksQueryMock())

    # When
    with container.list_tasks_query.override(list_tasks_query_mock):
        response = client.get("/projects/1/tasks")

    # Then
    assert response.status_code == 200
    list_tasks_query_mock.assert_called_once_with(ProjectID(1))
    assert response.json() == {
        "tasks": [
            {
                "number": 1,
                "name": "Some task",
                "completedAt": None,
            },
        ]
    }


def test_task_complete_endpoint(container: Container, client: TestClient):
    # Given
    mock_tasks_service = Mock(spec=TasksService)
    mock_tasks_service.create_task.return_value = TaskNumber(667)

    # When
    with container.tasks_service.override(mock_tasks_service):
        response = client.put(
            "/projects/665/tasks/667/complete",
            follow_redirects=False,
        )

    # Then
    assert response.status_code == 303
    assert response.headers["Location"] == "/api/projects/665/tasks/667"
    mock_tasks_service.complete_task.assert_called_once_with(ProjectID(665), TaskNumber(667))


def test_task_incomplete_endpoint(container: Container, client: TestClient):
    # Given
    mock_tasks_service = Mock(spec=TasksService)
    mock_tasks_service.create_task.return_value = TaskNumber(668)

    # When
    with container.tasks_service.override(mock_tasks_service):
        response = client.put(
            "/projects/665/tasks/668/incomplete",
            follow_redirects=False,
        )

    # Then
    assert response.status_code == 303
    assert response.headers["Location"] == "/api/projects/665/tasks/668"
    mock_tasks_service.incomplete_task.assert_called_once_with(ProjectID(665), TaskNumber(668))
