import json

from aiohttp import web


class AbortException(Exception):
    def __init__(self, response):
        self.response = response


class RestResponse(web.Response):
    status = None
    reason = None

    def __init__(self, status, reason, content=None, headers=None):
        body = json.dumps(content)
        override_headers = headers or {}

        headers = {
            'Content-Type': 'application/json',
        }

        for header, value in override_headers.items():
            headers[header] = value

        super().__init__(status=status, reason=reason, body=body, headers=headers)


class Ok(RestResponse):
    def __init__(self, content=None, headers=None):
        super().__init__(status=200, reason='Success', content=content, headers=headers)


class Created(RestResponse):
    def __init__(self, content=None, headers=None):
        super().__init__(status=201, reason='Created', content=content, headers=headers)


class NoContent(RestResponse):
    def __init__(self, headers=None):
        super().__init__(status=204, reason='No Content', headers=headers)


class BadRequest(RestResponse):
    def __init__(self, content=None, headers=None):
        super().__init__(status=400, reason='Bad Request', content=content, headers=headers)


class Unauthorized(RestResponse):
    def __init__(self, content=None, headers=None):
        super().__init__(status=401, reason='Unauthorized', content=content, headers=headers)


class Forbidden(RestResponse):
    def __init__(self, content=None, headers=None):
        super().__init__(status=403, reason='Forbidden', content=content, headers=headers)


class NotFound(RestResponse):
    def __init__(self, content=None, headers=None):
        super().__init__(status=404, reason='Not Found', content=content, headers=headers)


class ServerError(RestResponse):
    def __init__(self, content=None, headers=None):
        super().__init__(status=500, reason='Server Error', content=content, headers=headers)
