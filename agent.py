from abc import ABC, abstractmethod

from moves import Moves
from state import State


class Agent(ABC):
    """Abstract class that captures an agent, which decides, based on some
    strategy and with information of a game state, what move to make next."""

    @abstractmethod
    @staticmethod
    def get_move(state: State) -> Moves:
        """Given a game state, return a legal move by some strategy."""
        pass
