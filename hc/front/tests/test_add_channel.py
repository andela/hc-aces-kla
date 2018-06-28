from django.test.utils import override_settings

from hc.api.models import Channel
from hc.test import BaseTestCase


@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")
class AddChannelTestCase(BaseTestCase):

    def test_it_adds_email(self):
        url = "/integrations/add/"
        form = {"kind": "email", "value": "alice@example.org"}

        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(url, form)

        self.assertRedirects(response, "/integrations/")
        assert Channel.objects.count() == 1

    def test_it_trims_whitespace(self):
        """ Leading and trailing whitespace should get trimmed. """

        url = "/integrations/add/"
        form = {"kind": "email", "value": "   alice@example.org   "}

        self.client.login(username="alice@example.org", password="password")
        self.client.post(url, form)

        channels = Channel.objects.filter(value="alice@example.org")
        self.assertEqual(channels.count(), 1)

    def test_instructions_work(self):
        self.client.login(username="alice@example.org", password="password")
        kinds = ("email", "webhook", "pd", "pushover", "hipchat", "victorops")
        for frag in kinds:
            url = "/integrations/add_%s/" % frag
            response = self.client.get(url)
            self.assertContains(
                response,
                "Integration Settings",
                status_code=200)

    def test_team_access_works(self):
        """An added team member should add a channel using the team profile"""
        url = "/integrations/add/"
        form = {"kind": "email", "value": "alice@example.org"}
        self.client.login(username="alice@example.org", password="password")
        self.client.post(url, form)

        self.client.login(username="bob@example.org", password="password")
        response = self.client.get("/integrations/")
        self.assertContains(response, "alice@example.org")

    def test_non_member_cannot_access(self):
        """A non-member should not access team profile to add channel"""

        url = "/integrations/add/"
        form = {"kind": "email", "value": "alice@example.org"}
        self.client.login(username="alice@example.org", password="password")
        self.client.post(url, form)

        self.client.login(username="charlie@example.org", password="password")
        response = self.client.get("/integrations/")
        self.assertNotContains(response, "alice@example.org")

    # Test that bad kinds don't work
    def test_bad_kinds_dont_work(self):
        url = "/integrations/add/"
        form = {"kind": "food", "value": "meat"}

        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(url, form)
        assert response.status_code == 400
