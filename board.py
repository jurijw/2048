from random import choice, choices


class Board:
    WIDTH: int = 4
    HEIGHT: int = 4
    SIZE: int = WIDTH * HEIGHT
    PROBABILITY_TWO: float = 0.9
    PROBABILITY_FOUR: float = 0.1

    def __init__(self, grid=None) -> None:
        self._grid = grid if grid != None else self.make_grid()
        if grid == None:
            for _ in range(2):
                self.add_random_tile()

    @classmethod
    def make_grid(cls):
        grid = [0 for _ in range(cls.SIZE)]
        return grid

    def add_random_tile(self):
        empty_indices = self.filter_indices(self._grid) 
        # Choose a random empty index
        index = choice(empty_indices)
        # Choose whether to place a two or a four 
        val = choices([2, 4], weights=[self.PROBABILITY_TWO, self.PROBABILITY_FOUR], k=1)[0]
        # Add the tile
        self.set_index(index, val)

    @staticmethod
    def filter_indices(arr, target=0):
        """Returns a list of all indices where the list ARR equals TARGET, which defaults to 0."""
        return [index for index, val in enumerate(arr) if val == target]

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

    def get_index(self, index):
        return self._grid[index]

    def set_index(self, index, val):
        self._grid[index] = val 


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
