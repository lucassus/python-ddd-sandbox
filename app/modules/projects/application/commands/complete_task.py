from dataclasses import dataclass
from datetime import datetime

from app.modules.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.projects.domain.project import ProjectID
from app.modules.projects.domain.task import TaskNumber
from app.shared.message_bus import Command, CommandHandler


@dataclass(frozen=True)
class CompleteTask(Command):
    project_id: ProjectID
    task_number: TaskNumber
    now: datetime


class CompleteTaskHandler(CommandHandler[CompleteTask, None]):
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def __call__(self, command: CompleteTask) -> None:
        with self.uow:
            project = self.uow.projects.get(command.project_id)
            project.complete_task(command.task_number, command.now)

            self.uow.commit()
