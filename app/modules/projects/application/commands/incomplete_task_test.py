from app.modules.projects.application.commands.incomplete_task import IncompleteTask, IncompleteTaskHandler
from app.modules.projects.application.ports.abstract_project_repository import AbstractProjectRepository
from app.modules.projects.domain.project_builder import ProjectBuilder
from app.utc_datetime import utc_datetime


def test_incomplete_task_handler(repository: AbstractProjectRepository, fake_uow):
    project = repository.create(ProjectBuilder().build())
    task = project.add_task(name="Testing...")
    project.complete_task(task.number, now=utc_datetime(2021, 1, 8))

    handler = IncompleteTaskHandler(uow=fake_uow)
    handler(
        IncompleteTask(
            project_id=project.id,
            task_number=task.number,
        )
    )

    assert task.completed_at is None
    assert fake_uow.committed
