from json import JSONDecodeError
from typing import Dict
from aiohttp.web import Request as BaseRequest

from dyspo.response import BadRequest, AbortException


class Request(object):
    def __init__(self,
                 method: str=None,
                 scheme: str=None,
                 uri: str=None,
                 headers: Dict[str, str]=None,
                 data: Dict[str, str]=None,
                 params: Dict[str, str]=None,
                 query: Dict[str, str]=None,
                 username: str=None,
                 password: str=None):
        self.method = method
        self.scheme = scheme
        self.uri = uri
        self.headers = headers
        self.data = data
        self.params = params
        self.query = query
        self.username = username
        self.password = password

    @classmethod
    async def from_request(cls, request: BaseRequest) -> 'Request':
        method = request.method
        scheme = request.scheme
        uri = request.rel_url.path
        headers = dict(request.headers)
        params = dict(request.match_info)
        query = dict(request.query)

        if not request.content.at_eof():
            try:
                data = await request.json()
            except JSONDecodeError:
                raise AbortException(BadRequest('Malformed JSON data: {}'.format(await request.content.read())))
        else:
            data = {}

        username = None
        password = None

        if 'Authorization' in headers:
            username, password = cls.parse_auth(headers.pop('Authorization'))

        return cls(
            method=method,
            uri=uri,
            scheme=scheme,
            headers=headers,
            data=data,
            params=params,
            query=query,
            username=username,
            password=password,
        )

    @classmethod
    def parse_auth(cls, header):
        # Dumb attempt at parsing auth for now
        try:
            auth = header.split(' ')[1]
            parts = auth.split(':')
            return parts[0], parts[1]
        except:
            return None, None
