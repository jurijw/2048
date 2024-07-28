from agent import Agent
from state import State
from view import View


class Controller:
    def __init__(self, state: State, view: View, agent: Agent) -> None:
        self._state = state
        self._view = view
        self._agent = agent

    def play(self) -> None:
        self._view.display(self._state)
        move = self._agent.get_move(self._state)
        self._state.make_move(move)
