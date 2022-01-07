from typing import Any, Optional

from aiohttp.web import json_response as aiohttp_json_response
from aiohttp.web_response import Response
from asyncpg import Record


def json_response(data: Any = None, status: int = 200) -> Response:
    if data is None:
        data = {}
    return aiohttp_json_response(
        data={
            "status": status,
            "data": data
        },
        status=status,
    )


def error_json_response(
        http_status: int,
        message: Optional[str] = None,
        data: Optional[dict] = None,
):
    if data is None:
        data = {}
    return aiohttp_json_response(
        status=http_status,
        data={
            "status": http_status,
            "message": message,
            "data": data,
        })
