import falcon

from wizeline.falcon.errors.platform import (
    BotDoesNotExist,
    BotAlreadyExists,
    PlatformNotAvailable,
    PlatformAlreadySet,
    PlatformNotSupported,
    NLPEngineError,
    BotTrainingError,
    CanNotSendMessage
)

from falcon.testing.test_case import TestCase
from sure import expect
from falcon import testing


def _make_client(bot_http_error=None):
    app = falcon.API()
    resource = FakeErrorResource(
        bot_http_error=bot_http_error
    )
    app.add_route('/fail', resource)
    return testing.TestClient(app)


class FakeErrorResource:
    def __init__(self, bot_http_error=None):
        self.bot_http_error = bot_http_error

    def on_post(self, req, resp):
        raise self.bot_http_error


class TestBotPlatformError(TestCase):
    def test_bot_training_error(self):
        error = BotTrainingError(
            message='An error occurred training the bot'
        )
        client = _make_client(error)
        response = client.simulate_post(path='/fail', headers=None)
        expect(response.status).to.be.equal('400 Bad Request')
        expect(response.json['code']).to.be.equal('BotTrainingError')
        expect(response.json['message']).to.be.equal('An error occurred training the bot')

    def test_bot_does_not_exist_error(self):
        error = BotDoesNotExist(
            message='The bot with id 123 does not exist'
        )
        client = _make_client(error)
        response = client.simulate_post(path='/fail', headers=None)
        expect(response.status).to.be.equal('404 Not Found')
        expect(response.json['code']).to.be.equal('BotDoesNotExist')
        expect(response.json['message']).to.be.equal('The bot with id 123 does not exist')

    def test_bot_already_exists_error(self):
        error = BotAlreadyExists(
            message='The bot with id 123 already exists'
        )
        client = _make_client(error)
        response = client.simulate_post(path='/fail', headers=None)
        expect(response.status).to.be.equal('409 Conflict')
        expect(response.json['code']).to.be.equal('BotAlreadyExists')
        expect(response.json['message']).to.be.equal('The bot with id 123 already exists')

    def test_platform_not_available_error(self):
        error = PlatformNotAvailable(
            platform_name='Facebook',
            message='The Facebook platform is down'
        )
        client = _make_client(error)
        response = client.simulate_post(path='/fail', headers=None)
        expect(response.status).to.be.equal('409 Conflict')
        expect(response.json['code']).to.be.equal('PlatformNotAvailable')
        expect(response.json['message']).to.be.equal('The Facebook platform is down')
        expect(response.json['platform_name']).to.be.equal('Facebook')

    def test_platform_already_set_error(self):
        error = PlatformAlreadySet(
            platform_name='Webchat',
            message='The Webchat platform is already set'
        )
        client = _make_client(error)
        response = client.simulate_post(path='/fail', headers=None)
        expect(response.status).to.be.equal('409 Conflict')
        expect(response.json['code']).to.be.equal('PlatformAlreadySet')
        expect(response.json['message']).to.be.equal('The Webchat platform is already set')
        expect(response.json['platform_name']).to.be.equal('Webchat')

    def test_platform_not_supported_error(self):
        error = PlatformNotSupported(
            platform_name='Slack',
            message='The Slack platform is not supported'
        )
        client = _make_client(error)
        response = client.simulate_post(path='/fail', headers=None)
        expect(response.status).to.be.equal('409 Conflict')
        expect(response.json['code']).to.be.equal('PlatformNotSupported')
        expect(response.json['message']).to.be.equal('The Slack platform is not supported')
        expect(response.json['platform_name']).to.be.equal('Slack')

    def test_nlp_engine_error(self):
        error = NLPEngineError(
            message='The NLP engine has an error'
        )
        client = _make_client(error)
        response = client.simulate_post(path='/fail', headers=None)
        expect(response.status).to.be.equal('500 Internal Server Error')
        expect(response.json['code']).to.be.equal('NLPEngineError')
        expect(response.json['message']).to.be.equal('The NLP engine has an error')

    def test_can_not_send_message_error(self):
        error = CanNotSendMessage(
            message='An error occurred when trying to send a message'
        )
        client = _make_client(error)
        response = client.simulate_post(path='/fail', headers=None)
        expect(response.status).to.be.equal('500 Internal Server Error')
        expect(response.json['code']).to.be.equal('CanNotSendMessage')
        expect(response.json['message']).to.be.equal('An error occurred when trying to send a message')
