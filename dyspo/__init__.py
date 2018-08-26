from typing import List

from aiohttp import web

from dyspo.resource import Resource
from dyspo.runner import ServerRunner


class Api(web.Application):
    def run(self, debug=False, **kwargs):
        ServerRunner(self).run_server(debug, **kwargs)

    def add_routes(self, resources: List[Resource]):
        routes = [self._get_route(r) for r in resources]
        super().add_routes(routes)

    def _get_route(self, r: Resource):
        method = getattr(web, r.method)
        if method is None:
            raise Exception('Invalid method for resource: {}'.format(r))

        return method(r.route, r.endpoint.run)
