import os


from state import State
from view import View


class CLIView(View):
    @staticmethod
    def display(state: State):
        clear()
        print("Welcome to 2048.py!")
        print(add_padding(str(state), left=5, above=2, below=2))


def clear() -> None:
    """Runs the clear screen command for the current os."""
    os.system("clear" if os.name == "posix" else "cls")


def add_padding(msg: str, left: int, above: int, below: int):
    lines = msg.split("\n")
    padded_left = "\n".join([left * " " + line for line in lines])
    return "\n" * above + padded_left + "\n" * below
