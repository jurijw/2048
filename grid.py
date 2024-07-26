class Grid:
    def __init__(self, width, height) -> None:
        self._width = width
        self._height = height
        self._grid = [[0 for _ in range width] for _ in range height]
