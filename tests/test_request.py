from unittest.mock import Mock

from dyspo.request import Request
from dyspo.response import AbortException
from tests import AsyncTest


class TestRequest(AsyncTest):
    def get_request(self, method=None, scheme=None, path=None, data=None,
                    headers=None, params=None, query=None, json=None, at_eof=False):

        method = method or 'get'
        scheme = scheme or 'http'
        path = path or '/'
        data = data or {}
        headers = headers or {}
        params = params or {}
        query = query or {}
        json = json or self.mock_coroutine(return_value=data)

        return Mock(method=method,
                    scheme=scheme,
                    rel_url=Mock(path=path),
                    headers=headers,
                    match_info=params,
                    query=query,
                    json=json,
                    content=Mock(at_eof=Mock(return_value=at_eof)))

    def test_from_request_minimal(self):
        request = self.get_request()
        actual = self.run_coroutine(Request.from_request(request))

        self.assertEqual(actual.method, 'get')
        self.assertEqual(actual.scheme, 'http')
        self.assertEqual(actual.uri, '/')
        self.assertEqual(actual.headers, {})
        self.assertEqual(actual.query, {})
        self.assertEqual(actual.data, {})
        self.assertIsNone(actual.username)
        self.assertIsNone(actual.password)

    def test_from_request_maximal(self):
        request = self.get_request(method='post',
                                   scheme='https',
                                   path='/foo',
                                   data={'foo': 'bar'},
                                   params={'id': '1'},
                                   headers={'Content-Type': 'application/json', 'Authorization': 'Basic foo:hunter2'},
                                   query={'bar': 'baz'})

        actual = self.run_coroutine(Request.from_request(request))

        self.assertEqual(actual.method, 'post')
        self.assertEqual(actual.scheme, 'https')
        self.assertEqual(actual.uri, '/foo')
        self.assertEqual(actual.headers, {'Content-Type': 'application/json'})
        self.assertEqual(actual.query, {'bar': 'baz'})
        self.assertEqual(actual.data, {'foo': 'bar'})
        self.assertEqual(actual.params, {'id': '1'})
        self.assertEqual(actual.username, 'foo')
        self.assertEqual(actual.password, 'hunter2')

    def test_from_request_invalid_json_payload(self):
        json_exception_thrown = self.mock_coroutine(side_effect=AbortException(Mock()))
        request = self.get_request(json=json_exception_thrown)

        with self.assertRaises(AbortException):
            self.run_coroutine(Request.from_request(request))

    def test_from_request_at_eof(self):
        request = self.get_request(at_eof=True)

        actual = self.run_coroutine(Request.from_request(request))

        self.assertEqual(actual.data, {})

    def test_from_request_invalid_auth(self):
        request = self.get_request(headers={'Authorization': 'Invalid'})

        actual = self.run_coroutine(Request.from_request(request))
        self.assertIsNone(actual.username)
        self.assertIsNone(actual.password)
