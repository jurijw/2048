import argparse

from cli_view import CLIView
from controller import Controller
from pygame_view import PygameView
from random_agent import RandomAgent
from state import State
from user import User

parser = argparse.ArgumentParser(description="Parse script arguments.")
parser.add_argument(
    "--view",
    type=str,
    default="cli",
    choices=["cli", "pygame", "flask"],
    help="What mode to run the game in (default: CLI)",
)
parser.add_argument(
    "--agent",
    type=str,
    default="user",
    choices=["user", "random", "minimax"],
    help="What agent should the game use (default: user)",
)
parser.add_argument(
    "--width", type=int, default=4, help="The width of the grid to be played on."
)
parser.add_argument(
    "--height", type=int, default=4, help="The height of the grid to be played on."
)
parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")
args = parser.parse_args()


def main():
    state = State()
    match args.view:
        case "cli":
            view = CLIView()
        case "pygame":
            view = PygameView()
        case _:
            raise ValueError("View not available.")

    match args.agent:
        case "user":
            agent = User()
        case "random":
            agent = RandomAgent()
        case "evolution":
            raise NotImplementedError()
        case _:
            raise ValueError("Agent not available.")
    controller = Controller(state, view, agent)
    controller.play()


if __name__ == "__main__":
    main()
