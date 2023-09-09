from dataclasses import dataclass

from app.modules.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.projects.domain.project import ProjectID
from app.modules.projects.domain.task import TaskNumber
from app.shared.message_bus import Command, CommandHandler


@dataclass(frozen=True)
class CreateTask(Command[TaskNumber]):
    project_id: ProjectID
    name: str


class CreateTaskHandler(CommandHandler[CreateTask, TaskNumber]):
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def __call__(self, command: CreateTask) -> TaskNumber:
        with self.uow:
            project = self.uow.projects.get(command.project_id)

            task = project.add_task(command.name)
            self.uow.commit()

            return task.number
