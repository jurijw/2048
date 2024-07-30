from model import Moves, State
from abc import ABC, abstractmethod


class Game(ABC):
    """A class for playing and interacting with a game of 2048."""

    def __init__(self, state: State | None = None) -> None:
        """An instance of a 2048 game. Can optionally be instantiated
        with a state instance to start from any configuration desired."""
        if state is None:
            state = State()
        self._state = state
        self._has_won = state.won

    @abstractmethod
    def get_move(self) -> Moves:
        """Return a move to be played next. This must be a valid move
        given the current state of the game. This method must be implemented
        by any subclasses."""
        pass

    def do_before_game(self) -> None:
        """Excecutes once before the game starts."""
        pass

    def do_before_every_move(self) -> None:
        """Executes once before every move."""
        pass

    def do_after_every_move(self) -> None:
        """Executes once after every move."""
        pass

    def do_on_win(self) -> None:
        """Executes once when the winning state is achieved."""
        pass

    def do_after_win(self) -> None:
        """Executes once every turn after the winning state is achieved."""
        pass

    def do_on_game_over(self) -> None:
        """Executes once when the game is over."""

    def play(self):
        """Play a game from the current state until the game ends.
        Various methods are injected at differnt steps during the game,
        which can be overwritten in subclasses to control how to display
        and interact with the game."""
        self.do_before_game()
        while not self.game_over:
            if self.won:
                if not self.prev_won:
                    self.do_on_win()
                    self._prev_won = True
                else:
                    self.do_after_win()
            self.do_before_every_move()
            move = self.get_move()
            self.make_move(move)
            self.do_after_every_move()
        self.do_on_game_over()

    def make_move(self, move: Moves):
        """Apply a move to my state."""
        self._state.make_move(move)

    @property
    def state(self):
        """Return the state associated with this game."""
        return self._state

    @property
    def legal_moves(self):
        """Return a list of legal moves for the current game state."""
        return self._state.legal_moves

    @property
    def game_over(self):
        """Returns true iff the game is over."""
        return self._state.game_over

    @property
    def won(self):
        """Returns true iff the game has been won. Note that in 2048
        this doesn't mean the game ends."""
        return self._state.won

    @property
    def prev_won(self):
        """Returns true iff the game reached a winning state before this turn."""
        return self._prev_won

    def __str__(self) -> str:
        return str(self._state)
