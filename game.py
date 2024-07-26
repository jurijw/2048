from board import Board
from move import Move


class Game:
    def __init__(self, board=None) -> None:
        self._board = board if board is not None else Board()

    def play(self):
        while not self._board.game_over:
            print(self._board)
            user_input = input("Enter a move (hjkl) ").strip().lower()
            self.make_move(self.parse_move(user_input))

    @staticmethod
    def parse_move(user_input):
        match user_input:
            case "h":
                return Move.LEFT
            # FIXME: Swapped these two.
            case "j":
                return Move.UP
            case "k":
                return Move.DOWN
            case "l":
                return Move.RIGHT
        return Move.RIGHT

    def make_move(self, move: Move):
        self._board.make_move(move)

    def __str__(self) -> str:
        return str(self._board)
