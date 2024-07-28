import pygame

from event import KeyPressEvent
from state import State
from view import View

from collections import namedtuple

DisplaySize = namedtuple("DisplaySize", ["width", "height"])


class PygameView(View):
    def __init__(self) -> None:
        super().__init__()
        pygame.init()
        self._size = DisplaySize(1280, 1280)
        self._screen = pygame.display.set_mode(self._size)
        self._running = True
        self._color = "teal"

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
        pass
