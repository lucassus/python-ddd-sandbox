import abc
import functools
from dataclasses import dataclass


class Event(abc.ABC):
    pass


@dataclass
class UserCreated(Event):
    id: int
    email: str


@dataclass
class UserUpdated(Event):
    id: int
    email: str
    password: str


@functools.singledispatch
def dispatch(event: Event):
    raise NotImplementedError


@dispatch.register
def handle_user_created(event: UserCreated):
    print(f"Handling user created event for id={event.id}")


@dispatch.register
def handle_user_updated(event: UserUpdated):
    print(f"Handling user updated event for id={event.id}, password={event.password}")


if __name__ == "__main__":
    print(dispatch.registry.keys())
    dispatch(UserCreated(id=123, email="user@email.com"))
    dispatch(UserUpdated(id=123, email="new@email.com", password="password"))
    dispatch(UserCreated(id=124, email="another@email.com"))
