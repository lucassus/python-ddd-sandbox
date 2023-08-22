from unittest.mock import Mock

from starlette.testclient import TestClient

from app.modules.authentication_contract import AuthenticationContract
from app.modules.projects.application.tasks_service import TasksService
from app.modules.projects.domain.project import ProjectID
from app.modules.projects.domain.task import TaskNumber
from app.modules.projects.entrypoints.containers import Container
from app.modules.projects.entrypoints.dependencies import get_current_user
from app.modules.projects.queries.task_queries import ListTasksQuery
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID


def test_task_create_endpoint(container: Container, app, client: TestClient):
    # Given
    mock_tasks_service = Mock(spec=TasksService)
    mock_tasks_service.create_task.return_value = TaskNumber(1)

    app.dependency_overrides[get_current_user] = lambda: AuthenticationContract.CurrentUserDTO(
        id=UserID(1),
        email=EmailAddress("test@email.com"),
    )

    # When
    with container.application.tasks_service.override(mock_tasks_service):
        response = client.post(
            "/projects/123/tasks",
            json={"name": "Some task"},
            follow_redirects=False,
        )

    # Then
    assert response.status_code == 303
    assert response.headers["Location"] == "/api/projects/123/tasks/1"
    mock_tasks_service.create_task.assert_called_once_with(
        project_id=ProjectID(123),
        name="Some task",
        created_by=UserID(1),
    )


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

    list_tasks_query_mock = Mock(wraps=ListTasksQueryMock(engine=Mock()))

    # When
    with container.queries.list_tasks.override(list_tasks_query_mock):
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
    with container.application.tasks_service.override(mock_tasks_service):
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
    with container.application.tasks_service.override(mock_tasks_service):
        response = client.put(
            "/projects/665/tasks/668/incomplete",
            follow_redirects=False,
        )

    # Then
    assert response.status_code == 303
    assert response.headers["Location"] == "/api/projects/665/tasks/668"
    mock_tasks_service.incomplete_task.assert_called_once_with(ProjectID(665), TaskNumber(668))
