from django.test.utils import override_settings

from hc.api.models import Channel
from hc.test import BaseTestCase


@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")
class AddChannelTestCase(BaseTestCase):

    def test_it_adds_email(self):
        url = "/integrations/add/"
        form = {"kind": "email", "value": "alice@example.org"}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, form)

        self.assertRedirects(r, "/integrations/")
        assert Channel.objects.count() == 1

    def test_it_trims_whitespace(self):
        """ Leading and trailing whitespace should get trimmed. """

        url = "/integrations/add/"
        form = {"kind": "email", "value": "   alice@example.org   "}

        self.client.login(username="alice@example.org", password="password")
        self.client.post(url, form)

        q = Channel.objects.filter(value="alice@example.org")
        self.assertEqual(q.count(), 1)

    def test_instructions_work(self):
        self.client.login(username="alice@example.org", password="password")
        kinds = ("email", "webhook", "pd", "pushover", "hipchat", "victorops")
        for frag in kinds:
            url = "/integrations/add_%s/" % frag
            r = self.client.get(url)
            self.assertContains(r, "Integration Settings", status_code=200)

    # Test that the team access works
    def test_team_access_works(self):
        url = "/integrations/add/"
        form = {"kind": "email", "value": "alice@example.org"}

        # login alice and add channel
        self.client.login(username="alice@example.org", password="password")
        self.client.post(url, form)

        channel = Channel.objects.filter(value="alice@example.org")
        url_check = "/integrations/%s/checks/" % channel[0].code

        # Bob, alice's teammate tries to access Alice's channel
        self.client.login(username="bob@example.org", password="password")
        r = self.client.get(url_check)
        self.assertContains(r, "Assign Checks to Channel", status_code=200)

    # Test that non-member of team cannot access
    def test_non_member_cannot_access(self):
        url = "/integrations/add/"
        form = {"kind": "email", "value": "alice@example.org"}

        # login alice and add channel
        self.client.login(username="alice@example.org", password="password")
        self.client.post(url, form)

        q = Channel.objects.filter(value="alice@example.org")
        channel_code = q[0].code
        print("test")
        print(channel_code)
        url_check = "/integrations/%s/checks/" % q[0].code

        # login with charlie who is not a member of alice's team
        # and try to assign checks to the channel added by Alice
        self.client.login(username="charlie@example.org", password="password")
        r = self.client.get(url_check)
        self.assertEqual(r.status_code, 403)

    # Test that bad kinds don't work
    def test_bad_kinds_dont_work(self):
        url = "/integrations/add/"
        form = {"kind": "food", "value": "meat"}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, form)
        assert r.status_code == 400
