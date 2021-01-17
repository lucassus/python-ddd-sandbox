import pytest

from todos.utils import camelize


@pytest.mark.parametrize(
    "str,expected",
    [
        ("foo", "foo"),
        ("foo_bar", "fooBar"),
        ("foo_bar_baz", "fooBarBaz"),
    ],
)
def test_camelize(str, expected):
    assert camelize(str) == expected