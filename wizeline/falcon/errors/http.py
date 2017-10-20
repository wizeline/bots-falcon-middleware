from datetime import datetime

import falcon.status_codes as status
from falcon import util
from falcon.http_error import HTTPError


class BotHTTPError(HTTPError):
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
        super(BotHTTPError, self).__init__(
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
        return BotHTTPError(OptionalRepresentation, self).code is not None


class BotHTTPBadRequest(BotHTTPError):
    def __init__(self, code=None, message=None, **kwargs):
        super(BotHTTPBadRequest, self).__init__(
            status.HTTP_400,
            code,
            message,
            **kwargs
        )


class BotHTTPUnauthorized(BotHTTPError):
    def __init__(self, code=None, message=None, challenges=None, **kwargs):
        headers = kwargs.setdefault('headers', {})

        if challenges:
            headers['WWW-Authenticate'] = ', '.join(challenges)

        super(BotHTTPUnauthorized, self).__init__(
            status.HTTP_401,
            code,
            message,
            **kwargs
        )


class BotHTTPForbidden(BotHTTPError):
    def __init__(self, code=None, message=None, **kwargs):
        super(BotHTTPForbidden, self).__init__(
            status.HTTP_403,
            code,
            message,
            **kwargs
        )


class BotHTTPNotFound(OptionalRepresentation, BotHTTPError):
    def __init__(self, code=None, message=None, **kwargs):
        super(BotHTTPNotFound, self).__init__(
            status.HTTP_404,
            code,
            message,
            **kwargs
        )


class BotHTTPMethodNotAllowed(OptionalRepresentation, BotHTTPError):
    def __init__(self, allowed_methods, code=None, message=None, **kwargs):
        new_headers = {'Allow': ', '.join(allowed_methods)}

        super(BotHTTPMethodNotAllowed, self).__init__(
            status.HTTP_405,
            code,
            message,
            **kwargs
        )

        if not self.headers:
            self.headers = {}

        self.headers.update(new_headers)


class BotHTTPNotAcceptable(BotHTTPError):
    def __init__(self, code=None, message=None, **kwargs):
        super(BotHTTPNotAcceptable, self).__init__(
            status.HTTP_406,
            code,
            message,
            **kwargs
        )


class BotHTTPConflict(BotHTTPError):
    def __init__(self, code=None, message=None, **kwargs):
        super(BotHTTPConflict, self).__init__(
            status.HTTP_409,
            code,
            message,
            **kwargs
        )


class BotHTTPInternalServerError(BotHTTPError):
    def __init__(self, code=None, message=None, **kwargs):
        super(BotHTTPInternalServerError, self).__init__(
            status.HTTP_500,
            code,
            message,
            **kwargs
        )


class BotHTTPBadGateway(BotHTTPError):
    def __init__(self, code=None, message=None, **kwargs):
        super(BotHTTPBadGateway, self).__init__(
            status.HTTP_502,
            code,
            message,
            **kwargs
        )


class BotHTTPServiceUnavailable(BotHTTPError):
    def __init__(self, code=None, message=None, retry_after=None, **kwargs):
        headers = kwargs.setdefault('headers', {})

        if isinstance(retry_after, datetime):
            headers['Retry-After'] = util.dt_to_http(retry_after)
        elif retry_after is not None:
            headers['Retry-After'] = str(retry_after)

        super(BotHTTPServiceUnavailable, self).__init__(
            status.HTTP_503,
            code,
            message,
            **kwargs
        )
