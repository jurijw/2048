from collections import namedtuple

GridIndex = namedtuple("GridIndex", ["row", "col"])


class Grid:
    DEFAULT_WIDTH: int = 4
    DEFAULT_HEIGHT: int = 4

    def __init__(self, grid=None, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT) -> None:
        if grid is None:
            grid = [0 for _ in range(self.DEFAULT_WIDTH * self.DEFAULT_HEIGHT)]
        self._grid = grid
        self._width = width
        self._height = height

    def __getitem__(self, idx: GridIndex):
        return self._grid[self.linearized_index(idx)]

    def __setitem__(self, idx: GridIndex, val: int):
        self._grid[self.linearized_index(idx)] = val

    def linearized_index(self, idx: GridIndex):
        return self.width * idx.row + idx.col

    def row(self, row_index):
        return GridSlice(self, select_rows=True, axis=row_index)

    def col(self, col_index):
        return GridSlice(self, select_rows=False, axis=col_index)

    @property
    def grid(self):
        return self._grid

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def max(self):
        """Return the largest entry in the grid."""
        return max(self._grid)

    def __str__(self) -> str:
        """Return a readable string representation of the baord, in which all values are displayed in a column aligned format."""
        max_digits = len(str(self.max))
        board_str: str = ""
        for row in range(self.height):
            row_str = ""
            for col in range(self.width):
                val = self[GridIndex(row, col)]
                padding = max_digits - len(str(val))
                row_str += " " * padding + str(val) + " "
            board_str += row_str.strip() + "\n"
        return board_str.strip()


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

    def __repr__(self) -> str:
        return f"{__class__.__name__} select_rows={self._select_rows} axis={self._axis}"
