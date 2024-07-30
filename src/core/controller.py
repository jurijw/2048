from .agent import Agent
from .event import KeyPressEvent
from .model import Moves, State
from .observer import Observer
from .view import View


class Controller(Observer):
    def __init__(self, state: State, view: View, agent: Agent) -> None:
        self._state = state
        self._view = view
        view.attach(self)
        self._agent = agent

    def play(self) -> None:
        self._view.display(self._state)

    def update(self, event):
        if isinstance(event, KeyPressEvent):
            parsed_move = parse_move(event.key)
            if parsed_move in self._state.legal_moves:
                self._state.make_move(parsed_move)


def parse_move(user_input: str):
    """Parses a move string into a move. Invalid input returns None."""
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
