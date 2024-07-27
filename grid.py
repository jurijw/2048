from collections import namedtuple
from typing import Callable

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

    def __getitem__(self, idx: GridIndex | int):
        if isinstance(idx, GridIndex):
            return self._grid[self.linearized_index(idx)]
        return self._grid[idx]

    def __setitem__(self, idx: GridIndex | int, val: int):
        if isinstance(idx, GridIndex):
            self._grid[self.linearized_index(idx)] = val
        else:
            self._grid[idx] = val

    def linearized_index(self, idx: GridIndex):
        """Return a linearized index given a grid (row and column) index."""
        return self.width * idx.row + idx.col

    def row(self, row_index, reverse=False):
        """Return a view of the a row of the grid."""
        return GridSlice(self, select_rows=True, axis=row_index, reverse=reverse)

    def col(self, col_index, reverse=False):
        """Return a view of the a column of the grid."""
        return GridSlice(self, select_rows=False, axis=col_index, reverse=reverse)

    def where(self, condition: Callable[[object], bool]):
        """Return a list of all (linear) indices of a grid where a condition on the
        entries of the grid holds."""
        return [index for index, val in enumerate(self._grid) if condition(val)]

    @property
    def grid(self):
        return self._grid

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def __max__(self) -> int:
        """Return the largest entry in the grid."""
        return max(self._grid)

    def __str__(self) -> str:
        """Return a readable string representation of the baord, in which all values are displayed in a column aligned format."""
        max_digits = len(str(max(self)))
        board_str: str = ""
        for row in range(self.height):
            for col in range(self.width):
                val = (
                    self[GridIndex(row, col)] if self[GridIndex(row, col)] != 0 else "*"
                )
                padding = max_digits - len(str(val))
                board_str += " " * padding + str(val)
                if col != self.width:
                    board_str += " "
            if row != self.height - 1:
                board_str += "\n"
        return board_str


class GridSlice:
    """A view of a Grid instance that allows accessing and working with rows or columns
    of the grid similarly to a regular list. Any method that operates on the view will
    mutate the corrsponding entries of the grid instance assosciated with the view."""

    def __init__(self, grid: Grid, select_rows: bool, axis: int, reverse=False) -> None:
        self._grid = grid
        self._select_rows = select_rows
        self._axis = axis
        self._reverse = reverse

    def get_grid_index(self, index: int):
        """Convert an index, which is to be passed to a GridSlice view, to a GridIndex,
        which is to be passed to a Grid directly."""
        if self._reverse:
            index = len(self) - index - 1
        if self._select_rows:
            return GridIndex(self._axis, index)
        return GridIndex(index, self._axis)

    def __getitem__(self, index: int):
        return self._grid[self.get_grid_index(index)]

    def __setitem__(self, index: int, val):
        self._grid[self.get_grid_index(index)] = val

    def __len__(self):
        return self._grid.width if self._select_rows else self._grid.height

    def __eq__(self, other: object, /) -> bool:
        if isinstance(other, list):
            if len(self) != len(other):
                return False
            for i in range(len(self)):
                if self[i] != other[i]:
                    return False
            return True
        return super().__eq__(other)

    def __str__(self) -> str:
        return "[" + ", ".join([str(val) for val in self]) + "]"

    def __repr__(self) -> str:
        return f"{__class__.__name__}({self._grid.__class__.__name__} Object<{self._grid.__hash__()}>, select_rows={self._select_rows}, axis={self._axis})"
