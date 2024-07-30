from random import choice
from time import sleep

from agent import Agent
from core import Moves, State


class RandomAgent(Agent):
    SLEEP_TIME: float = 0.0

    def get_move(self, state: State) -> Moves:
        """Return a random legal move after a delay."""
        sleep(self.SLEEP_TIME)
        return choice(state.legal_moves)
