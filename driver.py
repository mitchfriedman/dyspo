from dyspo import Api
from dyspo.endpoint import Endpoint
from dyspo.resource import Get, Post
from dyspo.response import Created, Ok


class MyPostEndpoint(Endpoint):
    async def process(self, request):
        return Created({'test': 'foo'})


class MyGetEndpoint(Endpoint):
    async def process(self, request):
        return Ok({'test': 'foo1'})


if __name__ == '__main__':
    api = Api()

    api.add_routes([
        Get(MyGetEndpoint(), '/foo'),
        Post(MyPostEndpoint(), '/foo'),
    ])

    api.run(port=5000, debug=True)
