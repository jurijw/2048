from board import Board
from copy import deepcopy
import pytest

collapsable_lists = [
    [2, 2, 2, 2],
    [2, 4, 8, 16],
    [2, 2, 0, 0],
    [0, 0, 2, 2],
    [2, 4, 4, 2],
    [2, 4, 4, 4],
    [2, 0, 0, 2],
    [0, 0, 0, 0],
    [0, 0, 0, 1],
]

collapsable_lists_expected = [
    [4, 4, 0, 0],
    [2, 4, 8, 16],
    [4, 0, 0, 0],
    [4, 0, 0, 0],
    [2, 8, 2, 0],
    [2, 8, 4, 0],
    [4, 0, 0, 0],
    [0, 0, 0, 0],
    [1, 0, 0, 0],
]

points_expected = [
    8,
    0,
    4,
    4,
    8,
    8,
    4,
    0,
    0,
]

def test_collapse_destructive():
    for input_list, expected_list, expected_points in zip(deepcopy(collapsable_lists), collapsable_lists_expected, points_expected):
        points = Board.collapse_destructive(input_list)
        assert input_list == expected_list, f"Failed with input {input_list}."
        assert points == expected_points, f"Failed with input {input_list}."

def test_collapse_non_destructive():
    for input_list, expected_list, expected_points in zip(collapsable_lists, collapsable_lists_expected, points_expected):
        points, ouput_list = Board.collapse_non_destructive(input_list)
        assert ouput_list == expected_list, f"Failed with input {input_list}."
        assert points == expected_points, f"Failed with input {input_list}."
