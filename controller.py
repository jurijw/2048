from agent import Agent
from event import KeyPressEvent
from moves import Moves
from observer import Observer
from state import State
from view import View


class Controller(Observer):
    def __init__(self, state: State, view: View, agent: Agent) -> None:
        self._state = state
        self._view = view
        view.attatch(self)
        self._agent = agent

    def play(self) -> None:
        self._view.display(self._state)

    def update(self, event):
        if isinstance(event, KeyPressEvent):
            parsed_move = parse_move(event.key)
            if parsed_move is not None:
                self._state.make_move(parsed_move)
        # while not self._state.game_over:
        #     self._view.display(self._state)
        #     move = self._agent.get_move(self._state)
        #     self._state.make_move(move)


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
