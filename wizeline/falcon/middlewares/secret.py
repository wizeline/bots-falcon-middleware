import falcon


def require_secret(req, resp, resource, params):
    secret = req.get_header('Authorization')
    if not req._secret == secret:
        raise falcon.HTTPUnauthorized


class APISecretMiddleware:
    def __init__(self, secret, required=True):
        print(required)
        self._secret = secret
        self._required = required
    
    def _is_secret_required(self):
        if self._required:
            return True
        return False

    def _has_valid_secret(self, req):
        if not req.get_header('Authorization') == self._secret:
            return True
        return False

    def process_resource(self, req, resp, resource, params):
        if self._is_secret_required() and self._has_valid_secret(req):
            raise falcon.HTTPUnauthorized
        req._secret = self._secret
