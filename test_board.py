from copy import deepcopy

from board import Board
from move import Move

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
    [2, 2, 0, 4],
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
    # TODO: Double-check that this is correct.
    [0, 0, 4, 4],
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
    for input_list, expected_list, expected_points in zip(
        deepcopy(collapsable_lists), collapsable_lists_expected, points_expected
    ):
        points = Board.collapse_destructive(input_list)
        assert input_list == expected_list, f"Failed with input {input_list}."
        assert points == expected_points, f"Failed with input {input_list}."


def test_collapse_non_destructive():
    for input_list, expected_list, expected_points in zip(
        collapsable_lists, collapsable_lists_expected, points_expected
    ):
        points, ouput_list = Board.collapse_non_destructive(input_list)
        assert ouput_list == expected_list, f"Failed with input {input_list}."
        assert points == expected_points, f"Failed with input {input_list}."


def test_collapse_down():
    grid = [2, 0, 0, 0, 0, 8, 0, 0, 0, 0, 4, 0, 0, 0, 0, 16]
    expected = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 8, 4, 16]
    board = Board(grid)
    assert board.grid == grid
    board.make_move(Move.DOWN)
    assert board.grid == expected


def test_collapse_up():
    grid = [2, 0, 0, 0, 0, 8, 0, 0, 0, 0, 4, 0, 0, 0, 0, 16]
    expected = [2, 8, 4, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    board = Board(grid)
    assert board._grid == grid
    board.make_move(Move.UP)
    assert board.grid == expected


def test_collabsible():
    inputs = [
        [0, 0, 0, 0],
        [2, 0, 0, 0],
        [0, 0, 0, 2],
        [2, 0, 0, 2],
        [2, 0, 0, 4],
        [2, 2, 2, 2],
        [4, 2, 4, 2],
        [2, 4, 8, 16],
        [16, 8, 4, 0],
    ]
    expected = [
        False,
        False,
        True,
        True,
        True,
        True,
        False,
        False,
        False,
    ]

    for input, expected in zip(inputs, expected):
        print(input)
        assert Board.collapsible(input) == expected


def test_iscollapsible():
    grid = [0 for _ in range(Board.SIZE)]
    grid[3] = 2
    board = Board(grid)
    assert board.iscollapsible(Move.LEFT)
    assert board.iscollapsible(Move.DOWN)
    assert not board.iscollapsible(Move.UP)
    assert not board.iscollapsible(Move.RIGHT)


def test_game_over():
    inputs = [
        [2 for _ in range(Board.SIZE)],
        [2 * i for i in range(Board.SIZE)],
        [2 * i if i < Board.WIDTH else 0 for i in range(Board.SIZE)],
        [2 * (i % 2 + 1) for i in range(Board.SIZE)],
    ]
    expected = [False, True, False, False]
    for input, expected in zip(inputs, expected):
        board = Board(input)
    assert board.game_over == expected, f"Failed on input: {input}"
