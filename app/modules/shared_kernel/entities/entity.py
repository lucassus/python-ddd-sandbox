import abc
from dataclasses import dataclass


@dataclass
class Entity(metaclass=abc.ABCMeta):  # noqa: B024  intentional marker base class
    pass
