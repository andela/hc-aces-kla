import json

from hc.api.models import Channel
from hc.test import BaseTestCase


class ChannelsTestCase(BaseTestCase):

    def test_it_formats_complex_slack_value(self):
        channel = Channel(kind="slack", user=self.alice)
        channel.value = json.dumps({
            "ok": True,
            "team_name": "foo-team",
            "incoming_webhook": {
                "url": "http://example.org",
                "channel": "#bar"
            }
        })
        channel.save()

        self.client.login(username="alice@example.org", password="password")
        response = self.client.get("/integrations/")
        self.assertContains(response, "foo-team", status_code=200)
        self.assertContains(response, "#bar")
