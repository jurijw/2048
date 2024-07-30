from abc import ABC

from .observer import Observer


class Subject(ABC):
    def __init__(self) -> None:
        self._observers = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event):
        for observer in self._observers:
            observer.update(event)
