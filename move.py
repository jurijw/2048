from enum import Enum


class Move(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.name}>"
