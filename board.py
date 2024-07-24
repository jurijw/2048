class Board:
    WIDTH: int = 4
    HEIGHT: int = 4
    SIZE: int = WIDTH * HEIGHT
    PROBABILITY_TWO: float = 0.9
    PROBABILITY_FOUR: float = 0.1

    def __init__(self, grid=None) -> None:
        self._grid = grid if grid != None else self.make_grid()

    @classmethod
    def make_grid(cls):
        grid = [0 for _ in range(cls.SIZE)]
        return grid

    def add_random_tile(self):
        free_indices = [index for index in range(self.SIZE) if self._grid[index] == 0]
        # Choose a random index
        return

    @property
    def points(self):
        return sum(self._grid)

    @classmethod
    def linear_index(cls, row, col):
        return row * cls.WIDTH + col

    def get_at(self, row, col):
        return self._grid[self.linear_index(row, col)]

    def set_at(self, row, col, val):
        self._grid[self.linear_index(row, col)] = val


    @property
    def grid(self):
        return self._grid

    def __str__(self) -> str:
        max_digits: int = max(map(lambda x: len(str(x)), self._grid))
        board_str: str = ""
        for row in range(self.HEIGHT):
            for col in range(self.WIDTH):
                val = self.get_at(row, col)
                padding = max_digits - len(str(val))
                board_str += " " * padding + str(val) + " "
            board_str += "\n"
        return board_str
