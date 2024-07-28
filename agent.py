from abc import ABC, abstractmethod

from moves import Moves
from state import State


class Agent(ABC):
    """Abstract class that captures an agent, which decides, based on some
    strategy and with information of a game state, what move to make next."""

    def __init__(self, state: State) -> None:
        self._state = state

    @abstractmethod
    def get_move(self) -> Moves:
        """Return a legal move by some strategy."""
        pass
