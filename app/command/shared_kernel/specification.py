import abc
from abc import ABCMeta
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class Specification(Generic[T], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        raise NotImplementedError

    def __call__(self, candidate: T) -> bool:
        return self.is_satisfied_by(candidate)

    def __and__(self, other: "Specification[T]") -> "Specification[T]":
        return And(self, other)

    def __or__(self, other: "Specification[T]") -> "Specification[T]":
        return Or(self, other)

    def __invert__(self) -> "Specification[T]":
        return NotSpecification(self)


class BinarySpecification(Specification[T], metaclass=ABCMeta):
    def __init__(self, left: Specification[T], right: Specification[T]):
        self._left = left
        self._right = right


class And(BinarySpecification[T]):
    def is_satisfied_by(self, candidate: T) -> bool:
        return self._left.is_satisfied_by(candidate) and self._right.is_satisfied_by(candidate)


class Or(BinarySpecification[T]):
    def is_satisfied_by(self, candidate: T) -> bool:
        return self._left.is_satisfied_by(candidate) or self._right.is_satisfied_by(candidate)


class UnarySpecification(Specification[T], metaclass=ABCMeta):
    def __init__(self, spec: Specification[T]):
        self._spec = spec


class NotSpecification(UnarySpecification[T]):
    def is_satisfied_by(self, candidate: T) -> bool:
        return not self._spec.is_satisfied_by(candidate)


class AlwaysTrue(Specification[Any]):
    def is_satisfied_by(self, candidate: Any) -> bool:
        return True


class AlwaysFalse(Specification[Any]):
    def is_satisfied_by(self, candidate: Any) -> bool:
        return False
