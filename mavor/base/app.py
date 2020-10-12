import asyncio
from typing import Union, List
from abc import ABCMeta, abstractmethod

__all__ = ["AbstractApp"]


class AbstractApp:
    def __init__(
            self,
            host: Union[str, None] = None,
            port: Union[str, int, None] = None,
            loop: "asyncio.AbstractEventLoop" = None,
            limit: int = 10,
    ):
        self._host = host or "localhost"
        self._port = port or 8000
        self._loop = loop
        self._limit = limit

    async def run_server(self):
        pass
