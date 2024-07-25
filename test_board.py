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

def test_collapse_destructive():
    for input, expected in zip(deepcopy(collapsable_lists), collapsable_lists_expected):
        Board.collapse_destructive(input)
        assert input == expected

def test_collapse_non_destructive():
    for input, expected in zip(collapsable_lists, collapsable_lists_expected):
        assert Board.collapse_non_destructive(input) == expected
