from enum import Enum, auto


class Moves(Enum):
    LEFT = auto()
    DOWN = auto()
    UP = auto()
    RIGHT = auto()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.name}>"
