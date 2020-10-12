import asyncio
from typing import Union, Type, Optional

from .base import (
    AbstractApp, AbstractRequest, AbstractRequestBuilder, AbstractResponse, AbstractResponseBuilder
)
from .requests import RequestBuilder


class Mavor(AbstractApp):
    def __init__(
            self,
            host: Union[str, None] = "localhost",
            port: Union[str, int, None] = 8000,
            *,
            middlewares: list = None,
            request_class: Type[AbstractRequest] = None,
            response_class: Type[AbstractResponse] = None,
            request_builder: Type[AbstractRequestBuilder] = RequestBuilder,
            response_builder: Type[AbstractResponseBuilder] = None,
            loop: asyncio.AbstractEventLoop = None,
            limit: int = None,
    ):
        super().__init__(host, port, loop, limit)

        self._middlewares = middlewares or list()
        self._request_class = request_class
        self._response_class = response_class
        self._request_builder = request_builder(
            app=self, middlewares=middlewares
        )
        self._response_builder = response_builder

        self._is_running = False
        self._server: Optional["asyncio.AbstractServer"] = None

    async def _create_server(self) -> "asyncio.AbstractServer":
        self._server = await asyncio.start_server(
            client_connected_cb=self._request_builder.handle,
            host=self._host,
            port=self._port,
            # loop=self._loop,
            # limit=self._limit
        )
        return self._server

    async def run_server(self):
        await self._create_server()
        try:
            await self._server.serve_forever()
        except KeyboardInterrupt:
            self._server.close()
            await self._server.wait_closed()

        return None

    async def stop_server(self):
        self._server.close()
        await self._server.wait_closed()
