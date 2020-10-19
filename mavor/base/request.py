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
            path: str,
            schema: str,
            method: str,
            headers: dict,
            http_version: str = None,
            query_string: dict = None,
            raw_body: bytes = None,
    ):
        self.protocol = protocol
        self.path = path
        self.schema = schema
        self.method = method.upper()
        self.headers = headers
        self.http_version = http_version
        self.query_string = query_string
        self.raw_body = raw_body


class AbstractRequestBuilder(metaclass=ABCMeta):
    def __init__(
            self,
            app,
            middlewares: list
    ):
        self.__app = app
        self.__middlewares = middlewares

    @abstractmethod
    async def build(
            self,
            reader: "asyncio.StreamReader",
            writer: "asyncio.StreamWriter"
    ):
        pass
