from agent import Agent
from moves import Moves
from state import State


class User(Agent):
    @staticmethod
    def get_move(state: State):
        """Parse user input until a valid move is entered."""
        prompt_input()
        parsed_move = None
        while parsed_move not in state.legal_moves:
            user_input = input()
            parsed_move = parse_move(user_input)
        return parsed_move


def prompt_input():
    """Prompt the user for a move input."""
    print("Enter a move (hjkl): ", end="")


def parse_move(user_input: str):
    """Parses input from stdin into a move. Invalid input returns None and
    calls the optional callback function ON_FAIL."""
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
