from typing import NamedTuple
from move import Move
from random import choice, choices


class Board:
    WIDTH: int = 4
    HEIGHT: int = 4
    SIZE: int = WIDTH * HEIGHT
    PROBABILITY_TWO: float = 0.9
    PROBABILITY_FOUR: float = 0.1
    # TODO: Figure out why I can't use WIDTH and HEIGHT in the list comprehension.
    INDICES: list[list[int]] = [[row * 4 + col for col in range(4)] for row in range(4)]

    def __init__(self, grid=None, points=0) -> None:
        """Initialize a Board instance, which stores the value of all tiles in a linearized grid."""
        self._grid = grid if grid is not None else self.make_grid()
        if grid is None:
            for _ in range(2):
                self.add_random_tile()
        self._points = points

    @classmethod
    def make_grid(cls):
        """Create and return an empty grid."""
        return [0 for _ in range(cls.SIZE)]

    @staticmethod
    def filter_indices(arr, target=0):
        """Returns a list of all indices where the list ARR equals TARGET, which defaults to 0."""
        return [index for index, val in enumerate(arr) if val == target]

    def add_random_tile(self):
        """Add a random tile (weighted accordingly) to an empty position of the board."""
        empty_indices = self.filter_indices(self._grid)
        # Choose a random empty index
        index = choice(empty_indices)
        # Choose whether to place a two or a four
        val = choices(
            [2, 4], weights=[self.PROBABILITY_TWO, self.PROBABILITY_FOUR], k=1
        )[0]
        # Add the tile
        self.set_index(index, val)

    def get_index_lists_by_move(self, move: Move):
        if move is Move.LEFT:
            return self.left_indices()
        if move is Move.UP:
            return self.up_indices()
        if move is Move.RIGHT:
            return self.right_indices()
        return self.down_indices()

    def make_move(self, move: Move):
        # FIXME: only allow the move to be made if it changes the board
        for index_lst in self.get_index_lists_by_move(move):
            self._points += self.collapse_by_index_list(index_lst)
        self.add_random_tile()

    @staticmethod
    def collapsible(lst: list[int]) -> bool:
        """Returns True iff a list of integers is collapsible. That is,
        performing the collapse algorithm on it would result in a change.
        We check for collapsibility by traversing the list, checking if
        any subsequent entries are equal, and tracking if zero and non-zero
        entries have been observed. This algorithm runs in O(n) time complexity.
        """
        found_zero = False
        found_non_zero = False
        for i in range(len(lst) - 1):
            v1, v2 = lst[i], lst[i + 1]
            if v1 != 0 and v1 == v2:
                return True
            if v1 == 0 or v2 == 0:
                found_zero = True
            if v1 != 0 or v2 != 0:
                found_non_zero = True
        return found_zero and found_non_zero

    def extract(self, axis: int, move: Move) -> list[int]:
        """Extract a list from my grid corresponding to a move direction. The axis specifies
        which row / column is extracted."""
        output = []
        match move:
            case Move.LEFT:
                for col in range(self.WIDTH):
                    output.append(self.get_at(axis, col))
            case Move.DOWN:
                for row in range(self.HEIGHT):
                    output.append(self.get_at(row, axis))
            case Move.UP:
                for row in reversed(range(self.HEIGHT)):
                    output.append(self.get_at(row, axis))
            case Move.RIGHT:
                for col in reversed(range(self.WIDTH)):
                    output.append(self.get_at(axis, col))
        return output

    def get_by_index_seq(self, ptr, index_seq):
        return self.get_index(index_seq[ptr])

    def set_by_index_seq(self, ptr, val, index_seq):
        self.set_index(index_seq[ptr], val)

    def collapse_by_index_list(self, index_seq):
        def get(ptr):
            return self.get_by_index_seq(ptr, index_seq)

        def set_(ptr, val):
            return self.set_by_index_seq(ptr, val, index_seq)

        points = 0
        p1, p2 = 0, 1
        write = 0
        while p2 <= len(index_seq):
            if get(p1) == 0:
                p1 += 1
                p2 += 1
            elif p2 == len(index_seq):
                set_(write, get(p1))
                # p1 += 1
                p2 += 1
                write += 1
            elif get(p2) == 0:
                p2 += 1
            elif get(p1) == get(p2):
                points += get(p1) + get(p2)
                set_(write, get(p1) + get(p2))
                write += 1
                p1 = p2 + 1
                p2 = p1 + 1
            else:
                set_(write, get(p1))
                write += 1
                p1 = p2
                p2 = p1 + 1
        for i in range(write, len(index_seq)):
            set_(i, 0)
        return points

    @staticmethod
    def collapse_destructive(lst):
        """Take an input list LST and 'collapse' it to the left in place,
        mutating the original list. This merges consecutive non-overlapping
        pairs (grouped to the left) of non-zero integers. The sum of the pairs
        is written to the input list such that it overwrites the first value
        of the pair. Non-paired, non-zero integers are shifted left to the
        first index where no overwrite has occured. After mutating the input
        list, the number of points gained by the collapse are returned, which
        equal the sum of all merged list entries (tiles in 2048).
        This algorithm has O(n) time & space complexity, requiring only one
        pass through the list."""
        points = 0
        p1, p2 = 0, 1
        write = 0
        while p2 <= len(lst):
            if lst[p1] == 0:
                p1 += 1
                p2 += 1
            elif p2 == len(lst):
                lst[write] = lst[p1]
                # p1 += 1
                p2 += 1
                write += 1
            elif lst[p2] == 0:
                p2 += 1
            elif lst[p1] == lst[p2]:
                points += lst[p1] + lst[p2]
                lst[write] = lst[p1] + lst[p2]
                write += 1
                p1 = p2 + 1
                p2 = p1 + 1
            else:
                lst[write] = lst[p1]
                write += 1
                p1 = p2
                p2 = p1 + 1
        for i in range(write, len(lst)):
            lst[i] = 0
        return points

    @staticmethod
    def collapse_non_destructive(lst: list[int]) -> tuple[int, list[int]]:
        """Non-destructive version of #collapse_destructive."""
        output = [0 for _ in range(len(lst))]
        points = 0
        p1, p2 = 0, 1
        write = 0
        while p2 <= len(lst):
            if lst[p1] == 0:
                p1 += 1
                p2 += 1
            elif p2 == len(lst):
                output[write] = lst[p1]
                # p1 += 1
                p2 += 1
                # write += 1 -> may need in non-destructive method
            elif lst[p2] == 0:
                p2 += 1
            elif lst[p1] == lst[p2]:
                points += lst[p1] + lst[p2]
                output[write] = lst[p1] + lst[p2]
                write += 1
                p1 = p2 + 1
                p2 = p1 + 1
            else:
                output[write] = lst[p1]
                write += 1
                p1 = p2
                p2 = p1 + 1
        return points, output

    @classmethod
    def left_indices(cls):
        indices = []
        for row in range(cls.HEIGHT):
            row_indices = []
            for col in range(cls.WIDTH):
                row_indices.append(cls.linear_index(row, col))
            indices.append(row_indices)
        return indices

    @classmethod
    def right_indices(cls):
        # TODO: This is slow (copies list every time)
        return [row[::-1] for row in cls.left_indices()]

    @classmethod
    def down_indices(cls):
        indices = []
        for col in range(cls.WIDTH):
            col_indices = []
            for row in range(cls.HEIGHT):
                col_indices.append(cls.linear_index(row, col))
            indices.append(col_indices)
        return indices

    @classmethod
    def up_indices(cls):
        return [col[::-1] for col in cls.down_indices()]

    @property
    def game_over(self):
        # TODO:
        return False

    @property
    def points(self):
        """Returns the current number of points accrued."""
        return self._points

    @classmethod
    def linear_index(cls, row, col):
        """Return a linearized index given a row and column index."""
        return cls.INDICES[row][col]

    @classmethod
    def grid_index(cls, index):
        """Return a grid index (row and col) from a linearized index."""
        row = index % cls.WIDTH
        col = index - (row * cls.WIDTH)
        return GridIndex(row, col)

    def get_at(self, row, col):
        return self._grid[self.linear_index(row, col)]

    def set_at(self, row, col, val):
        self._grid[self.linear_index(row, col)] = val

    def get_index(self, index):
        return self._grid[index]

    def set_index(self, index, val):
        self._grid[index] = val

    @property
    def grid(self):
        return self._grid

    def __str__(self) -> str:
        """Return a readable string representation of the baord, in which all values are displayed in a column aligned format."""
        max_digits: int = max(map(lambda x: len(str(x)), self._grid))
        board_str: str = ""
        for row in range(self.HEIGHT):
            for col in range(self.WIDTH):
                val = self.get_at(row, col)
                padding = max_digits - len(str(val))
                board_str += " " * padding + str(val) + " "
            board_str += "\n"
        return board_str


class GridIndex(NamedTuple):
    row: int
    col: int
