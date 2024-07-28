from abc import ABC, abstractmethod

from state import State


class View(ABC):
    @abstractmethod
    @staticmethod
    def display(state: State) -> None:
        """Take a state and display it in some form."""
        pass
