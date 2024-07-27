from game import Game
from moves import Moves
from state import State
import os


class CLI(Game):
    def __init__(self, state: State | None = None) -> None:
        super().__init__(state)

    def get_move(self) -> Moves:
        """Parse user input until a valid move is entered."""
        user_input = input("Enter a move (hjkl) ")
        parsed_move = self.parse_move(user_input)
        while parsed_move is None or parsed_move not in self.legal_moves:
            parsed_move = self.parse_move(user_input)
        return parsed_move

    def do_before_game(self) -> None:
        self.clear()

    def do_before_every_move(self) -> None:
        print("Welcome to 2048.py!")
        print(self.add_padding(str(self.state), left=5, above=2, below=2))

    def do_after_every_move(self) -> None:
        self.clear()

    def do_on_win(self) -> None:
        print("Winner winner!")

    def do_after_win(self) -> None:
        print("You've one, but you can continue to play!")

    def do_on_game_over(self) -> None:
        print("Game over ;-;")

    @staticmethod
    def parse_move(user_input):
        """Parses input from stdin into a move. Invalid input returns None."""
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

    @staticmethod
    def clear() -> None:
        """Runs the clear screen command for the current os."""
        os.system("clear" if os.name == "posix" else "cls")

    @staticmethod
    def add_padding(msg: str, left: int, above: int, below: int):
        lines = msg.split("\n")
        padded_left = "\n".join([left * " " + line for line in lines])
        return "\n" * above + padded_left + "\n" * below
