import falcon


class SecretMiddleware: 
    def __init__(self, secret):
        self._secret = secret
    
    def process_resource(self, req, resp, resource, params):
        req._secret = self._secret
    
    def require_secret(req, resp, resource, params):
        secret = req.get_header('Authorization')

        if not req._secret == secret:
            raise falcon.HTTPUnauthorized


class AlwayRequireSecretMiddleware:
    def __init__(self, secret):
        self._secret = secret

    def process_resource(self, req, resp, resource, params):
        if not req.get_header('Authorization') == self._secret:
            raise falcon.HTTPUnauthorized
