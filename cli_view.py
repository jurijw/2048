import os


from event import KeyPressEvent
from state import State
from view import View


class CLIView(View):
    def display(self, state: State) -> None:
        clear()
        while not state.game_over:
            print("Welcome to 2048.py!")
            print(add_padding(str(state), left=5, above=2, below=2))
            user_input = input("Enter a move (hjkl): ")
            self.notify(KeyPressEvent(user_input))
            clear()


def clear() -> None:
    """Runs the clear screen command for the current os."""
    os.system("clear" if os.name == "posix" else "cls")


def add_padding(msg: str, left: int, above: int, below: int):
    lines = msg.split("\n")
    padded_left = "\n".join([left * " " + line for line in lines])
    return "\n" * above + padded_left + "\n" * below
