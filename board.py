from moves import Moves
from random import choice, choices
from grid import Grid, GridSlice, GridIndex


class Board:
    PROBABILITY_TWO: float = 0.9
    PROBABILITY_FOUR: float = 0.1
    WIN_THRESHOLD: int = 2048

    def __init__(self, grid: Grid | None = None, points: int = 0) -> None:
        """Initialize a Board instance, which stores the value of all tiles in a linearized grid."""
        if grid is None:
            self._grid: Grid = Grid()
            self.add_tile(num_tiles=2)
        else:
            self._grid: Grid = grid
        self._points = points
        self._has_won = self._grid.max > self.WIN_THRESHOLD
        self._views: dict[Moves, list[GridSlice]] = self.generate_views(self._grid)

    @staticmethod
    def generate_views(grid: Grid) -> dict[Moves, list[GridSlice]]:
        view_dict = {
            Moves.LEFT: [grid.row(row, reverse=False) for row in range(grid.height)],
            Moves.DOWN: [grid.col(col, reverse=True) for col in range(grid.width)],
            Moves.UP: [grid.row(col, reverse=False) for col in range(grid.width)],
            Moves.RIGHT: [grid.row(row, reverse=True) for row in range(grid.height)],
        }
        return view_dict

    def views(self, move: Moves) -> list[GridSlice]:
        return self._views[move]

    def add_tile(self, num_tiles=1):
        """Add a random tile (either a 2 or a 4), weighted accordingly, to an empty position of the board."""
        for _ in range(num_tiles):
            # Choose a random empty index
            index = choice(self.grid.where(lambda x: x == 0))
            # Choose whether to place a two or a four
            val = choices(
                [2, 4], weights=[self.PROBABILITY_TWO, self.PROBABILITY_FOUR], k=1
            )[0]
            self[index] = val

    def __getitem__(self, idx: GridIndex | int):
        return self.grid[idx]

    def __setitem__(self, idx: GridIndex | int, val: int):
        self.grid[idx] = val

    def make_move(self, move: Moves):
        if move not in self.legal_moves:
            raise Exception("Attempting to make an illegal move.")
        self.collapse(move)

    def collapse(self, move: Moves):
        for view in self.views(move):
            self._points += self.collapse_destructive(view)

    @staticmethod
    def is_list_collapsible(lst: list[int] | GridSlice) -> bool:
        """Returns True iff a list of integers is collapsible to the left. That is,
        performing the collapse algorithm on it would result in a change.
        We check for collapsibility by traversing the list, checking if
        any subsequent non-zero entries are equal or if any entry is preceeded by a
        zero. This algorithm runs in O(n) time complexity.
        """
        for i in range(len(lst) - 1):
            v1, v2 = lst[i], lst[i + 1]
            if v1 == 0 and v2 != 0:
                return True
            if v1 != 0 and v1 == v2:
                return True
        return False

    def collapsible_by_move(self, move: Moves):
        for view in self.views(move):
            if self.is_list_collapsible(view):
                return True
        return False

    def collapsible(self):
        for move in Moves:
            if self.collapsible_by_move(move):
                return True
        return False

    @property
    def legal_moves(self):
        return [move for move in Moves if self.collapsible_by_move(move)]

    @property
    def width(self):
        return self.grid.width

    @property
    def height(self):
        return self.grid.height

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

    @property
    def game_over(self):
        return len(self.legal_moves) == 0

    @property
    def points(self):
        """Returns the current number of points accrued."""
        return self._points

    @property
    def has_won(self):
        return self._has_won

    @property
    def grid(self):
        return self._grid

    def __str__(self) -> str:
        return str(self.grid)

    def __repr__(self) -> str:
        return f"<{__class__.__name__}()>"
