from moves import Moves
from random import choice, choices
from model.grid import Grid, GridView
from model.grid_index import GridIndex


class State:
    """
    A class describing the entire state of a game of 2048 at any instance.

    Stores the grid as a regular 1D list under the hood and uses views to
    operate on different rows and columns of the grid as though they were
    regular lists. Implements the collapse algorithm to merge elements of
    the grid according to the rules of 2048.
    """

    WIDTH = 4
    HEIGHT = 4
    SIZE = WIDTH * HEIGHT
    PROBABILITY_TWO: float = 0.9
    PROBABILITY_FOUR: float = 0.1
    WIN_THRESHOLD: int = 2048

    def __init__(self, grid: Grid | None = None, points: int = 0) -> None:
        """
        Initialize a Board instance, which stores the value of all tiles in a linearized grid.
        By default creates a grid of zeros of dimensions specified in the grid class.

        Args:
            grid: An optional Grid instance which stores the configuration of tiles. By default,
            a grid with only two tiles is created.
            points: The number of accrued points. Defaults to zero.
        """
        if grid is None:
            self._grid: Grid = Grid()
            self.add_tile(num_tiles=2)
        else:
            self._grid: Grid = grid
        self._points = points
        self._won = self._grid.max > self.WIN_THRESHOLD
        self._views: dict[Moves, list[GridView]] = self.generate_views(self._grid)

    @staticmethod
    def generate_views(grid: Grid) -> dict[Moves, list[GridView]]:
        """Returns a dictionary of all possible views for the given grid, where the keys of the
        keys of the dictionary are the moves corresponding to those views. Note that this should
        probably not be used for larger grid sizes, since the returned views are all stored in
        memory. This has the advantage that with smaller grid sizes we don't have to create view
        instances after instantiating a state. For larger grid sizes, consider a lazy loading
        approach. (Or just, you know, use numpy...)"""
        kwargs_dict = {
            Moves.LEFT: {"select_rows": True, "reverse": False},
            Moves.DOWN: {"select_rows": False, "reverse": True},
            Moves.UP: {"select_rows": False, "reverse": False},
            Moves.RIGHT: {"select_rows": True, "reverse": True},
        }
        num_axes_dict = {
            Moves.LEFT: grid.height,
            Moves.DOWN: grid.width,
            Moves.UP: grid.width,
            Moves.RIGHT: grid.height,
        }
        view_dict = {
            move: [
                grid.view(axis=axis, **kwargs_dict[move])
                for axis in range(num_axes_dict[move])
            ]
            for move in Moves
        }
        return view_dict

    def views(self, move: Moves) -> list[GridView]:
        """Return a list of views corresponding to a move. For example, if call #views(Moves.DOWN)
        we will get a list of views of all columns, where indexing reverse order."""
        return self._views[move]

    def add_tile(self, num_tiles=1):
        """Add random tile(s) (either a 2 or a 4), weighted accordingly, to an empty position of the board."""
        for _ in range(num_tiles):
            # Choose a random empty index
            index = choice(self.grid.where(lambda x: x == 0))
            # Choose whether to place a two or a four
            val = choices(
                [2, 4], weights=[self.PROBABILITY_TWO, self.PROBABILITY_FOUR], k=1
            )[0]
            self[index] = val

    def __getitem__(self, idx: GridIndex | int):
        """Get an element of my grid, either by a grid index (row and column)
        or by a linear index that directly accesses the underlying array."""
        return self.grid[idx]

    def __setitem__(self, idx: GridIndex | int, val: int):
        """Set an element of my grid, either by a grid index (row and column)
        or by a linear index that directly accesses the underlying array."""
        self.grid[idx] = val

    def make_move(self, move: Moves, add_tile: bool = True):
        """Apply a move to the state, collapsing the grid in the appropriate direction
        and then adding a tile randomly to an empty position if ADD_TILE is true."""
        if move not in self.legal_moves:
            raise Exception("Attempting to make an illegal move.")
        self.collapse(move)
        if add_tile:
            self.add_tile()

    def collapse(self, move: Moves):
        """Collapse the grid in a given direction by applying the collapse algorithm to
        all rows or columns of the grid in the correct direction."""
        for view in self.views(move):
            self._points += self.collapse_destructive(view)

    @staticmethod
    def is_list_collapsible(lst: list[int] | GridView) -> bool:
        """Returns True iff a list of integers (or a GridView) is collapsible to the left.
        That is, performing the collapse algorithm on it would result in a change.
        We check for collapsibility by traversing the list, checking if
        any subsequent non-zero entries are equal or if any entry is preceeded by a
        zero. This algorithm runs in O(n) time complexity as it performs a single pass.
        """
        if len(lst) < 2:
            return False
        for i in range(len(lst) - 1):
            v1, v2 = lst[i], lst[i + 1]
            if v1 == 0 and v2 != 0:
                return True
            if v1 != 0 and v1 == v2:
                return True
        return False

    def collapsible_by_move(self, move: Moves):
        """Returns true iff the grid is collapsible in a given move direction."""
        for view in self.views(move):
            if self.is_list_collapsible(view):
                return True
        return False

    def collapsible(self):
        """Returns true iff the grid is collapsible in any move direction."""
        for move in Moves:
            if self.collapsible_by_move(move):
                return True
        return False

    @property
    def legal_moves(self):
        """Return a list of all legal moves given the current game state."""
        return [move for move in Moves if self.collapsible_by_move(move)]

    @property
    def width(self):
        """The width of my grid."""
        return self.grid.width

    @property
    def height(self):
        """The height of my grid."""
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
    def won(self):
        return self._won

    @property
    def game_over(self):
        """Returns true iff the game is over, which is the case when no
        more legal moves are available."""
        return len(self.legal_moves) == 0

    @property
    def points(self):
        """Returns the current number of points accrued."""
        return self._points

    @property
    def grid(self):
        """The grid associated with my state."""
        return self._grid

    def __str__(self) -> str:
        """Return a readable representation of the state."""
        return f"Points: {self.points}\n{self.grid}"

    def __repr__(self) -> str:
        return f"<{__class__.__name__}(grid=<{self.grid.__class__.__name__} Object>, points={self.points})"
