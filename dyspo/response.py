import json

from aiohttp import web


class AbortException(Exception):
    def __init__(self, response):
        self.response = response


class RestResponse(web.Response):
    def __init__(self, status=None, reason=None, content=None, headers=None):
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


class BadRequest(RestResponse):
    def __init__(self, content=None, headers=None):
        super().__init__(status=400, reason='Bad Request', content=content, headers=headers)