import pytest
from grid import Grid, GridIndex, GridSlice


def test_str():
    grid = Grid()
    print(grid)
    expected = "0 0 0 0\n0 0 0 0\n0 0 0 0\n0 0 0 0"
    assert str(grid) == expected


def test_grid():
    grid = Grid([i for i in range(16)], width=4, height=4)
    assert grid.width == 4
    assert grid.height == 4
    assert grid[GridIndex(1, 0)] == 4
    assert grid[GridIndex(3, 3)] == 15


def test_grid_slice():
    # Test specific slice
    grid = Grid([i for i in range(16)], width=4, height=4)
    slice = GridSlice(grid, select_rows=False, axis=3)
    expected_list = [3, 7, 11, 15]
    assert slice == expected_list
    # Test all row slices
    slices = [GridSlice(grid, select_rows=True, axis=col) for col in range(4)]
    expected_lists = [[row * 4 + col for col in range(4)] for row in range(4)]
    for slice, expected in zip(slices, expected_lists):
        assert slice == expected
    # Test reversed row slices
    slices = [
        GridSlice(grid, select_rows=True, axis=col, reverse=True) for col in range(4)
    ]
    expected_lists = [[row * 4 + col for col in range(4)][::-1] for row in range(4)]
    for slice, expected in zip(slices, expected_lists):
        assert slice == expected
    # Test all column slices
    slices = [GridSlice(grid, select_rows=False, axis=col) for col in range(4)]
    expected_lists = [[x for x in range(i, i + 12 + 1, 4)] for i in range(4)]
    for slice, expected in zip(slices, expected_lists):
        assert slice == expected
    # Test reversed col slices
    slices = [
        GridSlice(grid, select_rows=False, axis=col, reverse=True) for col in range(4)
    ]
    expected_lists = [[x for x in range(i, i + 12 + 1, 4)][::-1] for i in range(4)]
    for slice, expected in zip(slices, expected_lists):
        assert slice == expected
