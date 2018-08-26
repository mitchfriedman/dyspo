from dyspo.endpoint import Endpoint


class Resource(object):
    method = None

    def __init__(self, endpoint: Endpoint, route: str):
        self.endpoint = endpoint
        self.route = route


Get = type('Get', (Resource,), {'method': 'get'})
Post = type('Post', (Resource,), {'method': 'post'})
Put = type('Put', (Resource,), {'method': 'put'})
Patch = type('Patch', (Resource,), {'method': 'patch'})
Delete = type('Delete', (Resource,), {'method': 'delete'})
