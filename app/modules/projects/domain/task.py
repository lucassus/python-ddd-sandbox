from datetime import datetime
from typing import NewType, Optional

from app.modules.shared_kernel.entities.entity import Entity

TaskNumber = NewType("TaskNumber", int)


class Task(Entity):
    _number: TaskNumber
    _name: str
    _completed_at: Optional[datetime] = None

    def __init__(
        self,
        number: TaskNumber,
        name: str,
    ):
        self._number = number
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def number(self) -> TaskNumber:
        return self._number

    @property
    def completed_at(self) -> Optional[datetime]:
        return self._completed_at

    @property
    def is_completed(self) -> bool:
        return self._completed_at is not None

    def complete(self, now: datetime) -> None:
        if not self.is_completed:
            self._completed_at = now

    def incomplete(self) -> None:
        if self.is_completed:
            self._completed_at = None
