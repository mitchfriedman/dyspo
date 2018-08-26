from dyspo.endpoint import Endpoint


class Resource(object):
    method = None

    def __init__(self, endpoint: Endpoint, route: str):
        self.endpoint = endpoint
        self.route = route


class Get(Resource):
    method = 'get'


class Post(Resource):
    method = 'post'
