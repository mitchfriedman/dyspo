import aiohttp

from dyspo import Api
from dyspo.endpoint import Endpoint
from dyspo.resource import Get, Post
from dyspo.response import Created, Ok, ServerError


class ExternalService(object):
    async def get_something(self):
        async with aiohttp.ClientSession() as session:
            resp = await session.get('https://google.com')
            return resp


class MyPostEndpoint(Endpoint):
    def __init__(self, service):
        self.service = service

    async def process(self, request):
        resp = await self.service.get_something()
        if resp.status != 200:
            return ServerError({'message': 'Unable to fetch from external service'})

        return Created({'test': 'foo2'})


class MyGetEndpoint(Endpoint):
    async def process(self, request):
        return Ok({'test2': 'foo2'})


class MyGetEndpointWithMatch(Endpoint):
    async def process(self, request):
        info = request.params.get('id')
        return Ok({'id': info})


if __name__ == '__main__':
    api = Api()

    api.add_routes([
        Get(MyGetEndpoint(), '/foo'),
        Get(MyGetEndpointWithMatch(), '/foo/{id}'),
        Post(MyPostEndpoint(ExternalService()), '/foo'),
    ])

    api.run(port=5000, debug=True)
