from hc.api.models import Channel
from hc.test import BaseTestCase


class AddWebhookTestCase(BaseTestCase):

    def test_it_adds_two_webhook_urls_and_redirects(self):
        form = {"value_down": "http://foo.com", "value_up": "https://bar.com"}

        self.client.login(username="alice@example.org", password="password")
        response = self.client.post("/integrations/add_webhook/", form)
        self.assertRedirects(response, "/integrations/")

        channel = Channel.objects.get()
        self.assertEqual(channel.value, "http://foo.com\nhttps://bar.com")

    def test_it_adds_webhook_using_team_access(self):
        form = {"value_down": "http://foo.com", "value_up": "https://bar.com"}

        # Logging in as bob, not alice. Bob has team access so this
        # should work.
        self.client.login(username="bob@example.org", password="password")
        self.client.post("/integrations/add_webhook/", form)

        channel = Channel.objects.get()
        self.assertEqual(channel.user, self.alice)
        self.assertEqual(channel.value, "http://foo.com\nhttps://bar.com")

    def test_it_rejects_non_http_webhook_urls(self):
        form = {"value_down": "foo", "value_up": "bar"}

        self.client.login(username="alice@example.org", password="password")
        response = self.client.post("/integrations/add_webhook/", form)
        self.assertContains(response, "Enter a valid URL.")

        self.assertEqual(Channel.objects.count(), 0)

    def test_it_handles_empty_down_url(self):
        form = {"value_down": "", "value_up": "http://foo.com"}

        self.client.login(username="alice@example.org", password="password")
        self.client.post("/integrations/add_webhook/", form)

        channel = Channel.objects.get()
        self.assertEqual(channel.value, "\nhttp://foo.com")
