from move import Move
from random import choice, choices


class Board:
    WIDTH: int = 4
    HEIGHT: int = 4
    SIZE: int = WIDTH * HEIGHT
    PROBABILITY_TWO: float = 0.9
    PROBABILITY_FOUR: float = 0.1

    def __init__(self, grid=None) -> None:
        """Initialize a Board instance, which stores the value of all tiles in a linearized grid."""
        self._grid = grid if grid != None else self.make_grid()
        if grid == None:
            for _ in range(2):
                self.add_random_tile()

    @classmethod
    def make_grid(cls):
        """Create an empty grid."""
        grid = [0 for _ in range(cls.SIZE)]
        return grid

    @staticmethod
    def filter_indices(arr, target=0):
        """Returns a list of all indices where the list ARR equals TARGET, which defaults to 0."""
        return [index for index, val in enumerate(arr) if val == target]

    def add_random_tile(self):
        """Add a random tile (weighted accordingly) to an empty position of the board."""
        empty_indices = self.filter_indices(self._grid) 
        # Choose a random empty index
        index = choice(empty_indices)
        # Choose whether to place a two or a four 
        val = choices([2, 4], weights=[self.PROBABILITY_TWO, self.PROBABILITY_FOUR], k=1)[0]
        # Add the tile
        self.set_index(index, val)

    def make_move(self, move: Move):
        pass

    def collapse(self, move: Move):
        pass

    @staticmethod
    def collapse_non_destructive(lst):
        start = 0
        write = 0
        output = [0 for _ in range(len(lst))]
        while start < len(lst):
            if start == len(lst) - 1:
                output[write] = lst[start]
                start += 1
            elif lst[start] == 0:
                start += 1
            elif lst[start] == lst[start + 1]:
                output[write] = lst[start] + lst[start + 1]
                start += 2
                write += 1
            else:
                output[write] = lst[start]
                start += 1
                write += 1
        return output

    @staticmethod
    def collapse_destructive(lst):
        start = 0
        write = 0
        while start < len(lst):
            if start == len(lst) - 1:
                lst[write] = lst[start]
                start += 1
                write += 1 # check
            elif lst[start] == 0:
                start += 1
            elif lst[start] == lst[start + 1]:
                lst[write] = lst[start] + lst[start + 1]
                start += 2
                write += 1
            else:
                lst[write] = lst[start]
                start += 1
                write += 1

        # Overwrite remaining 
        for i in range(write, len(lst)): # len(lst) should be start at this point
            lst[i] = 0
    

    @property
    def points(self):
        """Calculates the current points by summing the total value of all tiles."""
        return sum(self._grid)

    @classmethod
    def linear_index(cls, row, col):
        """Return a linearized index given a row and column index."""
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
        """Return a readable string representation of the baord, in which all values are displayed in a column aligned format."""
        max_digits: int = max(map(lambda x: len(str(x)), self._grid))
        board_str: str = ""
        for row in range(self.HEIGHT):
            for col in range(self.WIDTH):
                val = self.get_at(row, col)
                padding = max_digits - len(str(val))
                board_str += " " * padding + str(val) + " "
            board_str += "\n"
        return board_str
