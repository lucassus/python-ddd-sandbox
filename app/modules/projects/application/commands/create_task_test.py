from app.modules.projects.application.commands import CreateTask, CreateTaskHandler
from app.modules.projects.application.ports.abstract_project_repository import AbstractProjectRepository
from app.modules.projects.domain.project_builder import ProjectBuilder


def test_create_task_handler(repository: AbstractProjectRepository, fake_uow):
    project = repository.create(ProjectBuilder().build())

    handler = CreateTaskHandler(uow=fake_uow)
    handler(CreateTask(project_id=project.id, name="Testing..."))

    assert project.tasks[-1].name == "Testing..."
    assert fake_uow.committed
