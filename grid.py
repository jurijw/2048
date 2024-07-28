from __future__ import annotations
from collections import namedtuple
from typing import Callable, overload

GridIndex = namedtuple("GridIndex", ["row", "col"])


class Grid:
    """
    A 2d integer grid, backed by a single list, with support for row and column views.
    The grid can be accessed either by a linearized index or via a GridIndex (row and
    column tuple). The views allow operating on aribitrary rows or columns as though
    they were a single list.
    """

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

    @overload
    def __getitem__(self, idx: int) -> int:
        """Get an element of the grid by a linear index that directly accesses
        the underlying array."""
        self.__getitem__(idx)

    @overload
    def __getitem__(self, idx: GridIndex) -> int:
        """Get an element of the grid by a grid index (row and column)"""
        self.__getitem__(self.linearized_index(idx))

    def __getitem__(self, idx: GridIndex | int) -> int:
        """Get an element of the grid, either by a grid index (row and column)
        or by a linear index that directly accesses the underlying array."""
        if isinstance(idx, GridIndex):
            return self._arr[self.linearized_index(idx)]
        return self._arr[idx]

    @overload
    def __setitem__(self, idx: int, val: int):
        """Set an element of the grid by a linear index that directly
        accesses the underlying array."""
        self.__setitem__(idx, val)

    @overload
    def __setitem__(self, idx: GridIndex, val: int):
        """Set an element of the grid by a grid index (row and column)."""
        self.__setitem__(idx, val)

    def __setitem__(self, idx: GridIndex | int, val: int) -> None:
        """Set an element of the grid, either by a grid index (row and column)
        or by a linear index that directly accesses the underlying array."""
        if isinstance(idx, GridIndex):
            self._arr[self.linearized_index(idx)] = val
        else:
            self._arr[idx] = val

    def linearized_index(self, idx: GridIndex) -> int:
        """Return a linearized index given a grid index (row and column)."""
        return self.width * idx.row + idx.col

    def view(self, select_rows: bool, axis: int, reverse: bool) -> GridView:
        """Return a view of row or column of the grid."""
        return GridView(self, select_rows=select_rows, axis=axis, reverse=reverse)

    def where(self, condition: Callable[[int], bool]) -> list[int]:
        """Return a list of all (linear) indices of a grid where a condition on the
        entries of the grid holds."""
        return [index for index, val in enumerate(self._arr) if condition(val)]

    @property
    def width(self) -> int:
        """The width of the grid."""
        return self._width

    @property
    def height(self) -> int:
        """The height of the grid."""
        return self._height

    @property
    def size(self) -> int:
        """Return the number of entries in my grid."""
        return len(self._arr)

    @property
    def max(self) -> int:
        """Return the largest entry in the grid."""
        return max(self._arr)

    def __eq__(self, other: object) -> bool:
        """Returns true if this grid's underlying list equals that of
        OTHER, element-wise."""
        if isinstance(other, Grid):
            return self._arr == other._arr
        elif isinstance(other, list):
            return self._arr == other
        else:
            return super().__eq__(other)

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
                if col != self.width - 1:
                    board_str += " "
            if row != self.height - 1:
                board_str += "\n"
        return board_str

    def __repr__(self) -> str:
        return f"{__class__.__name__}(arr={self._arr}, width={self.width}, height={self.height})"


class GridView:
    """
    A view of a Grid instance that allows accessing and working with rows or columns
    of the grid similarly to a regular list. Any method that operates on the view will
    mutate the corrsponding entries of the grid instance assosciated with the view.
    """

    def __init__(
        self, grid: Grid, select_rows: bool, axis: int, reverse: bool = False
    ) -> None:
        """
        Initialize a grid view of any row or column of a grid.

        Args:
            select_rows: Specifies whether to choose rows or columns.
            axis: The row index from top to bottom in the case of rows
            or the column index from left to right in the case of columns.
            reverse: Reverses the order of the view iff true.
        """
        self._grid = grid
        self._select_rows = select_rows
        self._axis = axis
        self._reverse = reverse

    def get_grid_index(self, index: int) -> GridIndex:
        """Convert an index, which is to be passed to a GridView view, to a GridIndex,
        which is to be passed to a Grid directly."""
        if self._reverse:
            index = len(self) - index - 1
        if self._select_rows:
            return GridIndex(self._axis, index)
        return GridIndex(index, self._axis)

    def __getitem__(self, index: int) -> int:
        """Get an element of the view, which refers to an element of a grid."""
        return self._grid[self.get_grid_index(index)]

    def __setitem__(self, index: int, val) -> None:
        """Set an element of the view, which refers to an element of a grid."""
        self._grid[self.get_grid_index(index)] = val

    def __len__(self) -> int:
        """The length of my view, equivalent to the length of the row or column I represent."""
        return self._grid.width if self._select_rows else self._grid.height

    def __eq__(self, other: object, /) -> bool:
        """Add equality support for comparing a view to regular lists."""
        if isinstance(other, list):
            if len(self) != len(other):
                return False
            for i in range(len(self)):
                if self[i] != other[i]:
                    return False
            return True
        return super().__eq__(other)

    def __str__(self) -> str:
        """Return a readable representation of the contents of my view."""
        return "[" + ", ".join([str(val) for val in self]) + "]"

    def __repr__(self) -> str:
        return f"{__class__.__name__}(grid=<{self._grid.__class__.__name__} Object>, select_rows={self._select_rows}, axis={self._axis}, reverse={self._reverse})"
