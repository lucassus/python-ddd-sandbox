import abc
from dataclasses import dataclass


@dataclass
class Entity(metaclass=abc.ABCMeta):
    pass
