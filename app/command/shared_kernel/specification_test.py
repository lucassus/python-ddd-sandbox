from app.command.shared_kernel.specification import AlwaysFalse, AlwaysTrue, Specification


class GreaterThan(Specification[int]):
    def __init__(self, number: int):
        self._number = number

    def is_satisfied_by(self, candidate):
        return candidate > self._number


class SmallerThan(Specification[int]):
    def __init__(self, number: int):
        self._number = number

    def is_satisfied_by(self, candidate):
        return candidate < self._number


class IsEven(Specification[int]):
    def is_satisfied_by(self, candidate):
        return candidate % 2 == 0


def test_specification():
    spec = GreaterThan(7)

    assert spec.is_satisfied_by(8) is True
    assert spec.is_satisfied_by(7) is False


def test_and_specification():
    spec = GreaterThan(7) & IsEven() & SmallerThan(10)

    assert spec.is_satisfied_by(8) is True
    assert spec.is_satisfied_by(6) is False
    assert spec.is_satisfied_by(9) is False
    assert spec.is_satisfied_by(10) is False


def test_or_specification():
    spec = GreaterThan(3) | IsEven()

    assert spec.is_satisfied_by(2) is True
    assert spec.is_satisfied_by(5) is True


def test_always_true_specification():
    spec = AlwaysTrue()

    assert spec.is_satisfied_by(2) is True


def test_always_false_specification():
    spec = AlwaysFalse()

    assert spec.is_satisfied_by(2) is False
