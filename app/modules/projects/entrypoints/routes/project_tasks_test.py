from unittest.mock import ANY, Mock

import pytest
from httpx import AsyncClient

from app.modules.authentication_contract import AuthenticationContract
from app.modules.projects.application.commands import CompleteTask, CreateTask, IncompleteTask
from app.modules.projects.application.queries import ListTasks
from app.modules.projects.domain.project import ProjectID
from app.modules.projects.domain.task import TaskNumber
from app.modules.projects.entrypoints.dependencies import get_current_user
from app.modules.projects.infrastructure.containers import Container
from app.modules.projects.infrastructure.queries.task_query_handlers import ListTasksQueryHandler
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID
from app.shared.message_bus import MessageBus


@pytest.mark.asyncio
async def test_task_create_endpoint(container: Container, app, client: AsyncClient):
    # Given
    bus_mock = Mock(spec=MessageBus)
    bus_mock.execute.return_value = TaskNumber(1)
    user_id = UserID.generate()

    app.dependency_overrides[get_current_user] = lambda: AuthenticationContract.Identity(
        id=user_id,
        email=EmailAddress("test@email.com"),
    )

    # When
    with container.bus.override(bus_mock):
        response = await client.post(
            "/projects/123/tasks",
            json={"name": "Some task"},
            follow_redirects=False,
        )

    # Then
    assert response.status_code == 303
    assert response.headers["Location"] == "/api/projects/123/tasks/1"
    bus_mock.execute.assert_called_once_with(CreateTask(project_id=ProjectID(123), name="Some task"))


@pytest.mark.asyncio
async def test_task_list_endpoint(container: Container, client: AsyncClient):
    # Given
    class ListTasksQueryHandlerMock(ListTasksQueryHandler):
        async def __call__(self, query: ListTasks) -> ListTasks.Result:
            return ListTasks.Result(
                tasks=[
                    ListTasks.Result.Task(
                        number=TaskNumber(1),
                        name="Some task",
                        completed_at=None,
                    ),
                ]
            )

    handler_mock = Mock(wraps=ListTasksQueryHandlerMock(engine=Mock()))

    # When
    with container.queries.list_tasks_handler.override(handler_mock):
        response = await client.get("/projects/1/tasks")

    # Then
    assert response.status_code == 200
    handler_mock.assert_called_once_with(ListTasks(ProjectID(1)))
    assert response.json() == {
        "tasks": [
            {
                "number": 1,
                "name": "Some task",
                "completedAt": None,
            },
        ]
    }


@pytest.mark.asyncio
async def test_task_complete_endpoint(container: Container, client: AsyncClient):
    # Given
    bus_mock = Mock(spec=MessageBus)
    bus_mock.execute.return_value = TaskNumber(667)

    # When
    with container.bus.override(bus_mock):
        response = await client.put(
            "/projects/665/tasks/667/complete",
            follow_redirects=False,
        )

    # Then
    assert response.status_code == 303
    assert response.headers["Location"] == "/api/projects/665/tasks/667"
    bus_mock.execute.assert_called_once_with(
        CompleteTask(
            project_id=ProjectID(665),
            task_number=TaskNumber(667),
            now=ANY,
        )
    )


@pytest.mark.asyncio
async def test_task_incomplete_endpoint(container: Container, client: AsyncClient):
    # Given
    bus_mock = Mock(spec=MessageBus)
    bus_mock.execute.return_value = TaskNumber(668)

    # When
    with container.bus.override(bus_mock):
        response = await client.put(
            "/projects/665/tasks/668/incomplete",
            follow_redirects=False,
        )

    # Then
    assert response.status_code == 303
    assert response.headers["Location"] == "/api/projects/665/tasks/668"
    bus_mock.execute.assert_called_once_with(
        IncompleteTask(
            project_id=ProjectID(665),
            task_number=TaskNumber(668),
        )
    )
