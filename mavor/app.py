import asyncio
from typing import Union, Type, Optional, Callable, Pattern, List

from .base import *
from .requests import RequestBuilder, Request
from .router import Router

__all__ = ["Mavor"]


class Mavor(AbstractApp):
    def __init__(
            self,
            host: Union[str, None] = "localhost",
            port: Union[str, int, None] = 8000,
            *,
            middlewares: list = None,
            router: Type[AbstractRouter] = Router,
            request_class: Type[AbstractRequest] = Request,
            response_class: Type[AbstractResponse] = None,
            request_builder: Type[AbstractRequestBuilder] = RequestBuilder,
            response_builder: Type[AbstractResponseBuilder] = None,
            loop: asyncio.AbstractEventLoop = None,
            limit: int = None,
    ):
        super().__init__(host, port, loop, limit)

        self._middlewares: List[Callable] = middlewares or list()
        self.router = router()
        self._request_class = request_class
        self._response_class = response_class
        self._request_builder = request_builder(app=self)
        self._response_builder = response_builder

        self._is_running = False
        self._server: Optional["asyncio.AbstractServer"] = None

    async def _create_server(self) -> "asyncio.AbstractServer":
        self._server = await asyncio.start_server(
            client_connected_cb=self._handle_request,
            host=self._host,
            port=self._port,
            loop=self._loop
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

    async def _handle_request(
            self,
            reader: "asyncio.StreamReader",
            writer: "asyncio.StreamWriter"
    ):
        request = await self._request_builder.build(reader, writer)

        for middleware in self._middlewares:
            await middleware(self, request)

        handler = self.router.get_handler(request.method, request.path)
        await handler(request)
        return

    def add_middleware(
            self,
            middleware: Callable,
    ):
        self._middlewares.append(middleware)

    def add_route(
            self,
            method: str,
            pattern: Union[str, Pattern],
            handler: Callable
    ):
        self.router.add(method, pattern, handler)

    def add_router(
            self,
            router: str,
    ):
        self.router.add_router(router)
