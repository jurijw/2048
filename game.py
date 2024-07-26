from board import Board
from move import Move


class Game:
    def __init__(self, board=None) -> None:
        self._board = board if board is not None else Board()

    def play(self):
        while not self._board.game_over:
            print(f"Points: {self._board.points}")
            print(self._board)
            user_input = input("Enter a move (hjkl) ").strip().lower()
            parsed_move = self.parse_move(user_input)
            if parsed_move is not None:
                self.make_move(parsed_move)

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
        return None

    def make_move(self, move: Move):
        self._board.make_move(move)

    def __str__(self) -> str:
        return str(self._board)
