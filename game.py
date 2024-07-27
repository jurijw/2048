from board import Board
from moves import Moves
import os


class Game:
    def __init__(self, board=None) -> None:
        self._board = board if board is not None else Board()

    def play(self):
        # Clear the screen
        def cls():
            os.system("clear" if os.name == "posix" else "cls")

        cls()

        while not self._board.game_over:
            print("Welcome to 2048.py!")
            [print() for _ in range(3)]
            print(f"Points: {self._board.points}")
            print(self._board)
            [print() for _ in range(3)]
            user_input = input("Enter a move (hjkl) ")
            if self._board._has_won:
                print("Winner winner!")
            parsed_move = self.parse_move(user_input)
            if parsed_move is not None and parsed_move in self.legal_moves:
                self.make_move(parsed_move)
                self._board.add_tile()
                cls()
            else:
                print("Incorrect entry.")

    @staticmethod
    def parse_move(user_input):
        match user_input.strip().lower():
            case "h":
                return Moves.LEFT
            case "j":
                return Moves.DOWN
            case "k":
                return Moves.UP
            case "l":
                return Moves.RIGHT
        return None

    def make_move(self, move: Moves):
        self._board.make_move(move)

    @property
    def legal_moves(self):
        return self._board.legal_moves

    def __str__(self) -> str:
        return str(self._board)
