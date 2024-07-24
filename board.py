class Board:
    PROBABILITY_TWO: float = 0.9
    PROBABILITY_FOUR: float = 0.1

    def __init__(self) -> None:
        self._grid = [[0 for _ in range(4)] for _ in range(4)]

    @property
    def grid(self):
        return self._grid

    def __str__(self) -> str:
        max_digits: int = 0        
        for row in self._grid:
            for val in row:
                num_digits: int = len(str(val))
                if num_digits > max_digits:
                    max_digits = num_digits

        board_str: str = "\n".join([" ".join([" " * (len(str(val)) - max_digits) for val in row]) for row in self._grid])
        return board_str
