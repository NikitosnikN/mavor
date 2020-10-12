from abc import ABCMeta, abstractmethod
from http import HTTPStatus

__all__ = [
    "AbstractRequest",
    "AbstractRequestBuilder"
]


class AbstractRequest:
    def __init__(
            self,
            protocol: str,
            method: str,
            headers: dict,
            body: bytes,
    ):
        pass


class AbstractRequestBuilder(metaclass=ABCMeta):
    def __init__(
            self,
            app,
            middlewares: list
    ):
        self.__app = app
        self.__middlewares = middlewares

    @abstractmethod
    async def handle(
            self,
            reader: "asyncio.StreamReader",
            writer: "asyncio.StreamWriter"
    ):
        pass
