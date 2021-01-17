from dataclasses import dataclass, field
from datetime import date, datetime
from typing import TYPE_CHECKING, Callable, List, Optional

if TYPE_CHECKING:
    from todos.domain.models import Project


@dataclass
class Task:
    id: int = field(init=False)
    project_id: int = field(init=False)

    name: str

    project: Optional["Project"] = None  # TODO: More likely redundant association
    completed_at: Optional[date] = None

    @property
    def is_completed(self) -> bool:
        return self.completed_at is not None

    def complete(self, now: Callable[..., date] = datetime.utcnow) -> None:
        if not self.is_completed:
            self.completed_at = now()

    def incomplete(self) -> None:
        if self.is_completed:
            self.completed_at = None
