import pytest
from grid import Grid, GridIndex, GridSlice


def test_str():
    grid = Grid()
    print(grid)
    expected = "0 0 0 0\n0 0 0 0\n0 0 0 0\n0 0 0 0"
    assert str(grid) == expected


def test():
    grid = Grid([i for i in range(16)], width=4, height=4)
    assert grid.width == 4
    assert grid.height == 4
    assert grid[GridIndex(1, 0)] == 4
    assert grid[GridIndex(3, 3)] == 15
