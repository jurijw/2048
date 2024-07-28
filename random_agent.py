from random import choice
from time import sleep

from agent import Agent
from moves import Moves
from state import State


class RandomAgent(Agent):
    SLEEP_TIME = 0.1

    def get_move(self, state: State) -> Moves:
        """Return a random legal move after a delay."""
        sleep(self.SLEEP_TIME)
        return choice(state.legal_moves)
