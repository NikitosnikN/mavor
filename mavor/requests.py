import asyncio

from .base import AbstractRequest, AbstractRequestBuilder


class RequestBuilder(AbstractRequestBuilder):
    async def _parse_headers(self):
        pass

    async def _parse_data(self):
        pass

    async def handle(
            self,
            reader: asyncio.StreamReader,
            writer: asyncio.StreamWriter
    ):
        return
