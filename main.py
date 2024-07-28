from cli import CLI
import argparse

parser = argparse.ArgumentParser(description="Parse script arguments.")
parser.add_argument(
    "--mode",
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
    game = CLI()
    game.play()


if __name__ == "__main__":
    main()
