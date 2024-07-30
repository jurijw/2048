from abc import abstractmethod

from model.state import State
from subject import Subject


class View(Subject):
    @abstractmethod
    def display(self, state: State) -> None:
        """Take a state and display it in some form."""
        pass
