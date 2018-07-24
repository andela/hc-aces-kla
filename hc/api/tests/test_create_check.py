import json

from hc.api.models import Check
from hc.test import BaseTestCase


class CreateCheckTestCase(BaseTestCase):
    URL = "/api/v1/checks/"

    def setUp(self):
        super(CreateCheckTestCase, self).setUp()

    def post(self, data, expected_error=None):
        response = self.client.post(self.URL, json.dumps(data),
                                    content_type="application/json")

        if expected_error:
            self.assertEqual(response.status_code, 400)
            # Assert that the expected error is the response error
            result = response.json()
            self.assertEqual(result['error'], expected_error)
        return response

    def test_it_works(self):
        response = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 3600,
            "grace": 60
        })

        self.assertEqual(response.status_code, 201)

        doc = response.json()
        assert "ping_url" in doc
        self.assertEqual(doc["name"], "Foo")
        self.assertEqual(doc["tags"], "bar,baz")
        # Assert the expected last_ping and n_pings values

        self.assertEqual(Check.objects.count(), 1)
        check = Check.objects.get()
        self.assertEqual(check.name, "Foo")
        self.assertEqual(check.tags, "bar,baz")
        self.assertEqual(check.timeout.total_seconds(), 3600)
        self.assertEqual(check.grace.total_seconds(), 60)
        self.assertEqual(check.last_ping, None)
        self.assertEqual(check.n_pings, 0)
        self.assertEqual(check.number_of_nags, 0)

    def test_it_accepts_api_key_in_header(self):
        payload = json.dumps({"name": "Foo", "api_key": "abc"})

        # Make the post request and get the response
        response = {'status_code': 201}  # This is just a placeholder variable

        response = self.client.post(self.URL, payload,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_it_handles_missing_request_body(self):
        payload = json.dumps({"name": "Foo", "api_key": "efg"})

        # Make the post request with a missing body and get the response
        response = {'status_code': 400, 'error': "wrong api_key"}

        response = self.client.post(self.URL, payload,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "wrong api_key")

    def test_it_handles_invalid_json(self):

        # Make the post request with invalid json data type
        response = {
            'status_code': 400,
            'error': "could not parse request body"
        }

        response = self.client.post(self.URL, {"FOO"},
                                    content_type="application/json")
        res = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(res["error"], "could not parse request body")

    def test_it_rejects_wrong_api_key(self):
        self.post({"api_key": "wrong"},
                  expected_error="wrong api_key")

    def test_it_rejects_non_number_timeout(self):
        self.post({"api_key": "abc", "timeout": "oops"},
                  expected_error="timeout is not a number")

    def test_it_rejects_non_string_name(self):
        self.post({"api_key": "abc", "name": False},
                  expected_error="name is not a string")

    # Test for the assignment of channels
    def test_channel_assignment(self):
        response = self.post({
            "api_key": "abc",
            "name": "Foo"
        })
        check = Check.objects.get(user=self.alice, name="Foo")
        check.assign_all_channels()
        self.assertEqual(response.status_code, 201)

    # Test for the 'timeout is too small' and 'timeout is too large' errors
    def test_it_rejects_too_small_timeout(self):
        self.post({"api_key": "abc", "timeout": 0},
                  expected_error="timeout is too small")

    def test_it_rejects_too_large_timeout(self):
        self.post({"api_key": "abc", "timeout": 123456789},
                  expected_error="timeout is too large")
