from app.command.projects.application.create_project import CreateProject
from app.command.projects.application.ports.abstract_project_repository import AbstractProjectRepository
from app.command.shared_kernel.entities.user_id import UserID


def test_create_project_use_case(fake_uow, repository: AbstractProjectRepository):
    create_project = CreateProject(uow=fake_uow)
    project_id = create_project(user_id=UserID(1), name="Project X")

    assert fake_uow.committed

    project = repository.get(project_id)
    assert project.name == "Project X"
    assert project.user_id == UserID(1)
    assert len(project.tasks) == 0
