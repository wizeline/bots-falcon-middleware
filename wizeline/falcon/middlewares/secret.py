import falcon


def require_secret(req, resp, resource, params):
    secret = req.get_header('Authorization')

    if not req._secret == secret:
        raise falcon.HTTPUnauthorized

class APISecretMiddleware: 
    def __init__(self, secret):
        self._secret = secret
    
    def process_resource(self, req, resp, resource, params, required):
        if require:
            if not req.get_header('Authorization') == self._secret:
              raise falcon.HTTPUnauthorized
        req._secret = self._secret