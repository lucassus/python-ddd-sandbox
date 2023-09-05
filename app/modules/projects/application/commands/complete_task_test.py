from app.modules.projects.application.commands.complete_task import CompleteTask, CompleteTaskHandler
from app.modules.projects.application.ports.abstract_project_repository import AbstractProjectRepository
from app.modules.projects.domain.project_builder import ProjectBuilder
from app.utc_datetime import utc_datetime


def test_complete_task_handler(repository: AbstractProjectRepository, fake_uow):
    project = repository.create(ProjectBuilder().build())
    task = project.add_task(name="Testing...")
    now = utc_datetime(2021, 1, 8)

    handler = CompleteTaskHandler(uow=fake_uow)
    handler(
        CompleteTask(
            project_id=project.id,
            task_number=task.number,
            now=now,
        )
    )

    assert task.completed_at is now
    assert fake_uow.committed
