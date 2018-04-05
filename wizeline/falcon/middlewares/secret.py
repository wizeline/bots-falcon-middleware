import falcon


def require_secret(req, resp, resource, params):
    secret = req.get_header('Authorization')
    if not req._secret == secret:
        raise falcon.HTTPUnauthorized


class APISecretMiddleware:
    def __init__(self, secret, required=True):
        self._secret = secret
        self._is_secret_required = required

    def _has_valid_secret(self, req):
        return req.get_header('Authorization') == self._secret

    def process_resource(self, req, resp, resource, params):
        is_api_secret_required = getattr(resource, 'is_api_secret_required', True)
        if not is_api_secret_required:
            return

        if self._is_secret_required and not self._has_valid_secret(req):
            raise falcon.HTTPUnauthorized
        req._secret = self._secret
