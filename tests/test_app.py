import pytest

def add(x: int, y:int):
    return x + y



@pytest.mark.parametrize("x, y, expected",[(2, 3, 5),(4, 5, 9),(6, 7, 13)])
def test_add(x, y, expected):
    assert add(x, y) == expected


