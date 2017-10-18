import falcon


class SecretMiddleware:
    def __init__(self, secret):
        self._secret = secret

    def process_resource(self, req, resp, resource, params):
        if not req.get_header('Authorization') == self._secret:
            raise falcon.HTTPUnauthorized
