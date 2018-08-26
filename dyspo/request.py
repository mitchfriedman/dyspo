from json import JSONDecodeError
from typing import Dict

from dyspo.response import BadRequest, AbortException


class Request(object):
    def __init__(self,
                 method: str=None,
                 uri: str=None,
                 scheme: str=None,
                 headers: Dict[str, str]=None,
                 body: Dict[str, str]=None,
                 query: Dict[str, str]=None,
                 username: str=None,
                 password: str=None):
        self.method = method
        self.uri = uri
        self.scheme = scheme
        self.headers = headers
        self.body = body
        self.query = query
        self.username = username
        self.password = password

    @classmethod
    async def from_request(cls, request) -> 'Request':
        method = request.method
        scheme = request.scheme
        uri = request.rel_url.path
        headers = dict(request.headers)
        query = dict(request.query)

        try:
            body = await request.json()
        except JSONDecodeError:
            raise AbortException(BadRequest('Malformed JSON data: {}'.format(await request.content.read())))

        username = None
        password = None

        if 'Authorization' in headers:
            auth = headers['Authorization']
            parts = auth.split(':')
            username, password = parts[0], parts[1]

        return cls(
            method=method,
            uri=uri,
            scheme=scheme,
            headers=headers,
            body=body,
            query=query,
            username=username,
            password=password,
        )
