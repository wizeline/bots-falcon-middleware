import json
from json import JSONDecodeError

from falcon import (
    HTTPUnsupportedMediaType,
    HTTPBadRequest,
    HTTPInternalServerError
)


class JSONMiddleware:
    def process_resource(self, req, resp, resource, params):
        if (self._is_middleware_enabled(resource)
           and self._has_request_method_payload(req)):
            if not self._is_content_type_valid(req):
                raise HTTPUnsupportedMediaType()

            try:
                req.text = self._get_payload(req)
                req.json = (json.loads(req.text, encoding='utf-8')
                            if req.text.strip() != '' else {})
            except JSONDecodeError as error:
                raise HTTPBadRequest(f'Invalid JSON received: error={error}')
            except Exception as error:
                raise HTTPInternalServerError(f'Unexpected error: error={error}')

    def process_response(self, req, resp, resource, req_succeeded):
        if not self._has_body(resp):
            resp.body = self._serialize_json_to_string(resp)

    def _is_middleware_enabled(self, resource):
        return (not hasattr(resource, 'disable_json_middleware')
                or not resource.disable_json_middleware)

    def _has_request_method_payload(self, req):
        return req.method in ('POST', 'PUT')

    def _is_content_type_valid(self, req):
        return req.content_type and ('application/json' in req.content_type or 'text/json' in req.content_type)

    def _get_payload(self, req):
        return (req.bounded_stream.read()
                .decode('utf-8'))

    def _has_body(self, resp):
        return resp.body is not None

    def _serialize_json_to_string(self, resp):
        if self._has_json(resp):
            if not isinstance(resp.json, (dict, list)):
                raise HTTPInternalServerError(f'Unexpected error parsing response: payload={resp.json}')
            return json.dumps(resp.json)
        return json.dumps({})

    def _has_json(self, resp):
        return hasattr(resp, 'json')
