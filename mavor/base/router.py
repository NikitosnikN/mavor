from typing import Pattern, Callable

from abc import ABCMeta, abstractmethod


class AbstractRouter(metaclass=ABCMeta):
    @property
    @abstractmethod
    def routes(self):
        pass

    @abstractmethod
    def get_handler(self, *args, **kwargs):
        pass

    @abstractmethod
    def add(self, *args, **kwargs):
        pass

    @abstractmethod
    def add_router(self, *args, **kwargs):
        pass
