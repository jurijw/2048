from collections import namedtuple

GridIndex = namedtuple("GridIndex", ["row", "col"])


class Grid:
    DEFAULT_WIDTH: int = 4
    DEFAULT_HEIGHT: int = 4

    def __init__(self, grid=None) -> None:
        if grid is None:
            grid = [
                [0 for _ in range(self.DEFAULT_WIDTH)]
                for _ in range(self.DEFAULT_HEIGHT)
            ]
        self._grid = grid
        self._width = len(grid[0])
        self._height = len(grid)

    @property
    def grid(self):
        return self._grid

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def __getitem__(self, idx: GridIndex):
        return self._grid[idx.row][idx.col]

    def __setitem__(self, idx: GridIndex, val: int):
        self._grid[idx.row][idx.col] = val

    @property
    def max(self):
        """Return the largest entry in the grid."""
        max = 0
        for row in self.grid:
            for val in row:
                if val > max:
                    max = val
        return max

    def __str__(self) -> str:
        """Return a readable string representation of the baord, in which all values are displayed in a column aligned format."""
        max_digits = len(str(self.max))
        board_str: str = ""
        for row in self.grid:
            for val in row:
                padding = max_digits - len(str(val))
                board_str += " " * padding + str(val) + " "
            board_str += "\n"
        return board_str


class GridSlice:
    def __init__(self, grid: Grid, select_rows: bool, axis: int) -> None:
        self._grid = grid
        self._select_rows = select_rows
        self._axis = axis

    def __getitem__(self, index: int):
        if self._select_rows:
            return self._grid[GridIndex(self._axis, index)]
        return self._grid[GridIndex(index, self._axis)]

    def __setitem__(self, index: int, val):
        if self._select_rows:
            self._grid[GridIndex(self._axis, index)] = val
        else:
            self._grid[GridIndex(index, self._axis)] = val

    def __str__(self) -> str:
        return "[" + ", ".join([str(val) for val in self]) + "]"
