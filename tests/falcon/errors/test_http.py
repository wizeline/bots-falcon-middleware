import datetime

import falcon

from wizeline.falcon.errors.http import (
    BotHTTPError,
    BotHTTPBadRequest,
    BotHTTPUnauthorized,
    BotHTTPForbidden,
    BotHTTPNotFound,
    BotHTTPMethodNotAllowed,
    BotHTTPNotAcceptable,
    BotHTTPConflict,
    BotHTTPInternalServerError,
    BotHTTPBadGateway,
    BotHTTPServiceUnavailable
)

from falcon.testing.test_case import TestCase
from sure import expect
from falcon import testing

ERROR_HEADERS = {
    'X-Error-Status': '404 Not Found',
    'X-Error-Code': 'BotDoesNotExist',
    'X-Error-Message': 'Bot does not exist'
}


def _make_client(
        bot_http_error=None
):
    app = falcon.API()
    resource = FakeErrorResource(
        bot_http_error=bot_http_error
    )
    app.add_route('/fail', resource)
    return testing.TestClient(app)


class FakeErrorResource:
    def __init__(
            self,
            bot_http_error=None
    ):
        self.bot_http_error = bot_http_error

    def on_get(self, req, resp):
        status = req.get_header('X-Error-Status')
        code = req.get_header('X-Error-Code')
        message = req.get_header('X-Error-Message')
        raise BotHTTPError(
            status,
            code=code,
            message=message
        )

    def on_post(self, req, resp):
        raise self.bot_http_error


class TestBotHTTPError(TestCase):
    def test_bot_http_error(self):
        client = _make_client()
        response = client.simulate_get(path='/fail', headers=ERROR_HEADERS)
        expect(response.status).to.be.equal('404 Not Found')
        expect(response.json['code']).to.be.equal('BotDoesNotExist')
        expect(response.json['message']).to.be.equal('Bot does not exist')


class TestBotHTTPExtendedError(TestCase):
    def test_bot_http_bad_request_error(self):
        error = BotHTTPBadRequest(
            code='InvalidSyntaxRequest',
            message='The syntax of the request is not valid'
        )
        client = _make_client(error)
        response = client.simulate_post(path='/fail', headers=None)
        expect(response.status).to.be.equal('400 Bad Request')
        expect(response.json['code']).to.be.equal('InvalidSyntaxRequest')
        expect(response.json['message']).to.be.equal('The syntax of the request is not valid')

    def test_bot_http_unauthorized_request_error(self):
        error = BotHTTPUnauthorized(
            code='InvalidCredentials',
            message='Your credentials are invalid',
            challenges=['bot_auth_token']
        )
        client = _make_client(error)
        response = client.simulate_post(path='/fail', headers=None)
        expect(response.status).to.be.equal('401 Unauthorized')
        expect(response.json['code']).to.be.equal('InvalidCredentials')
        expect(response.json['message']).to.be.equal('Your credentials are invalid')
        expect(response.headers['WWW-Authenticate']).to.be.equal('bot_auth_token')

    def test_bot_http_forbidden_request_error(self):
        error = BotHTTPForbidden(
            code='NotAccess',
            message='You don\'t have enough permissions to see this resource'
        )
        client = _make_client(error)
        response = client.simulate_post(path='/fail', headers=None)
        expect(response.status).to.be.equal('403 Forbidden')
        expect(response.json['code']).to.be.equal('NotAccess')
        expect(response.json['message']).to.be.equal('You don\'t have enough permissions to see this resource')

    def test_bot_http_not_found_request_error(self):
        error = BotHTTPNotFound(
            code='BotDoesNotExist',
            message='The bot your looking for does not exist'
        )
        client = _make_client(error)
        response = client.simulate_post(path='/fail', headers=None)
        expect(response.status).to.be.equal('404 Not Found')
        expect(response.json['code']).to.be.equal('BotDoesNotExist')
        expect(response.json['message']).to.be.equal('The bot your looking for does not exist')

    def test_bot_http_method_not_allowed_request_error(self):
        error = BotHTTPMethodNotAllowed(
            ['delete'],
            code='InvalidMethodForDeleteBot',
            message='This method is not allowed for delete a Bot'
        )
        client = _make_client(error)
        response = client.simulate_post(path='/fail', headers=None)
        expect(response.status).to.be.equal('405 Method Not Allowed')
        expect(response.json['code']).to.be.equal('InvalidMethodForDeleteBot')
        expect(response.json['message']).to.be.equal('This method is not allowed for delete a Bot')
        expect(response.headers['allow']).to.be.equal('delete')

    def test_bot_http_not_acceptable_request_error(self):
        error = BotHTTPNotAcceptable(
            code='MediaFormatNotAcceptable',
            message='This media format is not supported'
        )
        client = _make_client(error)
        response = client.simulate_post(path='/fail', headers=None)
        expect(response.status).to.be.equal('406 Not Acceptable')
        expect(response.json['code']).to.be.equal('MediaFormatNotAcceptable')
        expect(response.json['message']).to.be.equal('This media format is not supported')

    def test_bot_http_conflict_request_error(self):
        error = BotHTTPConflict(
            code='BotAlreadyExists',
            message='Bot already exists'
        )
        client = _make_client(error)
        response = client.simulate_post(path='/fail', headers=None)
        expect(response.status).to.be.equal('409 Conflict')
        expect(response.json['code']).to.be.equal('BotAlreadyExists')
        expect(response.json['message']).to.be.equal('Bot already exists')

    def test_bot_http_internal_server_error_request_error(self):
        error = BotHTTPInternalServerError(
            code='NLPEngineError',
            message='Error in NLP Engine'
        )
        client = _make_client(error)
        response = client.simulate_post(path='/fail', headers=None)
        expect(response.status).to.be.equal('500 Internal Server Error')
        expect(response.json['code']).to.be.equal('NLPEngineError')
        expect(response.json['message']).to.be.equal('Error in NLP Engine')

    def test_bot_http_bad_gateway_request_error(self):
        error = BotHTTPBadGateway(
            code='NLPEngineError',
            message='NLP Engine is under maintenance. Try again later'
        )
        client = _make_client(error)
        response = client.simulate_post(path='/fail', headers=None)
        expect(response.status).to.be.equal('502 Bad Gateway')
        expect(response.json['code']).to.be.equal('NLPEngineError')
        expect(response.json['message']).to.be.equal('NLP Engine is under maintenance. Try again later')

    def test_bot_http_service_unavailable_request_error(self):
        error = BotHTTPServiceUnavailable(
            code='BotOperationsError',
            message='Bot Platform is under maintenance. Try again later',
            retry_after=datetime.datetime.now()
        )
        client = _make_client(error)
        response = client.simulate_post(path='/fail', headers=None)
        expect(response.status).to.be.equal('503 Service Unavailable')
        expect(response.json['code']).to.be.equal('BotOperationsError')
        expect(response.json['message']).to.be.equal('Bot Platform is under maintenance. Try again later')
        expect(response.headers['retry-after']).should_not.be.none
