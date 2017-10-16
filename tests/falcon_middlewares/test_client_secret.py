import falcon

from falcon_middlewares.client_secret import ClientSecretMiddleware

from falcon import testing
from sure import expect

TEST_ROUTE = '/test'


class Resource:
    def on_get(self, req, resp):
        resp.body = 'Hello'


class TestClientSecretMiddleware(testing.TestCase):
    def setUp(self):
        self.auth = ClientSecretMiddleware('secret')
        self.app = falcon.API(middleware=[self.auth])
        self.app.add_route(TEST_ROUTE, Resource())

    def test_access_without_token(self):
        response = self.simulate_get(TEST_ROUTE)
        expect(response.status).to.equal(falcon.HTTP_UNAUTHORIZED)

    def test_access_with_token(self):
        response = self.simulate_get(TEST_ROUTE, headers={
                'Authorization': 'secret'
            })
        expect(response.status).to.equal(falcon.HTTP_OK)

    def test_access_with_wrong_token(self):
        response = self.simulate_get(TEST_ROUTE, headers={
                'Authorization': 'this-is-not-the-right-token'
            })
        expect(response.status).to.equal(falcon.HTTP_UNAUTHORIZED)
