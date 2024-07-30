from copy import deepcopy

from grid import Grid
from state import State
from moves import Moves

MOVES = [move for move in Moves]
LEFT, DOWN, UP, RIGHT = MOVES

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
        points = State.collapse_destructive(input_list)
        assert input_list == expected_list, f"Failed with input {input_list}."
        assert points == expected_points, f"Failed with input {input_list}."


def test_collapse_down():
    grid = Grid([2, 0, 0, 0, 0, 8, 0, 0, 0, 0, 4, 0, 0, 0, 0, 16])
    expected = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 8, 4, 16]
    state = State(grid)
    assert state.grid == grid
    state.make_move(Moves.DOWN, add_tile=False)
    assert state.grid == expected


def test_collapse_up():
    grid = Grid([2, 0, 0, 0, 0, 8, 0, 0, 0, 0, 4, 0, 0, 0, 0, 16])
    expected = [2, 8, 4, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    state = State(grid)
    assert state.grid == grid
    state.make_move(Moves.UP, add_tile=False)
    assert state.grid == expected


def test_get_views():
    s = State(Grid([i for i in range(16)]))
    views = s.views(UP)
    assert views[3] == [3, 7, 11, 15]


def test_collapse_up_simple():
    s = State(Grid([2, 0, 0, 0], width=4, height=1))
    assert not s.collapsible_by_move(UP)

    expected = [False, False, False, True]
    for move, e in zip(MOVES, expected):
        assert s.collapsible_by_move(move) == e


def test_collapsible_by_move():
    arr = [0 for _ in range(16)]
    arr[3] = 2
    state = State(Grid(arr))
    assert state.collapsible_by_move(Moves.LEFT)
    assert state.collapsible_by_move(Moves.DOWN)
    assert not state.collapsible_by_move(Moves.UP)
    assert not state.collapsible_by_move(Moves.RIGHT)

    grid = Grid([2, 0, 0, 0, 0, 8, 0, 0, 0, 0, 4, 0, 0, 0, 0, 16])
    state = State(grid)
    collapsibility = [state.collapsible_by_move(move) for move in Moves]
    assert all(collapsibility)


def test_legal_moves():
    grid = Grid([2, 0, 0, 0, 0, 8, 0, 0, 0, 0, 4, 0, 0, 0, 0, 16])
    state = State(grid)

    assert state.legal_moves == [move for move in Moves]


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
        assert State.is_list_collapsible(input) == expected


def test_game_over():
    input_arrs = [
        [2 for _ in range(State.SIZE)],
        [2 * i for i in range(State.SIZE)],
        [2 * i if i < State.WIDTH else 0 for i in range(State.SIZE)],
        [2 * (i % 2 + 1) for i in range(State.SIZE)],
    ]
    expected = [False, False, False, False]
    for input, expected in zip(input_arrs, expected):
        state = State(Grid(input))
        assert state.game_over == expected, f"Failed on input: {input}"
