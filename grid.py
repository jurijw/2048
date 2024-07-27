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
        if type(other) is list:
            if len(self) != len(other):
                return False
            for i in range(len(self)):
                if self[i] != other[i]:
                    return False
            return True
        return super().__eq__(other)

    #
    # def __iter__(self):
    #     return SliceIterator(self)

    def __str__(self) -> str:
        return "[" + ", ".join([str(val) for val in self]) + "]"

    def __repr__(self) -> str:
        return f"{__class__.__name__}({self._grid.__class__.__name__} Object<{self._grid.__hash__()}>, select_rows={self._select_rows}, axis={self._axis})"


class SliceIterator:
    """Technically this class is not required since python implements #__iter__ automatically
    for any class that implements #__getitem__ and #__len__, however pyright complains when using
    the #zip method if __iter__ isn't specifically implemented."""

    def __init__(self, slice: GridSlice) -> None:
        self._slice = slice
        self._index = 0

    def __next__(self):
        if self._index < len(self._slice):
            result = self._slice[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration
