import pygame

from event import KeyPressEvent
from grid_index import GridIndex
from state import State
from view import View

from collections import namedtuple

DisplaySize = namedtuple("DisplaySize", ["width", "height"])


class PygameView(View):
    def __init__(self) -> None:
        super().__init__()
        pygame.init()
        self._size = DisplaySize(1280, 1280)
        self._width, self._height = self._size
        self._screen = pygame.display.set_mode(self._size)
        self._running = True
        self._color = "teal"
        self._font = pygame.font.SysFont("Times New Roman", 65, bold=True)

    def display(self, state: State) -> None:
        while self._running:
            print(state)
            # poll for events
            # pygame.quit event means the user clicked x to close your window
            for event in pygame.event.get():
                if event.type == pygame.quit:
                    self._running = False

                if event.type == pygame.KEYDOWN:
                    self.notify(KeyPressEvent(event.unicode))

            # fill the screen with a color to wipe away anything from last frame
            self._screen.fill(self._color)

            self.render_grid(state)
            self.render_entries(state)
            # flip() the display to put your work on screen
            pygame.display.flip()

    def render_grid(self, state: State):
        for row in range(state.height):
            start = (0, row * self._size.height / state.height)
            end = (self._size.width, row * self._size.height / state.height)
            pygame.draw.line(self._screen, "black", start, end, width=5)

        for col in range(state.width):
            start = (col * self._size.width / state.width, 0)
            end = (col * self._size.width / state.width, self._size.height)
            pygame.draw.line(self._screen, "black", start, end, width=5)

    def render_entries(self, state: State):
        dx, dy = self._width // state.width, self._height // state.height
        lattice_points = [
            [(x, y) for x in range(0, self._width, dx)]
            for y in range(0, self._height, dy)
        ]
        for row in range(state.width):
            for col in range(state.height):
                coordinates = lattice_points[row][col]
                x, y = coordinates
                x += dx // 2
                y += dy // 2
                val = state[GridIndex(row, col)]
                if val != 0:
                    text_surface = self._font.render(str(val), True, "orange")
                    self._screen.blit(text_surface, (x, y))
