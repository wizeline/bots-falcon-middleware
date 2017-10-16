import json

import falcon
from falcon import testing

from middlewares.json import JSONMiddleware

from sure import expect

ECHO_ROUTE = '/echo'
SETTABLE_ROUTE = '/settable'
DISABLED_ROUTE = '/without-middleware'


class EchoResource:
    def __init__(self):
        self.last_request = None

    def on_post(self, req, resp):
        self.last_request = req
        resp.body = json.dumps(req.json)

    def has_request_included_json(self):
        if not self.last_request:
            return False
        if not hasattr(self.last_request, 'json'):
            return False
        return self.last_request.json is not None

    def get_last_request(self):
        return self.last_request

    def get_requested_json_payload(self):
        if not self.has_request_included_json():
            return None
        return self.last_request.json


class SettableResource:
    def __init__(self):
        self.text_payload = None
        self.json_payload = None

    def set_text(self, payload):
        self.text_payload = payload

    def set_json(self, payload):
        self.json_payload = payload

    def on_get(self, req, resp):
        if self.text_payload:
            resp.body = self.text_payload
        if self.json_payload:
            resp.json = self.json_payload


class DisabledMiddlewareResource(EchoResource):
    disable_json_middleware = True

    def on_post(self, req, resp):
        self.last_request = req
        resp.body = json.dumps(req.stream.read().decode('utf-8'))


class JSONMiddlewareTest(testing.TestCase):
    def setUp(self):
        json_middleware = JSONMiddleware()
        self.app = falcon.API(middleware=[json_middleware])

        self.echo_resource = EchoResource()
        self.settable_resource = SettableResource()
        self.disabled_resource = DisabledMiddlewareResource()

        self.app.add_route(ECHO_ROUTE, self.echo_resource)
        self.app.add_route(SETTABLE_ROUTE, self.settable_resource)
        self.app.add_route(DISABLED_ROUTE, self.disabled_resource)

    def test_post_with_json_payload(self):
        payload = {'hello': 'world'}

        self.simulate_post(
            ECHO_ROUTE,
            body=json.dumps(payload),
            headers={'content-type': 'application/json'}
        )

        expect(self.echo_resource.has_request_included_json()).to.be.true
        expect(self.echo_resource.get_last_request()).to.have.property('json')
        expect(self.echo_resource.get_requested_json_payload()).to.equal(payload)

    def test_post_with_json_array_payload(self):
        payload = [{'id': 1, 'name': 'Bot'}]

        self.simulate_post(
            ECHO_ROUTE,
            body=json.dumps(payload),
            headers={'content-type': 'application/json'}
        )

        expect(self.echo_resource.has_request_included_json()).to.be.true
        expect(self.echo_resource.get_last_request()).to.have.property('json')
        expect(self.echo_resource.get_requested_json_payload()).to.equal(payload)

    def test_post_response_content_type_is_application_json(self):
        payload = {'hello': 'world'}

        response = self.simulate_post(
            ECHO_ROUTE,
            body=json.dumps(payload),
            headers={'content-type': 'application/json'}
        )

        expect(response.status).to.equal(falcon.HTTP_OK)
        expect(response.headers).to.contain('content-type')
        expect(response.headers['content-type']).to.contain('application/json')

    def test_post_with_text_payload(self):
        payload = 'This is plain text'

        response = self.simulate_post(ECHO_ROUTE, body=payload)
        expect(response.status).to.equal(falcon.HTTP_UNSUPPORTED_MEDIA_TYPE)

    def test_respond_with_a_json(self):
        self.settable_resource.set_json({'hello': 'world'})

        response = self.simulate_get(SETTABLE_ROUTE)
        expect(response.json).to.equal({'hello': 'world'})

    def test_respond_with_none_json(self):
        self.settable_resource.set_json(None)

        response = self.simulate_get(SETTABLE_ROUTE)
        expect(response.json).to.equal({})

    def test_respond_with_plain_text(self):
        self.settable_resource.set_json('This is plain text')

        response = self.simulate_get(SETTABLE_ROUTE)
        expect(response.status).to.equal(falcon.HTTP_INTERNAL_SERVER_ERROR)

    def test_respond_with_text_and_json(self):
        self.settable_resource.set_json({'hello': 'world'})
        self.settable_resource.set_text('This is plain text')

        response = self.simulate_get(SETTABLE_ROUTE)
        expect(response.text).to.equal('This is plain text')

    def test_respond_with_json_and_empty_text(self):
        self.settable_resource.set_json({'hello': 'world'})
        self.settable_resource.set_text('')

        response = self.simulate_get(SETTABLE_ROUTE)
        expect(response.json).to.equal({'hello': 'world'})

    def test_ignore_middleware(self):
        payload = {'hello': 'world'}

        self.simulate_post(
            DISABLED_ROUTE,
            body=json.dumps(payload)
        )

        expect(self.disabled_resource.has_request_included_json()).to.be.false
        expect(self.disabled_resource.get_last_request()).to.not_have.property('json')
