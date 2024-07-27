from __future__ import annotations
from collections import namedtuple
from typing import Callable

GridIndex = namedtuple("GridIndex", ["row", "col"])


class Grid:
    DEFAULT_WIDTH: int = 4
    DEFAULT_HEIGHT: int = 4

    def __init__(
        self,
        arr: list[int] | None = None,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
    ) -> None:
        if arr is None:
            arr = [0 for _ in range(self.DEFAULT_WIDTH * self.DEFAULT_HEIGHT)]
        self._arr = arr
        self._width = width
        self._height = height

    def __getitem__(self, idx: GridIndex | int) -> int:
        if isinstance(idx, GridIndex):
            return self._arr[self.linearized_index(idx)]
        return self._arr[idx]

    def __setitem__(self, idx: GridIndex | int, val: int) -> None:
        if isinstance(idx, GridIndex):
            self._arr[self.linearized_index(idx)] = val
        else:
            self._arr[idx] = val

    def linearized_index(self, idx: GridIndex) -> int:
        """Return a linearized index given a grid (row and column) index."""
        return self.width * idx.row + idx.col

    def row(self, row_index: int, reverse: bool = False) -> GridSlice:
        """Return a view of the a row of the grid."""
        return GridSlice(self, select_rows=True, axis=row_index, reverse=reverse)

    def col(self, col_index: int, reverse: bool = False) -> GridSlice:
        """Return a view of the a column of the grid."""
        return GridSlice(self, select_rows=False, axis=col_index, reverse=reverse)

    def where(self, condition: Callable[[int], bool]) -> list[int]:
        """Return a list of all (linear) indices of a grid where a condition on the
        entries of the grid holds."""
        return [index for index, val in enumerate(self._arr) if condition(val)]

    @property
    def arr(self) -> list[int]:
        return self._arr

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def max(self) -> int:
        """Return the largest entry in the grid."""
        return max(self._arr)

    def __str__(self) -> str:
        """Return a readable string representation of the baord, in which all values are displayed in a column aligned format."""
        max_digits = len(str(self.max))
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

    def __init__(
        self, grid: Grid, select_rows: bool, axis: int, reverse: bool = False
    ) -> None:
        self._grid = grid
        self._select_rows = select_rows
        self._axis = axis
        self._reverse = reverse

    def get_grid_index(self, index: int) -> GridIndex:
        """Convert an index, which is to be passed to a GridSlice view, to a GridIndex,
        which is to be passed to a Grid directly."""
        if self._reverse:
            index = len(self) - index - 1
        if self._select_rows:
            return GridIndex(self._axis, index)
        return GridIndex(index, self._axis)

    def __getitem__(self, index: int) -> int:
        return self._grid[self.get_grid_index(index)]

    def __setitem__(self, index: int, val) -> None:
        self._grid[self.get_grid_index(index)] = val

    def __len__(self) -> int:
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
