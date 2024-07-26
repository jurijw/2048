from board import Board
from move import Move
import os


class Game:
    def __init__(self, board=None) -> None:
        self._board = board if board is not None else Board()

    def play(self):
        # Clear the screen
        def cls():
            os.system("clear" if os.name == "posix" else "cls")

        while not self._board.game_over:
            print(f"Points: {self._board.points}")
            print(self._board)
            user_input = input("Enter a move (hjkl) ")
            if self._board._has_won:
                print("Winner winner!")
            parsed_move = self.parse_move(user_input)
            if parsed_move is not None and parsed_move in self.legal_moves:
                self.make_move(parsed_move)
                self._board.add_random_tile()
                cls()
            else:
                print("Incorrect entry.")

    @staticmethod
    def parse_move(user_input):
        match user_input.strip().lower():
            case "h":
                return Move.LEFT
            case "j":
                return Move.DOWN
            case "k":
                return Move.UP
            case "l":
                return Move.RIGHT
        return None

    def make_move(self, move: Move):
        self._board.make_move(move)

    @property
    def legal_moves(self):
        return self._board.legal_moves

    def __str__(self) -> str:
        return str(self._board)
