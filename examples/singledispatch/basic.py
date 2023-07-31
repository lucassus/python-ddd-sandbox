import functools
from typing import Any


@functools.singledispatch
def add(a, b):
    raise NotImplementedError


@add.register
def handle_integers(a: int, b: int) -> int:
    result = a + b
    print(f"The result is {result}")
    return result


@add.register
def handle_strings(a: str, b: str) -> str:
    result = a + b
    print(f"The result is {result}")
    return result


@add.register
def handle_lists(a: list[Any], b: list[Any]) -> list[Any]:
    result = a + b
    print(f"The result is {result}")
    return result


if __name__ == "__main__":
    add(1, 2)
    add("Python", "Programming")
    add([1, 2, 3], [5, 6, 7])
