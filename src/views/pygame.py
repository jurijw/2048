import pygame

from event import KeyPressEvent
from model.grid_index import GridIndex
from model.state import State
from views.view import View


class PygameView(View):
    def __init__(self, width: int = 720, height: int = 720) -> None:
        super().__init__()
        pygame.init()
        self._width = width
        self._height = height
        self._size = self._width, self._height
        self._running = True
        self._screen = pygame.display.set_mode(self._size)
        self._font = pygame.font.SysFont("Times New Roman", 65, bold=True)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def display(self, state: State) -> None:
        while self._running:
            self.render(state)
            for event in pygame.event.get():
                if event.type == pygame.quit:
                    self._running = False
                if event.type == pygame.KEYDOWN:
                    self.notify(KeyPressEvent(event.unicode))

    def render(self, state: State):
        self._screen.fill("white")
        self.render_grid(state)
        self.render_entries(state)
        pygame.display.flip()

    def render_grid(self, state: State):
        for row in range(state.height):
            start = (0, row * self.height / state.height)
            end = (self.width, row * self.height / state.height)
            pygame.draw.line(self._screen, "black", start, end, width=5)

        for col in range(state.width):
            start = (col * self.width / state.width, 0)
            end = (col * self.width / state.width, self.height)
            pygame.draw.line(self._screen, "black", start, end, width=5)

    def render_entries(self, state: State):
        dx, dy = self.width // state.width, self.height // state.height
        lattice_points = [
            [(x, y) for x in range(0, self.width, dx)]
            for y in range(0, self.height, dy)
        ]
        for row in range(state.width):
            for col in range(state.height):
                coordinates = lattice_points[row][col]
                x, y = coordinates
                x += dx // 2
                y += dy // 2
                val = state[GridIndex(row, col)]
                if val != 0:
                    text_surface = self._font.render(str(val), True, "black")
                    self._screen.blit(text_surface, (x, y))


class Block:
    def __init__(self, row: int, col: int, val: int) -> None:
        self._row = row
        self._col = col
        self._val = val

    def render(self, state: State):
        pass
