from dataclasses import dataclass

from app.infrastructure.message_bus import Command, CommandHandler
from app.modules.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.projects.domain.project import ProjectID
from app.modules.projects.domain.task import TaskNumber


@dataclass(frozen=True)
class IncompleteTask(Command[None]):
    project_id: ProjectID
    task_number: TaskNumber


class IncompleteTaskHandler(CommandHandler[IncompleteTask, None]):
    def __init__(self, uow: AbstractUnitOfWork):
        self._uow = uow

    def __call__(self, command: IncompleteTask) -> None:
        project_id, number = command.project_id, command.task_number

        with self._uow as uow:
            project = uow.projects.get(project_id)
            project.incomplete_task(number)

            uow.commit()
