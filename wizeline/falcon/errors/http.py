from datetime import datetime

import falcon.status_codes as status
from falcon import util
from falcon.http_error import HTTPError


class HTTPError(HTTPError):
    """Represents a generic Bot Platform HTTP error.

    This base error extends from Falcon HTTPError in order
    to have compatibility with Falcon but you should use errors
    that extends from this base class. Specially properties:
        status: Is the HTTP Error
        code: Is the name of the Error Class
        message: A description of the error

    """

    def __init__(
            self,
            status,
            code=None,
            message=None,
            headers=None,
            href=None,
            href_text=None
    ):
        super(HTTPError, self).__init__(
            status,
            headers=headers,
            href=href,
            href_text=href_text
        )

        self.status = status
        self.code = code
        self.message = message

    def to_dict(self, obj_type=dict):
        obj = obj_type()

        if self.status is not None:
            obj['status'] = self.status

        if self.code is not None:
            obj['code'] = self.code

        if self.message is not None:
            obj['message'] = self.message

        return obj


class OptionalRepresentation(object):
    @property
    def has_representation(self):
        return HTTPError(OptionalRepresentation, self).code is not None


class HTTPBadRequest(HTTPError):
    def __init__(self, code=None, message=None, **kwargs):
        super(HTTPBadRequest, self).__init__(
            status.HTTP_400,
            code,
            message,
            **kwargs
        )


class HTTPUnauthorized(HTTPError):
    def __init__(self, code=None, message=None, challenges=None, **kwargs):
        headers = kwargs.setdefault('headers', {})

        if challenges:
            headers['WWW-Authenticate'] = ', '.join(challenges)

        super(HTTPUnauthorized, self).__init__(
            status.HTTP_401,
            code,
            message,
            **kwargs
        )


class HTTPForbidden(HTTPError):
    def __init__(self, code=None, message=None, **kwargs):
        super(HTTPForbidden, self).__init__(
            status.HTTP_403,
            code,
            message,
            **kwargs
        )


class HTTPNotFound(OptionalRepresentation, HTTPError):
    def __init__(self, code=None, message=None, **kwargs):
        super(HTTPNotFound, self).__init__(
            status.HTTP_404,
            code,
            message,
            **kwargs
        )


class HTTPMethodNotAllowed(OptionalRepresentation, HTTPError):
    def __init__(self, allowed_methods, code=None, message=None, **kwargs):
        new_headers = {'Allow': ', '.join(allowed_methods)}

        super(HTTPMethodNotAllowed, self).__init__(
            status.HTTP_405,
            code,
            message,
            **kwargs
        )

        if not self.headers:
            self.headers = {}

        self.headers.update(new_headers)


class HTTPNotAcceptable(HTTPError):
    def __init__(self, code=None, message=None, **kwargs):
        super(HTTPNotAcceptable, self).__init__(
            status.HTTP_406,
            code,
            message,
            **kwargs
        )


class HTTPConflict(HTTPError):
    def __init__(self, code=None, message=None, **kwargs):
        super(HTTPConflict, self).__init__(
            status.HTTP_409,
            code,
            message,
            **kwargs
        )


class HTTPInternalServerError(HTTPError):
    def __init__(self, code=None, message=None, **kwargs):
        super(HTTPInternalServerError, self).__init__(
            status.HTTP_500,
            code,
            message,
            **kwargs
        )


class HTTPBadGateway(HTTPError):
    def __init__(self, code=None, message=None, **kwargs):
        super(HTTPBadGateway, self).__init__(
            status.HTTP_502,
            code,
            message,
            **kwargs
        )


class HTTPServiceUnavailable(HTTPError):
    def __init__(self, code=None, message=None, retry_after=None, **kwargs):
        headers = kwargs.setdefault('headers', {})

        if isinstance(retry_after, datetime):
            headers['Retry-After'] = util.dt_to_http(retry_after)
        elif retry_after is not None:
            headers['Retry-After'] = str(retry_after)

        super(HTTPServiceUnavailable, self).__init__(
            status.HTTP_503,
            code,
            message,
            **kwargs
        )
