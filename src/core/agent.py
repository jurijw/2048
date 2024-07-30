from abc import ABC, abstractmethod

from .model import Moves, State


class Agent(ABC):
    """Abstract class that captures an agent, which decides, based on some
    strategy and with information of a game state, what move to make next."""

    @abstractmethod
    def get_move(self, state: State) -> Moves:
        """Given a game state, return a legal move by some strategy."""
        pass
