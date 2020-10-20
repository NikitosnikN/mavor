import re
from collections import defaultdict
from typing import Union, Type, Iterable, Pattern, Callable

from .base import AbstractRouter

__all__ = ["Router"]


class Router(AbstractRouter):
    def __init__(self):
        self._routes = defaultdict(dict)

    @property
    def routes(self) -> dict:
        return self._routes

    def get_handler(
            self,
            method: str,
            path: str,
    ):
        handler = None
        for pattern, methods_ in self._routes.items():
            if pattern.match(path):
                handler = methods_.get(method.upper(), None)

        if not handler:
            raise AttributeError

        return handler

    def add(
            self,
            method: str,
            pattern: Union[str, Pattern],
            handler: Callable
    ):
        if isinstance(pattern, str):
            pattern = re.compile(pattern)

        if pattern in self._routes.keys():
            raise AttributeError

        method = method.upper()

        if method in self._routes.keys():
            raise AttributeError

        self._routes[pattern][method] = handler

    def add_router(
            self,
            router: "Router"
    ):
        for path, methods in router.routes.items():
            for method, handler in methods.items():
                self._routes[path][method] = handler

    def get(
            self,
            pattern: Union[str, Pattern],
            handler: Callable
    ):
        return self.add(
            "GET",
            pattern,
            handler
        )

    def post(
            self,
            pattern: Union[str, Pattern],
            handler: Callable
    ):
        return self.add(
            "POST",
            pattern,
            handler
        )

    def put(
            self,
            pattern: Union[str, Pattern],
            handler: Callable
    ):
        return self.add(
            "PUT",
            pattern,
            handler
        )

    def delete(
            self,
            pattern: Union[str, Pattern],
            handler: Callable
    ):
        return self.add(
            "DELETE",
            pattern,
            handler
        )
