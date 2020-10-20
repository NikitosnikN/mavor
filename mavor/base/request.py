import asyncio
from abc import ABCMeta, abstractmethod

__all__ = [
    "AbstractRequest",
    "AbstractRequestBuilder"
]


class AbstractRequest:
    def __init__(
            self,
            protocol: str,
            path: str,
            method: str,
            headers: dict,
            query_string: dict = None,
            raw_body: bytes = None,
    ):
        self.protocol = protocol
        self.path = path
        self.method = method.upper()
        self.headers = headers
        self.query_string = query_string
        self.raw_body = raw_body


class AbstractRequestBuilder(metaclass=ABCMeta):

    @abstractmethod
    async def build(
            self,
            reader: "asyncio.StreamReader",
            writer: "asyncio.StreamWriter"
    ):
        pass
