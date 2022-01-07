import datetime
import json
import typing

from aiohttp.web_exceptions import HTTPUnprocessableEntity, HTTPClientError
from aiohttp.web_middlewares import middleware
from aiohttp_apispec import validation_middleware

from .utils import error_json_response

if typing.TYPE_CHECKING:
    from app.app import Application, Request

HTTP_ERROR_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "not_implemented",
    409: "conflict",
    500: "internal_server_error",
}


@middleware
async def error_handling_middleware(request: "Request", handler):
    try:
        print(
            f'[{datetime.datetime.now().time()}] request: {request}')
        response = await handler(request)
        print(f'[{datetime.datetime.now().time()}] response: {json.loads(response.body)}')
        return response

    except HTTPUnprocessableEntity as e:
        print(f'HTTPUnprocessableEntity: {json.loads(e.text)}')
        return error_json_response(
            http_status=400,
            message=e.reason,
            data=json.loads(e.text),
        )
    except HTTPClientError as e:
        print(f'HTTPClientError: {e.text}')

        return error_json_response(
            http_status=e.status_code,
            message=e.reason,
            data=e.text
        )
    except Exception as e:
        import traceback

        print(f'Exception: {str(e)}')
        traceback.print_exc()

        return error_json_response(
            http_status=500,
            message=str(e.with_traceback()))


def setup_middlewares(app: 'Application'):
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(validation_middleware)
