from dyspo.request import Request
from dyspo.response import RestResponse, AbortException


class Endpoint(object):
    async def run(self, request):
        try:
            request = await self.transform_request(request)

            response = await self.process(request)
            return response
        except AbortException as e:
            return e.response

    async def process(self, request) -> RestResponse:
        raise NotImplementedError()

    def transform_request(self, request):
        return Request.from_request(request)
