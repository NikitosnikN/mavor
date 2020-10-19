import asyncio
import json
from typing import Any
from urllib import parse

from .base import AbstractRequest, AbstractRequestBuilder


class Request(AbstractRequest):
    def __init__(
            self,
            protocol: str,
            path: str,
            schema: str,
            method: str,
            headers: dict,
            query_string: dict = None,
            raw_body: bytes = None,
            body: Any = None,
            **kwargs
    ):
        super().__init__(protocol, path, schema, method, headers, query_string, raw_body)
        self._body = body


class RequestBuilder(AbstractRequestBuilder):
    @classmethod
    async def _parse_starting_line(
            cls,
            reader: "asyncio.StreamReader",
            params: dict
    ) -> None:
        line = (await reader.readuntil(b"\r\n")).decode("utf-8").strip("\r\n").split(" ")
        params["method"], params["uri"] = line[0].upper(), line[1]
        params["protocol"], params["version"] = line[-1].split("/")
        return None

    @classmethod
    async def _parse_uri(
            cls,
            params: dict
    ) -> None:
        url_data = parse.urlparse(params["uri"])
        params["path"] = url_data.path
        params["qs"] = parse.parse_qs(url_data.query)
        return None

    @classmethod
    async def _parse_headers(
            cls,
            reader: "asyncio.StreamReader",
            params: dict
    ) -> None:
        params["headers"] = dict()
        line = await reader.readuntil(b"\r\n")
        while True:
            line = line.decode("utf-8").strip("\r\n")

            if not line:
                break

            line = line.split(":", 1)
            params["headers"][line[0].lower()] = line[1].strip()
            line = await reader.readuntil(b"\r\n")

        return None

    @classmethod
    async def _parse_raw_payload(
            cls,
            reader: "asyncio.StreamReader",
            params: dict
    ) -> None:
        params["raw_body"] = await reader.read()
        return None

    @classmethod
    async def _prettify_payload(
            cls,
            params: dict,
    ) -> Any:
        content_type = params["headers"].get("content-type", "")

        if content_type == "application/json":
            params["body"] = json.loads(params["raw_body"].decode("utf-8"))
        elif content_type == "application/x-www-form-urlencoded":
            params["body"] = parse.parse_qs(params["raw_body"].decode("utf-8"))
        elif "multipart/form-data" in content_type:
            # TODO form-data support
            pass

        return None

    async def build(
            self,
            reader: "asyncio.StreamReader",
            writer: "asyncio.StreamWriter",
    ):
        params = {}
        await self._parse_starting_line(reader, params)
        await self._parse_uri(params)
        await self._parse_headers(reader, params)
        await self._parse_raw_payload(reader, params)
        await self._prettify_payload(params)
        return Request(**params)
