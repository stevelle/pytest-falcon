import json

import falcon
import pytest

application = falcon.API()


@pytest.fixture
def app():
    return application


def test_get(client):

    class Resource:

        def on_get(self, req, resp, **kwargs):
            resp.body = '{"foo": "bar"}'

    application.add_route('/route', Resource())

    resp = client.get('/route')
    assert resp.status == falcon.HTTP_OK
    assert resp.json['foo'] == 'bar'


def test_post(client):

    class Resource:

        def on_post(self, req, resp, **kwargs):
            resp.body = json.dumps(req.params)

    application.add_route('/route', Resource())

    resp = client.post('/route', {'myparam': 'myvalue'})
    assert resp.status == falcon.HTTP_OK
    assert resp.json['myparam'] == 'myvalue'


def test_put(client):

    class Resource:

        def on_put(self, req, resp, **kwargs):
            resp.body = req.stream.read().decode()

    application.add_route('/route', Resource())

    resp = client.put('/route', '{"myparam": "myvalue"}')
    assert resp.status == falcon.HTTP_OK
    assert resp.json['myparam'] == 'myvalue'


def test_custom_header(client):

    class Resource:

        def on_get(self, req, resp, **kwargs):
            resp.set_headers(req.headers)

    application.add_route('/route', Resource())
    resp = client.get('/route', headers={'X-Foo': 'Bar'})
    assert resp.headers['X-Foo'] == 'Bar'


def test_non_json_content_type(client):

    class Resource:

        def on_get(self, req, resp, **kwargs):
            resp.set_header('Content-Type', 'text/html')
            resp.body = '<html></html>'

    application.add_route('/route', Resource())
    resp = client.get('/route')
    assert resp.body == '<html></html>'