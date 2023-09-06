from unittest.mock import Mock

from app.modules.projects.application.commands import CreateProject, CreateProjectHandler
from app.modules.projects.application.ports.abstract_project_repository import AbstractProjectRepository
from app.modules.projects.domain.project import Project, ProjectName
from app.modules.shared_kernel.entities.user_id import UserID
from app.modules.shared_kernel.message_bus import MessageBus


def test_create_project_use_case(fake_uow, message_bus: MessageBus, repository: AbstractProjectRepository):
    # Given
    create_project = CreateProjectHandler(uow=fake_uow, bus=message_bus)
    listener_mock = Mock()
    message_bus.listen(Project.Created, listener_mock)
    user_id = UserID.generate()

    # When
    project_id = create_project(CreateProject(user_id=user_id, name=ProjectName("Project X")))

    # Then
    assert fake_uow.committed

    project = repository.get(project_id)
    assert project.name == "Project X"
    assert project.user_id == user_id
    assert len(project.tasks) == 0

    listener_mock.assert_called_once_with(Project.Created(project_id=project_id))
