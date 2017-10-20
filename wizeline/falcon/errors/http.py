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
    """Mixin for ``BotHttpError`` child classes that may have a representation.

    This class can be mixed in when inheriting from ``BotHttpError`` in order
    to override the `has_representation` property, such that it will
    return ``False`` when the error instance has no code
    (i.e., the `code` kwarg was not set).

    You can use this mixin when defining errors that do not include
    a body in the HTTP response by default, serializing details only when
    the web developer provides a description of the error.

    """
    @property
    def has_representation(self):
        return BotHTTPError(OptionalRepresentation, self).code is not None


class BotHTTPBadRequest(BotHTTPError):
    """400 Bad Request.

    The server cannot or will not process the request due to something
    that is perceived to be a client error (e.g., malformed request
    syntax, invalid request message framing, or deceptive request
    routing).

    """

    def __init__(self, code=None, message=None, **kwargs):
        super(BotHTTPBadRequest, self).__init__(
            status.HTTP_400,
            code,
            message,
            **kwargs
        )


class BotHTTPUnauthorized(BotHTTPError):
    """401 Unauthorized.

    The request has not been applied because it lacks valid
    authentication credentials for the target resource.

    The server generating a 401 response MUST send a WWW-Authenticate
    header field containing at least one challenge applicable to the
    target resource.

    If the request included authentication credentials, then the 401
    response indicates that authorization has been refused for those
    credentials. The user agent MAY repeat the request with a new or
    replaced Authorization header field. If the 401 response contains
    the same challenge as the prior response, and the user agent has
    already attempted authentication at least once, then the user agent
    SHOULD present the enclosed representation to the user, since it
    usually contains relevant diagnostic information.

    """

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
    """403 Forbidden.

    The server understood the request but refuses to authorize it.

    A server that wishes to make public why the request has been
    forbidden can describe that reason in the response payload (if any).

    If authentication credentials were provided in the request, the
    server considers them insufficient to grant access. The client
    SHOULD NOT automatically repeat the request with the same
    credentials. The client MAY repeat the request with new or different
    credentials. However, a request might be forbidden for reasons
    unrelated to the credentials.

    An origin server that wishes to "hide" the current existence of a
    forbidden target resource MAY instead respond with a status code of
    404 Not Found.

    """

    def __init__(self, code=None, message=None, **kwargs):
        super(BotHTTPForbidden, self).__init__(
            status.HTTP_403,
            code,
            message,
            **kwargs
        )


class BotHTTPNotFound(OptionalRepresentation, BotHTTPError):
    """404 Not Found.

    The origin server did not find a current representation for the
    target resource or is not willing to disclose that one exists.

    A 404 status code does not indicate whether this lack of
    representation is temporary or permanent; the 410 Gone status code
    is preferred over 404 if the origin server knows, presumably through
    some configurable means, that the condition is likely to be
    permanent.

    A 404 response is cacheable by default; i.e., unless otherwise
    indicated by the method definition or explicit cache controls.

    """

    def __init__(self, code=None, message=None, **kwargs):
        super(BotHTTPNotFound, self).__init__(
            status.HTTP_404,
            code,
            message,
            **kwargs
        )


class BotHTTPMethodNotAllowed(OptionalRepresentation, BotHTTPError):
    """405 Method Not Allowed.

    The method received in the request-line is known by the origin
    server but not supported by the target resource.

    The origin server MUST generate an Allow header field in a 405
    response containing a list of the target resource's currently
    supported methods.

    A 405 response is cacheable by default; i.e., unless otherwise
    indicated by the method definition or explicit cache controls.

    """

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
    """406 Not Acceptable.

    The target resource does not have a current representation that
    would be acceptable to the user agent, according to the proactive
    negotiation header fields received in the request, and the server
    is unwilling to supply a default representation.

    The server SHOULD generate a payload containing a list of available
    representation characteristics and corresponding resource
    identifiers from which the user or user agent can choose the one
    most appropriate. A user agent MAY automatically select the most
    appropriate choice from that list. However, this specification does
    not define any standard for such automatic selection, as described
    in RFC 7231, Section 6.4.1
    """

    def __init__(self, code=None, message=None, **kwargs):
        super(BotHTTPNotAcceptable, self).__init__(
            status.HTTP_406,
            code,
            message,
            **kwargs
        )


class BotHTTPConflict(BotHTTPError):
    """409 Conflict.

    The request could not be completed due to a conflict with the
    current state of the target resource. This code is used in
    situations where the user might be able to resolve the conflict and
    resubmit the request.

    The server SHOULD generate a payload that includes enough
    information for a user to recognize the source of the conflict.

    Conflicts are most likely to occur in response to a PUT request. For
    example, if versioning were being used and the representation being
    PUT included changes to a resource that conflict with those made by
    an earlier (third-party) request, the origin server might use a 409
    response to indicate that it can't complete the request. In this
    case, the response representation would likely contain information
    useful for merging the differences based on the revision history.
    """

    def __init__(self, code=None, message=None, **kwargs):
        super(BotHTTPConflict, self).__init__(
            status.HTTP_409,
            code,
            message,
            **kwargs
        )


class BotHTTPInternalServerError(BotHTTPError):
    """500 Internal Server Error.

    The server encountered an unexpected condition that prevented it
    from fulfilling the request.

    """

    def __init__(self, code=None, message=None, **kwargs):
        super(BotHTTPInternalServerError, self).__init__(
            status.HTTP_500,
            code,
            message,
            **kwargs
        )


class BotHTTPBadGateway(BotHTTPError):
    """502 Bad Gateway.

    The server, while acting as a gateway or proxy, received an invalid
    response from an inbound server it accessed while attempting to
    fulfill the request.

    """

    def __init__(self, code=None, message=None, **kwargs):
        super(BotHTTPBadGateway, self).__init__(
            status.HTTP_502,
            code,
            message,
            **kwargs
        )


class BotHTTPServiceUnavailable(BotHTTPError):
    """503 Service Unavailable.

    The server is currently unable to handle the request due to a
    temporary overload or scheduled maintenance, which will likely be
    alleviated after some delay.

    The server MAY send a Retry-After header field to suggest an
    appropriate amount of time for the client to wait before retrying
    the request.

    Note: The existence of the 503 status code does not imply that a
    server has to use it when becoming overloaded. Some servers might
    simply refuse the connection.

    """

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
