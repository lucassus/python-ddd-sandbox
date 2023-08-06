from typing import Generic, List, Tuple, TypeVar

T = TypeVar("T", int, str)


class Stack(Generic[T]):
    def __init__(self):
        self._items: List[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()


R = TypeVar("R")


def swap(x: T, y: R) -> Tuple[R, T]:
    return y, x


if __name__ == "__main__":
    stack = Stack[int]()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    assert stack.pop() == 3  # noqa: S101

    x, y = swap(1, "foo")
