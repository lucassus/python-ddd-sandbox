from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Callable, Optional


@dataclass
class Task:
    id: int = field(init=False)
    name: str
    completed_at: Optional[date] = None

    @property
    def is_completed(self) -> bool:
        return self.completed_at is not None

    # TODO: Figure out how to dry it
    def complete(self, now: Callable[..., date] = datetime.utcnow) -> None:
        if not self.is_completed:
            self.completed_at = now()

    def incomplete(self) -> None:
        if self.is_completed:
            self.completed_at = None
