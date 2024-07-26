from os import wait3


class Grid:
    WIDTH: int = 4
    HEIGHT: int = 4
    SIZE: int = WIDTH * HEIGHT

    def __init__(self, width, height) -> None:
        self._width = width
        self._height = height
        self._grid = [[0 for _ in range(width)] for _ in range(height)]

    def apply_to_row(f, reverse=False):
        pass

    @property
    def grid(self):
        return self._grid

    def get(self, row, col):
        return self._grid[row][col]

    def set_(self, row, col, val):
        self._grid[row][col] = val

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
