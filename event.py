from abc import ABC


class Event(ABC):
    pass


class KeyPressEvent(Event):
    def __init__(self, key) -> None:
        super().__init__()
        self._key = key

    @property
    def key(self):
        return self._key
