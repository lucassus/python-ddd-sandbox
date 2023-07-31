from abc import abstractmethod
from typing import Protocol, runtime_checkable


@runtime_checkable
class Printable(Protocol):
    @abstractmethod
    def print(self) -> None:
        raise NotImplementedError


class MyPrintable:
    def print(self) -> None:
        print("Hello DEV!")


class NonPrintable:
    pass


def simple_print(printable: Printable):
    if isinstance(printable, Printable):
        print("It is a printable!")
        printable.print()
    else:
        print("boooo, not a printable")


if __name__ == "__main__":
    simple_print(MyPrintable())
    # simple_print(NonPrintable())
